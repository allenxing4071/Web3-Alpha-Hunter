"""项目数据模型"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Integer, Text, DECIMAL, 
    TIMESTAMP, Index, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Project(Base):
    """项目主表"""
    
    __tablename__ = "projects"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 基础信息
    project_name = Column(String(255), nullable=False, index=True)
    symbol = Column(String(50))
    contract_address = Column(String(255), unique=True)
    blockchain = Column(String(50), index=True)
    category = Column(String(100), index=True)  # DeFi, NFT, GameFi, Infrastructure
    
    # 描述信息
    description = Column(Text)
    website = Column(String(500))
    whitepaper_url = Column(String(500))
    twitter_handle = Column(String(100))
    telegram_channel = Column(String(100))
    discord_link = Column(String(500))
    github_repo = Column(String(500))
    
    # 评分相关
    overall_score = Column(DECIMAL(5, 2), index=True)  # 综合评分 0-100
    team_score = Column(DECIMAL(5, 2))
    tech_score = Column(DECIMAL(5, 2))
    community_score = Column(DECIMAL(5, 2))
    tokenomics_score = Column(DECIMAL(5, 2))
    market_timing_score = Column(DECIMAL(5, 2))
    risk_score = Column(DECIMAL(5, 2))
    
    grade = Column(String(1), index=True)  # S, A, B, C
    
    # 关联外键
    social_metrics_id = Column(Integer, ForeignKey('social_metrics.id', ondelete='SET NULL'), nullable=True, index=True)
    onchain_metrics_id = Column(Integer, ForeignKey('onchain_metrics.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # 状态
    status = Column(String(50), default="discovered")  # discovered, analyzing, published, archived
    first_discovered_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    last_updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 元数据
    discovered_from = Column(String(100))  # twitter, telegram, youtube, etc.
    logo_url = Column(String(500))
    
    # JSONB字段存储灵活数据
    extra_metadata = Column(JSON)  # 额外的元数据(重命名避免与SQLAlchemy保留字冲突)
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    social_metrics = relationship("SocialMetrics", foreign_keys=[social_metrics_id], lazy="joined")
    onchain_metrics = relationship("OnchainMetrics", foreign_keys=[onchain_metrics_id], lazy="joined")
    
    # 索引
    __table_args__ = (
        Index('idx_score_grade', 'overall_score', 'grade'),
        Index('idx_discovered_at', 'first_discovered_at'),
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.project_name}', grade='{self.grade}', score={self.overall_score})>"


class SocialMetrics(Base):
    """社交媒体指标"""
    
    __tablename__ = "social_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    
    # Twitter数据
    twitter_followers = Column(Integer)
    twitter_engagement_rate = Column(DECIMAL(5, 2))
    
    # Telegram数据
    telegram_members = Column(Integer)
    telegram_online_members = Column(Integer)
    telegram_message_frequency = Column(Integer)  # 消息/小时
    
    # Discord数据
    discord_members = Column(Integer)
    discord_online_members = Column(Integer)
    
    # YouTube数据
    youtube_mentions = Column(Integer)  # 被提及次数
    youtube_total_views = Column(Integer)
    
    # GitHub数据
    github_stars = Column(Integer)
    github_forks = Column(Integer)
    github_commits_last_week = Column(Integer)
    github_contributors = Column(Integer)
    
    # 时间戳
    snapshot_time = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_social_metrics_project', 'project_id', 'snapshot_time'),
    )


class OnchainMetrics(Base):
    """链上数据指标"""
    
    __tablename__ = "onchain_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    
    # 基础数据
    market_cap = Column(DECIMAL(20, 2))
    total_supply = Column(DECIMAL(30, 2))
    circulating_supply = Column(DECIMAL(30, 2))
    price_usd = Column(DECIMAL(20, 8))
    
    # 流动性数据
    liquidity_usd = Column(DECIMAL(20, 2))
    volume_24h = Column(DECIMAL(20, 2))
    
    # 持有者数据
    holder_count = Column(Integer)
    top_10_holders_percentage = Column(DECIMAL(5, 2))
    
    # 交易数据
    transaction_count_24h = Column(Integer)
    unique_wallets_24h = Column(Integer)
    
    # TVL (for DeFi)
    tvl_usd = Column(DECIMAL(20, 2))
    
    # 时间戳
    snapshot_time = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_onchain_metrics_project', 'project_id', 'snapshot_time'),
    )


class AIAnalysis(Base):
    """AI分析结果"""
    
    __tablename__ = "ai_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    
    # 文本分析
    whitepaper_summary = Column(Text)
    key_features = Column(JSON)  # ["特性1", "特性2", ...]
    similar_projects = Column(JSON)  # [{"name": "Solana", "similarity": 0.85}, ...]
    
    # 情感分析
    sentiment_score = Column(DECIMAL(5, 2))  # -1 到 1
    sentiment_label = Column(String(20))  # positive, neutral, negative
    
    # 风险识别
    risk_flags = Column(JSON)  # [{"type": "team_anonymous", "severity": "medium"}, ...]
    scam_probability = Column(DECIMAL(5, 2))  # 0-100
    
    # 推荐建议
    investment_suggestion = Column(Text)
    position_size = Column(String(50))  # 1-3%, 3-5%, 5-10%
    entry_timing = Column(String(100))
    stop_loss_percentage = Column(DECIMAL(5, 2))
    
    # 时间戳
    analyzed_at = Column(TIMESTAMP, server_default=func.now())
    
    def __repr__(self):
        return f"<AIAnalysis(project_id={self.project_id}, sentiment='{self.sentiment_label}')>"

