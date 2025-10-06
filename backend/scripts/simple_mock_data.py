#!/usr/bin/env python3
"""简化版测试数据生成 - 只生成项目基础数据"""

import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from app.core.config import settings

# 项目模板
PROJECTS = [
    ("DeFi Protocol Alpha", "DEFI", "Ethereum", "DeFi"),
    ("MetaVerse World", "META", "Polygon", "GameFi"),
    ("GameFi Arena Pro", "GAME", "Solana", "GameFi"),
    ("AI Trading Bot X", "AITX", "Arbitrum", "AI"),
    ("Cross-Chain Bridge", "XCB", "Optimism", "Infrastructure"),
    ("NFT Marketplace Hub", "NFT", "Ethereum", "NFT"),
    ("Liquid Staking Pro", "LST", "Ethereum", "DeFi"),
    ("DAO Governance Tool", "DAO", "Polygon", "DAO"),
    ("Privacy Layer Network", "PRIV", "Solana", "Privacy"),
    ("Oracle Data Protocol", "ORC", "Arbitrum", "Infrastructure"),
    ("Lending Protocol Pro", "LEND", "Optimism", "DeFi"),
    ("Yield Optimizer Max", "YIELD", "Avalanche", "DeFi"),
    ("Social-Fi Platform", "SOCIAL", "Base", "Social"),
    ("RWA Tokenization Hub", "RWA", "Ethereum", "Infrastructure"),
    ("ZK Rollup Chain X", "ZKR", "Ethereum", "Infrastructure"),
]

def main():
    print("=" * 60)
    print("🚀 生成测试数据 (简化版)")
    print("=" * 60)
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 清空现有数据（可选）
        # conn.execute(text("TRUNCATE TABLE projects CASCADE"))
        # conn.commit()
        
        created = 0
        for name, symbol, blockchain, category in PROJECTS:
            # 生成评分
            team_score = round(random.uniform(65, 95), 1)
            tech_score = round(random.uniform(70, 98), 1)
            community_score = round(random.uniform(55, 90), 1)
            tokenomics_score = round(random.uniform(60, 92), 1)
            market_score = round(random.uniform(65, 95), 1)
            overall_score = round((team_score + tech_score + community_score + tokenomics_score + market_score) / 5, 1)
            
            # 确定等级
            if overall_score >= 85:
                grade = "S"
            elif overall_score >= 75:
                grade = "A"
            elif overall_score >= 65:
                grade = "B"
            else:
                grade = "C"
            
            # 插入项目
            try:
                conn.execute(text("""
                    INSERT INTO projects (
                        project_name, symbol, blockchain, category,
                        description, grade, status,
                        overall_score, team_score, tech_score,
                        community_score, tokenomics_score, market_timing_score,
                        created_at, updated_at
                    ) VALUES (
                        :name, :symbol, :blockchain, :category,
                        :desc, :grade, :status,
                        :overall, :team, :tech,
                        :community, :tokenomics, :market,
                        NOW(), NOW()
                    )
                """), {
                    "name": name,
                    "symbol": symbol,
                    "blockchain": blockchain,
                    "category": category,
                    "desc": f"A revolutionary {category} project on {blockchain}",
                    "grade": grade,
                    "status": random.choice(["active", "testnet", "mainnet"]),
                    "overall": overall_score,
                    "team": team_score,
                    "tech": tech_score,
                    "community": community_score,
                    "tokenomics": tokenomics_score,
                    "market": market_score
                })
                created += 1
                print(f"✅ {created}. {name} ({grade}级, {overall_score}分)")
            except Exception as e:
                print(f"❌ 失败: {name} - {e}")
        
        conn.commit()
    
    print("=" * 60)
    print(f"🎉 完成！共创建 {created} 个项目")
    
    # 统计
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM projects")).scalar()
        grades = conn.execute(text("""
            SELECT grade, COUNT(*) as cnt 
            FROM projects 
            GROUP BY grade 
            ORDER BY grade
        """)).fetchall()
        
        print(f"\n📊 当前数据库统计:")
        print(f"   总项目数: {total}")
        print(f"   等级分布: {dict(grades)}")

if __name__ == "__main__":
    main()

