"""Medium数据采集服务"""

import re
import feedparser
import requests
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from bs4 import BeautifulSoup


class MediumCollector:
    """Medium数据采集器"""
    
    # RSS订阅源
    RSS_SOURCES = [
        # 顶级作者
        "https://medium.com/feed/@VitalikButerin",
        "https://medium.com/feed/@coinbase",
        
        # 标签订阅
        "https://medium.com/feed/tag/web3",
        "https://medium.com/feed/tag/defi",
        "https://medium.com/feed/tag/cryptocurrency",
        "https://medium.com/feed/tag/blockchain",
    ]
    
    def __init__(self):
        """初始化采集器"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        logger.info("✅ Medium Collector initialized")
    
    def collect_from_rss(self, rss_url: str, max_results: int = 20) -> List[Dict]:
        """从RSS源采集文章
        
        Args:
            rss_url: RSS订阅地址
            max_results: 最大结果数
            
        Returns:
            文章列表
        """
        try:
            feed = feedparser.parse(rss_url)
            
            articles = []
            for entry in feed.entries[:max_results]:
                article = {
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "author": entry.get("author", ""),
                    "published": entry.get("published_parsed"),
                    "summary": entry.get("summary", ""),
                    "tags": [tag.term for tag in entry.get("tags", [])],
                    "source": "rss",
                    "rss_url": rss_url
                }
                
                # 检查是否Web3相关
                if self.is_web3_related(article):
                    articles.append(article)
            
            logger.info(f"✅ Collected {len(articles)} articles from RSS")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from RSS {rss_url}: {e}")
            return []
    
    def is_web3_related(self, article: Dict) -> bool:
        """判断文章是否Web3相关"""
        text = (article.get("title", "") + " " + article.get("summary", "")).lower()
        
        keywords = [
            "web3", "crypto", "blockchain", "defi", "nft",
            "dao", "ethereum", "solana", "layer2", "rollup",
            "metaverse", "gamefi", "socialfi"
        ]
        
        return any(keyword in text for keyword in keywords)
    
    def scrape_article(self, url: str) -> Optional[Dict]:
        """爬取文章全文
        
        Args:
            url: 文章URL
            
        Returns:
            文章数据
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title_tag = soup.find('h1')
            title = title_tag.text if title_tag else ""
            
            # 提取作者
            author_tag = soup.find('a', {'rel': 'author'})
            if not author_tag:
                author_tag = soup.find('a', {'data-action': 'show-user-card'})
            author = author_tag.text if author_tag else ""
            
            # 提取发布时间
            time_tag = soup.find('time')
            published = time_tag['datetime'] if time_tag and 'datetime' in time_tag.attrs else None
            
            # 提取正文
            article_body = soup.find('article')
            if article_body:
                paragraphs = article_body.find_all('p')
                full_text = '\n\n'.join([p.text for p in paragraphs])
            else:
                full_text = ""
            
            # 提取统计数据
            claps = self.extract_claps(soup)
            
            # 提取提及的项目
            mentioned_projects = self.extract_project_names(full_text)
            
            return {
                "url": url,
                "title": title,
                "author": author,
                "published": published,
                "full_text": full_text,
                "word_count": len(full_text.split()),
                "claps": claps,
                "mentioned_projects": mentioned_projects,
                "scraped_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    def extract_claps(self, soup) -> int:
        """提取拍手数"""
        try:
            clap_button = soup.find('button', {'data-action': 'show-recommends'})
            if clap_button:
                clap_text = clap_button.text
                # 提取数字
                numbers = re.findall(r'\d+', clap_text)
                if numbers:
                    # 处理K, M等单位
                    if 'K' in clap_text:
                        return int(float(numbers[0]) * 1000)
                    elif 'M' in clap_text:
                        return int(float(numbers[0]) * 1000000)
                    else:
                        return int(numbers[0])
            return 0
        except:
            return 0
    
    def extract_project_names(self, text: str) -> List[str]:
        """从文本中提取项目名称"""
        projects = []
        
        # 正则匹配大写开头的词组
        pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        matches = re.findall(pattern, text)
        projects.extend(matches)
        
        # 去重和清洗
        projects = list(set([p.strip() for p in projects if len(p) > 2]))
        
        # 过滤常见词汇
        noise_words = [
            "The", "This", "That", "Medium", "Twitter", "Facebook",
            "Google", "Apple", "Microsoft", "Amazon"
        ]
        projects = [p for p in projects if p not in noise_words]
        
        # 限制数量
        return projects[:50]
    
    def analyze_article(self, article: Dict) -> Dict:
        """分析文章（使用AI）
        
        Args:
            article: 文章数据
            
        Returns:
            分析结果
        """
        # TODO: 集成AI分析
        
        text = article.get("full_text", "")
        
        # 简单的关键词分析
        article_type = "General"
        if any(kw in text.lower() for kw in ["technical", "architecture", "protocol"]):
            article_type = "Technical"
        elif any(kw in text.lower() for kw in ["investment", "valuation", "token"]):
            article_type = "Investment"
        elif any(kw in text.lower() for kw in ["update", "progress", "milestone"]):
            article_type = "Update"
        
        # 计算重要性
        importance = self.calculate_importance(article)
        
        return {
            "article_url": article["url"],
            "article_type": article_type,
            "mentioned_projects": article.get("mentioned_projects", []),
            "importance_score": importance,
            "has_alpha": importance > 80,
            "analyzed_at": datetime.utcnow()
        }
    
    def calculate_importance(self, article: Dict) -> int:
        """计算文章重要性（0-100）"""
        score = 0
        
        # 因子1: 拍手数（30分）
        claps = article.get("claps", 0)
        score += min(30, claps / 1000 * 30)
        
        # 因子2: 字数（20分）
        word_count = article.get("word_count", 0)
        if 1000 < word_count < 5000:
            score += 20
        elif word_count >= 5000:
            score += 15
        
        # 因子3: 作者（20分）
        author = article.get("author", "").lower()
        if "vitalik" in author or "coinbase" in author:
            score += 20
        
        # 因子4: 项目提及数量（15分）
        projects = article.get("mentioned_projects", [])
        score += min(15, len(projects) * 3)
        
        # 因子5: 发布时间（15分）
        # 越新的文章越重要
        published = article.get("published")
        if published:
            try:
                pub_time = datetime(*published[:6]) if isinstance(published, tuple) else datetime.fromisoformat(published)
                age_hours = (datetime.utcnow() - pub_time).total_seconds() / 3600
                if age_hours < 24:
                    score += 15
                elif age_hours < 72:
                    score += 10
                elif age_hours < 168:
                    score += 5
            except:
                pass
        
        return min(100, int(score))
    
    def collect_all_rss_sources(self, max_articles_per_source: int = 20) -> List[Dict]:
        """采集所有RSS源
        
        Args:
            max_articles_per_source: 每个源最大文章数
            
        Returns:
            所有文章列表
        """
        logger.info(f"🔍 Collecting from {len(self.RSS_SOURCES)} RSS sources...")
        
        all_articles = []
        
        for rss_url in self.RSS_SOURCES:
            articles = self.collect_from_rss(rss_url, max_articles_per_source)
            all_articles.extend(articles)
        
        logger.info(f"✅ Collected {len(all_articles)} articles from all RSS sources")
        return all_articles
    
    def collect_and_analyze(self, scrape_full_text: bool = True) -> List[Dict]:
        """采集并分析文章
        
        Args:
            scrape_full_text: 是否爬取全文
            
        Returns:
            分析后的文章列表
        """
        logger.info("🔍 Starting Medium collection...")
        
        # 1. 从RSS采集
        articles = self.collect_all_rss_sources()
        
        # 2. 爬取全文（可选）
        if scrape_full_text:
            logger.info("📄 Scraping full text for high-priority articles...")
            
            # 只爬取前10篇（避免过度请求）
            for article in articles[:10]:
                full_article = self.scrape_article(article["url"])
                if full_article:
                    article.update(full_article)
        
        # 3. 分析文章
        analyzed_articles = []
        for article in articles:
            analysis = self.analyze_article(article)
            
            # 合并数据
            article["analysis"] = analysis
            analyzed_articles.append(article)
        
        # 4. 按重要性排序
        analyzed_articles.sort(
            key=lambda x: x["analysis"].get("importance_score", 0),
            reverse=True
        )
        
        logger.info(f"✅ Analyzed {len(analyzed_articles)} articles")
        return analyzed_articles


# 全局采集器实例
medium_collector = MediumCollector()

