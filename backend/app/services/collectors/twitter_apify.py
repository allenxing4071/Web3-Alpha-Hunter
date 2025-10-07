"""基于Apify的Twitter数据采集服务"""

import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from apify_client import ApifyClient
from app.core.config import settings


class TwitterApifyCollector:
    """Apify Twitter采集器 - 使用第三方服务替代官方API"""
    
    # 监控的关键词列表 (与原Twitter采集器保持一致)
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
        "cz_binance",
        "elonmusk",
        "brian_armstrong",
        "justinsuntron",
        "APompliano",
        "TheCryptoLark",
        "inversebrah",
        "CryptoWendyO",
    ]
    
    def __init__(self):
        """初始化Apify客户端"""
        if not settings.APIFY_API_KEY:
            logger.warning("⚠️  Apify API key not configured")
            self.client = None
            return
        
        try:
            self.client = ApifyClient(settings.APIFY_API_KEY)
            logger.info("✅ Apify Twitter collector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Apify client: {e}")
            self.client = None
    
    def search_tweets(
        self, 
        query: str, 
        max_results: int = 100,
        hours: int = 24
    ) -> List[Dict]:
        """搜索推文
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            hours: 搜索过去N小时的推文
            
        Returns:
            推文列表
        """
        if not self.client:
            logger.warning("Apify client not available")
            return []
        
        try:
            # 计算时间范围
            start_time = datetime.utcnow() - timedelta(hours=hours)
            
            # Apify Twitter Scraper输入参数
            run_input = {
                "searchTerms": [query],
                "maxTweets": max_results,
                "includeSearchTerms": True,
                "onlyImage": False,
                "onlyVideo": False,
                "onlyQuote": False,
                "onlyTwitterBlue": False,
                "language": "en",
                "startDate": start_time.strftime("%Y-%m-%d"),
            }
            
            logger.info(f"🔍 Searching tweets for: {query} (max: {max_results})")
            
            # 运行actor
            run = self.client.actor(settings.APIFY_TWITTER_ACTOR_ID).call(
                run_input=run_input,
                timeout_secs=300  # 5分钟超时
            )
            
            # 获取结果
            tweets = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                normalized = self._normalize_tweet(item)
                if normalized:
                    tweets.append(normalized)
            
            logger.info(f"✅ Found {len(tweets)} tweets for query: {query}")
            return tweets
            
        except Exception as e:
            logger.error(f"❌ Error searching tweets: {e}")
            return []
    
    def track_user_tweets(
        self, 
        username: str, 
        max_results: int = 10
    ) -> List[Dict]:
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
            run_input = {
                "handles": [username],
                "tweetsDesired": max_results,
                "includeReplies": False,
                "includeRetweets": False,
            }
            
            logger.info(f"📊 Tracking tweets from @{username}")
            
            run = self.client.actor(settings.APIFY_TWITTER_ACTOR_ID).call(
                run_input=run_input,
                timeout_secs=180
            )
            
            tweets = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                normalized = self._normalize_tweet(item)
                if normalized:
                    tweets.append(normalized)
            
            logger.info(f"✅ Collected {len(tweets)} tweets from @{username}")
            return tweets
            
        except Exception as e:
            logger.error(f"❌ Error tracking KOL {username}: {e}")
            return []
    
    def _normalize_tweet(self, raw_tweet: Dict) -> Optional[Dict]:
        """标准化推文格式，与原Twitter API保持一致
        
        Args:
            raw_tweet: Apify返回的原始推文数据
            
        Returns:
            标准化的推文字典
        """
        try:
            author = raw_tweet.get("author", {})
            
            return {
                "tweet_id": raw_tweet.get("id"),
                "text": raw_tweet.get("text", ""),
                "created_at": self._parse_date(raw_tweet.get("createdAt")),
                "author_id": author.get("id"),
                "author_username": author.get("userName"),
                "author_verified": author.get("isBlue", False),
                "author_followers": author.get("followers", 0),
                "likes": raw_tweet.get("likeCount", 0),
                "retweets": raw_tweet.get("retweetCount", 0),
                "replies": raw_tweet.get("replyCount", 0),
                "entities": self._extract_entities(raw_tweet),
            }
        except Exception as e:
            logger.warning(f"Failed to normalize tweet: {e}")
            return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return None
    
    def _extract_entities(self, tweet: Dict) -> Dict:
        """提取实体信息（URLs、hashtags、mentions）"""
        entities = {
            "urls": [],
            "hashtags": [],
            "mentions": []
        }
        
        # 提取URLs
        urls = tweet.get("urls", [])
        if isinstance(urls, list):
            entities["urls"] = [{"url": url} for url in urls if isinstance(url, str)]
        
        # 从文本提取hashtags
        text = tweet.get("text", "")
        hashtags = re.findall(r'#(\w+)', text)
        entities["hashtags"] = [{"tag": tag} for tag in hashtags]
        
        # 从文本提取mentions
        mentions = re.findall(r'@(\w+)', text)
        entities["mentions"] = [{"username": mention} for mention in mentions]
        
        return entities
    
    def monitor_keywords(self, hours: int = 1) -> List[Dict]:
        """监控关键词相关推文
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            所有关键词的推文列表
        """
        all_tweets = []
        
        # 由于Apify有调用限制，我们优化关键词策略
        # 选择最重要的5个关键词进行监控
        priority_keywords = ["presale", "airdrop", "IDO", "fair launch", "Web3"]
        
        for keyword in priority_keywords:
            # 构建查询(排除转发)
            query = f"{keyword} -RT"
            
            tweets = self.search_tweets(
                query=query,
                max_results=30,  # 每个关键词30条
                hours=hours
            )
            
            all_tweets.extend(tweets)
        
        # 去重
        unique_tweets = {tweet["tweet_id"]: tweet for tweet in all_tweets}
        logger.info(f"📊 Collected {len(unique_tweets)} unique tweets from keyword monitoring")
        
        return list(unique_tweets.values())
    
    def track_all_kols(self) -> List[Dict]:
        """追踪所有顶级KOL的推文
        
        Returns:
            所有KOL的推文列表
        """
        all_tweets = []
        
        # 选择前5位KOL进行监控（节省API配额）
        priority_kols = self.TOP_KOLS[:5]
        
        for username in priority_kols:
            tweets = self.track_user_tweets(username, max_results=5)
            all_tweets.extend(tweets)
        
        logger.info(f"📊 Collected {len(all_tweets)} tweets from {len(priority_kols)} KOLs")
        return all_tweets
    
    def extract_project_info(self, tweet: Dict) -> Optional[Dict]:
        """从推文中提取项目信息
        
        Args:
            tweet: 推文数据
            
        Returns:
            项目信息字典或None
        """
        text = tweet.get("text", "").lower()
        
        # 检查是否包含项目相关关键词
        project_indicators = [
            "presale", "launch", "airdrop", "mint", 
            "token", "ico", "ido", "whitelist"
        ]
        
        if not any(indicator in text for indicator in project_indicators):
            return None
        
        # 提取项目名称 (简化版)
        project_name = self._extract_project_name(tweet)
        if not project_name:
            return None
        
        # 计算质量分数
        quality_score = self._calculate_quality_score(tweet)
        
        return {
            "name": project_name,
            "description": tweet.get("text", "")[:500],
            "twitter_handle": self._extract_twitter_handle(tweet),
            "discovered_at": tweet.get("created_at") or datetime.utcnow(),
            "source": "twitter_apify",
            "source_url": f"https://twitter.com/{tweet.get('author_username')}/status/{tweet.get('tweet_id')}",
            "engagement_score": quality_score,
            "metadata": {
                "likes": tweet.get("likes", 0),
                "retweets": tweet.get("retweets", 0),
                "author_followers": tweet.get("author_followers", 0),
            }
        }
    
    def _extract_project_name(self, tweet: Dict) -> Optional[str]:
        """提取项目名称"""
        text = tweet.get("text", "")
        
        # 尝试从hashtags提取
        entities = tweet.get("entities", {})
        hashtags = entities.get("hashtags", [])
        
        if hashtags:
            # 过滤掉通用标签
            exclude_tags = {"crypto", "web3", "defi", "nft", "blockchain"}
            for hashtag in hashtags:
                tag = hashtag.get("tag", "").lower()
                if tag and tag not in exclude_tags:
                    return hashtag.get("tag")
        
        # 尝试从文本提取（简化版）
        # 查找 "project_name is launching" 模式
        patterns = [
            r'(\w+)\s+(?:is|will be|announces)',
            r'(?:introducing|announcing)\s+(\w+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1)
                if len(name) > 2:  # 至少3个字符
                    return name.capitalize()
        
        return None
    
    def _extract_twitter_handle(self, tweet: Dict) -> Optional[str]:
        """提取Twitter handle"""
        entities = tweet.get("entities", {})
        mentions = entities.get("mentions", [])
        
        if mentions:
            return mentions[0].get("username")
        
        return None
    
    def _calculate_quality_score(self, tweet: Dict) -> float:
        """计算推文质量分数
        
        基于点赞数、转发数、作者粉丝数等指标
        
        Returns:
            0-100的质量分数
        """
        likes = tweet.get("likes", 0)
        retweets = tweet.get("retweets", 0)
        followers = tweet.get("author_followers", 0)
        verified = tweet.get("author_verified", False)
        
        # 参与度分数 (0-50)
        engagement_score = min(50, (likes + retweets * 2) / 10)
        
        # 作者影响力分数 (0-30)
        influence_score = min(30, followers / 1000)
        
        # 认证加分 (0-20)
        verified_score = 20 if verified else 0
        
        total_score = engagement_score + influence_score + verified_score
        
        return min(100, total_score)
    
    def collect_and_extract(self, hours: int = 1) -> List[Dict]:
        """采集推文并提取项目信息（主入口）
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            项目信息列表
        """
        logger.info(f"🔍 Starting Apify Twitter collection (last {hours} hours)...")
        
        if not self.client:
            logger.error("❌ Apify client not initialized")
            return []
        
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
twitter_apify_collector = TwitterApifyCollector()
