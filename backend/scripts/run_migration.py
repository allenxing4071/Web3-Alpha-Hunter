"""
执行数据库迁移脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def run_migration():
    """执行SQL迁移脚本"""
    
    print("=" * 60)
    print("开始执行AI系统数据库迁移...")
    print("=" * 60)
    
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    # 读取SQL文件
    sql_file = os.path.join(os.path.dirname(__file__), 'create_ai_system_tables.sql')
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 执行SQL
    try:
        with engine.begin() as conn:
            # 直接执行整个SQL文件
            conn.execute(text(sql_content))
            print("✓ SQL脚本执行完成")
        
        print("\n" + "=" * 60)
        print("✅ 数据库迁移完成!")
        print("=" * 60)
        
        # 验证结果
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM kols WHERE tier = 1"))
            tier1_count = result.scalar()
            print(f"📊 Tier1 KOL数量: {tier1_count}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM twitter_keywords WHERE enabled = TRUE"))
            keywords_count = result.scalar()
            print(f"🔑 活跃关键词数量: {keywords_count}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM platform_search_rules"))
            platforms_count = result.scalar()
            print(f"🌍 配置平台数量: {platforms_count}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)

