"""插入测试数据到数据库"""

import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Project

# 数据库连接
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/web3_alpha_hunter"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 真实的Web3项目测试数据
TEST_PROJECTS = [
    {
        "project_name": "Uniswap",
        "symbol": "UNI",
        "blockchain": "Ethereum",
        "category": "DeFi",
        "description": "去中心化交易协议,AMM龙头",
        "overall_score": 92.5,
        "grade": "S",
        "website": "https://uniswap.org",
        "twitter_handle": "@Uniswap",
        "logo_url": "https://cryptologos.cc/logos/uniswap-uni-logo.png"
    },
    {
        "project_name": "Arbitrum",
        "symbol": "ARB",
        "blockchain": "Ethereum L2",
        "category": "Infrastructure",
        "description": "以太坊L2扩容方案,Optimistic Rollup",
        "overall_score": 89.3,
        "grade": "S",
        "website": "https://arbitrum.io",
        "twitter_handle": "@arbitrum",
        "logo_url": "https://cryptologos.cc/logos/arbitrum-arb-logo.png"
    },
    {
        "project_name": "Jupiter",
        "symbol": "JUP",
        "blockchain": "Solana",
        "category": "DeFi",
        "description": "Solana生态最大DEX聚合器",
        "overall_score": 88.7,
        "grade": "S",
        "website": "https://jup.ag",
        "twitter_handle": "@JupiterExchange",
        "logo_url": "https://jup.ag/logo.png"
    },
    {
        "project_name": "Wormhole",
        "symbol": "W",
        "blockchain": "Multi-chain",
        "category": "Infrastructure",
        "description": "跨链通信协议,连接各大公链",
        "overall_score": 81.2,
        "grade": "A",
        "website": "https://wormhole.com",
        "twitter_handle": "@wormhole",
        "logo_url": "https://wormhole.com/logo.png"
    },
    {
        "project_name": "Jito",
        "symbol": "JTO",
        "blockchain": "Solana",
        "category": "DeFi",
        "description": "Solana流动性质押协议,MEV优化",
        "overall_score": 78.9,
        "grade": "A",
        "website": "https://jito.network",
        "twitter_handle": "@jito_sol",
        "logo_url": "https://jito.network/logo.png"
    },
    {
        "project_name": "Optimism",
        "symbol": "OP",
        "blockchain": "Ethereum L2",
        "category": "Infrastructure",
        "description": "以太坊L2,Optimistic Rollup方案",
        "overall_score": 85.6,
        "grade": "S",
        "website": "https://optimism.io",
        "twitter_handle": "@Optimism",
        "logo_url": "https://cryptologos.cc/logos/optimism-ethereum-op-logo.png"
    },
    {
        "project_name": "Polygon",
        "symbol": "MATIC",
        "blockchain": "Ethereum L2",
        "category": "Infrastructure",
        "description": "以太坊侧链,多链扩容方案",
        "overall_score": 83.4,
        "grade": "A",
        "website": "https://polygon.technology",
        "twitter_handle": "@0xPolygon",
        "logo_url": "https://cryptologos.cc/logos/polygon-matic-logo.png"
    },
    {
        "project_name": "Lido",
        "symbol": "LDO",
        "blockchain": "Ethereum",
        "category": "DeFi",
        "description": "流动性质押协议,stETH发行方",
        "overall_score": 87.2,
        "grade": "S",
        "website": "https://lido.fi",
        "twitter_handle": "@LidoFinance",
        "logo_url": "https://cryptologos.cc/logos/lido-dao-ldo-logo.png"
    },
    {
        "project_name": "Aave",
        "symbol": "AAVE",
        "blockchain": "Ethereum",
        "category": "DeFi",
        "description": "去中心化借贷协议龙头",
        "overall_score": 86.8,
        "grade": "S",
        "website": "https://aave.com",
        "twitter_handle": "@AaveAave",
        "logo_url": "https://cryptologos.cc/logos/aave-aave-logo.png"
    },
    {
        "project_name": "Sui",
        "symbol": "SUI",
        "blockchain": "Sui",
        "category": "Infrastructure",
        "description": "Move语言新公链,高性能L1",
        "overall_score": 79.5,
        "grade": "A",
        "website": "https://sui.io",
        "twitter_handle": "@SuiNetwork",
        "logo_url": "https://sui.io/logo.png"
    },
    {
        "project_name": "Aptos",
        "symbol": "APT",
        "blockchain": "Aptos",
        "category": "Infrastructure",
        "description": "Move语言新公链,前Meta团队",
        "overall_score": 77.3,
        "grade": "A",
        "website": "https://aptosfoundation.org",
        "twitter_handle": "@Aptos",
        "logo_url": "https://aptosfoundation.org/logo.png"
    },
    {
        "project_name": "Celestia",
        "symbol": "TIA",
        "blockchain": "Celestia",
        "category": "Infrastructure",
        "description": "模块化区块链,数据可用性层",
        "overall_score": 80.1,
        "grade": "A",
        "website": "https://celestia.org",
        "twitter_handle": "@CelestiaOrg",
        "logo_url": "https://celestia.org/logo.png"
    },
    {
        "project_name": "Pendle",
        "symbol": "PENDLE",
        "blockchain": "Ethereum",
        "category": "DeFi",
        "description": "利率衍生品协议,yield trading",
        "overall_score": 75.8,
        "grade": "B",
        "website": "https://pendle.finance",
        "twitter_handle": "@pendle_fi",
        "logo_url": "https://pendle.finance/logo.png"
    },
    {
        "project_name": "Blur",
        "symbol": "BLUR",
        "blockchain": "Ethereum",
        "category": "NFT",
        "description": "NFT交易聚合平台,专业交易工具",
        "overall_score": 72.4,
        "grade": "B",
        "website": "https://blur.io",
        "twitter_handle": "@blur_io",
        "logo_url": "https://blur.io/logo.png"
    },
    {
        "project_name": "dYdX",
        "symbol": "DYDX",
        "blockchain": "Ethereum",
        "category": "DeFi",
        "description": "去中心化衍生品交易所",
        "overall_score": 84.2,
        "grade": "A",
        "website": "https://dydx.exchange",
        "twitter_handle": "@dYdX",
        "logo_url": "https://dydx.exchange/logo.png"
    },
    {
        "project_name": "GMX",
        "symbol": "GMX",
        "blockchain": "Arbitrum",
        "category": "DeFi",
        "description": "去中心化永续合约交易所",
        "overall_score": 82.7,
        "grade": "A",
        "website": "https://gmx.io",
        "twitter_handle": "@GMX_IO",
        "logo_url": "https://gmx.io/logo.png"
    },
    {
        "project_name": "Render",
        "symbol": "RNDR",
        "blockchain": "Ethereum",
        "category": "AI",
        "description": "去中心化GPU渲染网络",
        "overall_score": 76.9,
        "grade": "B",
        "website": "https://render.com",
        "twitter_handle": "@rendernetwork",
        "logo_url": "https://render.com/logo.png"
    },
    {
        "project_name": "Immutable X",
        "symbol": "IMX",
        "blockchain": "Ethereum L2",
        "category": "NFT",
        "description": "NFT专用L2,零Gas费",
        "overall_score": 78.5,
        "grade": "A",
        "website": "https://immutable.com",
        "twitter_handle": "@Immutable",
        "logo_url": "https://immutable.com/logo.png"
    },
    {
        "project_name": "StarkNet",
        "symbol": "STRK",
        "blockchain": "Ethereum L2",
        "category": "Infrastructure",
        "description": "ZK-Rollup L2,Cairo语言",
        "overall_score": 81.8,
        "grade": "A",
        "website": "https://starknet.io",
        "twitter_handle": "@StarkNetFndn",
        "logo_url": "https://starknet.io/logo.png"
    },
    {
        "project_name": "Mantle",
        "symbol": "MNT",
        "blockchain": "Ethereum L2",
        "category": "Infrastructure",
        "description": "模块化L2,Bybit投资",
        "overall_score": 74.6,
        "grade": "B",
        "website": "https://mantle.xyz",
        "twitter_handle": "@0xMantle",
        "logo_url": "https://mantle.xyz/logo.png"
    }
]


def seed_projects():
    """插入项目数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing_count = db.query(Project).count()
        if existing_count > 0:
            print(f"⚠️  数据库中已有 {existing_count} 条项目数据")
            response = input("是否清空并重新插入? (y/N): ")
            if response.lower() != 'y':
                print("❌ 取消操作")
                return
            
            # 清空现有数据
            db.query(Project).delete()
            db.commit()
            print("✅ 已清空现有数据")
        
        # 插入测试数据
        print(f"\n开始插入 {len(TEST_PROJECTS)} 条测试数据...")
        
        for i, project_data in enumerate(TEST_PROJECTS, 1):
            project = Project(
                **project_data,
                first_discovered_at=datetime.now(),
                last_updated_at=datetime.now()
            )
            db.add(project)
            print(f"  [{i}/{len(TEST_PROJECTS)}] ✓ {project_data['project_name']}")
        
        db.commit()
        
        # 验证
        final_count = db.query(Project).count()
        print(f"\n✅ 成功插入 {final_count} 条项目数据!")
        print(f"📊 数据库: web3_alpha_hunter")
        print(f"📋 表名: projects")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 插入数据失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🌱 Web3 Alpha Hunter - 数据库种子数据脚本")
    print("=" * 60)
    print()
    
    seed_projects()
    
    print()
    print("=" * 60)
    print("✨ 完成!")
    print("=" * 60)
