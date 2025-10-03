"""测试数据采集器(用于本地开发,不需要真实API)"""

from typing import List, Dict
from datetime import datetime, timedelta
import random
from loguru import logger


class MockTwitterCollector:
    """模拟Twitter采集器(用于测试)"""
    
    def __init__(self):
        logger.info("📝 Using MOCK Twitter collector (for testing)")
    
    def collect_and_extract(self, hours: int = 1) -> List[Dict]:
        """生成模拟数据"""
        
        mock_projects = [
            {
                "tweet_id": "1234567890",
                "discovered_at": datetime.utcnow() - timedelta(hours=2),
                "source": "twitter",
                "source_url": "https://twitter.com/VitalikButerin/status/1234567890",
                "text": "Excited to announce our new DeFi protocol launching next week! 🚀 Fair launch, no presale. #DeFi #Web3",
                "urls": ["https://defiprotocol.io"],
                "contracts": ["0x1234567890abcdef1234567890abcdef12345678"],
                "hashtags": ["DeFi", "Web3"],
                "mentions": ["defiprotocol"],
                "engagement": {
                    "likes": 5420,
                    "retweets": 1234,
                    "replies": 456,
                },
                "author": {
                    "username": "VitalikButerin",
                    "verified": True,
                    "followers": 5000000,
                }
            },
            {
                "tweet_id": "9876543210",
                "discovered_at": datetime.utcnow() - timedelta(hours=5),
                "source": "twitter",
                "source_url": "https://twitter.com/a16z/status/9876543210",
                "text": "We're thrilled to lead the $50M Series A for @NextGenProtocol. Revolutionary cross-chain infrastructure.",
                "urls": ["https://nextgenprotocol.xyz"],
                "contracts": [],
                "hashtags": ["Web3", "Investment"],
                "mentions": ["NextGenProtocol"],
                "engagement": {
                    "likes": 8900,
                    "retweets": 2100,
                    "replies": 678,
                },
                "author": {
                    "username": "a16z",
                    "verified": True,
                    "followers": 2000000,
                }
            },
            {
                "tweet_id": "1111222233",
                "discovered_at": datetime.utcnow() - timedelta(minutes=30),
                "source": "twitter",
                "source_url": "https://twitter.com/CryptoWhale/status/1111222233",
                "text": "New GameFi project launching testnet tomorrow. Team from former Axie Infinity developers. #GameFi #NFT",
                "urls": ["https://newgamefi.gg"],
                "contracts": ["0xabcdef1234567890abcdef1234567890abcdef12"],
                "hashtags": ["GameFi", "NFT"],
                "mentions": [],
                "engagement": {
                    "likes": 3200,
                    "retweets": 890,
                    "replies": 234,
                },
                "author": {
                    "username": "CryptoWhale",
                    "verified": False,
                    "followers": 450000,
                }
            }
        ]
        
        logger.info(f"✅ Generated {len(mock_projects)} mock projects")
        return mock_projects


class MockTelegramCollector:
    """模拟Telegram采集器(用于测试)"""
    
    def __init__(self):
        logger.info("📝 Using MOCK Telegram collector (for testing)")
    
    async def collect_and_extract(self, hours: int = 1) -> List[Dict]:
        """生成模拟数据"""
        
        mock_projects = [
            {
                "message_id": 12345,
                "discovered_at": datetime.utcnow() - timedelta(hours=1),
                "source": "telegram",
                "source_channel": "@CryptoGemAlerts",
                "text": "🚨 NEW GEM ALERT 🚨\n\nProject: SolanaSwap\nWebsite: https://solanaswap.io\nAudit: Certik ✅\nLiquidity: $2M locked\n\nFair launch in 2 hours!",
                "urls": ["https://solanaswap.io"],
                "contracts": [],
                "telegram_links": ["solanaswap_official"],
                "keywords": ["launch", "fair launch"],
                "engagement": {
                    "views": 15000,
                    "forwards": 450,
                    "replies": 89,
                }
            },
            {
                "message_id": 67890,
                "discovered_at": datetime.utcnow() - timedelta(hours=3),
                "source": "telegram",
                "source_channel": "@whale_alert",
                "text": "Major update: @BaseProtocol announces mainnet launch next month. Team revealed, all doxxed. Binance Labs backed.",
                "urls": ["https://baseprotocol.xyz"],
                "contracts": ["0xbaseprotocolcontractaddresshere1234567890ab"],
                "telegram_links": ["BaseProtocol"],
                "keywords": ["mainnet", "launch"],
                "engagement": {
                    "views": 25000,
                    "forwards": 890,
                    "replies": 156,
                }
            }
        ]
        
        logger.info(f"✅ Generated {len(mock_projects)} mock Telegram projects")
        return mock_projects


# 导出模拟采集器
mock_twitter_collector = MockTwitterCollector()
mock_telegram_collector = MockTelegramCollector()

