"""用户Schema"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """用户基础Schema"""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: str = Field(default="user", pattern="^(admin|user)$")


class UserCreate(UserBase):
    """创建用户Schema"""
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """更新用户Schema"""
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    role: Optional[str] = Field(None, pattern="^(admin|user)$")
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """用户响应Schema（不包含密码）"""
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """用户登录Schema"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """登录响应Schema"""
    success: bool
    message: str
    user: Optional[UserResponse] = None
    token: Optional[str] = None

