"""
添加模拟的待审核项目（用于测试）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import get_db
from app.services.ai_agent import create_ai_agent


def seed_pending_projects():
    """添加模拟项目"""
    
    # 模拟原始数据
    mock_projects = [
        {
            'name': 'Parallel Finance',
            'symbol': 'PARA',
            'description': 'Polkadot生态DeFi协议,提供借贷、流动性挖矿和跨链功能',
            'source': 'twitter',
            'source_url': 'https://twitter.com/ParallelFi/status/123456',
            'content': 'Parallel Finance announces testnet launch...',
            'website': 'https://parallel.fi',
            'twitter': '@ParallelFi',
            'team_public': True,
            'team_experienced': True,
            'has_github': True,
            'has_whitepaper': True,
            'innovation_level': 8,
            'followers': 25000,
            'engagement_rate': 4.5,
            'has_token_plan': True,
            'trending': True,
            'vc_backed': True,
            'vc_names': 'Polychain Capital, Pantera Capital'
        },
        {
            'name': 'zkSync Era',
            'symbol': 'ZKS',
            'description': '以太坊Layer2扩容方案,使用零知识证明技术',
            'source': 'telegram',
            'source_url': 'https://t.me/zksync/98765',
            'content': 'zkSync Era mainnet launching soon...',
            'website': 'https://zksync.io',
            'twitter': '@zksync',
            'telegram': '@zksync',
            'team_public': True,
            'team_experienced': True,
            'team_doxxed': True,
            'has_github': True,
            'has_whitepaper': True,
            'innovation_level': 9,
            'followers': 150000,
            'engagement_rate': 6.8,
            'github_stars': 2500,
            'has_token_plan': True,
            'trending': True,
            'vc_backed': True,
            'vc_names': 'a16z, Variant'
        },
        {
            'name': 'Fuel Network',
            'symbol': 'FUEL',
            'description': '模块化执行层,为以太坊提供高性能rollup',
            'source': 'discord',
            'source_url': 'https://discord.com/fuel/56789',
            'content': 'Fuel Network announces incentivized testnet...',
            'website': 'https://fuel.network',
            'twitter': '@fuel_network',
            'discord': 'https://discord.gg/fuel',
            'team_public': True,
            'team_experienced': True,
            'has_github': True,
            'innovation_level': 8,
            'followers': 45000,
            'engagement_rate': 5.2,
            'github_stars': 1200,
            'has_token_plan': True,
            'vc_backed': True,
            'vc_names': 'CoinFund, Blockchain Capital'
        },
        {
            'name': 'Berachain',
            'symbol': 'BERA',
            'description': 'EVM兼容的L1区块链,采用Proof of Liquidity共识',
            'source': 'twitter',
            'source_url': 'https://twitter.com/berachain/status/789012',
            'content': 'Berachain testnet is live...',
            'website': 'https://berachain.com',
            'twitter': '@berachain',
            'telegram': '@berachain',
            'team_public': True,
            'has_github': True,
            'innovation_level': 7,
            'followers': 80000,
            'engagement_rate': 7.5,
            'has_token_plan': True,
            'fair_launch': True,
            'trending': True,
            'vc_backed': True,
            'vc_names': 'Polychain, Framework Ventures'
        },
        {
            'name': 'Hyperliquid',
            'symbol': 'HYPE',
            'description': '去中心化永续合约交易所,高性能订单簿',
            'source': 'twitter',
            'source_url': 'https://twitter.com/HyperliquidX/status/345678',
            'content': 'Hyperliquid announces points program...',
            'website': 'https://hyperliquid.xyz',
            'twitter': '@HyperliquidX',
            'team_public': False,  # 匿名团队
            'has_github': True,
            'innovation_level': 8,
            'followers': 35000,
            'engagement_rate': 5.8,
            'has_token_plan': True,
            'trending': True
        },
    ]
    
    db = next(get_db())
    ai_agent = create_ai_agent(db)
    
    saved_count = 0
    
    for project_data in mock_projects:
        print(f"\n🔍 分析项目: {project_data['name']}")
        
        # AI分析
        analysis = ai_agent.analyze_project(project_data)
        
        if analysis:
            print(f"   AI评分: {analysis['ai_score']:.1f} ({analysis['ai_grade']}级)")
            print(f"   置信度: {analysis['ai_confidence']*100:.0f}%")
            print(f"   推荐理由: {len(analysis['ai_recommendation_reason']['reasons'])}条")
            
            # 保存到待审核表
            project_id = ai_agent.save_to_pending(analysis)
            print(f"   ✅ 已保存到待审核表 (ID: {project_id})")
            saved_count += 1
        else:
            print(f"   ❌ 不符合推荐标准 (评分过低)")
    
    print(f"\n" + "="*60)
    print(f"✅ 完成! 共添加 {saved_count}/{len(mock_projects)} 个待审核项目")
    print("="*60)
    
    # 检查配额
    quota = ai_agent.check_daily_quota()
    print(f"\n📊 今日推荐配额:")
    print(f"   已推荐: {quota['today_recommended']}/{quota['max_allowed']}")
    print(f"   剩余配额: {quota['max_allowed'] - quota['today_recommended']}")


if __name__ == "__main__":
    seed_pending_projects()

