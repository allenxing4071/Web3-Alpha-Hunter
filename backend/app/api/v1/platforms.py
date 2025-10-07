"""
平台管理API
管理Twitter/Telegram/Discord三个平台的配置和数据采集
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel

from app.db.session import get_db

router = APIRouter()


# Request models
class TogglePlatformRequest(BaseModel):
    enabled: bool


@router.get("/")
async def get_all_platforms(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取所有平台配置和状态
    """
    try:
        # 从platform_search_rules表获取配置
        result = db.execute(text("""
            SELECT 
                platform,
                enabled,
                priority,
                frequency_minutes,
                search_keywords,
                min_engagement,
                min_author_followers,
                max_results_per_run
            FROM platform_search_rules
            ORDER BY priority DESC
        """))
        
        platforms = []
        for row in result:
            platform_data = {
                "id": row[0],  # platform name as ID
                "name": row[0],
                "enabled": row[1],
                "priority": row[2],
                "frequency_minutes": row[3],
                "search_keywords": row[4] if row[4] else [],
                "min_engagement": row[5],
                "min_author_followers": row[6],
                "max_results_per_run": row[7]
            }
            
            # 获取今日统计
            stats_result = db.execute(text("""
                SELECT 
                    data_collected,
                    projects_discovered,
                    kols_discovered,
                    projects_recommended
                FROM platform_daily_stats
                WHERE platform = :platform AND stat_date = CURRENT_DATE
            """), {"platform": row[0]})
            
            stats_row = stats_result.fetchone()
            if stats_row:
                platform_data.update({
                    "today_collected": stats_row[0] or 0,
                    "today_projects": stats_row[1] or 0,
                    "today_kols": stats_row[2] or 0,
                    "today_recommended": stats_row[3] or 0
                })
            else:
                platform_data.update({
                    "today_collected": 0,
                    "today_projects": 0,
                    "today_kols": 0,
                    "today_recommended": 0
                })
            
            # TODO: 获取最后采集时间（从实际采集日志表）
            platform_data["last_collected_at"] = None
            
            platforms.append(platform_data)
        
        return {
            "success": True,
            "platforms": platforms
        }
        
    except Exception as e:
        print(f"❌ 获取平台列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{platform_id}/toggle")
async def toggle_platform(
    platform_id: str,
    request: TogglePlatformRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    启用/停用某个平台
    """
    try:
        db.execute(text("""
            UPDATE platform_search_rules
            SET enabled = :enabled,
                updated_at = CURRENT_TIMESTAMP
            WHERE platform = :platform
        """), {"enabled": request.enabled, "platform": platform_id})
        
        db.commit()
        
        return {
            "success": True,
            "message": f"平台 {platform_id} {'已启用' if request.enabled else '已停用'}"
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ 切换平台状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{platform_id}/collect")
async def trigger_manual_collection(
    platform_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    手动触发一次数据采集
    """
    try:
        # 检查平台是否存在
        result = db.execute(text("""
            SELECT enabled FROM platform_search_rules
            WHERE platform = :platform
        """), {"platform": platform_id})
        
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"平台 {platform_id} 不存在")
        
        # TODO: 实际触发Celery采集任务
        # 这里先返回模拟响应
        
        return {
            "success": True,
            "message": f"已触发 {platform_id} 数据采集任务",
            "task_id": f"manual-{platform_id}-{datetime.now().timestamp()}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 触发采集失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{platform_id}/stats")
async def get_platform_stats(
    platform_id: str,
    days: int = 7,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取平台统计数据（过去N天）
    """
    try:
        # 获取历史统计
        result = db.execute(text("""
            SELECT 
                stat_date,
                data_collected,
                projects_discovered,
                kols_discovered,
                projects_recommended,
                projects_approved,
                projects_rejected
            FROM platform_daily_stats
            WHERE platform = :platform
                AND stat_date >= CURRENT_DATE - INTERVAL '%s days'
            ORDER BY stat_date DESC
        """ % days), {"platform": platform_id})
        
        daily_stats = []
        for row in result:
            daily_stats.append({
                "date": row[0].isoformat() if row[0] else None,
                "collected": row[1] or 0,
                "projects": row[2] or 0,
                "kols": row[3] or 0,
                "recommended": row[4] or 0,
                "approved": row[5] or 0,
                "rejected": row[6] or 0
            })
        
        # 计算总计
        total_result = db.execute(text("""
            SELECT 
                SUM(data_collected),
                SUM(projects_discovered),
                SUM(kols_discovered),
                SUM(projects_recommended),
                SUM(projects_approved),
                SUM(projects_rejected)
            FROM platform_daily_stats
            WHERE platform = :platform
                AND stat_date >= CURRENT_DATE - INTERVAL '%s days'
        """ % days), {"platform": platform_id})
        
        total_row = total_result.fetchone()
        
        return {
            "success": True,
            "platform": platform_id,
            "days": days,
            "daily_stats": daily_stats,
            "total": {
                "collected": int(total_row[0] or 0),
                "projects": int(total_row[1] or 0),
                "kols": int(total_row[2] or 0),
                "recommended": int(total_row[3] or 0),
                "approved": int(total_row[4] or 0),
                "rejected": int(total_row[5] or 0)
            }
        }
        
    except Exception as e:
        print(f"❌ 获取平台统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{platform_id}/keywords")
async def get_platform_keywords(
    platform_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取平台关键词列表（仅Twitter）
    """
    if platform_id != "twitter":
        return {
            "success": True,
            "keywords": [],
            "message": "该平台不使用关键词管理"
        }
    
    try:
        result = db.execute(text("""
            SELECT 
                id,
                keyword,
                category,
                priority,
                weight,
                enabled,
                match_count,
                last_matched_at
            FROM twitter_keywords
            ORDER BY priority DESC, match_count DESC
        """))
        
        keywords = []
        for row in result:
            keywords.append({
                "id": row[0],
                "keyword": row[1],
                "category": row[2],
                "priority": row[3],
                "weight": row[4],
                "enabled": row[5],
                "match_count": row[6] or 0,
                "last_matched_at": row[7].isoformat() if row[7] else None
            })
        
        return {
            "success": True,
            "keywords": keywords,
            "total": len(keywords),
            "enabled_count": sum(1 for k in keywords if k["enabled"])
        }
        
    except Exception as e:
        print(f"❌ 获取关键词列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{platform_id}/kols")
async def get_platform_kols(
    platform_id: str,
    tier: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取平台KOL列表（仅Twitter）
    """
    if platform_id != "twitter":
        return {
            "success": True,
            "kols": [],
            "message": "该平台不使用KOL管理"
        }
    
    try:
        query = """
            SELECT 
                id,
                username,
                display_name,
                followers,
                tier,
                influence_score,
                tags,
                total_mentions,
                this_week_mentions,
                status,
                discovery_method,
                last_checked_at
            FROM kols
            WHERE platform = 'twitter'
        """
        
        params = {}
        if tier is not None:
            query += " AND tier = :tier"
            params["tier"] = tier
        
        if status:
            query += " AND status = :status"
            params["status"] = status
        
        query += " ORDER BY tier ASC, influence_score DESC LIMIT :limit"
        params["limit"] = limit
        
        result = db.execute(text(query), params)
        
        kols = []
        for row in result:
            kols.append({
                "id": row[0],
                "username": row[1],
                "display_name": row[2],
                "followers": row[3] or 0,
                "tier": row[4],
                "influence_score": row[5] or 0,
                "tags": row[6] if row[6] else [],
                "total_mentions": row[7] or 0,
                "this_week_mentions": row[8] or 0,
                "status": row[9],
                "discovery_method": row[10],
                "last_checked_at": row[11].isoformat() if row[11] else None
            })
        
        # 统计分层数据
        tier_stats_result = db.execute(text("""
            SELECT tier, COUNT(*) 
            FROM kols 
            WHERE platform = 'twitter' AND status = 'active'
            GROUP BY tier
            ORDER BY tier
        """))
        
        tier_stats = {}
        for row in tier_stats_result:
            tier_stats[f"tier{row[0]}"] = row[1]
        
        return {
            "success": True,
            "kols": kols,
            "total": len(kols),
            "tier_stats": tier_stats
        }
        
    except Exception as e:
        print(f"❌ 获取KOL列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

