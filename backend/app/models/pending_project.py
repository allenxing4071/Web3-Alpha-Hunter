"""待审核项目数据模型"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Text, DECIMAL, 
    TIMESTAMP, Index, JSON
)
from sqlalchemy.sql import func
from app.db.session import Base


class PendingProject(Base):
    """待审核项目表 - AI推荐等待人工确认的项目"""
    
    __tablename__ = "projects_pending"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 基础信息
    project_name = Column(String(255), nullable=False, index=True)
    symbol = Column(String(50))
    description = Column(Text)
    
    # 发现来源
    discovered_from = Column(String(100))  # twitter, telegram, coingecko
    source_url = Column(String(500))  # 原始链接
    
    # AI评估结果
    ai_score = Column(DECIMAL(5, 2))  # AI评分 0-100
    ai_grade = Column(String(1))  # S, A, B, C, D
    ai_confidence = Column(DECIMAL(5, 2))  # AI置信度 0-1
    ai_recommendation_reason = Column(JSON)  # AI推荐理由
    ai_extracted_info = Column(JSON)  # AI提取的完整信息
    
    # 审核状态
    review_status = Column(String(20), default="pending", index=True)  # pending, approved, rejected
    reviewed_at = Column(TIMESTAMP)
    reviewed_by = Column(String(100))  # 审核人
    reject_reason = Column(Text)  # 拒绝理由
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 索引
    __table_args__ = (
        Index('idx_pending_status_score', 'review_status', 'ai_score'),
        Index('idx_pending_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<PendingProject(id={self.id}, name='{self.project_name}', grade='{self.ai_grade}', status='{self.review_status}')>"
