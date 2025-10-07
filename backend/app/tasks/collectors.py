"""数据采集任务"""

import asyncio
from loguru import logger
from sqlalchemy import text
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


def update_platform_stats(db, platform: str, collected: int, discovered: int):
    """更新平台每日统计"""
    try:
        db.execute(text("""
            INSERT INTO platform_daily_stats (platform, stat_date, data_collected, projects_discovered)
            VALUES (:platform, CURRENT_DATE, :collected, :discovered)
            ON CONFLICT (platform, stat_date) 
            DO UPDATE SET 
                data_collected = platform_daily_stats.data_collected + :collected,
                projects_discovered = platform_daily_stats.projects_discovered + :discovered
        """), {"platform": platform, "collected": collected, "discovered": discovered})
        db.commit()
        logger.info(f"📊 [{platform}] Stats updated: {collected} collected, {discovered} discovered")
    except Exception as e:
        logger.warning(f"⚠️ [{platform}] Failed to update stats: {e}")


@celery_app.task(name="app.tasks.collectors.collect_twitter_data")
def collect_twitter_data():
    """采集Twitter数据(定时任务)"""
    logger.info("🚀 Starting Twitter data collection task...")
    
    try:
        # 真实采集 - 不使用mock数据
        projects = twitter_collector.collect_and_extract(hours=1)
        
        if not projects or len(projects) == 0:
            logger.warning("⚠️ No data from Twitter API - check API configuration")
            return {
                "success": False,
                "error": "No data collected - API may not be configured",
                "projects_found": 0,
                "projects_saved": 0
            }
        
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
                
                # 更新平台统计
                update_platform_stats(db, 'twitter', len(projects), saved_count)
                
                # 触发AI分析
                if saved_count > 0:
                    from app.tasks.analyzers import analyze_new_projects
                    analyze_new_projects.delay()
                    logger.info(f"🤖 Triggered AI analysis for {saved_count} new Twitter projects")
                
            except Exception as db_error:
                logger.error(f"❌ Database save failed: {db_error}")
                db.rollback()
            finally:
                db.close()
        
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
        # 真实采集 - 不使用mock数据
        projects = asyncio.run(
            telegram_collector.collect_and_extract(hours=1)
        )
        
        if not projects or len(projects) == 0:
            logger.warning("⚠️ No data from Telegram API - check API configuration")
            return {
                "success": False,
                "error": "No data collected - API may not be configured",
                "projects_found": 0,
                "projects_saved": 0
            }
        
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
                
                # 更新平台统计
                update_platform_stats(db, 'telegram', len(projects), saved_count)
                
                # 触发AI分析
                if saved_count > 0:
                    from app.tasks.analyzers import analyze_new_projects
                    analyze_new_projects.delay()
                    logger.info(f"🤖 Triggered AI analysis for {saved_count} new Telegram projects")
                
            except Exception as db_error:
                logger.error(f"❌ Database save failed: {db_error}")
                db.rollback()
            finally:
                db.close()
        
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
                            website=project_data.get('website'),
                            discovered_from='coingecko',
                            status='discovered'
                        )
                        db.add(new_project)
                        saved_count += 1
                
                db.commit()
                logger.info(f"💾 Saved {saved_count} new projects to database")
                
                # 更新平台统计
                update_platform_stats(db, 'coingecko', len(projects), saved_count)
                
                # 触发AI分析
                if saved_count > 0:
                    from app.tasks.analyzers import analyze_new_projects
                    analyze_new_projects.delay()
                    logger.info(f"🤖 Triggered AI analysis for {saved_count} new CoinGecko projects")
                
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


@celery_app.task(name="app.tasks.collectors.collect_medium_data")
def collect_medium_data():
    """采集Medium数据"""
    logger.info("🚀 Starting Medium data collection task...")
    
    try:
        from app.services.collectors.medium_collector import medium_collector
        
        # 采集文章
        articles = medium_collector.collect_and_analyze(scrape_full_text=False)
        
        logger.info(f"✅ Medium collection completed: {len(articles)} articles found")
        
        # TODO: 保存到数据库
        
        return {
            "success": True,
            "articles_found": len(articles),
            "source": "medium"
        }
        
    except Exception as e:
        logger.error(f"❌ Medium collection failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "articles_found": 0
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
    
    # Medium
    medium_result = collect_medium_data()
    results.append(medium_result)
    
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


@celery_app.task(name="app.tasks.collectors.discover_and_analyze_projects")
def discover_and_analyze_projects():
    """项目发现与分析任务（完整流程）"""
    logger.info("🚀 Starting project discovery and analysis workflow...")
    
    try:
        from app.services.project_discovery import project_discovery_service
        from app.services.scoring_engine import scoring_engine
        from app.services.action_plan_generator import action_plan_generator
        from datetime import datetime
        
        # 1. 收集各平台最新数据
        logger.info("📥 Step 1: Collecting data from all platforms...")
        
        twitter_data = twitter_collector.collect_and_extract(hours=6)
        telegram_data = asyncio.run(telegram_collector.collect_and_extract(hours=6))
        
        from app.services.collectors.medium_collector import medium_collector
        medium_data = medium_collector.collect_and_analyze(scrape_full_text=False)
        
        data_sources = {
            "twitter": twitter_data,
            "telegram": telegram_data,
            "medium": medium_data
        }
        
        logger.info(f"  ✅ Collected data from {len(data_sources)} platforms")
        
        # 2. 项目发现与聚合
        logger.info("🔍 Step 2: Discovering projects...")
        discovered_projects = project_discovery_service.discover_projects(data_sources)
        logger.info(f"  ✅ Discovered {len(discovered_projects)} high-quality projects")
        
        # 3. AI评分与分析
        logger.info("🤖 Step 3: Scoring projects...")
        analyzed_projects = []
        
        for project in discovered_projects[:20]:  # 只分析前20个
            try:
                # 评分
                score = scoring_engine.calculate_comprehensive_score(project)
                
                # 发币概率
                launch_prob = scoring_engine.predict_token_launch_probability(project)
                
                # 空投价值
                airdrop_value = scoring_engine.estimate_airdrop_value(project)
                
                # 生成行动计划（仅S和A级）
                action_plan = None
                if score.grade in ["S", "A"]:
                    action_plan = action_plan_generator.generate_action_plan(
                        project=project,
                        score=score.dict(),
                        launch_prob=launch_prob,
                        airdrop_value=airdrop_value
                    )
                
                analyzed_projects.append({
                    "project": project,
                    "score": score.dict(),
                    "launch_prob": launch_prob,
                    "airdrop_value": airdrop_value,
                    "action_plan": action_plan.dict() if action_plan else None,
                    "analyzed_at": str(datetime.utcnow())
                })
                
            except Exception as e:
                logger.error(f"  ❌ Error analyzing {project['project_name']}: {e}")
        
        logger.info(f"  ✅ Analyzed {len(analyzed_projects)} projects")
        
        # 4. 按分级分组
        s_tier = [p for p in analyzed_projects if p["score"]["grade"] == "S"]
        a_tier = [p for p in analyzed_projects if p["score"]["grade"] == "A"]
        b_tier = [p for p in analyzed_projects if p["score"]["grade"] == "B"]
        
        logger.info(f"  📊 Results: S-tier: {len(s_tier)}, A-tier: {len(a_tier)}, B-tier: {len(b_tier)}")
        
        # TODO: 保存报告到数据库
        # TODO: 发送S级项目的即时推送
        
        logger.info("✅ Project discovery and analysis workflow completed")
        
        return {
            "success": True,
            "discovered": len(discovered_projects),
            "analyzed": len(analyzed_projects),
            "s_tier": len(s_tier),
            "a_tier": len(a_tier)
        }
        
    except Exception as e:
        logger.error(f"❌ Error in discovery workflow: {e}")
        return {"success": False, "error": str(e)}

