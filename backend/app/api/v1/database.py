"""数据库统计API"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from app.db import get_db

router = APIRouter(prefix="/database", tags=["database"])


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
                    "default": str(col['default']) if col['default'] else None
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

