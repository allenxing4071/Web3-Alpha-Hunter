"""
AI配置模型 - 存储AI模型API密钥和配置
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.session import Base


class AIConfig(Base):
    """AI模型配置表"""
    __tablename__ = "ai_configs"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="AI模型名称 (DeepSeek/Claude/OpenAI)")
    api_key = Column(Text, nullable=False, comment="加密后的API密钥")
    enabled = Column(Boolean, default=False, comment="是否启用")
    model = Column(String, nullable=False, comment="模型名称")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AIConfig {self.name} enabled={self.enabled}>"

