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
    
    def extract_project_info(self, coin: Dict, source_type: str = "trending") -> Dict:
        """从CoinGecko数据提取项目信息"""
        
        if source_type == "trending":
            # Trending coins格式
            item = coin.get("item", {})
            return {
                "name": item.get("name"),
                "symbol": item.get("symbol", "").upper(),
                "description": f"Trending on CoinGecko - Rank #{item.get('market_cap_rank', 'N/A')}",
                "coingecko_id": item.get("id"),
                "market_cap_rank": item.get("market_cap_rank"),
                "price_btc": item.get("price_btc"),
                "thumb": item.get("thumb"),
                "source_url": f"https://www.coingecko.com/en/coins/{item.get('id')}",
                "discovered_at": datetime.utcnow(),
                "source": f"coingecko_{source_type}"
            }
        else:
            # Markets格式 (top gainers)
            return {
                "name": coin.get("name"),
                "symbol": coin.get("symbol", "").upper(),
                "description": f"24h Change: +{coin.get('price_change_percentage_24h', 0):.2f}%",
                "coingecko_id": coin.get("id"),
                "market_cap_rank": coin.get("market_cap_rank"),
                "current_price": coin.get("current_price"),
                "market_cap": coin.get("market_cap"),
                "price_change_24h": coin.get("price_change_percentage_24h"),
                "source_url": f"https://www.coingecko.com/en/coins/{coin.get('id')}",
                "discovered_at": datetime.utcnow(),
                "source": f"coingecko_{source_type}"
            }
    
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



