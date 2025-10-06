#!/usr/bin/env python3
"""重置管理员密码"""

import bcrypt
from sqlalchemy import create_engine, text
from app.core.config import settings

def hash_password(password: str) -> str:
    """密码加密"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def reset_admin_password():
    """重置管理员密码为 admin123"""
    
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    # 新密码
    new_password = "admin123"
    hashed = hash_password(new_password)
    
    print(f"🔐 重置管理员密码")
    print(f"新密码: {new_password}")
    print(f"密码哈希: {hashed}")
    
    # 更新数据库
    with engine.connect() as conn:
        # 检查admin用户是否存在
        result = conn.execute(text("SELECT id, username, role FROM users WHERE username = 'admin'"))
        user = result.fetchone()
        
        if user:
            print(f"\n✅ 找到用户: {user[1]} (ID: {user[0]}, 角色: {user[2]})")
            
            # 更新密码
            conn.execute(
                text("UPDATE users SET password_hash = :hash, is_active = true WHERE username = 'admin'"),
                {"hash": hashed}
            )
            conn.commit()
            print(f"✅ 密码已更新")
            
        else:
            print("\n❌ 未找到admin用户，创建新用户...")
            
            # 创建管理员用户
            conn.execute(
                text("""
                    INSERT INTO users (id, username, email, password_hash, role, is_active, created_at, updated_at)
                    VALUES (gen_random_uuid(), 'admin', 'admin@example.com', :hash, 'admin', true, NOW(), NOW())
                """),
                {"hash": hashed}
            )
            conn.commit()
            print(f"✅ 管理员用户已创建")
    
    print(f"\n🎉 完成！现在可以使用以下凭据登录：")
    print(f"   用户名: admin")
    print(f"   密码: {new_password}")

if __name__ == "__main__":
    reset_admin_password()

