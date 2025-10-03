"""项目相关的Pydantic模型"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ProjectGrade(str, Enum):
    """项目等级"""
    S = "S"
    A = "A"
    B = "B"
    C = "C"


class ProjectCategory(str, Enum):
    """项目分类"""
    DEFI = "DeFi"
    NFT = "NFT"
    GAMEFI = "GameFi"
    INFRASTRUCTURE = "Infrastructure"
    AI = "AI"
    SOCIAL = "Social"


class ProjectScores(BaseModel):
    """项目评分详情"""
    overall: float = Field(..., ge=0, le=100, description="综合评分")
    team: float = Field(..., ge=0, le=100, description="团队评分")
    technology: float = Field(..., ge=0, le=100, description="技术评分")
    community: float = Field(..., ge=0, le=100, description="社区评分")
    tokenomics: float = Field(..., ge=0, le=100, description="代币经济学评分")
    market_timing: float = Field(..., ge=0, le=100, description="市场时机评分")
    risk: float = Field(..., ge=0, le=100, description="风险评分")


class SocialLinks(BaseModel):
    """社交媒体链接"""
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    discord: Optional[str] = None
    github: Optional[str] = None


class RiskFlag(BaseModel):
    """风险标记"""
    type: str = Field(..., description="风险类型")
    severity: str = Field(..., description="严重程度: low, medium, high")
    message: str = Field(..., description="风险描述")


class CurrentMetrics(BaseModel):
    """当前指标"""
    market_cap: Optional[float] = None
    price_usd: Optional[float] = None
    volume_24h: Optional[float] = None
    tvl_usd: Optional[float] = None
    holder_count: Optional[int] = None
    twitter_followers: Optional[int] = None
    telegram_members: Optional[int] = None
    github_stars: Optional[int] = None
    github_commits_last_week: Optional[int] = None


class ProjectBase(BaseModel):
    """项目基础信息"""
    name: str = Field(..., min_length=1, max_length=255)
    symbol: Optional[str] = Field(None, max_length=50)
    blockchain: Optional[str] = None
    category: Optional[ProjectCategory] = None
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """创建项目"""
    contract_address: Optional[str] = None
    website: Optional[str] = None
    discovered_from: str = Field(..., description="发现来源")


class ProjectListItem(BaseModel):
    """项目列表项"""
    project_id: str
    name: str
    symbol: Optional[str] = None
    grade: ProjectGrade
    overall_score: float
    category: Optional[str] = None
    blockchain: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    social_links: SocialLinks
    key_highlights: List[str] = Field(default_factory=list)
    risk_flags: List[RiskFlag] = Field(default_factory=list)
    metrics: CurrentMetrics
    first_discovered_at: datetime
    last_updated_at: datetime
    
    class Config:
        from_attributes = True


class SimilarProject(BaseModel):
    """相似项目"""
    name: str
    similarity_score: float = Field(..., ge=0, le=1)
    matching_features: List[str]


class AIAnalysisDetail(BaseModel):
    """AI分析详情"""
    summary: str
    key_features: List[str]
    similar_projects: List[SimilarProject]
    sentiment: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    investment_suggestion: Dict[str, Any]


class ProjectDetail(ProjectListItem):
    """项目详情"""
    contract_address: Optional[str] = None
    whitepaper_url: Optional[str] = None
    github_repo: Optional[str] = None
    
    scores: ProjectScores
    ai_analysis: Optional[AIAnalysisDetail] = None
    
    discovery: Dict[str, Any]  # 发现来源信息
    

class ProjectListResponse(BaseModel):
    """项目列表响应"""
    success: bool = True
    data: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "projects": [],
                    "pagination": {
                        "current_page": 1,
                        "total_pages": 5,
                        "total_items": 47,
                        "items_per_page": 10
                    }
                }
            }
        }


class ProjectDetailResponse(BaseModel):
    """项目详情响应"""
    success: bool = True
    data: ProjectDetail

