#!/usr/bin/env python3
"""
补充项目评分和指标数据
为现有项目生成合理的评分数据和社交/链上指标
"""

import sys
import os
from pathlib import Path
import random
from decimal import Decimal
from datetime import datetime, timedelta

# 添加项目路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.project import Project, SocialMetrics, OnchainMetrics

def generate_score_from_overall(overall_score: float) -> dict:
    """
    根据综合评分生成各维度评分
    保持一定的合理性和随机性
    """
    # 基础偏差范围 (-10 到 +10)
    def variant(base: float, variance: float = 10.0) -> float:
        return max(0, min(100, base + random.uniform(-variance, variance)))
    
    # 根据综合分数生成各维度分数
    return {
        'team_score': round(variant(overall_score, 8), 2),
        'tech_score': round(variant(overall_score, 10), 2),
        'community_score': round(variant(overall_score, 12), 2),
        'tokenomics_score': round(variant(overall_score, 10), 2),
        'market_timing_score': round(variant(overall_score, 15), 2),
        'risk_score': round(100 - variant(overall_score, 5), 2),  # 分数越高风险越低
    }

def generate_social_metrics(grade: str, overall_score: float) -> dict:
    """根据项目等级生成社交媒体指标"""
    
    # 根据评分等级确定基础规模
    base_multiplier = {
        'S': 10.0,
        'A': 5.0,
        'B': 2.0,
        'C': 1.0,
        'D': 0.5
    }.get(grade, 1.0)
    
    # 添加评分影响
    score_factor = overall_score / 100.0
    multiplier = base_multiplier * score_factor
    
    return {
        'twitter_followers': int(random.randint(1000, 5000) * multiplier),
        'twitter_engagement_rate': round(random.uniform(2, 8) * multiplier, 2),
        'telegram_members': int(random.randint(500, 3000) * multiplier),
        'telegram_online_members': int(random.randint(50, 500) * multiplier),
        'telegram_message_frequency': int(random.randint(10, 100) * multiplier),
        'discord_members': int(random.randint(800, 4000) * multiplier),
        'discord_online_members': int(random.randint(100, 800) * multiplier),
        'github_stars': int(random.randint(50, 500) * multiplier) if random.random() > 0.3 else None,
        'github_forks': int(random.randint(10, 100) * multiplier) if random.random() > 0.3 else None,
        'github_commits_last_week': int(random.randint(5, 50) * multiplier) if random.random() > 0.3 else None,
        'github_contributors': int(random.randint(3, 30) * multiplier) if random.random() > 0.3 else None,
        'youtube_mentions': int(random.randint(1, 20) * multiplier),
        'youtube_total_views': int(random.randint(1000, 50000) * multiplier),
    }

def generate_onchain_metrics(grade: str, overall_score: float, category: str) -> dict:
    """根据项目等级和类别生成链上指标"""
    
    # 根据评分等级确定基础规模
    base_multiplier = {
        'S': 100.0,
        'A': 50.0,
        'B': 20.0,
        'C': 10.0,
        'D': 5.0
    }.get(grade, 10.0)
    
    score_factor = overall_score / 100.0
    multiplier = base_multiplier * score_factor
    
    metrics = {
        'market_cap': round(random.uniform(1_000_000, 10_000_000) * multiplier, 2),
        'price_usd': round(random.uniform(0.1, 100) * multiplier, 8),
        'volume_24h': round(random.uniform(100_000, 1_000_000) * multiplier, 2),
        'holder_count': int(random.randint(500, 5000) * multiplier),
        'top_10_holders_percentage': round(random.uniform(20, 45), 2),
        'transaction_count_24h': int(random.randint(100, 1000) * multiplier),
        'unique_wallets_24h': int(random.randint(50, 500) * multiplier),
    }
    
    # DeFi项目添加TVL
    if category in ['DeFi', 'Infrastructure', 'Layer2']:
        metrics['tvl_usd'] = round(random.uniform(500_000, 5_000_000) * multiplier, 2)
    
    return metrics

def fill_project_data(db: Session):
    """为所有项目补充数据"""
    
    projects = db.query(Project).all()
    print(f"找到 {len(projects)} 个项目，开始补充数据...\n")
    
    for project in projects:
        print(f"处理项目: {project.project_name} (ID: {project.id})")
        
        # 1. 补充评分数据
        if project.overall_score and (
            not project.team_score or 
            not project.tech_score or 
            float(project.team_score) == 0
        ):
            scores = generate_score_from_overall(float(project.overall_score))
            project.team_score = Decimal(str(scores['team_score']))
            project.tech_score = Decimal(str(scores['tech_score']))
            project.community_score = Decimal(str(scores['community_score']))
            project.tokenomics_score = Decimal(str(scores['tokenomics_score']))
            project.market_timing_score = Decimal(str(scores['market_timing_score']))
            project.risk_score = Decimal(str(scores['risk_score']))
            print(f"  ✅ 更新评分数据: team={scores['team_score']}, tech={scores['tech_score']}")
        
        # 2. 创建或更新社交媒体指标
        existing_social = db.query(SocialMetrics).filter(
            SocialMetrics.project_id == project.id
        ).order_by(SocialMetrics.snapshot_time.desc()).first()
        
        if not existing_social:
            social_data = generate_social_metrics(
                project.grade or 'B', 
                float(project.overall_score or 70)
            )
            social_metrics = SocialMetrics(
                project_id=project.id,
                **social_data,
                snapshot_time=datetime.now()
            )
            db.add(social_metrics)
            print(f"  ✅ 创建社交媒体指标: Twitter={social_data.get('twitter_followers')}, Telegram={social_data.get('telegram_members')}")
        
        # 3. 创建或更新链上指标
        existing_onchain = db.query(OnchainMetrics).filter(
            OnchainMetrics.project_id == project.id
        ).order_by(OnchainMetrics.snapshot_time.desc()).first()
        
        if not existing_onchain:
            onchain_data = generate_onchain_metrics(
                project.grade or 'B',
                float(project.overall_score or 70),
                project.category or 'Unknown'
            )
            onchain_metrics = OnchainMetrics(
                project_id=project.id,
                **onchain_data,
                snapshot_time=datetime.now()
            )
            db.add(onchain_metrics)
            tvl_info = f", TVL=${onchain_data.get('tvl_usd', 0):,.0f}" if onchain_data.get('tvl_usd') else ""
            print(f"  ✅ 创建链上指标: MarketCap=${onchain_data.get('market_cap', 0):,.0f}{tvl_info}")
        
        print()
    
    # 提交所有更改
    try:
        db.commit()
        print("✅ 所有数据已成功保存到数据库！")
    except Exception as e:
        db.rollback()
        print(f"❌ 保存失败: {e}")
        raise

def main():
    """主函数"""
    print("=" * 60)
    print("项目数据补充工具")
    print("=" * 60)
    print()
    
    db = next(get_db())
    try:
        fill_project_data(db)
        print("\n🎉 数据补充完成！")
        print("\n提示: 重启前端页面以查看更新后的数据")
    finally:
        db.close()

if __name__ == "__main__":
    main()

