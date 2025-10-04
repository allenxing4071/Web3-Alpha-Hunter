"""AI评分引擎 - 6维度项目评分系统"""

from typing import Dict, Optional
from datetime import datetime
from loguru import logger
from pydantic import BaseModel


class ProjectScore(BaseModel):
    """项目评分模型"""
    
    # 六大维度
    team_score: int  # 团队背景（0-100）
    tech_score: int  # 技术创新（0-100）
    community_score: int  # 社区热度（0-100）
    tokenomics_score: int  # 代币经济（0-100）
    market_score: int  # 市场时机（0-100）
    risk_score: int  # 风险评估（0-100，越高越安全）
    
    # 综合得分
    composite_score: int  # 加权综合分（0-100）
    
    # 分级
    grade: str  # S/A/B/C
    
    # 推荐度
    recommendation: str  # Strong Buy, Buy, Hold, Pass


class ScoringEngine:
    """评分引擎"""
    
    # 维度权重
    WEIGHTS = {
        "team": 0.20,
        "tech": 0.25,
        "community": 0.20,
        "tokenomics": 0.15,
        "market": 0.10,
        "risk": 0.10
    }
    
    def __init__(self):
        """初始化"""
        logger.info("✅ Scoring Engine initialized")
    
    def assess_team_background(self, project_data: Dict) -> int:
        """评估团队背景（0-100分）
        
        Args:
            project_data: 项目数据
            
        Returns:
            团队背景评分
        """
        score = 0
        
        team_info = project_data.get("team_info", {})
        
        if not team_info:
            return 20  # 基础分
        
        # 因子1: 团队成员数量（15分）
        team_size = len(team_info.get("members", []))
        score += min(15, team_size * 3)
        
        # 因子2: 成员背景（40分）
        members = team_info.get("members", [])
        for member in members[:5]:  # 只看前5个核心成员
            # FAANG背景
            if member.get("from_faang"):
                score += 8
            
            # Web3成功项目经验
            if member.get("web3_success"):
                score += 5
            
            # 顶级学府
            if member.get("top_education"):
                score += 3
        
        score = min(score, 40)
        
        # 因子3: 团队完整性（20分）
        roles = team_info.get("roles", [])
        has_ceo = "CEO" in roles or "Founder" in roles
        has_cto = "CTO" in roles
        has_cmo = "CMO" in roles or "Marketing" in roles
        
        completeness = sum([has_ceo, has_cto, has_cmo]) / 3
        score += completeness * 20
        
        # 因子4: 社交影响力（15分）
        social_reach = team_info.get("social_reach", 0)
        score += min(15, social_reach / 50000 * 15)  # 5万粉丝满分
        
        # 因子5: 团队透明度（10分）
        transparency = team_info.get("transparency_score", 0.5)
        score += transparency * 10
        
        return min(100, int(score))
    
    def assess_technical_innovation(self, project_data: Dict) -> int:
        """评估技术创新（0-100分）
        
        Args:
            project_data: 项目数据
            
        Returns:
            技术创新评分
        """
        score = 0
        
        # 因子1: GitHub活跃度（30分）
        github = project_data.get("github", {})
        if github:
            commits_30d = github.get("commits_30d", 0)
            score += min(10, commits_30d / 10)
            
            contributors = github.get("contributors", 0)
            score += min(10, contributors * 2)
            
            stars = github.get("stars", 0)
            score += min(10, stars / 500)
        
        # 因子2: 技术文档质量（20分）
        docs_quality = project_data.get("docs_quality", 0)
        score += docs_quality * 20
        
        # 因子3: 技术创新性（30分）
        innovation_score = project_data.get("innovation_score", 0.5)
        score += innovation_score * 30
        
        # 因子4: 安全审计（20分）
        audit_status = project_data.get("audit_status", {})
        if audit_status.get("has_audit"):
            score += 10
            if audit_status.get("top_auditor"):
                score += 10
        
        return min(100, int(score))
    
    def assess_community_heat(self, project_data: Dict) -> int:
        """评估社区热度（0-100分）
        
        Args:
            project_data: 项目数据
            
        Returns:
            社区热度评分
        """
        score = 0
        
        # 因子1: Twitter（30分）
        twitter = project_data.get("twitter", {})
        if twitter:
            followers = twitter.get("followers", 0)
            score += min(15, followers / 10000 * 15)
            
            engagement_rate = twitter.get("engagement_rate", 0)
            score += min(15, engagement_rate * 100 * 15)
        
        # 因子2: Telegram（25分）
        telegram = project_data.get("telegram", {})
        if telegram:
            members = telegram.get("members", 0)
            score += min(15, members / 5000 * 15)
            
            activity = telegram.get("daily_messages", 0)
            score += min(10, activity / 1000 * 10)
        
        # 因子3: Discord（25分）
        discord = project_data.get("discord", {})
        if discord:
            activity_score = discord.get("activity_score", 0)
            score += activity_score * 0.25
        
        # 因子4: 增长趋势（20分）
        growth = project_data.get("growth_data", {})
        twitter_growth = growth.get("twitter_growth_30d", 0)
        score += min(10, twitter_growth * 100)
        
        telegram_growth = growth.get("telegram_growth_30d", 0)
        score += min(10, telegram_growth * 100)
        
        return min(100, int(score))
    
    def assess_tokenomics(self, project_data: Dict) -> int:
        """评估代币经济（0-100分）
        
        Args:
            project_data: 项目数据
            
        Returns:
            代币经济评分
        """
        score = 50  # 基础分（很多项目还未公布代币经济学）
        
        tokenomics = project_data.get("tokenomics", {})
        
        if not tokenomics:
            return score
        
        # 因子1: 代币分配合理性（30分）
        distribution = tokenomics.get("distribution", {})
        if distribution:
            team_allocation = distribution.get("team", 0)
            community_allocation = distribution.get("community", 0)
            
            # 团队占比不应过高
            if team_allocation < 0.2:  # <20%
                score += 15
            elif team_allocation < 0.3:
                score += 10
            
            # 社区占比应该较高
            if community_allocation > 0.5:  # >50%
                score += 15
            elif community_allocation > 0.3:
                score += 10
        
        # 因子2: 释放机制（30分）
        vesting = tokenomics.get("vesting", {})
        if vesting:
            team_lockup = vesting.get("team_lockup_months", 0)
            if team_lockup >= 12:
                score += 15
            elif team_lockup >= 6:
                score += 10
            
            release_schedule = vesting.get("release_schedule", "")
            if "gradual" in release_schedule.lower():
                score += 15
        
        # 因子3: 代币用途（20分）
        utility = tokenomics.get("utility", [])
        utility_count = len(utility)
        score += min(20, utility_count * 5)
        
        # 因子4: 供应机制（20分）
        supply = tokenomics.get("supply", {})
        has_burning = supply.get("has_burning", False)
        has_staking = supply.get("has_staking", False)
        
        if has_burning:
            score += 10
        if has_staking:
            score += 10
        
        return min(100, int(score))
    
    def assess_market_timing(self, project_data: Dict) -> int:
        """评估市场时机（0-100分）
        
        Args:
            project_data: 项目数据
            
        Returns:
            市场时机评分
        """
        score = 50  # 基础分
        
        # 因子1: 赛道热度（40分）
        category = project_data.get("category", "")
        
        # 当前热门赛道（2024-2025）
        hot_tracks = {
            "AI": 95,
            "DePIN": 90,
            "RWA": 85,
            "Gaming": 80,
            "DeFi": 75,
            "SocialFi": 70,
            "Layer2": 85,
            "Restaking": 90
        }
        
        track_score = hot_tracks.get(category, 60)
        score += (track_score - 50) * 0.4
        
        # 因子2: 竞品分析（30分）
        competitors = project_data.get("competitors", [])
        competitor_count = len(competitors)
        
        if competitor_count == 0:
            # 蓝海市场
            score += 30
        elif competitor_count <= 3:
            # 竞争适中
            score += 20
        elif competitor_count <= 5:
            # 竞争激烈
            score += 10
        # else: 竞争过于激烈，不加分
        
        # 因子3: 叙事契合度（30分）
        narrative = project_data.get("narrative_fit", 0.5)
        score += narrative * 30
        
        return min(100, int(score))
    
    def assess_risks(self, project_data: Dict) -> int:
        """评估风险（0-100分，分数越高越安全）
        
        Args:
            project_data: 项目数据
            
        Returns:
            风险评分
        """
        score = 100  # 从满分开始扣分
        
        # 风险1: 团队匿名（-30分）
        if project_data.get("team_anonymous", True):
            score -= 30
        
        # 风险2: 未审计（-20分）
        if not project_data.get("audit_status", {}).get("has_audit"):
            score -= 20
        
        # 风险3: 代币集中度过高（-15分）
        token_concentration = project_data.get("token_concentration", 0)
        if token_concentration > 0.5:
            score -= 15
        elif token_concentration > 0.3:
            score -= 10
        
        # 风险4: 社交媒体刷量（-15分）
        if project_data.get("bot_suspicion", 0) > 0.5:
            score -= 15
        
        # 风险5: 白皮书抄袭（-20分）
        if project_data.get("whitepaper_plagiarism", 0) > 0.8:
            score -= 20
        
        # 风险6: 域名年龄过短（-10分）
        domain_age_days = project_data.get("domain_age_days", 0)
        if domain_age_days < 30:
            score -= 10
        
        return max(0, int(score))
    
    def calculate_comprehensive_score(self, project_data: Dict) -> ProjectScore:
        """计算综合评分
        
        Args:
            project_data: 项目数据
            
        Returns:
            项目评分
        """
        logger.info(f"🔍 Calculating score for {project_data.get('project_name', 'Unknown')}")
        
        # 1. 计算各维度得分
        team_score = self.assess_team_background(project_data)
        tech_score = self.assess_technical_innovation(project_data)
        community_score = self.assess_community_heat(project_data)
        tokenomics_score = self.assess_tokenomics(project_data)
        market_score = self.assess_market_timing(project_data)
        risk_score = self.assess_risks(project_data)
        
        # 2. 计算加权综合分
        composite = (
            team_score * self.WEIGHTS["team"] +
            tech_score * self.WEIGHTS["tech"] +
            community_score * self.WEIGHTS["community"] +
            tokenomics_score * self.WEIGHTS["tokenomics"] +
            market_score * self.WEIGHTS["market"] +
            risk_score * self.WEIGHTS["risk"]
        )
        
        # 3. 致命风险降级
        if project_data.get("is_likely_scam", False):
            composite *= 0.3  # 降70%
            logger.warning("⚠️ Scam suspicion detected, score reduced")
        
        # 4. 顶级VC加分
        if project_data.get("has_top_tier_vc", False):
            composite = min(100, composite + 5)
            logger.info("✨ Top-tier VC backing, score boosted")
        
        composite = max(0, min(100, int(composite)))
        
        # 5. 确定分级
        if composite >= 85:
            grade = "S"
            recommendation = "Strong Buy"
        elif composite >= 70:
            grade = "A"
            recommendation = "Buy"
        elif composite >= 55:
            grade = "B"
            recommendation = "Hold"
        else:
            grade = "C"
            recommendation = "Pass"
        
        score_result = ProjectScore(
            team_score=team_score,
            tech_score=tech_score,
            community_score=community_score,
            tokenomics_score=tokenomics_score,
            market_score=market_score,
            risk_score=risk_score,
            composite_score=composite,
            grade=grade,
            recommendation=recommendation
        )
        
        logger.info(f"✅ Score calculated: {composite}/100 (Grade {grade})")
        
        return score_result
    
    def predict_token_launch_probability(self, project_data: Dict) -> Dict:
        """预测发币概率
        
        Args:
            project_data: 项目数据
            
        Returns:
            发币概率数据
        """
        probability = 0
        signals = []
        
        # 强信号
        if project_data.get("snapshot_announced"):
            probability += 15
            signals.append("已宣布快照时间")
        
        if project_data.get("tokenomics_published"):
            probability += 15
            signals.append("代币经济学已公开")
        
        if project_data.get("points_system_live"):
            probability += 12
            signals.append("积分系统运行中")
        
        if project_data.get("audit_completed"):
            probability += 10
            signals.append("审计完成")
        
        # 中等信号
        if project_data.get("mainnet_live"):
            probability += 8
            signals.append("主网已上线")
        
        funding = project_data.get("funding_amount", 0)
        if funding > 20_000_000:
            probability += 8
            signals.append(f"完成${funding/1e6:.0f}M融资")
        
        # 弱信号
        if project_data.get("roadmap_mentions_token"):
            probability += 5
            signals.append("路线图提及代币")
        
        probability = min(100, probability)
        
        # 确定时间线
        if probability >= 80:
            timeline = "1-2个月内"
            confidence = "Very High"
        elif probability >= 60:
            timeline = "2-4个月内"
            confidence = "High"
        elif probability >= 40:
            timeline = "4-6个月内"
            confidence = "Medium"
        elif probability >= 20:
            timeline = "6-12个月内"
            confidence = "Low"
        else:
            timeline = "未知或12个月以上"
            confidence = "Very Low"
        
        return {
            "project_name": project_data.get("project_name"),
            "launch_probability": probability,
            "confidence": confidence,
            "estimated_timeline": timeline,
            "detected_signals": signals,
            "signal_count": len(signals)
        }
    
    def estimate_airdrop_value(self, project_data: Dict) -> Dict:
        """估算空投价值
        
        Args:
            project_data: 项目数据
            
        Returns:
            空投价值估算
        """
        # 历史案例参考
        historical_cases = {
            "DeFi": {"avg": 1500, "max": 5000},
            "Layer2": {"avg": 2000, "max": 8000},
            "NFT": {"avg": 800, "max": 3000},
            "GameFi": {"avg": 500, "max": 2000}
        }
        
        category = project_data.get("category", "DeFi")
        reference = historical_cases.get(category, historical_cases["DeFi"])
        
        base_value = reference["avg"]
        
        # 调整因子
        adjustment = 1.0
        
        # TVL调整
        tvl = project_data.get("tvl", 0)
        if tvl > 100_000_000:
            adjustment *= 1.5
        elif tvl > 50_000_000:
            adjustment *= 1.3
        elif tvl > 10_000_000:
            adjustment *= 1.1
        
        # 融资调整
        funding = project_data.get("funding_amount", 0)
        if funding > 50_000_000:
            adjustment *= 1.4
        elif funding > 20_000_000:
            adjustment *= 1.2
        
        estimated_value = int(base_value * adjustment)
        
        return {
            "project_name": project_data.get("project_name"),
            "estimated_value_usd": estimated_value,
            "value_range_usd": {
                "min": int(estimated_value * 0.5),
                "max": min(int(estimated_value * 2), reference["max"])
            },
            "confidence": "Medium",
            "reference_category": category
        }


# 全局服务实例
scoring_engine = ScoringEngine()

