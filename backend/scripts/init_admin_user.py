#!/usr/bin/env python3
"""初始化管理员用户"""

from app.db.session import SessionLocal
from app.models.user import User
from app.api.v1.users import hash_password
import uuid

def main():
    db = SessionLocal()
    try:
        # 检查admin用户是否存在
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            # 创建admin用户
            admin = User(
                id=str(uuid.uuid4()),
                username='admin',
                email='admin@web3hunter.com',
                password_hash=hash_password('admin123'),
                role='admin',
                is_active=True
            )
            db.add(admin)
            db.commit()
            print('✅ 管理员已创建')
            print('   用户名: admin')
            print('   密码: admin123')
        else:
            print('✅ 管理员已存在')
            print(f'   ID: {admin.id}')
            print(f'   用户名: {admin.username}')
            print(f'   角色: {admin.role}')
            
    except Exception as e:
        print(f'❌ 错误: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()

