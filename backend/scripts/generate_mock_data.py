#!/usr/bin/env python3
"""
生成测试数据 - 用于大屏展示
包含：项目、社交指标、链上数据、AI分析、KOL、发现记录等
"""

import random
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import create_engine, text
from app.core.config import settings
import json

# 模拟数据池
PROJECT_NAMES = [
    "DeFi Protocol Alpha", "MetaVerse World", "GameFi Arena", 
    "AI Trading Bot", "Cross-Chain Bridge", "NFT Marketplace Pro",
    "Liquid Staking Hub", "DAO Governance Tool", "Privacy Layer",
    "Oracle Network", "Lending Protocol X", "Yield Optimizer",
    "Social-Fi Platform", "RWA Tokenization", "ZK Rollup Chain",
    "MEV Protection", "Perpetual DEX", "Options Platform",
    "Prediction Market", "Decentralized CDN"
]

BLOCKCHAINS = ["Ethereum", "Solana", "Arbitrum", "Optimism", "Polygon", "BSC", "Avalanche", "Base"]
CATEGORIES = ["DeFi", "GameFi", "NFT", "Infrastructure", "Social", "AI", "Privacy", "DAO"]
GRADES = ["S", "A", "B", "C"]
STATUSES = ["active", "testnet", "upcoming", "mainnet"]

KOL_NAMES = [
    "CryptoWhale", "DeFiMaxi", "BlockchainGuru", "NFTCollector",
    "AlphaHunter", "YieldFarmer", "MEVKing", "TokenAnalyst",
    "ChainWatcher", "SmartMoneyFlow", "CryptoInsider", "OnchainSleuth"
]

DISCOVERY_SOURCES = ["twitter", "telegram", "discord", "github", "medium"]

def generate_projects(engine, count=30):
    """生成项目数据"""
    print(f"📦 生成 {count} 个项目...")
    
    with engine.connect() as conn:
        for i in range(count):
            project_name = random.choice(PROJECT_NAMES) + f" {random.randint(1, 999)}"
            blockchain = random.choice(BLOCKCHAINS)
            category = random.choice(CATEGORIES)
            
            # 基础评分
            team_score = round(random.uniform(60, 95), 1)
            tech_score = round(random.uniform(65, 98), 1)
            community_score = round(random.uniform(50, 90), 1)
            tokenomics_score = round(random.uniform(55, 92), 1)
            market_timing_score = round(random.uniform(60, 95), 1)
            risk_score = round(random.uniform(20, 60), 1)
            
            overall_score = round(
                (team_score * 0.25 + tech_score * 0.25 + community_score * 0.2 + 
                 tokenomics_score * 0.15 + market_timing_score * 0.15) * 0.9, 1
            )
            
            # 根据评分确定等级
            if overall_score >= 85:
                grade = "S"
            elif overall_score >= 75:
                grade = "A"
            elif overall_score >= 65:
                grade = "B"
            else:
                grade = "C"
            
            # 插入项目 (使用UUID或自增ID)
            days_ago = random.randint(1, 90)
            discovered_at = datetime.utcnow() - timedelta(days=days_ago)
            
            # 插入并获取ID
            result = conn.execute(text("""
                INSERT INTO projects (
                    project_name, symbol, blockchain, category, description,
                    website, twitter_handle, telegram_channel, github_repo,
                    overall_score, team_score, tech_score, community_score,
                    tokenomics_score, market_timing_score, risk_score,
                    grade, status, first_discovered_at, created_at, updated_at,
                    token_launch_probability, airdrop_value_estimate, risk_level
                ) VALUES (
                    :name, :symbol, :blockchain, :category, :description,
                    :website, :twitter, :telegram, :github,
                    :overall_score, :team_score, :tech_score, :community_score,
                    :tokenomics_score, :market_timing_score, :risk_score,
                    :grade, :status, :discovered_at, :discovered_at, NOW(),
                    :launch_prob, :airdrop_est, :risk_level
                )
                RETURNING id
            """), {
                "name": project_name,
                "symbol": project_name.upper().replace(" ", "")[:6],
                "blockchain": blockchain,
                "category": category,
                "description": f"A revolutionary {category} project on {blockchain}",
                "website": f"https://{project_name.lower().replace(' ', '')}.io",
                "twitter": f"@{project_name.replace(' ', '')}",
                "telegram": f"https://t.me/{project_name.replace(' ', '')}",
                "github": f"https://github.com/{project_name.replace(' ', '')}",
                "overall_score": overall_score,
                "team_score": team_score,
                "tech_score": tech_score,
                "community_score": community_score,
                "tokenomics_score": tokenomics_score,
                "market_timing_score": market_timing_score,
                "risk_score": risk_score,
                "grade": grade,
                "status": random.choice(STATUSES),
                "discovered_at": discovered_at,
                "launch_prob": round(random.uniform(0.4, 0.95), 2),
                "airdrop_est": round(random.uniform(500, 5000), 2),
                "risk_level": random.choice(["low", "medium", "high"])
            })
            
            # 获取插入的项目ID
            project_id = result.fetchone()[0]
            
            # 生成社交指标
            try:
                conn.execute(text("""
                    INSERT INTO social_metrics (
                        project_id, twitter_followers, twitter_engagement_rate,
                        telegram_members, discord_members, github_stars,
                        github_commits_last_week, community_sentiment,
                        snapshot_time, created_at
                    ) VALUES (
                        :project_id, :twitter_followers, :engagement_rate,
                        :telegram_members, :discord_members, :github_stars,
                        :commits, :sentiment, NOW(), NOW()
                    )
                """), {
                "project_id": project_id,
                "twitter_followers": random.randint(5000, 500000),
                "engagement_rate": round(random.uniform(2, 15), 2),
                "telegram_members": random.randint(1000, 100000),
                "discord_members": random.randint(500, 50000),
                    "github_stars": random.randint(100, 10000),
                    "commits": random.randint(5, 50),
                    "sentiment": round(random.uniform(0.5, 0.9), 2)
                })
            except Exception as e:
                print(f"  ⚠️  社交指标插入失败: {e}")
            
            # 生成链上指标
            if random.random() > 0.3:  # 70%的项目有链上数据
                try:
                    conn.execute(text("""
                        INSERT INTO onchain_metrics (
                            project_id, market_cap, price_usd, holder_count,
                            volume_24h, tvl_usd, active_addresses,
                            snapshot_time, created_at
                        ) VALUES (
                            :project_id, :market_cap, :price, :holders,
                            :volume, :tvl, :active_addresses, NOW(), NOW()
                        )
                    """), {
                    "project_id": project_id,
                    "market_cap": round(random.uniform(1000000, 500000000), 2),
                    "price": round(random.uniform(0.01, 100), 4),
                    "holders": random.randint(1000, 100000),
                        "volume": round(random.uniform(100000, 50000000), 2),
                        "tvl": round(random.uniform(500000, 100000000), 2),
                        "active_addresses": random.randint(500, 50000)
                    })
                except Exception as e:
                    print(f"  ⚠️  链上指标插入失败: {e}")
            
            # 生成AI分析
            try:
                conn.execute(text("""
                    INSERT INTO ai_analysis (
                        project_id, sentiment_score, sentiment_label,
                        scam_probability, tech_innovation_score,
                        team_background_score, market_potential_score,
                        summary, analyzed_at, created_at
                    ) VALUES (
                        :project_id, :sentiment_score, :sentiment_label,
                        :scam_prob, :tech_score, :team_score, :market_score,
                        :summary, NOW(), NOW()
                    )
                """), {
                "project_id": project_id,
                "sentiment_score": round(random.uniform(0.6, 0.95), 2),
                "sentiment_label": random.choice(["bullish", "neutral", "bearish"]),
                "scam_prob": round(random.uniform(0.05, 0.3), 2),
                "tech_score": tech_score,
                    "team_score": team_score,
                    "market_score": market_timing_score,
                    "summary": f"Strong {category} project with solid fundamentals"
                })
            except Exception as e:
                print(f"  ⚠️  AI分析插入失败: {e}")
            
            # 生成项目发现记录
            try:
                conn.execute(text("""
                    INSERT INTO project_discoveries (
                        project_id, total_mentions, platforms, heat_score,
                        mentions_24h, is_trending, first_seen_at, created_at
                    ) VALUES (
                        :project_id, :mentions, :platforms, :heat,
                        :mentions_24h, :trending, :first_seen, NOW()
                    )
                """), {
                "project_id": project_id,
                "mentions": random.randint(50, 5000),
                "platforms": json.dumps(random.sample(DISCOVERY_SOURCES, k=random.randint(2, 4))),
                "heat": round(random.uniform(50, 95), 1),
                    "mentions_24h": random.randint(10, 500),
                    "trending": random.random() > 0.7,
                    "first_seen": discovered_at
                })
            except Exception as e:
                print(f"  ⚠️  发现记录插入失败: {e}")
        
        conn.commit()
    
    print(f"✅ 完成项目数据生成")

def generate_kols(engine, count=15):
    """生成KOL数据"""
    print(f"👥 生成 {count} 个KOL...")
    
    with engine.connect() as conn:
        for i in range(count):
            kol_name = random.choice(KOL_NAMES) + f"{random.randint(1, 99)}"
            
            conn.execute(text("""
                INSERT INTO kols (
                    twitter_handle, display_name, followers, tier,
                    avg_engagement_rate, influence_score, quality_score,
                    this_week_mentions, created_at, discovered_at
                ) VALUES (
                    :handle, :name, :followers, :tier,
                    :engagement, :influence, :quality,
                    :mentions, NOW(), NOW()
                )
            """), {
                "handle": f"@{kol_name}",
                "name": kol_name,
                "followers": random.randint(10000, 1000000),
                "tier": random.randint(1, 3),
                "engagement": round(random.uniform(3, 12), 2),
                "influence": round(random.uniform(70, 98), 1),
                "quality": round(random.uniform(65, 95), 1),
                "mentions": random.randint(5, 50)
            })
        
        conn.commit()
    
    print(f"✅ 完成KOL数据生成")

def generate_pending_projects(engine, count=8):
    """生成待审核项目"""
    print(f"⏳ 生成 {count} 个待审核项目...")
    
    with engine.connect() as conn:
        for i in range(count):
            project_name = random.choice(PROJECT_NAMES) + f" New {random.randint(1, 99)}"
            ai_score = round(random.uniform(70, 95), 1)
            
            if ai_score >= 85:
                grade = "S"
            elif ai_score >= 75:
                grade = "A"
            else:
                grade = "B"
            
            conn.execute(text("""
                INSERT INTO projects_pending (
                    project_name, blockchain, category,
                    ai_score, ai_grade, review_status,
                    ai_recommendation_reason, submitted_at, created_at
                ) VALUES (
                    :name, :blockchain, :category,
                    :score, :grade, :status,
                    :reason, NOW(), NOW()
                )
            """), {
                "name": project_name,
                "blockchain": random.choice(BLOCKCHAINS),
                "category": random.choice(CATEGORIES),
                "score": ai_score,
                "grade": grade,
                "status": "pending",
                "reason": f"High-quality {random.choice(CATEGORIES)} project with strong fundamentals"
            })
        
        conn.commit()
    
    print(f"✅ 完成待审核项目生成")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 开始生成测试数据")
    print("=" * 60)
    
    engine = create_engine(settings.DATABASE_URL)
    
    # 生成数据
    generate_projects(engine, count=30)
    generate_kols(engine, count=15)
    generate_pending_projects(engine, count=8)
    
    # 统计数据
    with engine.connect() as conn:
        stats = {
            "projects": conn.execute(text("SELECT COUNT(*) FROM projects")).scalar(),
            "social_metrics": conn.execute(text("SELECT COUNT(*) FROM social_metrics")).scalar(),
            "onchain_metrics": conn.execute(text("SELECT COUNT(*) FROM onchain_metrics")).scalar(),
            "ai_analysis": conn.execute(text("SELECT COUNT(*) FROM ai_analysis")).scalar(),
            "discoveries": conn.execute(text("SELECT COUNT(*) FROM project_discoveries")).scalar(),
            "kols": conn.execute(text("SELECT COUNT(*) FROM kols")).scalar(),
            "pending": conn.execute(text("SELECT COUNT(*) FROM projects_pending")).scalar(),
        }
    
    print("\n" + "=" * 60)
    print("📊 数据生成完成统计")
    print("=" * 60)
    print(f"✅ 项目总数: {stats['projects']}")
    print(f"✅ 社交指标: {stats['social_metrics']}")
    print(f"✅ 链上数据: {stats['onchain_metrics']}")
    print(f"✅ AI分析: {stats['ai_analysis']}")
    print(f"✅ 发现记录: {stats['discoveries']}")
    print(f"✅ KOL数量: {stats['kols']}")
    print(f"✅ 待审核: {stats['pending']}")
    print("=" * 60)
    print("🎉 所有测试数据已生成！")

if __name__ == "__main__":
    main()

