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
        
        # 查找未分析的项目
        projects = db.query(Project).filter(
            and_(
                Project.status == 'discovered',
                Project.overall_score == None
            )
        ).limit(10).all()
        
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
                
                # 调用AI分析服务
                result = ai_analyzer.analyze_project_text(
                    text=project_text,
                    source=project.discovered_from or 'unknown'
                )
                
                if result and result.get('overall_score'):
                    # 更新项目评分
                    project.overall_score = result.get('overall_score')
                    project.team_score = result.get('team_score')
                    project.tech_score = result.get('tech_score')
                    project.community_score = result.get('community_score')
                    project.tokenomics_score = result.get('tokenomics_score')
                    project.market_timing_score = result.get('market_timing_score')
                    project.risk_score = result.get('risk_score')
                    project.grade = result.get('grade')
                    project.status = 'analyzed'
                    
                    # 保存AI分析记录（简化版，只保存项目评分）
                    # AIAnalysis表暂不使用，评分已保存在Project表中
                    # existing_analysis = db.query(AIAnalysis).filter(
                    #     AIAnalysis.project_id == project.id
                    # ).first()
                    
                    # if not existing_analysis:
                    #     ai_analysis = AIAnalysis(
                    #         project_id=project.id,
                    #         investment_suggestion=result.get('reasoning', '')
                    #     )
                    #     db.add(ai_analysis)
                    
                    analyzed_count += 1
                    logger.info(f"✅ Analyzed {project.project_name}: Grade {result.get('grade')}, Score {result.get('overall_score')}")
                else:
                    logger.warning(f"⚠️ Failed to analyze {project.project_name}: No score returned")
                    
            except Exception as e:
                logger.error(f"❌ Error analyzing project {project.id}: {e}")
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

