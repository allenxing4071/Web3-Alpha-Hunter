"""用户模型"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Index
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    """系统用户表"""
    
    __tablename__ = "users"
    
    # 主键
    id = Column(String(50), primary_key=True, index=True)
    
    # 认证信息
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # 权限
    role = Column(String(20), nullable=False, default="user", index=True)  # admin, user
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    last_login_at = Column(TIMESTAMP, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

