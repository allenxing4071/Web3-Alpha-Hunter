"""应用配置管理"""

from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基础配置
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "web3-alpha-hunter-dev-secret-key-change-in-production"
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Web3 Alpha Hunter"
    VERSION: str = "1.0.0"
    
    # 数据库
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/web3hunter"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v) -> str:
        """解析CORS origins - 返回字符串,FastAPI会自动split"""
        if isinstance(v, str):
            return v
        elif isinstance(v, list):
            return ",".join(v)
        return "http://localhost:3000,http://localhost:3001"
    
    def get_cors_origins_list(self) -> List[str]:
        """获取CORS origins列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # AI服务
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None  # DeepSeek AI (国内)
    
    # Twitter API
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    # Telegram API
    TELEGRAM_API_ID: Optional[str] = None
    TELEGRAM_API_HASH: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # YouTube API
    YOUTUBE_API_KEY: Optional[str] = None
    
    # Web3
    INFURA_PROJECT_ID: Optional[str] = None
    ETHEREUM_RPC_URL: Optional[str] = None
    SOLANA_RPC_URL: Optional[str] = None
    
    # CoinGecko
    COINGECKO_API_KEY: Optional[str] = None
    
    # Cloudflare R2
    R2_ACCOUNT_ID: Optional[str] = None
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_BUCKET_NAME: str = "web3-alpha-hunter-assets"
    
    # 监控
    SENTRY_DSN: Optional[str] = None
    LOGTAIL_TOKEN: Optional[str] = None
    
    # 邮件
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "noreply@web3alphahunter.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()

