"""测试API端点"""

from fastapi import APIRouter
from app.services.collectors.test_collector import (
    mock_twitter_collector,
    mock_telegram_collector
)

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/twitter-collection")
async def test_twitter_collection():
    """测试Twitter数据采集"""
    projects = mock_twitter_collector.collect_and_extract(hours=24)
    
    return {
        "success": True,
        "message": "Mock Twitter collection test",
        "projects_found": len(projects),
        "projects": projects
    }


@router.get("/telegram-collection")
async def test_telegram_collection():
    """测试Telegram数据采集"""
    projects = await mock_telegram_collector.collect_and_extract(hours=24)
    
    return {
        "success": True,
        "message": "Mock Telegram collection test",
        "projects_found": len(projects),
        "projects": projects
    }


@router.get("/all-sources")
async def test_all_sources():
    """测试所有数据源"""
    twitter_projects = mock_twitter_collector.collect_and_extract(hours=24)
    telegram_projects = await mock_telegram_collector.collect_and_extract(hours=24)
    
    all_projects = twitter_projects + telegram_projects
    
    return {
        "success": True,
        "total_projects": len(all_projects),
        "twitter": len(twitter_projects),
        "telegram": len(telegram_projects),
        "projects": all_projects
    }

