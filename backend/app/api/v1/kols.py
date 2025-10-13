"""KOL (意见领袖) API路由"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.db.session import get_db

router = APIRouter(prefix="/kols", tags=["kols"])


@router.get("/top-influencers")
async def get_top_influencers(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    tier: Optional[int] = Query(None, ge=1, le=3, description="KOL等级筛选"),
    platform: Optional[str] = Query(None, description="平台筛选"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取推荐关注的Top KOL
    
    返回格式化的KOL数据，用于前端展示
    """
    try:
        # 构建查询条件
        where_clauses = ["status = 'active'"]
        
        if tier:
            where_clauses.append(f"tier = {tier}")
        
        if platform:
            where_clauses.append(f"platform = '{platform}'")
        
        where_sql = " AND ".join(where_clauses)
        
        # 查询KOL数据
        query = text(f"""
            SELECT 
                id,
                username,
                display_name,
                platform,
                followers,
                tier,
                influence_score,
                tags,
                bio,
                profile_url,
                verified
            FROM kols
            WHERE {where_sql}
            ORDER BY influence_score DESC, followers DESC
            LIMIT :limit
        """)
        
        result = db.execute(query, {"limit": limit})
        rows = result.fetchall()
        
        # 格式化数据
        influencers = []
        for row in rows:
            # 构建URL（优先使用profile_url）
            url = row.profile_url if row.profile_url else f"https://twitter.com/{row.username}"
            
            # 格式化粉丝数
            followers_formatted = format_followers(row.followers or 0)
            
            # 获取分类标签（从tags字符串中取第一个）
            category = "Crypto"
            if row.tags:
                try:
                    # tags可能是字符串"tag1,tag2,tag3"
                    tag_list = row.tags.split(',')
                    if tag_list and len(tag_list) > 0:
                        category = tag_list[0].strip()
                except:
                    pass
            
            # 使用bio或生成描述
            description = row.bio if row.bio else generate_description(row)
            
            influencer = {
                "id": str(row.id),
                "name": row.display_name or row.username,
                "platform": row.platform.capitalize() if row.platform else "Twitter",
                "platformIcon": "𝕏" if row.platform == "twitter" else "📱",
                "handle": f"@{row.username}",
                "url": url,
                "followers": followers_formatted,
                "category": category,
                "description": description,
                "verified": row.verified or False,
                "tier": row.tier,
                "influenceScore": float(row.influence_score or 0)
            }
            influencers.append(influencer)
        
        return {
            "success": True,
            "influencers": influencers,
            "total": len(influencers)
        }
        
    except Exception as e:
        print(f"❌ 获取Top KOL失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_kols(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    tier: Optional[int] = Query(None, ge=1, le=3, description="等级筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取KOL列表（分页）"""
    try:
        # 构建查询条件
        where_clauses = []
        
        if tier:
            where_clauses.append(f"tier = {tier}")
        
        if status:
            where_clauses.append(f"status = '{status}'")
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        # 查询总数
        count_query = text(f"SELECT COUNT(*) FROM kols WHERE {where_sql}")
        total = db.execute(count_query).scalar()
        
        # 查询数据
        offset = (page - 1) * limit
        query = text(f"""
            SELECT *
            FROM kols
            WHERE {where_sql}
            ORDER BY influence_score DESC, followers DESC
            LIMIT :limit OFFSET :offset
        """)
        
        result = db.execute(query, {"limit": limit, "offset": offset})
        rows = result.fetchall()
        
        kols = []
        for row in rows:
            kol_dict = dict(row._mapping)
            kols.append(kol_dict)
        
        return {
            "success": True,
            "kols": kols,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        }
        
    except Exception as e:
        print(f"❌ 获取KOL列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{kol_id}")
async def get_kol_detail(
    kol_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取KOL详情"""
    try:
        query = text("SELECT * FROM kols WHERE id = :kol_id")
        result = db.execute(query, {"kol_id": kol_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="KOL不存在")
        
        kol = dict(row._mapping)
        
        return {
            "success": True,
            "kol": kol
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 获取KOL详情失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 辅助函数 ====================

def format_followers(count: int) -> str:
    """格式化粉丝数显示"""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.0f}K"
    else:
        return str(count)


def generate_description(row) -> str:
    """生成KOL描述"""
    descriptions = {
        1: "顶级加密意见领袖，行业影响力巨大",
        2: "知名Web3专家，深度行业洞察",
        3: "新兴加密影响者，潜力巨大"
    }
    
    tier_desc = descriptions.get(row.tier or 3, "加密领域影响者")
    
    # 如果有特定标签，可以生成更具体的描述
    if row.tags:
        try:
            import json
            tags = json.loads(row.tags) if isinstance(row.tags, str) else row.tags
            if tags and len(tags) > 0:
                tag_str = "、".join(tags[:2])
                return f"{tier_desc}，专注{tag_str}"
        except:
            pass
    
    return tier_desc

