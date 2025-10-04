"""
初始化AI配置 - 将WildCard密钥写入数据库
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 强制使用SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./web3hunter.db'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.models.ai_config import AIConfig
from cryptography.fernet import Fernet
import base64
import hashlib
import uuid

# 创建SQLite引擎
engine = create_engine('sqlite:///./web3hunter.db', connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 解密密钥（与admin.py保持一致）
ENCRYPTION_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"web3-alpha-hunter-secret-key").digest())
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_api_key(api_key: str) -> str:
    """加密API密钥"""
    return cipher_suite.encrypt(api_key.encode()).decode()

def init_ai_configs():
    """初始化AI配置"""
    db = SessionLocal()
    
    try:
        # WildCard统一密钥
        wildcard_key = "sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB"
        
        # 配置列表
        configs = [
            {
                "name": "DeepSeek",
                "api_key": wildcard_key,
                "enabled": False,  # 默认不启用
                "model": "deepseek-chat"
            },
            {
                "name": "Claude",
                "api_key": wildcard_key,
                "enabled": True,  # 默认启用Claude
                "model": "claude-3-5-sonnet-20241022"
            },
            {
                "name": "OpenAI",
                "api_key": wildcard_key,
                "enabled": False,  # 默认不启用
                "model": "gpt-3.5-turbo"
            }
        ]
        
        for config_data in configs:
            # 查找是否已存在
            existing = db.query(AIConfig).filter(
                AIConfig.name == config_data["name"]
            ).first()
            
            if existing:
                # 更新现有配置
                existing.api_key = encrypt_api_key(config_data["api_key"])
                existing.enabled = config_data["enabled"]
                existing.model = config_data["model"]
                print(f"✅ 更新 {config_data['name']} 配置")
            else:
                # 创建新配置
                new_config = AIConfig(
                    id=str(uuid.uuid4()),
                    name=config_data["name"],
                    api_key=encrypt_api_key(config_data["api_key"]),
                    enabled=config_data["enabled"],
                    model=config_data["model"]
                )
                db.add(new_config)
                print(f"✅ 创建 {config_data['name']} 配置")
        
        db.commit()
        print("\n🎉 AI配置初始化完成！")
        print("\n当前配置：")
        
        all_configs = db.query(AIConfig).all()
        for cfg in all_configs:
            status = "✅ 已启用" if cfg.enabled else "⭕ 未启用"
            print(f"  - {cfg.name}: {status} (model: {cfg.model})")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 开始初始化AI配置...")
    init_ai_configs()

