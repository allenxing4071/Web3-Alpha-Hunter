"""
Dashboard实时监控API
提供大屏展示所需的实时统计数据
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.db.session import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取实时统计数据
    返回: 总项目数、新项目、S/A级项目、待审核、平均分等
    """
    try:
        # 总项目数
        total_projects = db.execute(
            text("SELECT COUNT(*) FROM projects")
        ).scalar() or 0
        
        # 今日新增 (24小时内)
        new_today = db.execute(text("""
            SELECT COUNT(*) FROM projects 
            WHERE created_at >= NOW() - INTERVAL '24 hours'
        """)).scalar() or 0
        
        # S级项目数
        s_grade = db.execute(text("""
            SELECT COUNT(*) FROM projects WHERE grade = 'S'
        """)).scalar() or 0
        
        # A级项目数
        a_grade = db.execute(text("""
            SELECT COUNT(*) FROM projects WHERE grade = 'A'
        """)).scalar() or 0
        
        # B级项目数
        b_grade = db.execute(text("""
            SELECT COUNT(*) FROM projects WHERE grade = 'B'
        """)).scalar() or 0
        
        # 待审核项目
        pending = db.execute(text("""
            SELECT COUNT(*) FROM projects_pending 
            WHERE review_status = 'pending'
        """)).scalar() or 0
        
        # 热门项目 (最近7天有发现记录的)
        trending = db.execute(text("""
            SELECT COUNT(DISTINCT id) FROM projects 
            WHERE created_at >= NOW() - INTERVAL '7 days'
            AND overall_score >= 75
        """)).scalar() or 0
        
        # 总TVL (如果有链上数据)
        total_tvl = db.execute(text("""
            SELECT COALESCE(SUM(tvl_usd), 0) 
            FROM onchain_metrics om
            INNER JOIN (
                SELECT project_id, MAX(snapshot_time) as max_time
                FROM onchain_metrics
                GROUP BY project_id
            ) latest ON om.project_id = latest.project_id 
            AND om.snapshot_time = latest.max_time
        """)).scalar() or 0
        
        # 平均评分
        avg_score = db.execute(text("""
            SELECT COALESCE(AVG(overall_score), 0) 
            FROM projects 
            WHERE overall_score IS NOT NULL
        """)).scalar() or 0
        
        return {
            "success": True,
            "data": {
                "total_projects": total_projects,
                "new_today": new_today,
                "s_grade": s_grade,
                "a_grade": a_grade,
                "b_grade": b_grade,
                "pending": pending,
                "trending": trending,
                "total_tvl": float(total_tvl),
                "avg_score": round(float(avg_score), 1),
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }


@router.get("/recent")
async def get_recent_projects(
    hours: int = 24,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取最近发现的项目
    hours: 回溯时间（小时），默认24小时
    返回项目列表，标记5分钟内的为is_new
    """
    try:
        result = db.execute(text("""
            SELECT 
                id,
                project_name,
                symbol,
                grade,
                overall_score,
                category,
                blockchain,
                created_at,
                CASE 
                    WHEN created_at >= NOW() - INTERVAL '5 minutes' THEN true
                    ELSE false
                END as is_new
            FROM projects
            WHERE created_at >= NOW() - INTERVAL ':hours hours'
            ORDER BY created_at DESC
            LIMIT 50
        """).bindparams(hours=hours))
        
        items = []
        for row in result:
            items.append({
                "id": row[0],
                "name": row[1],
                "symbol": row[2],
                "grade": row[3],
                "score": float(row[4]) if row[4] else 0,
                "category": row[5],
                "blockchain": row[6],
                "discovered_at": row[7].isoformat() if row[7] else None,
                "is_new": row[8]
            })
        
        return {
            "success": True,
            "data": {
                "items": items,
                "count": len(items),
                "hours": hours
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }


@router.get("/top-projects")
async def get_top_projects(
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取Top N高分项目
    """
    try:
        result = db.execute(text("""
            SELECT 
                id,
                project_name,
                symbol,
                grade,
                overall_score,
                category,
                blockchain,
                team_score,
                tech_score,
                community_score
            FROM projects
            WHERE overall_score IS NOT NULL
            ORDER BY overall_score DESC, created_at DESC
            LIMIT :limit
        """).bindparams(limit=limit))
        
        items = []
        rank = 1
        for row in result:
            items.append({
                "rank": rank,
                "id": row[0],
                "name": row[1],
                "symbol": row[2],
                "grade": row[3],
                "score": float(row[4]) if row[4] else 0,
                "category": row[5],
                "blockchain": row[6],
                "scores": {
                    "team": float(row[7]) if row[7] else 0,
                    "tech": float(row[8]) if row[8] else 0,
                    "community": float(row[9]) if row[9] else 0
                }
            })
            rank += 1
        
        return {
            "success": True,
            "data": {
                "items": items,
                "count": len(items)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }


@router.get("/grade-distribution")
async def get_grade_distribution(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取项目等级分布统计
    """
    try:
        result = db.execute(text("""
            SELECT 
                grade,
                COUNT(*) as count
            FROM projects
            WHERE grade IS NOT NULL
            GROUP BY grade
            ORDER BY grade
        """))
        
        distribution = {}
        total = 0
        for row in result:
            grade = row[0]
            count = row[1]
            distribution[grade] = count
            total += count
        
        # 计算百分比
        distribution_with_percent = []
        for grade in ['S', 'A', 'B', 'C']:
            count = distribution.get(grade, 0)
            percent = round((count / total * 100), 1) if total > 0 else 0
            distribution_with_percent.append({
                "grade": grade,
                "count": count,
                "percent": percent
            })
        
        return {
            "success": True,
            "data": {
                "distribution": distribution_with_percent,
                "total": total
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }


@router.get("/category-stats")
async def get_category_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取各类别项目统计
    """
    try:
        result = db.execute(text("""
            SELECT 
                category,
                COUNT(*) as count,
                AVG(overall_score) as avg_score,
                COUNT(CASE WHEN grade IN ('S', 'A') THEN 1 END) as high_grade_count
            FROM projects
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
        """))
        
        categories = []
        for row in result:
            categories.append({
                "category": row[0],
                "count": row[1],
                "avg_score": round(float(row[2]), 1) if row[2] else 0,
                "high_grade_count": row[3]
            })
        
        return {
            "success": True,
            "data": {
                "categories": categories,
                "total_categories": len(categories)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }


@router.get("/activity-timeline")
async def get_activity_timeline(
    hours: int = 1,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取最近活动时间线
    包括: 项目发现、AI分析、项目审核等事件
    """
    try:
        activities = []
        
        # 1. 最近发现的项目
        projects_result = db.execute(text("""
            SELECT 
                'project_discovered' as type,
                project_name as title,
                created_at as timestamp,
                grade,
                overall_score
            FROM projects
            WHERE created_at >= NOW() - INTERVAL ':hours hours'
            ORDER BY created_at DESC
            LIMIT 20
        """).bindparams(hours=hours))
        
        for row in projects_result:
            activities.append({
                "type": row[0],
                "title": row[1],
                "timestamp": row[2].isoformat() if row[2] else None,
                "grade": row[3],
                "score": float(row[4]) if row[4] else 0
            })
        
        # 2. AI分析事件
        ai_result = db.execute(text("""
            SELECT 
                'ai_analysis' as type,
                p.project_name as title,
                a.analyzed_at as timestamp,
                a.sentiment_label,
                a.sentiment_score
            FROM ai_analysis a
            JOIN projects p ON a.project_id = p.id
            WHERE a.analyzed_at >= NOW() - INTERVAL ':hours hours'
            ORDER BY a.analyzed_at DESC
            LIMIT 15
        """).bindparams(hours=hours))
        
        for row in ai_result:
            activities.append({
                "type": row[0],
                "title": row[1],
                "timestamp": row[2].isoformat() if row[2] else None,
                "sentiment": row[3],
                "score": float(row[4]) if row[4] else 0
            })
        
        # 3. 项目审核事件
        review_result = db.execute(text("""
            SELECT 
                'project_reviewed' as type,
                project_name as title,
                reviewed_at as timestamp,
                review_status,
                ai_score
            FROM projects_pending
            WHERE reviewed_at >= NOW() - INTERVAL ':hours hours'
            AND review_status != 'pending'
            ORDER BY reviewed_at DESC
            LIMIT 10
        """).bindparams(hours=hours))
        
        for row in review_result:
            activities.append({
                "type": row[0],
                "title": row[1],
                "timestamp": row[2].isoformat() if row[2] else None,
                "status": row[3],
                "score": float(row[4]) if row[4] else 0
            })
        
        # 按时间排序
        activities.sort(key=lambda x: x['timestamp'] if x['timestamp'] else '', reverse=True)
        
        return {
            "success": True,
            "data": {
                "activities": activities[:30],  # 限制返回30条
                "count": len(activities[:30]),
                "hours": hours
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }


@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取大屏所有数据的汇总接口 (一次请求获取全部)
    """
    try:
        stats = await get_dashboard_stats(db)
        recent = await get_recent_projects(24, db)
        top_projects = await get_top_projects(10, db)
        distribution = await get_grade_distribution(db)
        categories = await get_category_stats(db)
        timeline = await get_activity_timeline(24, db)  # 改为24小时
        
        return {
            "success": True,
            "data": {
                "stats": stats.get("data"),
                "recent": recent.get("data"),
                "top_projects": top_projects.get("data"),
                "distribution": distribution.get("data"),
                "categories": categories.get("data"),
                "timeline": timeline.get("data"),
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }

