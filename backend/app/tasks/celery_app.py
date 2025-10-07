"""Celery应用配置"""

from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# 创建Celery应用
celery_app = Celery(
    "web3_alpha_hunter",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.collectors", "app.tasks.analyzers"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分钟超时
    worker_prefetch_multiplier=1,
)

# 定时任务配置
celery_app.conf.beat_schedule = {
    # 每30分钟采集CoinGecko数据（免费API）
    "collect-coingecko-data": {
        "task": "app.tasks.collectors.collect_coingecko_data",
        "schedule": crontab(minute="*/30"),  # 每30分钟
    },
    
    # 每15分钟采集Twitter数据（Apify第三方服务）
    "collect-twitter-data": {
        "task": "app.tasks.collectors.collect_twitter_data",
        "schedule": crontab(minute="*/15"),  # 每15分钟（平衡配额和数据新鲜度）
    },
    
    # 每15分钟采集Telegram数据（免费API）
    "collect-telegram-data": {
        "task": "app.tasks.collectors.collect_telegram_data",
        "schedule": crontab(minute="*/15"),  # 每15分钟
    },
    
    # 每小时更新项目评分
    "update-project-scores": {
        "task": "app.tasks.analyzers.update_all_scores",
        "schedule": crontab(minute=0),  # 每小时整点
    },
    
    # 每天早上9点生成报告
    "generate-daily-report": {
        "task": "app.tasks.reporters.generate_daily_report",
        "schedule": crontab(hour=9, minute=0),  # 每天9:00
    },
}

