"""用户管理API"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
import bcrypt
import uuid
from datetime import datetime

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, LoginResponse
)

router = APIRouter(prefix="/users", tags=["users"])


def hash_password(password: str) -> str:
    """密码加密"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


@router.post("/login")
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """用户登录"""
    try:
        # 查询用户
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user:
            return LoginResponse(
                success=False,
                message="用户名或密码错误",
                user=None,
                token=None
            )
        
        # 验证密码
        if not verify_password(login_data.password, user.password_hash):
            return LoginResponse(
                success=False,
                message="用户名或密码错误",
                user=None,
                token=None
            )
        
        # 检查账号状态
        if not user.is_active:
            return LoginResponse(
                success=False,
                message="账号已被禁用",
                user=None,
                token=None
            )
        
        # 更新最后登录时间
        user.last_login_at = datetime.utcnow()
        db.commit()
        
        # 生成简单token（实际应使用JWT）
        token = f"{user.id}:{user.username}:{user.role}"
        
        return LoginResponse(
            success=True,
            message="登录成功",
            user=UserResponse.from_orm(user),
            token=token
        )
        
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[UserResponse])
async def list_users(
    db: Session = Depends(get_db)
) -> List[UserResponse]:
    """获取所有用户列表"""
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        return [UserResponse.from_orm(user) for user in users]
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
) -> UserResponse:
    """获取单个用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return UserResponse.from_orm(user)


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """创建新用户"""
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="邮箱已被使用")
        
        # 创建用户
        new_user = User(
            id=str(uuid.uuid4()),
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role=user_data.role,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserResponse.from_orm(new_user)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ 创建用户失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """更新用户信息"""
    try:
        # 查找用户
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 更新字段
        if user_data.username is not None:
            # 检查新用户名是否已存在
            existing = db.query(User).filter(
                User.username == user_data.username,
                User.id != user_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="用户名已存在")
            user.username = user_data.username
        
        if user_data.email is not None:
            # 检查新邮箱是否已被使用
            existing = db.query(User).filter(
                User.email == user_data.email,
                User.id != user_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="邮箱已被使用")
            user.email = user_data.email
        
        if user_data.password is not None:
            user.password_hash = hash_password(user_data.password)
        
        if user_data.role is not None:
            user.role = user_data.role
        
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        
        db.commit()
        db.refresh(user)
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ 更新用户失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除用户"""
    try:
        # 查找用户
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 不允许删除管理员
        if user.role == "admin":
            raise HTTPException(status_code=403, detail="不能删除管理员账号")
        
        # 检查是否是最后一个用户
        user_count = db.query(User).count()
        if user_count <= 1:
            raise HTTPException(status_code=403, detail="不能删除最后一个用户")
        
        db.delete(user)
        db.commit()
        
        return {
            "success": True,
            "message": "用户已删除"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ 删除用户失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/init-default")
async def initialize_default_users(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """初始化默认用户（如果不存在）"""
    try:
        # 检查是否已有管理员
        admin = db.query(User).filter(User.role == "admin").first()
        if admin:
            return {
                "success": True,
                "message": "默认管理员已存在",
                "created": False
            }
        
        # 创建默认管理员
        admin_user = User(
            id="admin-default-001",
            username="admin",
            email="admin@web3hunter.com",
            password_hash=hash_password("admin123"),
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        return {
            "success": True,
            "message": "默认管理员已创建",
            "created": True,
            "username": "admin",
            "default_password": "admin123"
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ 初始化默认用户失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

