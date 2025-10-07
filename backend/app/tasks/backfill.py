"""数据回填任务 - 补全现有项目的缺失字段"""

from loguru import logger
from sqlalchemy import text
from app.tasks.celery_app import celery_app
from app.db import SessionLocal
from app.models import Project
from app.services.collectors.coingecko import coingecko_collector
from app.services.enhancers.data_enricher import data_enricher


@celery_app.task(name="app.tasks.backfill.backfill_existing_projects")
def backfill_existing_projects():
    """回填现有项目的完整数据
    
    对于每个项目：
    1. 如果来源是CoinGecko且有coingecko_id，调用详情API补全
    2. 否则，使用AI + 文本提取补全
    3. 批量更新数据库
    """
    logger.info("🔄 Starting backfill task for existing projects...")
    
    try:
        db = SessionLocal()
        
        # 查询所有项目
        all_projects = db.query(Project).all()
        logger.info(f"📊 Found {len(all_projects)} projects to potentially backfill")
        
        # 统计需要补全的项目
        incomplete_projects = []
        for project in all_projects:
            # 检查数据完整度
            is_incomplete = (
                not project.blockchain or
                not project.category or
                not project.website or
                not project.twitter_handle
            )
            
            if is_incomplete:
                incomplete_projects.append(project)
        
        logger.info(f"🎯 Found {len(incomplete_projects)} incomplete projects to backfill")
        
        if not incomplete_projects:
            logger.info("✅ All projects are complete, no backfill needed")
            return {
                "success": True,
                "backfilled": 0,
                "total": len(all_projects)
            }
        
        backfilled_count = 0
        
        for project in incomplete_projects:
            try:
                logger.info(f"🔍 Backfilling project: {project.project_name} (ID: {project.id})")
                
                enriched_data = {}
                
                # 方法1：如果是CoinGecko项目且有coingecko_id
                if project.discovered_from == 'coingecko':
                    # 尝试从extra_metadata中获取coingecko_id
                    coingecko_id = None
                    if project.extra_metadata and isinstance(project.extra_metadata, dict):
                        coingecko_id = project.extra_metadata.get('coingecko_id')
                    
                    # 如果没有coingecko_id，尝试从项目名称生成
                    if not coingecko_id:
                        # CoinGecko ID通常是小写+连字符
                        coingecko_id = project.project_name.lower().replace(' ', '-')
                    
                    logger.info(f"  📡 Fetching CoinGecko details for: {coingecko_id}")
                    details = coingecko_collector.get_coin_details(coingecko_id)
                    
                    if details:
                        enriched_data = details
                        logger.info(f"  ✅ Got details from CoinGecko API")
                    else:
                        logger.warning(f"  ⚠️ Failed to get CoinGecko details, falling back to AI")
                
                # 方法2：使用AI补全（如果方法1失败或不适用）
                if not enriched_data or not enriched_data.get('blockchain'):
                    project_data = {
                        'name': project.project_name,
                        'description': project.description or '',
                        'symbol': project.symbol,
                    }
                    ai_enriched = data_enricher.enrich_project(project_data)
                    logger.info(f"  🤖 Used AI enrichment")
                    
                    # 合并AI推理的数据到enriched_data
                    if not enriched_data:
                        enriched_data = ai_enriched
                    else:
                        # 只填充CoinGecko没有获取到的字段
                        for key, value in ai_enriched.items():
                            if not enriched_data.get(key) and value:
                                enriched_data[key] = value
                
                # 更新项目字段（只更新缺失的字段）
                updated = False
                
                if not project.blockchain and enriched_data.get('blockchain'):
                    project.blockchain = enriched_data['blockchain']
                    updated = True
                
                if not project.category and enriched_data.get('category'):
                    project.category = enriched_data['category']
                    updated = True
                
                if not project.website and enriched_data.get('website'):
                    project.website = enriched_data['website']
                    updated = True
                
                if not project.twitter_handle and enriched_data.get('twitter'):
                    project.twitter_handle = enriched_data['twitter']
                    updated = True
                
                if not project.telegram_channel and enriched_data.get('telegram'):
                    project.telegram_channel = enriched_data['telegram']
                    updated = True
                
                if not project.discord_link and enriched_data.get('discord'):
                    project.discord_link = enriched_data['discord']
                    updated = True
                
                if not project.github_repo and enriched_data.get('github'):
                    project.github_repo = enriched_data['github']
                    updated = True
                
                if not project.logo_url and enriched_data.get('logo_url'):
                    project.logo_url = enriched_data['logo_url']
                    updated = True
                
                if updated:
                    backfilled_count += 1
                    logger.info(f"  ✅ Updated {project.project_name}")
                else:
                    logger.info(f"  ℹ️ No new data for {project.project_name}")
                
                # 每处理10个项目提交一次
                if backfilled_count % 10 == 0 and backfilled_count > 0:
                    db.commit()
                    logger.info(f"💾 Committed batch ({backfilled_count} backfilled so far)")
                    
            except Exception as e:
                logger.error(f"❌ Error backfilling project {project.id}: {e}")
                continue
        
        # 最终提交
        db.commit()
        db.close()
        
        logger.info(f"🎉 Backfill completed: {backfilled_count}/{len(incomplete_projects)} projects updated")
        
        return {
            "success": True,
            "backfilled": backfilled_count,
            "total": len(all_projects),
            "incomplete": len(incomplete_projects)
        }
        
    except Exception as e:
        logger.error(f"❌ Backfill task failed: {e}")
        return {"success": False, "error": str(e)}


@celery_app.task(name="app.tasks.backfill.enrich_incomplete_projects")
def enrich_incomplete_projects():
    """定时任务：自动补全数据完整度低于70%的项目
    
    每6小时运行一次，检查并补全不完整的项目
    """
    logger.info("🔄 Starting periodic enrichment task...")
    
    try:
        db = SessionLocal()
        
        # 查询不完整的项目
        incomplete_query = db.query(Project).filter(
            db.query(Project).filter(
                (Project.blockchain == None) |
                (Project.category == None) |
                (Project.website == None) |
                (Project.twitter_handle == None)
            ).exists()
        ).limit(20)  # 每次处理20个
        
        incomplete_projects = incomplete_query.all()
        
        if not incomplete_projects:
            logger.info("✅ No incomplete projects found")
            return {"success": True, "enriched": 0}
        
        logger.info(f"📊 Found {len(incomplete_projects)} incomplete projects")
        
        enriched_count = 0
        
        for project in incomplete_projects:
            try:
                # 构建项目数据
                project_data = {
                    'name': project.project_name,
                    'description': project.description or '',
                    'symbol': project.symbol,
                }
                
                # AI补全
                enriched_data = data_enricher.enrich_project(project_data)
                
                # 更新缺失字段
                if not project.blockchain and enriched_data.get('blockchain'):
                    project.blockchain = enriched_data['blockchain']
                
                if not project.category and enriched_data.get('category'):
                    project.category = enriched_data['category']
                
                if not project.website and enriched_data.get('website'):
                    project.website = enriched_data['website']
                
                if not project.twitter_handle and enriched_data.get('twitter'):
                    project.twitter_handle = enriched_data['twitter']
                
                enriched_count += 1
                logger.info(f"✅ Enriched {project.project_name}")
                
            except Exception as e:
                logger.error(f"❌ Error enriching project {project.id}: {e}")
                continue
        
        db.commit()
        db.close()
        
        logger.info(f"🎉 Periodic enrichment completed: {enriched_count} projects")
        
        return {
            "success": True,
            "enriched": enriched_count
        }
        
    except Exception as e:
        logger.error(f"❌ Periodic enrichment failed: {e}")
        return {"success": False, "error": str(e)}
