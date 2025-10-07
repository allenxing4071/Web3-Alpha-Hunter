"""CoinGecko数据采集服务"""

import requests
from typing import List, Dict
from datetime import datetime
from loguru import logger


class CoinGeckoCollector:
    """CoinGecko数据采集器"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        """初始化CoinGecko客户端"""
        logger.info("✅ CoinGecko collector initialized")
    
    def get_trending_coins(self) -> List[Dict]:
        """获取trending coins"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/search/trending",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                coins = data.get("coins", [])
                logger.info(f"📊 Fetched {len(coins)} trending coins from CoinGecko")
                return coins
            else:
                logger.warning(f"CoinGecko API returned {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Failed to fetch trending coins: {e}")
            return []
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict]:
        """获取top gainers"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "price_change_percentage_24h_desc",
                    "per_page": limit,
                    "page": 1,
                    "sparkline": False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                coins = response.json()
                logger.info(f"📊 Fetched {len(coins)} top gainers from CoinGecko")
                return coins
            else:
                logger.warning(f"CoinGecko API returned {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Failed to fetch top gainers: {e}")
            return []
    
    def get_recently_added(self) -> List[Dict]:
        """获取recently added coins"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/coins/list/new",
                timeout=10
            )
            
            if response.status_code == 200:
                coins = response.json()
                logger.info(f"📊 Fetched {len(coins)} recently added coins")
                return coins[:20]  # 限制20个
            else:
                logger.warning(f"CoinGecko API returned {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Failed to fetch recently added coins: {e}")
            return []
    
    def get_coin_details(self, coin_id: str) -> Dict:
        """获取币种完整详情信息
        
        Args:
            coin_id: CoinGecko币种ID (如 'bitcoin', 'ethereum')
            
        Returns:
            完整的币种详情字典，包含：
            - blockchain: 区块链平台
            - category: 项目分类
            - website: 官网
            - twitter: Twitter账号
            - telegram: Telegram频道
            - discord: Discord链接
            - github: GitHub仓库
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/coins/{coin_id}",
                params={
                    "localization": "false",  # 不需要多语言
                    "tickers": "false",       # 不需要交易所数据
                    "market_data": "true",    # 需要市场数据
                    "community_data": "false",# 不需要社区数据
                    "developer_data": "false",# 不需要开发者数据
                    "sparkline": "false"      # 不需要价格走势
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 提取区块链平台
                blockchain = None
                platforms = data.get("platforms", {})
                if platforms:
                    # 获取第一个平台
                    blockchain = list(platforms.keys())[0] if platforms else None
                    # 标准化区块链名称
                    if blockchain:
                        blockchain_mapping = {
                            "ethereum": "Ethereum",
                            "binance-smart-chain": "BSC",
                            "polygon-pos": "Polygon",
                            "solana": "Solana",
                            "arbitrum-one": "Arbitrum",
                            "optimistic-ethereum": "Optimism",
                            "avalanche": "Avalanche"
                        }
                        blockchain = blockchain_mapping.get(blockchain, blockchain.title())
                
                # 提取分类
                categories = data.get("categories", [])
                category = categories[0] if categories else None
                
                # 提取社交链接
                links = data.get("links", {})
                website = links.get("homepage", [""])[0] or None
                
                # 提取Twitter (从 twitter_screen_name)
                twitter_handle = links.get("twitter_screen_name")
                if twitter_handle:
                    twitter_handle = f"@{twitter_handle}" if not twitter_handle.startswith("@") else twitter_handle
                
                # 提取Telegram
                telegram_url = links.get("telegram_channel_identifier")
                telegram_channel = f"@{telegram_url}" if telegram_url and not telegram_url.startswith("@") else telegram_url
                
                # 提取其他链接
                repos = links.get("repos_url", {})
                github_repo = repos.get("github", [""])[0] if isinstance(repos, dict) else None
                
                # Discord和其他
                chat_urls = links.get("chat_url", [])
                discord_link = next((url for url in chat_urls if "discord" in url.lower()), None)
                
                # 提取描述
                description_en = data.get("description", {}).get("en", "")
                # 截取前300字符作为简短描述
                if description_en and len(description_en) > 300:
                    description_en = description_en[:297] + "..."
                
                details = {
                    "blockchain": blockchain,
                    "category": category,
                    "website": website,
                    "twitter": twitter_handle,
                    "telegram": telegram_channel,
                    "discord": discord_link,
                    "github": github_repo,
                    "description_full": description_en,
                    "logo_url": data.get("image", {}).get("large"),
                    "market_cap_rank": data.get("market_cap_rank"),
                }
                
                logger.info(f"✅ Fetched details for {coin_id}: blockchain={blockchain}, category={category}")
                return details
            
            elif response.status_code == 429:
                logger.warning(f"⚠️ Rate limit reached for {coin_id}, skipping details")
                return {}
            else:
                logger.warning(f"⚠️ Failed to fetch details for {coin_id}: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error fetching details for {coin_id}: {e}")
            return {}
    
    def extract_project_info(self, coin: Dict, source_type: str = "trending") -> Dict:
        """从CoinGecko数据提取项目信息（包含完整详情）"""
        
        # 提取基础信息
        if source_type == "trending":
            # Trending coins格式
            item = coin.get("item", {})
            coin_id = item.get("id")
            base_info = {
                "name": item.get("name"),
                "symbol": item.get("symbol", "").upper(),
                "description": f"Trending on CoinGecko - Rank #{item.get('market_cap_rank', 'N/A')}",
                "coingecko_id": coin_id,
                "market_cap_rank": item.get("market_cap_rank"),
                "price_btc": item.get("price_btc"),
                "thumb": item.get("thumb"),
                "source_url": f"https://www.coingecko.com/en/coins/{coin_id}",
                "discovered_at": datetime.utcnow(),
                "source": f"coingecko_{source_type}"
            }
        else:
            # Markets格式 (top gainers)
            coin_id = coin.get("id")
            base_info = {
                "name": coin.get("name"),
                "symbol": coin.get("symbol", "").upper(),
                "description": f"24h Change: +{coin.get('price_change_percentage_24h', 0):.2f}%",
                "coingecko_id": coin_id,
                "market_cap_rank": coin.get("market_cap_rank"),
                "current_price": coin.get("current_price"),
                "market_cap": coin.get("market_cap"),
                "price_change_24h": coin.get("price_change_percentage_24h"),
                "source_url": f"https://www.coingecko.com/en/coins/{coin_id}",
                "discovered_at": datetime.utcnow(),
                "source": f"coingecko_{source_type}"
            }
        
        # 获取完整详情并合并
        if coin_id:
            details = self.get_coin_details(coin_id)
            if details:
                # 使用详情中的完整描述（如果有的话）
                if details.get("description_full"):
                    base_info["description"] = details["description_full"]
                
                # 合并所有详情字段
                base_info.update({
                    "blockchain": details.get("blockchain"),
                    "category": details.get("category"),
                    "website": details.get("website"),
                    "twitter": details.get("twitter"),
                    "telegram": details.get("telegram"),
                    "discord": details.get("discord"),
                    "github": details.get("github"),
                    "logo_url": details.get("logo_url"),
                })
                
                logger.info(f"📦 Enhanced {base_info['name']} with full details")
        
        return base_info
    
    def collect_and_extract(self) -> List[Dict]:
        """采集并提取项目信息"""
        logger.info("🔍 Starting CoinGecko collection...")
        
        projects = []
        
        # 1. Trending coins
        trending = self.get_trending_coins()
        for coin in trending:
            project = self.extract_project_info(coin, "trending")
            projects.append(project)
        
        # 2. Top gainers
        gainers = self.get_top_gainers(limit=5)
        for coin in gainers:
            project = self.extract_project_info(coin, "top_gainer")
            projects.append(project)
        
        logger.info(f"✅ Collected {len(projects)} projects from CoinGecko")
        return projects


# 全局采集器实例
coingecko_collector = CoinGeckoCollector()



