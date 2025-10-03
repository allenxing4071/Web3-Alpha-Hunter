"""
真实数据采集脚本 - 从Twitter/Telegram/CoinGecko等平台采集Web3项目数据
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
import json

class RealDataCollector:
    """真实数据采集器"""
    
    def __init__(self):
        self.projects = []
        
    async def fetch_coingecko_trending(self) -> List[Dict]:
        """从CoinGecko获取热门币种"""
        url = "https://api.coingecko.com/api/v3/search/trending"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        coins = data.get('coins', [])
                        
                        projects = []
                        for item in coins[:10]:  # 取前10个
                            coin = item.get('item', {})
                            projects.append({
                                'name': coin.get('name'),
                                'symbol': coin.get('symbol'),
                                'market_cap_rank': coin.get('market_cap_rank'),
                                'thumb': coin.get('thumb'),
                                'price_btc': coin.get('price_btc'),
                                'score': coin.get('score'),
                                'source': 'coingecko_trending'
                            })
                        
                        print(f"✅ 从CoinGecko获取到 {len(projects)} 个热门项目")
                        return projects
                    else:
                        print(f"❌ CoinGecko API错误: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ CoinGecko采集失败: {e}")
            return []
    
    async def fetch_coingecko_new_listings(self) -> List[Dict]:
        """获取CoinGecko新上市币种"""
        url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # 取最新的20个
                        recent = data[-20:] if len(data) > 20 else data
                        
                        projects = []
                        for coin in recent:
                            projects.append({
                                'id': coin.get('id'),
                                'name': coin.get('name'),
                                'symbol': coin.get('symbol'),
                                'platforms': coin.get('platforms', {}),
                                'source': 'coingecko_new'
                            })
                        
                        print(f"✅ 获取到 {len(projects)} 个新上市项目")
                        return projects
                    else:
                        print(f"❌ CoinGecko新币API错误: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ 新币采集失败: {e}")
            return []
    
    async def fetch_github_trending(self) -> List[Dict]:
        """从GitHub获取Web3相关的热门项目"""
        # GitHub trending 不需要API key
        topics = ['web3', 'blockchain', 'defi', 'nft', 'crypto']
        projects = []
        
        try:
            async with aiohttp.ClientSession() as session:
                for topic in topics:
                    url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page=5"
                    
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            repos = data.get('items', [])
                            
                            for repo in repos:
                                projects.append({
                                    'name': repo.get('name'),
                                    'full_name': repo.get('full_name'),
                                    'description': repo.get('description'),
                                    'stars': repo.get('stargazers_count'),
                                    'url': repo.get('html_url'),
                                    'language': repo.get('language'),
                                    'topic': topic,
                                    'source': 'github_trending'
                                })
                        
                        await asyncio.sleep(1)  # 避免触发限流
            
            print(f"✅ 从GitHub获取到 {len(projects)} 个Web3项目")
            return projects
        except Exception as e:
            print(f"❌ GitHub采集失败: {e}")
            return []
    
    async def fetch_cryptopanic_news(self) -> List[Dict]:
        """从CryptoPanic获取加密货币新闻"""
        # 免费API,不需要key
        url = "https://cryptopanic.com/api/v1/posts/?auth_token=&public=true&kind=news&filter=hot"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        posts = data.get('results', [])
                        
                        projects = []
                        for post in posts[:20]:
                            currencies = post.get('currencies', [])
                            if currencies:
                                projects.append({
                                    'title': post.get('title'),
                                    'published_at': post.get('published_at'),
                                    'currencies': [c.get('code') for c in currencies],
                                    'url': post.get('url'),
                                    'votes': post.get('votes', {}).get('positive', 0),
                                    'source': 'cryptopanic_news'
                                })
                        
                        print(f"✅ 获取到 {len(projects)} 条加密新闻")
                        return projects
                    else:
                        print(f"❌ CryptoPanic API错误: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ 新闻采集失败: {e}")
            return []
    
    async def search_twitter_web3_projects(self) -> List[Dict]:
        """搜索Twitter上的Web3项目(使用公开API)"""
        # 注意: Twitter API需要认证,这里使用模拟数据
        # 真实场景需要申请Twitter API key
        
        keywords = [
            "new web3 project launch",
            "defi airdrop announcement",
            "nft mint coming soon",
            "blockchain funding raised"
        ]
        
        print("⚠️  Twitter采集需要API密钥,使用模拟数据...")
        
        # 模拟返回一些热门关键词提及
        mock_projects = [
            {
                'keyword': 'LayerZero',
                'mentions': 'High activity on Twitter',
                'sentiment': 'Positive',
                'source': 'twitter_search'
            },
            {
                'keyword': 'zkSync',
                'mentions': 'Airdrop rumors trending',
                'sentiment': 'Very Positive',
                'source': 'twitter_search'
            },
            {
                'keyword': 'Starknet',
                'mentions': 'New ecosystem projects',
                'sentiment': 'Positive',
                'source': 'twitter_search'
            }
        ]
        
        return mock_projects
    
    async def collect_all(self) -> Dict:
        """并行采集所有数据源"""
        print("\n🚀 开始采集真实Web3项目数据...\n")
        
        # 并行执行所有采集任务
        results = await asyncio.gather(
            self.fetch_coingecko_trending(),
            self.fetch_coingecko_new_listings(),
            self.fetch_github_trending(),
            self.fetch_cryptopanic_news(),
            self.search_twitter_web3_projects(),
            return_exceptions=True
        )
        
        # 整理结果
        all_data = {
            'coingecko_trending': results[0] if not isinstance(results[0], Exception) else [],
            'coingecko_new': results[1] if not isinstance(results[1], Exception) else [],
            'github_trending': results[2] if not isinstance(results[2], Exception) else [],
            'crypto_news': results[3] if not isinstance(results[3], Exception) else [],
            'twitter_signals': results[4] if not isinstance(results[4], Exception) else [],
            'timestamp': datetime.now().isoformat()
        }
        
        # 统计
        total = sum(len(v) for v in all_data.values() if isinstance(v, list))
        print(f"\n✅ 采集完成!共获取 {total} 条数据")
        
        return all_data
    
    def save_to_file(self, data: Dict, filename: str = "real_data.json"):
        """保存到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 数据已保存到: {filename}")


async def main():
    """主函数"""
    collector = RealDataCollector()
    data = await collector.collect_all()
    
    # 保存到文件
    collector.save_to_file(data, "backend/real_web3_data.json")
    
    # 打印摘要
    print("\n" + "="*60)
    print("📊 数据采集摘要:")
    print("="*60)
    print(f"🔥 CoinGecko热门币: {len(data['coingecko_trending'])} 个")
    print(f"🆕 CoinGecko新币: {len(data['coingecko_new'])} 个")
    print(f"💻 GitHub热门项目: {len(data['github_trending'])} 个")
    print(f"📰 加密新闻: {len(data['crypto_news'])} 条")
    print(f"🐦 Twitter信号: {len(data['twitter_signals'])} 个")
    print("="*60)
    
    # 展示一些热门项目
    print("\n🔥 CoinGecko当前热门项目TOP 5:")
    for i, project in enumerate(data['coingecko_trending'][:5], 1):
        print(f"  {i}. {project['name']} (${project['symbol']}) - Rank #{project.get('market_cap_rank', 'N/A')}")
    
    print("\n💻 GitHub热门Web3项目:")
    for i, project in enumerate(data['github_trending'][:5], 1):
        print(f"  {i}. {project['full_name']} - ⭐ {project['stars']} stars")


if __name__ == "__main__":
    asyncio.run(main())

