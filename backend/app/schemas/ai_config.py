"""
AI配置Pydantic模型
"""

from pydantic import BaseModel
from typing import Optional


class AIConfigBase(BaseModel):
    """AI配置基础模型"""
    name: str
    key: str
    enabled: bool
    model: str


class AIConfigCreate(AIConfigBase):
    """创建AI配置"""
    pass


class AIConfigUpdate(BaseModel):
    """更新AI配置"""
    key: Optional[str] = None
    enabled: Optional[bool] = None
    model: Optional[str] = None


class AIConfigResponse(BaseModel):
    """AI配置响应"""
    id: str
    name: str
    enabled: bool
    model: str
    has_key: bool  # 是否已配置密钥(不返回实际密钥)
    
    class Config:
        from_attributes = True


class AITestRequest(BaseModel):
    """AI连接测试请求"""
    provider: str  # deepseek/claude/openai
    api_key: str
    model: str


class AITestResponse(BaseModel):
    """AI连接测试响应"""
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None

