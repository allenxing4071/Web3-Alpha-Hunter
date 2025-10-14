"""AI分析任务"""

from loguru import logger
from app.tasks.celery_app import celery_app
from app.db import SessionLocal
from app.models import Project, AIAnalysis
from app.services.analyzers import ai_analyzer
from sqlalchemy import and_


@celery_app.task(name="app.tasks.analyzers.analyze_new_projects")
def analyze_new_projects():
    """分析新发现的项目"""
    logger.info("🤖 Starting AI analysis for new projects...")
    
    try:
        db = SessionLocal()
        
        # 查找未分析的项目（每次处理50个）
        projects = db.query(Project).filter(
            and_(
                Project.status == 'discovered',
                Project.overall_score == None
            )
        ).limit(50).all()
        
        if not projects:
            logger.info("ℹ️ No new projects to analyze")
            return {"success": True, "analyzed": 0}
        
        logger.info(f"📊 Found {len(projects)} projects to analyze")
        
        analyzed_count = 0
        for project in projects:
            try:
                # 构建项目描述文本
                project_text = f"""
项目名称: {project.project_name}
符号: {project.symbol or 'N/A'}
描述: {project.description or 'N/A'}
来源: {project.discovered_from}
Twitter: {project.twitter_handle or 'N/A'}
"""

                # 1. 调用AI评分分析
                score_result = ai_analyzer.analyze_project_text(
                    text=project_text,
                    source=project.discovered_from or 'unknown'
                )

                if not score_result or not score_result.get('overall_score'):
                    logger.warning(f"⚠️ Failed to analyze {project.project_name}: No score returned")
                    continue

                # 更新项目评分
                project.overall_score = score_result.get('overall_score')
                project.team_score = score_result.get('team_score')
                project.tech_score = score_result.get('tech_score')
                project.community_score = score_result.get('community_score')
                project.tokenomics_score = score_result.get('tokenomics_score')
                project.market_timing_score = score_result.get('market_timing_score')
                project.risk_score = score_result.get('risk_score')
                project.grade = score_result.get('grade')
                project.category = score_result.get('category', project.category)
                project.status = 'analyzed'

                # 2. 生成详细AI分析（基于真实数据）
                from datetime import datetime
                from sqlalchemy import text

                # 获取项目的真实指标数据
                metrics_query = text("""
                    SELECT
                        COALESCE(sm.twitter_followers, 0) as twitter_followers,
                        COALESCE(sm.telegram_members, 0) as telegram_members,
                        COALESCE(sm.github_stars, 0) as github_stars
                    FROM projects p
                    LEFT JOIN social_metrics sm ON sm.project_id = p.id
                    WHERE p.id = :project_id
                    ORDER BY sm.snapshot_time DESC
                    LIMIT 1
                """)

                metrics_result = db.execute(metrics_query, {"project_id": project.id}).fetchone()

                project_data_for_ai = {
                    "name": project.project_name,
                    "description": project.description or "暂无描述",
                    "category": project.category or "Unknown",
                    "blockchain": project.blockchain or "Unknown",
                    "metrics": {
                        "twitter_followers": metrics_result[0] if metrics_result else 0,
                        "telegram_members": metrics_result[1] if metrics_result else 0,
                        "github_stars": metrics_result[2] if metrics_result else 0,
                    },
                    "scores": {
                        "overall": project.overall_score,
                        "team": project.team_score,
                        "tech": project.tech_score,
                        "community": project.community_score,
                    }
                }

                detailed_analysis = ai_analyzer.generate_detailed_analysis(project_data_for_ai)

                # 3. 保存详细AI分析到ai_analysis表
                existing_analysis = db.query(AIAnalysis).filter(
                    AIAnalysis.project_id == project.id
                ).first()

                if existing_analysis:
                    # 更新现有记录
                    existing_analysis.whitepaper_summary = detailed_analysis.get('summary', '')
                    existing_analysis.key_features = detailed_analysis.get('key_features', [])
                    existing_analysis.similar_projects = []  # 暂时为空
                    existing_analysis.sentiment_score = 0.75
                    existing_analysis.sentiment_label = 'positive'
                    existing_analysis.risk_flags = []
                    existing_analysis.scam_probability = 5.0
                    existing_analysis.investment_suggestion = detailed_analysis.get('investment_suggestion', {}).get('action', '')
                    existing_analysis.position_size = detailed_analysis.get('investment_suggestion', {}).get('position_size', '')
                    existing_analysis.entry_timing = detailed_analysis.get('investment_suggestion', {}).get('entry_timing', '')
                    existing_analysis.stop_loss_percentage = detailed_analysis.get('investment_suggestion', {}).get('stop_loss', 0)
                    existing_analysis.analyzed_at = datetime.utcnow()
                else:
                    # 创建新记录
                    ai_analysis = AIAnalysis(
                        project_id=project.id,
                        whitepaper_summary=detailed_analysis.get('summary', ''),
                        key_features=detailed_analysis.get('key_features', []),
                        similar_projects=[],
                        sentiment_score=0.75,
                        sentiment_label='positive',
                        risk_flags=[],
                        scam_probability=5.0,
                        investment_suggestion=detailed_analysis.get('investment_suggestion', {}).get('action', ''),
                        position_size=detailed_analysis.get('investment_suggestion', {}).get('position_size', ''),
                        entry_timing=detailed_analysis.get('investment_suggestion', {}).get('entry_timing', ''),
                        stop_loss_percentage=detailed_analysis.get('investment_suggestion', {}).get('stop_loss', 0),
                        analyzed_at=datetime.utcnow()
                    )
                    db.add(ai_analysis)

                analyzed_count += 1
                logger.info(f"✅ Analyzed {project.project_name}: Grade {project.grade}, Score {project.overall_score:.1f}")
                logger.info(f"   📝 Summary: {detailed_analysis.get('summary', '')[:80]}...")

            except Exception as e:
                logger.error(f"❌ Error analyzing project {project.id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
                continue
        
        db.commit()
        db.close()
        
        logger.info(f"🎉 AI analysis completed: {analyzed_count}/{len(projects)} projects analyzed")
        
        return {
            "success": True,
            "analyzed": analyzed_count,
            "total": len(projects)
        }
        
    except Exception as e:
        logger.error(f"❌ AI analysis task failed: {e}")
        return {"success": False, "error": str(e)}


@celery_app.task(name="app.tasks.analyzers.update_all_scores")
def update_all_scores():
    """更新所有项目评分（定时任务）"""
    logger.info("🔄 Starting periodic score update...")
    
    try:
        db = SessionLocal()
        
        # 查找需要更新的项目（已分析但评分较旧的）
        projects = db.query(Project).filter(
            Project.status == 'analyzed'
        ).order_by(
            Project.last_updated_at.asc()
        ).limit(20).all()
        
        if not projects:
            logger.info("ℹ️ No projects to update")
            return {"success": True, "updated": 0}
        
        updated_count = 0
        for project in projects:
            try:
                # 构建项目描述文本
                project_text = f"""
项目名称: {project.project_name}
符号: {project.symbol or 'N/A'}
描述: {project.description or 'N/A'}
来源: {project.discovered_from}
"""
                
                # 重新分析
                result = ai_analyzer.analyze_project_text(
                    text=project_text,
                    source=project.discovered_from or 'unknown'
                )
                
                if result and result.get('overall_score'):
                    project.overall_score = result.get('overall_score')
                    project.grade = result.get('grade')
                    updated_count += 1
                    
            except Exception as e:
                logger.error(f"❌ Error updating project {project.id}: {e}")
                continue
        
        db.commit()
        db.close()
        
        logger.info(f"✅ Score update completed: {updated_count} projects updated")
        
        return {
            "success": True,
            "updated": updated_count
        }
        
    except Exception as e:
        logger.error(f"❌ Score update failed: {e}")
        return {"success": False, "error": str(e)}

