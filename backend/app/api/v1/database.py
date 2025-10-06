"""数据库统计API"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from app.db import get_db

router = APIRouter(prefix="/database", tags=["database"])


# 字段中文说明映射
FIELD_DESCRIPTIONS = {
    # 通用字段
    "id": "主键ID",
    "created_at": "创建时间",
    "updated_at": "更新时间",
    
    # projects 表
    "project_name": "项目名称",
    "symbol": "代币符号",
    "contract_address": "合约地址",
    "blockchain": "区块链平台",
    "category": "项目类别",
    "description": "项目描述",
    "website": "官方网站",
    "whitepaper_url": "白皮书链接",
    "twitter_handle": "Twitter账号",
    "telegram_channel": "Telegram频道",
    "discord_link": "Discord链接",
    "github_repo": "GitHub仓库",
    "overall_score": "综合评分 (0-100)",
    "team_score": "团队评分",
    "tech_score": "技术评分",
    "community_score": "社区评分",
    "tokenomics_score": "代币经济评分",
    "market_timing_score": "市场时机评分",
    "risk_score": "风险评分",
    "grade": "项目等级 (S/A/B/C)",
    "status": "项目状态",
    "first_discovered_at": "首次发现时间",
    "last_updated_at": "最后更新时间",
    "discovered_from": "发现来源",
    "logo_url": "Logo图片链接",
    "extra_metadata": "额外元数据(JSON)",
    "launch_date": "启动日期",
    "token_launch_probability": "发币概率",
    "airdrop_value_estimate": "空投价值估算",
    "risk_level": "风险等级",
    "investment_suggestion": "投资建议",
    
    # social_metrics 表
    "project_id": "关联项目ID",
    "twitter_followers": "Twitter粉丝数",
    "twitter_engagement_rate": "Twitter互动率",
    "telegram_members": "Telegram成员数",
    "telegram_online_members": "Telegram在线人数",
    "telegram_message_frequency": "Telegram消息频率(/小时)",
    "telegram_active_rate": "Telegram活跃率",
    "discord_members": "Discord成员数",
    "discord_online_members": "Discord在线人数",
    "community_sentiment": "社区情绪分值",
    "youtube_mentions": "YouTube提及次数",
    "youtube_total_views": "YouTube总观看数",
    "github_stars": "GitHub Star数",
    "github_forks": "GitHub Fork数",
    "github_commits_last_week": "上周提交次数",
    "github_contributors": "贡献者数量",
    "snapshot_time": "快照时间",
    
    # onchain_metrics 表
    "market_cap": "市值",
    "total_supply": "总供应量",
    "circulating_supply": "流通供应量",
    "price_usd": "价格(USD)",
    "liquidity_usd": "流动性(USD)",
    "volume_24h": "24小时交易量",
    "holder_count": "持有者数量",
    "top_10_holders_percentage": "前10持有者占比(%)",
    "transaction_count_24h": "24小时交易数",
    "unique_wallets_24h": "24小时活跃钱包数",
    "tvl_usd": "总锁仓量TVL(USD)",
    "tvl": "总锁仓量",
    "transaction_volume": "交易量",
    "active_addresses": "活跃地址数",
    "contract_interactions": "合约交互次数",
    "token_holders": "代币持有者数",
    
    # ai_analysis 表
    "whitepaper_summary": "白皮书摘要",
    "key_features": "关键特性(JSON)",
    "similar_projects": "相似项目(JSON)",
    "sentiment_score": "情感评分",
    "sentiment_label": "情感标签",
    "risk_flags": "风险标记(JSON)",
    "scam_probability": "诈骗可能性(%)",
    "position_size": "建议仓位比例",
    "entry_timing": "入场时机",
    "stop_loss_percentage": "止损比例(%)",
    "analyzed_at": "分析时间",
    "tech_innovation_score": "技术创新评分",
    "team_background_score": "团队背景评分",
    "market_potential_score": "市场潜力评分",
    "risk_factors": "风险因素(JSON)",
    "opportunities": "机会点(JSON)",
    "summary": "AI总结",
    
    # ai_configs 表
    "name": "配置名称",
    "api_key": "API密钥",
    "enabled": "是否启用",
    "model": "模型名称",
    
    # token_launch_predictions 表
    "launch_probability": "发币概率(%)",
    "estimated_timeline": "预计时间线",
    "confidence": "置信度",
    "signal_count": "信号数量",
    "detected_signals": "检测到的信号(JSON)",
    "has_snapshot_announced": "是否宣布快照",
    "has_tokenomics_published": "是否发布代币经济学",
    "has_points_system": "是否有积分系统",
    "has_audit_completed": "是否完成审计",
    "has_mainnet_live": "主网是否上线",
    "has_roadmap_token_mention": "路线图是否提及代币",
    "predicted_at": "预测时间",
    
    # airdrop_value_estimates 表
    "estimated_value_usd": "预估价值(USD)",
    "estimated_value_cny": "预估价值(CNY)",
    "min_value_usd": "最小值(USD)",
    "max_value_usd": "最大值(USD)",
    "basis": "估算依据",
    "comparable_projects": "可比项目(JSON)",
    "estimated_at": "估算时间",
    
    # investment_action_plans 表
    "project_tier": "项目等级",
    "total_budget": "总预算(USD)",
    "urgency": "紧急程度",
    "expected_roi": "预期回报率",
    "total_steps": "总步骤数",
    "steps": "行动步骤(JSON)",
    "timeline": "时间线",
    "risk_mitigation": "风险缓解措施(JSON)",
    "success_criteria": "成功标准(JSON)",
    "plan_created_at": "计划创建时间",
    
    # project_discoveries 表
    "total_mentions": "总提及次数",
    "num_platforms": "平台数量",
    "heat_score": "热度分值",
    "mentions_24h": "24小时提及",
    "growth_rate": "增长率",
    "is_trending": "是否热门",
    "is_surge": "是否暴涨",
    "first_seen_at": "首次发现时间",
    "last_seen_at": "最后发现时间",
    "platforms": "平台列表(JSON)",
    
    # projects_pending 表
    "ai_score": "AI评分",
    "ai_grade": "AI等级 (S/A/B/C)",
    "review_status": "审核状态",
    "rejection_reason": "拒绝原因",
    "reviewed_by": "审核人",
    "reviewed_at": "审核时间",
    "submitted_at": "提交时间",
    
    # ai_work_config 表
    "primary_goal": "主要目标",
    "target_roi": "目标ROI (%)",
    "risk_tolerance": "风险偏好",
    "min_ai_score": "最低推荐分数",
    "max_projects_per_day": "每日项目上限",
    "preferred_categories": "偏好类别(JSON)",
    "excluded_categories": "排除类别(JSON)",
    "min_market_cap": "最小市值要求",
    "max_market_cap": "最大市值要求",
    
    # ai_learning_feedback 表
    "feedback_type": "反馈类型",
    "user_decision": "用户决策",
    "reason": "原因说明",
    "related_project_id": "关联项目ID",
    "feedback_value": "反馈值",
    
    # kols 表
    "twitter_handle": "Twitter用户名",
    "followers_count": "粉丝数",
    "tier": "层级 (1-3)",
    "verified": "是否认证",
    "bio": "个人简介",
    "location": "所在地",
    "website_url": "个人网站",
    "avg_engagement_rate": "平均互动率",
    "focus_areas": "关注领域(JSON)",
    "influence_score": "影响力评分",
    "added_at": "添加时间",
    
    # kols_pending 表
    "recommendation_reason": "推荐理由",
    
    # kol_performances 表
    "kol_id": "KOL ID",
    "prediction_accuracy": "预测准确率",
    "total_predictions": "总预测数",
    "successful_predictions": "成功预测数",
    "avg_roi": "平均投资回报率",
    "best_call": "最佳推荐(JSON)",
    "worst_call": "最差推荐(JSON)",
    "evaluation_period_start": "评估开始时间",
    "evaluation_period_end": "评估结束时间",
    
    # platform_search_rules 表
    "platform_name": "平台名称",
    "search_frequency_hours": "搜索频率(小时)",
    "search_keywords": "搜索关键词(JSON)",
    "filters": "过滤条件(JSON)",
    "priority": "优先级",
    "last_search_at": "最后搜索时间",
    
    # twitter_keywords 表
    "keyword": "关键词",
    "priority": "优先级 (1-3)",
    "search_count": "搜索次数",
    "hit_count": "命中次数",
    "last_used_at": "最后使用时间",
    
    # telegram_channels 表
    "channel_id": "频道ID",
    "channel_name": "频道名称",
    "channel_username": "频道用户名",
    "member_count": "成员数",
    "description": "频道描述",
    "last_monitored_at": "最后监控时间",
    
    # discord_servers 表
    "server_id": "服务器ID",
    "server_name": "服务器名称",
    "invite_link": "邀请链接",
    "member_count": "成员数",
    "online_count": "在线人数",
    "last_monitored_at": "最后监控时间",
    
    # platform_daily_stats 表
    "platform_name": "平台名称",
    "date": "日期",
    "collections": "采集次数",
    "projects_discovered": "发现项目数",
    "new_keywords_added": "新增关键词数",
    "errors_count": "错误次数",
    
    # users 表
    "username": "用户名",
    "email": "邮箱地址",
    "password_hash": "密码哈希",
    "role": "用户角色",
    "is_active": "是否激活",
    "last_login_at": "最后登录时间",
}


def get_field_description(field_name: str) -> str:
    """获取字段的中文说明"""
    return FIELD_DESCRIPTIONS.get(field_name, "-")


@router.get("/stats")
async def get_database_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取数据库统计信息
    
    返回:
    - table_count: 数据表数量
    - project_count: 项目数量
    - database_type: 数据库类型
    - database_port: 数据库端口
    - tables: 表名列表
    """
    
    # 获取所有表名
    inspector = inspect(db.bind)
    all_tables = inspector.get_table_names()
    
    # 排除系统表
    business_tables = [t for t in all_tables if t != 'alembic_version']
    
    # 获取项目数量
    try:
        result = db.execute(text("SELECT COUNT(*) as count FROM projects"))
        project_count = result.fetchone()[0]
    except:
        project_count = 0
    
    # 获取数据库类型和端口
    database_url = str(db.bind.url)
    if 'postgresql' in database_url:
        db_type = 'PostgreSQL'
        db_port = 5432
    elif 'mysql' in database_url:
        db_type = 'MySQL'
        db_port = 3306
    elif 'sqlite' in database_url:
        db_type = 'SQLite'
        db_port = None
    else:
        db_type = 'Unknown'
        db_port = None
    
    return {
        "success": True,
        "data": {
            "table_count": len(business_tables),
            "project_count": project_count,
            "database_type": db_type,
            "database_port": db_port,
            "tables": sorted(business_tables),
            "table_details": {
                table_name: {
                    "name": table_name,
                    "columns": len(inspector.get_columns(table_name))
                }
                for table_name in business_tables
            }
        }
    }


@router.get("/tables/{table_name}/info")
async def get_table_info(
    table_name: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取指定表的详细信息
    
    参数:
    - table_name: 表名
    
    返回:
    - columns: 列信息
    - indexes: 索引信息
    - foreign_keys: 外键信息
    - row_count: 数据行数
    """
    
    inspector = inspect(db.bind)
    
    # 检查表是否存在
    if table_name not in inspector.get_table_names():
        return {
            "success": False,
            "error": f"Table '{table_name}' not found"
        }
    
    # 获取列信息
    columns = inspector.get_columns(table_name)
    
    # 获取索引信息
    indexes = inspector.get_indexes(table_name)
    
    # 获取外键信息
    foreign_keys = inspector.get_foreign_keys(table_name)
    
    # 获取行数
    try:
        result = db.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
        row_count = result.fetchone()[0]
    except:
        row_count = 0
    
    return {
        "success": True,
        "data": {
            "table_name": table_name,
            "columns": [
                {
                    "name": col['name'],
                    "type": str(col['type']),
                    "nullable": col['nullable'],
                    "default": str(col['default']) if col['default'] else None,
                    "description": get_field_description(col['name'])
                }
                for col in columns
            ],
            "indexes": [
                {
                    "name": idx['name'],
                    "columns": idx['column_names'],
                    "unique": idx['unique']
                }
                for idx in indexes
            ],
            "foreign_keys": [
                {
                    "name": fk.get('name'),
                    "columns": fk['constrained_columns'],
                    "referred_table": fk['referred_table'],
                    "referred_columns": fk['referred_columns']
                }
                for fk in foreign_keys
            ],
            "row_count": row_count
        }
    }


@router.get("/tables/{table_name}/data")
async def get_table_data(
    table_name: str,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取指定表的数据
    
    参数:
    - table_name: 表名
    - page: 页码 (从1开始)
    - limit: 每页数量 (默认20, 最大50)
    
    返回:
    - data: 数据列表
    - total: 总行数
    - page: 当前页
    - limit: 每页数量
    - total_pages: 总页数
    """
    
    inspector = inspect(db.bind)
    
    # 检查表是否存在
    if table_name not in inspector.get_table_names():
        return {
            "success": False,
            "error": f"Table '{table_name}' not found"
        }
    
    # 限制每页数量
    limit = min(limit, 50)
    offset = (page - 1) * limit
    
    try:
        # 获取总行数
        count_result = db.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
        total = count_result.fetchone()[0]
        
        # 获取数据
        data_result = db.execute(text(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT :limit OFFSET :offset"), 
                                 {"limit": limit, "offset": offset})
        
        # 获取列名
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        
        # 转换为字典列表
        data = []
        for row in data_result:
            row_dict = {}
            for i, col_name in enumerate(columns):
                value = row[i]
                # 处理特殊类型
                if value is not None:
                    if isinstance(value, (dict, list)):
                        row_dict[col_name] = value
                    else:
                        row_dict[col_name] = str(value) if not isinstance(value, (int, float, bool)) else value
                else:
                    row_dict[col_name] = None
            data.append(row_dict)
        
        total_pages = (total + limit - 1) // limit if total > 0 else 0
        
        return {
            "success": True,
            "data": {
                "table_name": table_name,
                "columns": columns,
                "rows": data,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages
            }
        }
        
    except Exception as e:
        print(f"❌ 获取表数据失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


