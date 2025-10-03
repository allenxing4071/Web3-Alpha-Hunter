"""AI分析API"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Optional
from app.services.analyzers.ai_analyzer import ai_analyzer
from app.services.analyzers.risk_detector import risk_detector

router = APIRouter(prefix="/analyze", tags=["analyze"])


class AnalyzeRequest(BaseModel):
    """分析请求"""
    text: str
    source: str = "twitter"
    author: Optional[Dict] = None
    engagement: Optional[Dict] = None


@router.post("/project")
async def analyze_project(request: AnalyzeRequest):
    """分析项目
    
    请求体示例:
    ```json
    {
      "text": "Excited to announce our new DeFi protocol! Fair launch, audited by Certik.",
      "source": "twitter",
      "author": {
        "username": "VitalikButerin",
        "followers": 5000000,
        "verified": true
      },
      "engagement": {
        "likes": 5000,
        "retweets": 1200,
        "replies": 300
      }
    }
    ```
    """
    
    # 构建项目数据
    project_data = {
        "text": request.text,
        "source": request.source,
    }
    
    if request.author:
        project_data["author"] = request.author
    
    if request.engagement:
        project_data["engagement"] = request.engagement
    
    # 执行分析
    analysis = ai_analyzer.analyze_full_project(project_data)
    
    # 检测风险
    risks = risk_detector.detect_risks(project_data)
    scam_probability = risk_detector.calculate_scam_probability(risks)
    
    return {
        "success": True,
        "data": {
            **analysis,
            "risks": risks,
            "scam_probability": scam_probability,
        }
    }


@router.post("/quick-score")
async def quick_score(request: AnalyzeRequest):
    """快速评分(不使用LLM,仅基于规则)"""
    
    project_data = {
        "text": request.text,
        "source": request.source,
        "author": request.author or {},
        "engagement": request.engagement or {},
    }
    
    # 各维度评分
    scores = {
        "team": ai_analyzer.score_team_background(project_data),
        "technology": ai_analyzer.score_technology(project_data),
        "community": ai_analyzer.score_community(project_data),
        "tokenomics": ai_analyzer.score_tokenomics(project_data),
        "market_timing": ai_analyzer.score_market_timing(project_data),
        "risk": risk_detector.calculate_risk_score(project_data),
    }
    
    # 计算综合评分
    from app.services.analyzers.scorer import project_scorer
    
    overall_score = project_scorer.calculate_overall_score(
        team_score=scores["team"],
        tech_score=scores["technology"],
        community_score=scores["community"],
        tokenomics_score=scores["tokenomics"],
        market_timing_score=scores["market_timing"],
        risk_score=scores["risk"],
    )
    
    grade = project_scorer.calculate_grade(overall_score)
    
    return {
        "success": True,
        "data": {
            "overall_score": overall_score,
            "grade": grade,
            "scores": scores,
        }
    }


@router.post("/risk-check")
async def check_risk(request: AnalyzeRequest):
    """风险检查"""
    
    project_data = {
        "text": request.text,
        "source": request.source,
    }
    
    # 检测风险
    risks = risk_detector.detect_risks(project_data)
    scam_probability = risk_detector.calculate_scam_probability(risks)
    has_fatal = risk_detector.has_fatal_risk(risks)
    
    return {
        "success": True,
        "data": {
            "risks": risks,
            "scam_probability": scam_probability,
            "has_fatal_risk": has_fatal,
            "risk_level": "high" if scam_probability > 70 else "medium" if scam_probability > 30 else "low"
        }
    }

