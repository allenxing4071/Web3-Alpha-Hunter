"""数据采集任务"""

import asyncio
from loguru import logger
from app.tasks.celery_app import celery_app
from app.services.collectors.twitter import twitter_collector
from app.services.collectors.telegram import telegram_collector
from app.db import SessionLocal
from app.models import Project


@celery_app.task(name="app.tasks.collectors.collect_twitter_data")
def collect_twitter_data():
    """采集Twitter数据(定时任务)"""
    logger.info("🚀 Starting Twitter data collection task...")
    
    try:
        # 采集过去1小时的数据
        projects = twitter_collector.collect_and_extract(hours=1)
        
        logger.info(f"✅ Twitter collection completed: {len(projects)} projects found")
        
        # TODO: 保存到数据库
        # TODO: 触发AI分析
        
        return {
            "success": True,
            "projects_found": len(projects),
            "source": "twitter"
        }
        
    except Exception as e:
        logger.error(f"❌ Twitter collection failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@celery_app.task(name="app.tasks.collectors.collect_telegram_data")
def collect_telegram_data():
    """采集Telegram数据(定时任务)"""
    logger.info("🚀 Starting Telegram data collection task...")
    
    try:
        # 使用asyncio运行异步函数
        projects = asyncio.run(
            telegram_collector.collect_and_extract(hours=1)
        )
        
        logger.info(f"✅ Telegram collection completed: {len(projects)} projects found")
        
        # TODO: 保存到数据库
        # TODO: 触发AI分析
        
        return {
            "success": True,
            "projects_found": len(projects),
            "source": "telegram"
        }
        
    except Exception as e:
        logger.error(f"❌ Telegram collection failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@celery_app.task(name="app.tasks.collectors.collect_all_sources")
def collect_all_sources():
    """采集所有数据源"""
    logger.info("🚀 Starting multi-source data collection...")
    
    results = []
    
    # Twitter
    twitter_result = collect_twitter_data()
    results.append(twitter_result)
    
    # Telegram
    telegram_result = collect_telegram_data()
    results.append(telegram_result)
    
    # 统计
    total_projects = sum(r.get("projects_found", 0) for r in results)
    
    logger.info(f"✅ Multi-source collection completed: {total_projects} total projects")
    
    return {
        "success": True,
        "total_projects": total_projects,
        "results": results
    }

