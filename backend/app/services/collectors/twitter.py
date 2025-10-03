"""Twitter数据采集服务"""

import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
import tweepy
from app.core.config import settings


class TwitterCollector:
    """Twitter数据采集器"""
    
    # 监控的关键词列表
    KEYWORDS = [
        "presale",
        "fair launch",
        "new token",
        "airdrop",
        "testnet",
        "mainnet launch",
        "IDO",
        "ICO",
        "token sale",
        "Web3",
        "DeFi",
        "NFT mint",
    ]
    
    # 顶级加密KOL列表
    TOP_KOLS = [
        "VitalikButerin",
        "aantonop",
        "CZ_Binance",
        "SBF_FTX",
        "brian_armstrong",
        "justinsuntron",
        "APompliano",
        "TheCryptoLark",
        "inversebrah",
        "CryptoWendyO",
    ]
    
    def __init__(self):
        """初始化Twitter客户端"""
        if not settings.TWITTER_BEARER_TOKEN:
            logger.warning("Twitter Bearer Token not configured")
            self.client = None
            return
            
        try:
            self.client = tweepy.Client(
                bearer_token=settings.TWITTER_BEARER_TOKEN,
                wait_on_rate_limit=True
            )
            logger.info("✅ Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            self.client = None
    
    def search_recent_tweets(
        self,
        query: str,
        max_results: int = 100,
        hours: int = 24
    ) -> List[Dict]:
        """搜索最近的推文
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数 (10-100)
            hours: 搜索过去N小时的推文
            
        Returns:
            推文列表
        """
        if not self.client:
            logger.warning("Twitter client not available")
            return []
        
        try:
            # 计算时间范围
            start_time = datetime.utcnow() - timedelta(hours=hours)
            
            # 搜索推文
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                start_time=start_time,
                tweet_fields=["created_at", "public_metrics", "author_id", "entities"],
                expansions=["author_id"],
                user_fields=["username", "verified", "public_metrics"]
            )
            
            if not tweets.data:
                logger.info(f"No tweets found for query: {query}")
                return []
            
            # 解析推文数据
            results = []
            users = {user.id: user for user in tweets.includes.get("users", [])}
            
            for tweet in tweets.data:
                author = users.get(tweet.author_id)
                
                result = {
                    "tweet_id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "author_id": tweet.author_id,
                    "author_username": author.username if author else None,
                    "author_verified": author.verified if author else False,
                    "author_followers": author.public_metrics["followers_count"] if author else 0,
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"],
                    "replies": tweet.public_metrics["reply_count"],
                    "entities": tweet.entities if hasattr(tweet, "entities") else {},
                }
                
                results.append(result)
            
            logger.info(f"✅ Found {len(results)} tweets for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    def monitor_keywords(self, hours: int = 1) -> List[Dict]:
        """监控关键词相关推文
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            所有关键词的推文列表
        """
        all_tweets = []
        
        for keyword in self.KEYWORDS:
            # 构建查询(排除转发)
            query = f"{keyword} -is:retweet lang:en"
            
            tweets = self.search_recent_tweets(
                query=query,
                max_results=50,
                hours=hours
            )
            
            # 标记关键词
            for tweet in tweets:
                tweet["matched_keyword"] = keyword
            
            all_tweets.extend(tweets)
        
        logger.info(f"✅ Total tweets collected: {len(all_tweets)}")
        return all_tweets
    
    def track_kol_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """追踪KOL的最新推文
        
        Args:
            username: Twitter用户名
            max_results: 最大结果数
            
        Returns:
            推文列表
        """
        if not self.client:
            return []
        
        try:
            # 获取用户
            user = self.client.get_user(username=username)
            if not user.data:
                logger.warning(f"User not found: {username}")
                return []
            
            user_id = user.data.id
            
            # 获取用户推文
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "entities"],
                exclude=["retweets", "replies"]  # 只要原创推文
            )
            
            if not tweets.data:
                return []
            
            results = []
            for tweet in tweets.data:
                result = {
                    "tweet_id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "author_username": username,
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"],
                    "replies": tweet.public_metrics["reply_count"],
                    "entities": tweet.entities if hasattr(tweet, "entities") else {},
                }
                results.append(result)
            
            logger.info(f"✅ Collected {len(results)} tweets from @{username}")
            return results
            
        except Exception as e:
            logger.error(f"Error tracking KOL {username}: {e}")
            return []
    
    def track_all_kols(self) -> List[Dict]:
        """追踪所有顶级KOL的推文
        
        Returns:
            所有KOL的推文列表
        """
        all_tweets = []
        
        for username in self.TOP_KOLS:
            tweets = self.track_kol_tweets(username, max_results=10)
            
            # 标记为KOL推文
            for tweet in tweets:
                tweet["is_kol_tweet"] = True
                tweet["kol_username"] = username
            
            all_tweets.extend(tweets)
        
        logger.info(f"✅ Total KOL tweets collected: {len(all_tweets)}")
        return all_tweets
    
    def extract_project_info(self, tweet: Dict) -> Optional[Dict]:
        """从推文中提取项目信息
        
        Args:
            tweet: 推文数据
            
        Returns:
            项目信息字典 or None
        """
        text = tweet["text"]
        entities = tweet.get("entities", {})
        
        # 提取URL
        urls = []
        if "urls" in entities:
            urls = [url["expanded_url"] for url in entities["urls"]]
        
        # 提取提及的用户
        mentions = []
        if "mentions" in entities:
            mentions = [mention["username"] for mention in entities["mentions"]]
        
        # 提取hashtags
        hashtags = []
        if "hashtags" in entities:
            hashtags = [tag["tag"] for tag in entities["hashtags"]]
        
        # 尝试提取合约地址(以太坊地址格式)
        contract_pattern = r"0x[a-fA-F0-9]{40}"
        contracts = re.findall(contract_pattern, text)
        
        # 如果没有找到明显的项目信息，返回None
        if not urls and not contracts and not hashtags:
            return None
        
        return {
            "tweet_id": tweet["tweet_id"],
            "discovered_at": tweet["created_at"],
            "source": "twitter",
            "source_url": f"https://twitter.com/{tweet.get('author_username')}/status/{tweet['tweet_id']}",
            "text": text,
            "urls": urls,
            "contracts": contracts,
            "hashtags": hashtags,
            "mentions": mentions,
            "engagement": {
                "likes": tweet["likes"],
                "retweets": tweet["retweets"],
                "replies": tweet["replies"],
            },
            "author": {
                "username": tweet.get("author_username"),
                "verified": tweet.get("author_verified", False),
                "followers": tweet.get("author_followers", 0),
            }
        }
    
    def collect_and_extract(self, hours: int = 1) -> List[Dict]:
        """采集推文并提取项目信息
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            项目信息列表
        """
        logger.info(f"🔍 Starting Twitter collection (last {hours} hours)...")
        
        # 1. 监控关键词
        keyword_tweets = self.monitor_keywords(hours=hours)
        
        # 2. 追踪KOL
        kol_tweets = self.track_all_kols()
        
        # 3. 合并去重
        all_tweets = keyword_tweets + kol_tweets
        unique_tweets = {tweet["tweet_id"]: tweet for tweet in all_tweets}
        
        logger.info(f"📊 Collected {len(unique_tweets)} unique tweets")
        
        # 4. 提取项目信息
        projects = []
        for tweet in unique_tweets.values():
            project_info = self.extract_project_info(tweet)
            if project_info:
                projects.append(project_info)
        
        logger.info(f"✅ Extracted {len(projects)} potential projects")
        return projects


# 全局采集器实例
twitter_collector = TwitterCollector()

