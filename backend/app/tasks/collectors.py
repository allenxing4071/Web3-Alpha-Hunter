"""数据采集任务"""

import asyncio
from loguru import logger
from app.tasks.celery_app import celery_app
from app.services.collectors.twitter import twitter_collector
from app.services.collectors.telegram import telegram_collector
from app.services.collectors.coingecko import coingecko_collector
from app.services.collectors.test_collector import (
    mock_twitter_collector, 
    mock_telegram_collector
)
from app.db import SessionLocal
from app.models import Project


@celery_app.task(name="app.tasks.collectors.collect_twitter_data")
def collect_twitter_data():
    """采集Twitter数据(定时任务)"""
    logger.info("🚀 Starting Twitter data collection task...")
    
    try:
        # 先尝试真实采集
        projects = twitter_collector.collect_and_extract(hours=1)
        
        # 如果没有数据,使用mock数据
        if not projects or len(projects) == 0:
            logger.warning("⚠️ No data from real Twitter API, using mock data")
            projects = mock_twitter_collector.collect_and_extract(hours=1)
        
        logger.info(f"✅ Twitter collection completed: {len(projects)} projects found")
        
        # 保存到数据库
        saved_count = 0
        if projects:
            db = SessionLocal()
            try:
                for project_data in projects:
                    # 检查项目是否已存在
                    existing = db.query(Project).filter(
                        Project.project_name == project_data.get('name')
                    ).first()
                    
                    if not existing:
                        # 创建新项目
                        new_project = Project(
                            project_name=project_data.get('name', 'Unknown'),
                            symbol=project_data.get('symbol'),
                            description=project_data.get('description'),
                            twitter_handle=project_data.get('twitter'),
                            discovered_from='twitter',
                            status='discovered'
                        )
                        db.add(new_project)
                        saved_count += 1
                
                db.commit()
                logger.info(f"💾 Saved {saved_count} new projects to database")
                
            except Exception as db_error:
                logger.error(f"❌ Database save failed: {db_error}")
                db.rollback()
            finally:
                db.close()
        
        # TODO: 触发AI分析 (需要API密钥)
        
        return {
            "success": True,
            "projects_found": len(projects),
            "projects_saved": saved_count,
            "source": "twitter"
        }
        
    except Exception as e:
        logger.error(f"❌ Twitter collection failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "projects_found": 0
        }


@celery_app.task(name="app.tasks.collectors.collect_telegram_data")
def collect_telegram_data():
    """采集Telegram数据(定时任务)"""
    logger.info("🚀 Starting Telegram data collection task...")
    
    try:
        # 先尝试真实采集
        projects = asyncio.run(
            telegram_collector.collect_and_extract(hours=1)
        )
        
        # 如果没有数据,使用mock数据
        if not projects or len(projects) == 0:
            logger.warning("⚠️ No data from real Telegram API, using mock data")
            projects = asyncio.run(mock_telegram_collector.collect_and_extract(hours=1))
        
        logger.info(f"✅ Telegram collection completed: {len(projects)} projects found")
        
        # 保存到数据库
        saved_count = 0
        if projects:
            db = SessionLocal()
            try:
                for project_data in projects:
                    # 检查项目是否已存在
                    existing = db.query(Project).filter(
                        Project.project_name == project_data.get('name')
                    ).first()
                    
                    if not existing:
                        # 创建新项目
                        new_project = Project(
                            project_name=project_data.get('name', 'Unknown'),
                            symbol=project_data.get('symbol'),
                            description=project_data.get('description'),
                            telegram_channel=project_data.get('telegram'),
                            discovered_from='telegram',
                            status='discovered'
                        )
                        db.add(new_project)
                        saved_count += 1
                
                db.commit()
                logger.info(f"💾 Saved {saved_count} new projects to database")
                
            except Exception as db_error:
                logger.error(f"❌ Database save failed: {db_error}")
                db.rollback()
            finally:
                db.close()
        
        # TODO: 触发AI分析 (需要API密钥)
        
        return {
            "success": True,
            "projects_found": len(projects),
            "projects_saved": saved_count,
            "source": "telegram"
        }
        
    except Exception as e:
        logger.error(f"❌ Telegram collection failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "projects_found": 0
        }


@celery_app.task(name="app.tasks.collectors.collect_coingecko_data")
def collect_coingecko_data():
    """采集CoinGecko数据"""
    logger.info("🚀 Starting CoinGecko data collection task...")
    
    try:
        # CoinGecko采集
        projects = coingecko_collector.collect_and_extract()
        
        logger.info(f"✅ CoinGecko collection completed: {len(projects)} projects found")
        
        # 保存到数据库
        saved_count = 0
        if projects:
            db = SessionLocal()
            try:
                for project_data in projects:
                    # 检查项目是否已存在
                    existing = db.query(Project).filter(
                        Project.project_name == project_data.get('name')
                    ).first()
                    
                    if not existing:
                        # 创建新项目
                        new_project = Project(
                            project_name=project_data.get('name', 'Unknown'),
                            symbol=project_data.get('symbol'),
                            description=project_data.get('description'),
                            coingecko_id=project_data.get('coingecko_id'),
                            market_cap_rank=project_data.get('market_cap_rank'),
                            discovered_from='coingecko',
                            status='discovered'
                        )
                        db.add(new_project)
                        saved_count += 1
                
                db.commit()
                logger.info(f"💾 Saved {saved_count} new projects to database")
                
            except Exception as db_error:
                logger.error(f"❌ Database save failed: {db_error}")
                db.rollback()
            finally:
                db.close()
        
        return {
            "success": True,
            "projects_found": len(projects),
            "projects_saved": saved_count,
            "source": "coingecko"
        }
        
    except Exception as e:
        logger.error(f"❌ CoinGecko collection failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "projects_found": 0
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
    
    # CoinGecko
    coingecko_result = collect_coingecko_data()
    results.append(coingecko_result)
    
    # 统计
    total_projects = sum(r.get("projects_found", 0) for r in results)
    total_saved = sum(r.get("projects_saved", 0) for r in results)
    
    logger.info(f"✅ Multi-source collection completed: {total_projects} projects found, {total_saved} saved")
    
    return {
        "success": True,
        "total_projects": total_projects,
        "projects_saved": total_saved,
        "results": results
    }

