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
    
    def get_tweet_replies(self, tweet_id: str, max_results: int = 100) -> List[Dict]:
        """获取推文的评论
        
        Args:
            tweet_id: 推文ID
            max_results: 最大评论数
            
        Returns:
            评论列表
        """
        if not self.client:
            return []
        
        try:
            # 构建查询：conversation_id等于该推文ID的所有回复
            query = f"conversation_id:{tweet_id}"
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=["created_at", "public_metrics", "author_id", "entities"],
                expansions=["author_id"],
                user_fields=["username", "verified", "public_metrics"]
            )
            
            if not tweets.data:
                return []
            
            # 解析评论数据
            results = []
            users = {user.id: user for user in tweets.includes.get("users", [])}
            
            for tweet in tweets.data:
                author = users.get(tweet.author_id)
                
                result = {
                    "comment_id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "author_username": author.username if author else None,
                    "author_followers": author.public_metrics["followers_count"] if author else 0,
                    "likes": tweet.public_metrics["like_count"],
                    "replies": tweet.public_metrics["reply_count"],
                    "entities": tweet.entities if hasattr(tweet, "entities") else {},
                }
                
                results.append(result)
            
            logger.info(f"✅ Collected {len(results)} replies for tweet {tweet_id}")
            return results
            
        except Exception as e:
            logger.error(f"Error getting replies for tweet {tweet_id}: {e}")
            return []
    
    def calculate_comment_quality(self, comment: Dict) -> int:
        """计算评论质量分（0-100）
        
        Args:
            comment: 评论数据
            
        Returns:
            质量分数
        """
        score = 0
        
        # 因子1: 评论者粉丝数（30分）
        followers = comment.get("author_followers", 0)
        score += min(30, followers / 1000)
        
        # 因子2: 评论互动数（30分）
        engagement = comment.get("likes", 0) + comment.get("replies", 0)
        score += min(30, engagement / 10)
        
        # 因子3: 评论长度（20分）- 长评论往往更有价值
        text_length = len(comment.get("text", ""))
        if 50 < text_length < 280:
            score += 20
        elif text_length >= 280:
            score += 15
        
        # 因子4: 包含链接或合约地址（20分）
        text = comment.get("text", "")
        has_url = "http" in text
        has_contract = bool(re.search(r"0x[a-fA-F0-9]{40}", text))
        if has_url or has_contract:
            score += 20
        
        # 惩罚项: 垃圾评论特征
        spam_keywords = ["follow me", "dm me", "check my profile", "100x guaranteed"]
        for keyword in spam_keywords:
            if keyword.lower() in text.lower():
                score -= 30
        
        return max(0, min(100, int(score)))
    
    def extract_project_names(self, text: str) -> List[str]:
        """从文本中提取项目名称
        
        Args:
            text: 文本内容
            
        Returns:
            项目名称列表
        """
        projects = []
        
        # 方法1: 正则匹配（大写开头的词组）
        pattern1 = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        matches1 = re.findall(pattern1, text)
        projects.extend(matches1)
        
        # 方法2: 识别特定模式
        pattern2 = r'(?:check out|introducing|new project)\s+([A-Z][a-zA-Z\s]+?)(?:\.|,|$)'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        projects.extend(matches2)
        
        # 方法3: 识别网站链接
        urls = re.findall(r'https?://([a-zA-Z0-9-]+)\.[a-z]+', text)
        for url in urls:
            project_name = url.replace('-', ' ').title()
            projects.append(project_name)
        
        # 去重和清洗
        projects = list(set([p.strip() for p in projects if p.strip()]))
        
        # 过滤噪音（通用词汇）
        noise_words = ["The", "This", "That", "Twitter", "Discord", "Telegram"]
        projects = [p for p in projects if p not in noise_words and len(p) > 2]
        
        return projects
    
    def mine_comment_section(self, tweet_id: str) -> List[Dict]:
        """挖掘评论区
        
        Args:
            tweet_id: 推文ID
            
        Returns:
            发现的项目提及列表
        """
        # 1. 获取所有评论
        comments = self.get_tweet_replies(tweet_id, max_results=100)
        
        if not comments:
            return []
        
        # 2. 质量过滤
        quality_comments = []
        for comment in comments:
            quality = self.calculate_comment_quality(comment)
            if quality > 60:
                comment["quality_score"] = quality
                quality_comments.append(comment)
        
        logger.info(f"📊 {len(quality_comments)}/{len(comments)} comments passed quality filter")
        
        # 3. 提取项目提及
        project_mentions = []
        
        for comment in quality_comments:
            projects = self.extract_project_names(comment["text"])
            
            for project in projects:
                project_mentions.append({
                    "project_name": project,
                    "mentioned_in_comment": comment["comment_id"],
                    "comment_author": comment["author_username"],
                    "comment_likes": comment["likes"],
                    "context": comment["text"][:200],
                    "quality_score": comment["quality_score"],
                    "discovered_at": comment["created_at"]
                })
        
        logger.info(f"✅ Extracted {len(project_mentions)} project mentions from comments")
        return project_mentions
    
    def mine_hot_tweets_comments(self, hours: int = 6, min_engagement: int = 100) -> List[Dict]:
        """挖掘热门推文的评论区
        
        Args:
            hours: 过去N小时
            min_engagement: 最小互动数
            
        Returns:
            所有发现的项目提及
        """
        logger.info(f"🔍 Mining comment sections from hot tweets (last {hours} hours)...")
        
        # 1. 搜索高互动的加密相关推文
        query = "(crypto OR web3 OR DeFi OR NFT) min_faves:" + str(min_engagement)
        
        try:
            hot_tweets = self.search_recent_tweets(
                query=query,
                max_results=50,
                hours=hours
            )
            
            logger.info(f"📊 Found {len(hot_tweets)} hot tweets")
            
            # 2. 挖掘每条推文的评论区
            all_mentions = []
            
            for tweet in hot_tweets[:20]:  # 限制处理前20条，避免API限流
                mentions = self.mine_comment_section(tweet["tweet_id"])
                all_mentions.extend(mentions)
            
            logger.info(f"✅ Total project mentions from comments: {len(all_mentions)}")
            return all_mentions
            
        except Exception as e:
            logger.error(f"Error mining hot tweets comments: {e}")
            return []
    
    def calculate_topic_heat(self, topic: str, time_window: int = 24) -> Dict:
        """计算话题热度
        
        Args:
            topic: 话题或项目名称
            time_window: 时间窗口（小时）
            
        Returns:
            热度数据
        """
        try:
            # 搜索该话题的推文
            tweets = self.search_recent_tweets(
                query=topic,
                max_results=100,
                hours=time_window
            )
            
            mention_count = len(tweets)
            
            # 计算KOL参与度
            kol_count = sum(1 for t in tweets if t.get("author_followers", 0) > 10000)
            
            # 计算平均互动数
            if tweets:
                avg_engagement = sum(
                    t.get("likes", 0) + t.get("retweets", 0) + t.get("replies", 0)
                    for t in tweets
                ) / len(tweets)
            else:
                avg_engagement = 0
            
            # 计算热度分（0-100）
            heat_score = min(100, (
                min(50, mention_count / 10) +  # 提及数
                min(30, kol_count * 6) +  # KOL参与
                min(20, avg_engagement / 50)  # 平均互动
            ))
            
            return {
                "topic": topic,
                "mention_count": mention_count,
                "kol_count": kol_count,
                "avg_engagement": int(avg_engagement),
                "heat_score": int(heat_score),
                "is_trending": heat_score > 70,
                "checked_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error calculating topic heat for {topic}: {e}")
            return {
                "topic": topic,
                "heat_score": 0,
                "error": str(e)
            }
    
    def collect_and_extract(self, hours: int = 1) -> List[Dict]:
        """采集推文并提取项目信息（增强版）
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            项目信息列表
        """
        logger.info(f"🔍 Starting enhanced Twitter collection (last {hours} hours)...")
        
        # 1. 监控关键词
        keyword_tweets = self.monitor_keywords(hours=hours)
        
        # 2. 追踪KOL
        kol_tweets = self.track_all_kols()
        
        # 3. 挖掘评论区（新功能）
        comment_mentions = self.mine_hot_tweets_comments(hours=hours*6, min_engagement=100)
        
        # 4. 合并去重
        all_tweets = keyword_tweets + kol_tweets
        unique_tweets = {tweet["tweet_id"]: tweet for tweet in all_tweets}
        
        logger.info(f"📊 Collected {len(unique_tweets)} unique tweets")
        logger.info(f"💬 Found {len(comment_mentions)} project mentions from comments")
        
        # 5. 提取项目信息
        projects = []
        for tweet in unique_tweets.values():
            project_info = self.extract_project_info(tweet)
            if project_info:
                project_info["source_type"] = "tweet"
                projects.append(project_info)
        
        # 6. 添加评论区发现的项目
        for mention in comment_mentions:
            projects.append({
                "project_name": mention["project_name"],
                "discovered_at": mention["discovered_at"],
                "source": "twitter_comment",
                "source_type": "comment",
                "context": mention["context"],
                "quality_score": mention["quality_score"]
            })
        
        logger.info(f"✅ Extracted {len(projects)} potential projects (tweets + comments)")
        return projects


# 全局采集器实例
twitter_collector = TwitterCollector()

