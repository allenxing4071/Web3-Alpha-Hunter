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
    
    # airdrop_value_estimates 表
    "estimated_value_usd": "预估价值(USD)",
    "estimated_value_cny": "预估价值(CNY)",
    "min_value_usd": "最小值(USD)",
    "max_value_usd": "最大值(USD)",
    
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


