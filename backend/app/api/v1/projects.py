"""项目相关API"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.schemas import (
    ProjectGrade,
    ProjectListResponse,
    ProjectDetailResponse,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "",
    response_model=ProjectListResponse,
    summary="获取项目列表",
    description="根据筛选条件获取项目列表"
)
async def list_projects(
    grade: Optional[ProjectGrade] = Query(None, description="项目等级"),
    category: Optional[str] = Query(None, description="项目分类"),
    blockchain: Optional[str] = Query(None, description="区块链"),
    min_score: float = Query(0, ge=0, le=100, description="最低评分"),
    sort_by: str = Query("score", description="排序字段: score, discovered_at"),
    order: str = Query("desc", description="排序方向: asc, desc"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取项目列表
    
    - **grade**: 筛选等级 (S/A/B/C)
    - **category**: 项目分类 (DeFi, NFT, GameFi等)
    - **blockchain**: 区块链 (Ethereum, Solana等)
    - **min_score**: 最低评分
    - **sort_by**: 排序字段
    - **order**: 排序方向
    - **page**: 页码
    - **limit**: 每页数量
    """
    
    # 构建查询（包含所有项目，包括未评分的）
    query = db.query(Project).filter(
        (Project.overall_score >= min_score) | (Project.overall_score.is_(None))
    )
    
    # 应用筛选
    if grade:
        query = query.filter(Project.grade == grade.value)
    if category:
        query = query.filter(Project.category == category)
    if blockchain:
        query = query.filter(Project.blockchain == blockchain)
    
    # 计算总数
    total_items = query.count()
    
    # 排序
    if sort_by == "score":
        if order == "desc":
            query = query.order_by(Project.overall_score.desc())
        else:
            query = query.order_by(Project.overall_score.asc())
    elif sort_by == "discovered_at":
        if order == "desc":
            query = query.order_by(Project.first_discovered_at.desc())
        else:
            query = query.order_by(Project.first_discovered_at.asc())
    
    # 分页
    skip = (page - 1) * limit
    projects = query.offset(skip).limit(limit).all()
    
    # 计算总页数
    total_pages = (total_items + limit - 1) // limit
    
    # 构建响应
    return ProjectListResponse(
        success=True,
        data={
            "projects": [
                {
                    "project_id": f"proj_{p.id}",
                    "name": p.project_name,
                    "symbol": p.symbol,
                    "grade": p.grade,
                    "overall_score": float(p.overall_score) if p.overall_score else 0,
                    "category": p.category,
                    "blockchain": p.blockchain,
                    "description": p.description,
                    "logo_url": p.logo_url,
                    "website": p.website,
                    "social_links": {
                        "twitter": p.twitter_handle,
                        "telegram": p.telegram_channel,
                        "discord": p.discord_link,
                        "github": p.github_repo,
                    },
                    "key_highlights": [],  # TODO: 从AI分析中获取
                    "risk_flags": [],  # TODO: 从AI分析中获取
                    "metrics": {},  # TODO: 从最新指标中获取
                    "first_discovered_at": p.first_discovered_at,
                    "last_updated_at": p.last_updated_at,
                }
                for p in projects
            ],
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "items_per_page": limit
            }
        }
    )


@router.get(
    "/{project_id}",
    response_model=ProjectDetailResponse,
    summary="获取项目详情",
    description="获取单个项目的详细信息"
)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    """
    获取项目详情
    
    - **project_id**: 项目ID (格式: proj_123)
    """
    
    # 解析ID
    try:
        pid = int(project_id.replace("proj_", ""))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID format")
    
    # 查询项目
    project = db.query(Project).filter(Project.id == pid).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # TODO: 获取AI分析、社交指标、链上数据
    
    return ProjectDetailResponse(
        success=True,
        data={
            "project_id": f"proj_{project.id}",
            "name": project.project_name,
            "symbol": project.symbol,
            "grade": project.grade,
            "overall_score": float(project.overall_score) if project.overall_score else 0,
            "category": project.category,
            "blockchain": project.blockchain,
            "description": project.description,
            "logo_url": project.logo_url,
            "website": project.website,
            "contract_address": project.contract_address,
            "whitepaper_url": project.whitepaper_url,
            "github_repo": project.github_repo,
            "social_links": {
                "twitter": project.twitter_handle,
                "telegram": project.telegram_channel,
                "discord": project.discord_link,
                "github": project.github_repo,
            },
            "scores": {
                "overall": float(project.overall_score or 0),
                "team": float(project.team_score or 0),
                "technology": float(project.tech_score or 0),
                "community": float(project.community_score or 0),
                "tokenomics": float(project.tokenomics_score or 0),
                "market_timing": float(project.market_timing_score or 0),
                "risk": float(project.risk_score or 0),
            },
            "key_highlights": [],
            "risk_flags": [],
            "metrics": {},
            "ai_analysis": None,  # TODO
            "discovery": {
                "source": project.discovered_from,
                "discovered_at": project.first_discovered_at,
            },
            "first_discovered_at": project.first_discovered_at,
            "last_updated_at": project.last_updated_at,
        }
    )


@router.get(
    "/{project_id}/history",
    summary="获取项目历史数据",
    description="获取项目的历史指标数据"
)
async def get_project_history(
    project_id: str,
    metric: str = Query(..., description="指标类型: social, onchain, score"),
    days: int = Query(7, ge=1, le=90, description="天数"),
    db: Session = Depends(get_db)
):
    """获取项目历史数据"""
    
    # TODO: 实现历史数据查询
    
    return {
        "success": True,
        "data": {
            "project_id": project_id,
            "metric_type": metric,
            "time_series": []
        }
    }

