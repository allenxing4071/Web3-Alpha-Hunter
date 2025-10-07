#!/usr/bin/env python3
"""
修复已存在metrics数据与projects的关联
为那些有metrics数据但project外键为NULL的记录建立关联
"""

import sys
from pathlib import Path

# 添加项目路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.project import Project, SocialMetrics, OnchainMetrics

def fix_social_metrics_relations(db: Session):
    """修复social_metrics关联"""
    print("\n📊 修复Social Metrics关联:")
    print("=" * 70)
    
    # 找到所有有social_metrics数据但project没关联的记录
    social_metrics = db.query(SocialMetrics).all()
    
    fixed = 0
    for sm in social_metrics:
        # 查找对应的project
        project = db.query(Project).filter(Project.id == sm.project_id).first()
        if project and not project.social_metrics_id:
            project.social_metrics_id = sm.id
            fixed += 1
            print(f"  ✅ {project.project_name} (ID:{project.id}) → social_metrics#{sm.id}")
    
    print(f"\n✅ 修复了 {fixed} 个social_metrics关联")
    return fixed

def fix_onchain_metrics_relations(db: Session):
    """修复onchain_metrics关联"""
    print("\n📊 修复Onchain Metrics关联:")
    print("=" * 70)
    
    # 找到所有有onchain_metrics数据但project没关联的记录
    onchain_metrics = db.query(OnchainMetrics).all()
    
    fixed = 0
    for om in onchain_metrics:
        # 查找对应的project
        project = db.query(Project).filter(Project.id == om.project_id).first()
        if project and not project.onchain_metrics_id:
            project.onchain_metrics_id = om.id
            fixed += 1
            print(f"  ✅ {project.project_name} (ID:{project.id}) → onchain_metrics#{om.id}")
    
    print(f"\n✅ 修复了 {fixed} 个onchain_metrics关联")
    return fixed

def main():
    print("🔧 开始修复Metrics关联")
    print("=" * 70)
    
    db = next(get_db())
    
    try:
        social_fixed = fix_social_metrics_relations(db)
        onchain_fixed = fix_onchain_metrics_relations(db)
        
        db.commit()
        
        print("\n" + "=" * 70)
        print(f"✅ 修复完成！")
        print(f"  Social Metrics: {social_fixed}个")
        print(f"  Onchain Metrics: {onchain_fixed}个")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 错误: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
