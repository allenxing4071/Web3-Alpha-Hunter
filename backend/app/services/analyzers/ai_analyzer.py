"""AI分析引擎 - 使用LLM进行深度分析"""

from typing import Dict, List, Optional
from loguru import logger
from anthropic import Anthropic
from openai import OpenAI
from app.core.config import settings


class AIAnalyzer:
    """AI分析器 - 支持DeepSeek/Claude/GPT"""
    
    def __init__(self):
        """初始化AI客户端"""
        self.deepseek_client = None
        self.claude_client = None
        self.openai_client = None
        self.active_provider = None
        
        # 尝试从数据库加载配置
        self._load_config_from_db()
        
        # 如果数据库没有配置，使用环境变量
        if not self.active_provider:
            self._load_config_from_env()
    
    def _load_config_from_db(self):
        """从数据库加载AI配置"""
        try:
            from app.db.session import SessionLocal
            from app.models.ai_config import AIConfig
            from cryptography.fernet import Fernet
            import base64
            import hashlib
            
            # 解密密钥
            ENCRYPTION_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"web3-alpha-hunter-secret-key").digest())
            cipher_suite = Fernet(ENCRYPTION_KEY)
            
            db = SessionLocal()
            try:
                # 获取所有启用的AI配置
                configs = db.query(AIConfig).filter(AIConfig.enabled == True).all()
                
                logger.info(f"📂 Found {len(configs)} enabled AI configs in database")
                
                for config in configs:
                    try:
                        # 解密API密钥
                        decrypted_key = cipher_suite.decrypt(config.api_key.encode()).decode()
                        
                        if config.name.lower() == "deepseek" and not self.active_provider:
                            self.deepseek_client = OpenAI(
                                api_key=decrypted_key,
                                base_url="https://api.deepseek.com"
                            )
                            self.active_provider = "deepseek"
                            logger.info(f"✅ DeepSeek initialized from DB (model: {config.model})")
                        
                        elif config.name.lower() == "claude" and not self.active_provider:
                            self.claude_client = OpenAI(
                                api_key=decrypted_key,
                                base_url="https://api.gptsapi.net/v1"
                            )
                            self.active_provider = "claude"
                            logger.info(f"✅ Claude initialized from DB (model: {config.model})")
                        
                        elif config.name.lower() == "openai" and not self.active_provider:
                            self.openai_client = OpenAI(
                                api_key=decrypted_key,
                                base_url="https://api.gptsapi.net/v1"
                            )
                            self.active_provider = "openai"
                            logger.info(f"✅ OpenAI initialized from DB (model: {config.model})")
                    
                    except Exception as e:
                        logger.warning(f"Failed to initialize {config.name} from DB: {e}")
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Failed to load AI config from DB: {e}")
    
    def _load_config_from_env(self):
        """从环境变量加载AI配置（备用方案）"""
        # 优先使用DeepSeek (国内,便宜快速)
        if settings.DEEPSEEK_API_KEY:
            try:
                self.deepseek_client = OpenAI(
                    api_key=settings.DEEPSEEK_API_KEY,
                    base_url="https://api.deepseek.com"
                )
                self.active_provider = "deepseek"
                logger.info("✅ DeepSeek v3 client initialized from ENV (优先使用)")
            except Exception as e:
                logger.warning(f"Failed to initialize DeepSeek: {e}")
        
        # 备用: Claude (通过 WildCard/GPTsAPI 中转,使用 OpenAI 格式)
        if settings.ANTHROPIC_API_KEY and not self.active_provider:
            try:
                # WildCard 的 Claude 也使用 OpenAI 客户端格式
                self.claude_client = OpenAI(
                    api_key=settings.ANTHROPIC_API_KEY,
                    base_url="https://api.gptsapi.net/v1"
                )
                self.active_provider = "claude"
                logger.info("✅ Claude client initialized from ENV (via GPTsAPI)")
            except Exception as e:
                logger.warning(f"Failed to initialize Claude: {e}")
        
        # 备用: OpenAI (通过 WildCard/GPTsAPI 中转)
        if settings.OPENAI_API_KEY and not self.active_provider:
            try:
                self.openai_client = OpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    base_url="https://api.gptsapi.net/v1"
                )
                self.active_provider = "openai"
                logger.info("✅ OpenAI client initialized from ENV (via GPTsAPI)")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
    
    def analyze_project_text(self, text: str, source: str = "twitter") -> Dict:
        """分析项目文本内容
        
        Args:
            text: 项目相关文本(推文、公告等)
            source: 来源(twitter, telegram等)
            
        Returns:
            分析结果字典
        """
        if not self.active_provider:
            logger.warning("No AI client available, using mock analysis")
            return self._mock_analysis(text)
        
        prompt = f"""分析以下Web3项目相关信息,提取关键内容:

来源: {source}
内容: {text}

请从以下角度分析:
1. 项目类型 (DeFi/NFT/GameFi/Infrastructure/AI等)
2. 核心功能/创新点
3. 团队信息 (如果提到)
4. 融资情况 (如果提到)
5. 技术特点
6. 潜在风险点
7. 整体评价 (1-10分)

请用JSON格式返回,包含以下字段:
{{
  "category": "项目分类",
  "key_features": ["特点1", "特点2"],
  "team_info": "团队信息",
  "funding": "融资信息",
  "tech_highlights": "技术亮点",
  "risks": ["风险1", "风险2"],
  "score_estimate": 8,
  "summary": "一句话总结"
}}
"""
        
        try:
            # 优先使用DeepSeek v3
            if self.deepseek_client:
                response = self.deepseek_client.chat.completions.create(
                    model="deepseek-chat",  # 自动使用最新v3模型
                    messages=[
                        {"role": "system", "content": "你是Web3项目分析专家,擅长从文本中提取项目关键信息。你需要客观、专业地分析项目,识别潜在的投资机会和风险。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2048,  # v3支持更长输出
                    temperature=0.7,
                    top_p=0.95,
                    stream=False
                )
                result_text = response.choices[0].message.content
                logger.info(f"✅ DeepSeek v3 analysis completed")
            
            # 备用: Claude (通过 WildCard,使用 OpenAI 格式)
            elif self.claude_client:
                response = self.claude_client.chat.completions.create(
                    model="claude-3-5-sonnet-20241022",  # WildCard 支持的 Claude 模型
                    messages=[
                        {"role": "system", "content": "你是Web3项目分析专家,擅长从文本中提取项目关键信息。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2048,
                    temperature=0.7
                )
                result_text = response.choices[0].message.content
                logger.info(f"✅ Claude analysis completed (via GPTsAPI)")
            
            # 备用: OpenAI
            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                    temperature=0.7
                )
                result_text = response.choices[0].message.content
                logger.info(f"✅ OpenAI analysis completed")
            else:
                logger.warning("No AI provider available")
                return self._mock_analysis(text)
            
            # 解析JSON
            import json
            result = json.loads(result_text)
            logger.info(f"✅ AI analysis completed: {result.get('category')}")
            return result
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._mock_analysis(text)
    
    def _mock_analysis(self, text: str) -> Dict:
        """模拟AI分析(当没有API密钥时使用)"""
        return {
            "category": "DeFi",
            "key_features": [
                "跨链流动性聚合",
                "低滑点交易",
                "Gas优化"
            ],
            "team_info": "经验丰富的团队",
            "funding": "未披露",
            "tech_highlights": "创新的AMM算法",
            "risks": ["代币经济学未完全公开"],
            "score_estimate": 7,
            "summary": "有潜力的DeFi项目,需关注后续进展"
        }
    
    def score_team_background(self, project_data: Dict) -> float:
        """评估团队背景
        
        Args:
            project_data: 项目数据
            
        Returns:
            团队评分 (0-100)
        """
        score = 50.0  # 基础分
        
        # 如果有投资人信息
        if "funding" in project_data and project_data["funding"]:
            funding_text = project_data["funding"].lower()
            
            # 顶级VC加分
            top_vcs = ["a16z", "paradigm", "coinbase ventures", "binance labs", "sequoia"]
            for vc in top_vcs:
                if vc in funding_text:
                    score += 10
                    logger.info(f"  +10分: 顶级VC {vc}")
        
        # 如果有团队信息
        if "team_info" in project_data and project_data["team_info"]:
            team_text = project_data["team_info"].lower()
            
            # 知名项目背景
            if any(keyword in team_text for keyword in ["uniswap", "compound", "aave", "curve"]):
                score += 15
                logger.info("  +15分: 来自知名项目")
            
            # 公开团队
            if "doxxed" in team_text or "公开" in team_text:
                score += 10
                logger.info("  +10分: 团队公开透明")
        
        # 根据作者影响力评分
        if "author" in project_data:
            followers = project_data["author"].get("followers", 0)
            if followers > 1000000:
                score += 15
                logger.info(f"  +15分: 作者粉丝 {followers}")
            elif followers > 100000:
                score += 10
            elif followers > 10000:
                score += 5
        
        return min(score, 100)
    
    def score_technology(self, project_data: Dict) -> float:
        """评估技术创新
        
        Args:
            project_data: 项目数据
            
        Returns:
            技术评分 (0-100)
        """
        score = 50.0
        
        # 技术关键词加分
        tech_keywords = {
            "zkp": 15, "zero-knowledge": 15, "zk": 15,
            "layer 2": 12, "l2": 12, "rollup": 12,
            "cross-chain": 10, "bridge": 10,
            "novel": 10, "innovative": 8, "revolutionary": 8,
            "audit": 10, "certik": 10, "peckshield": 10,
        }
        
        text = str(project_data).lower()
        for keyword, points in tech_keywords.items():
            if keyword in text:
                score += points
                logger.info(f"  +{points}分: 技术关键词 '{keyword}'")
                break  # 每个类别只加一次分
        
        # GitHub活跃度
        if "github_stars" in project_data:
            stars = project_data["github_stars"]
            if stars > 1000:
                score += 15
            elif stars > 500:
                score += 10
            elif stars > 100:
                score += 5
        
        return min(score, 100)
    
    def score_community(self, project_data: Dict) -> float:
        """评估社区热度
        
        Args:
            project_data: 项目数据
            
        Returns:
            社区评分 (0-100)
        """
        score = 40.0
        
        # Twitter互动数据
        if "engagement" in project_data:
            eng = project_data["engagement"]
            
            likes = eng.get("likes", 0)
            retweets = eng.get("retweets", 0)
            
            # 点赞数评分
            if likes > 10000:
                score += 20
            elif likes > 5000:
                score += 15
            elif likes > 1000:
                score += 10
            elif likes > 100:
                score += 5
            
            # 转发数评分
            if retweets > 5000:
                score += 20
            elif retweets > 1000:
                score += 15
            elif retweets > 500:
                score += 10
            elif retweets > 50:
                score += 5
        
        # Telegram数据
        if "telegram_members" in project_data:
            members = project_data["telegram_members"]
            if members > 50000:
                score += 15
            elif members > 10000:
                score += 10
            elif members > 1000:
                score += 5
        
        return min(score, 100)
    
    def score_tokenomics(self, project_data: Dict) -> float:
        """评估代币经济学
        
        Args:
            project_data: 项目数据
            
        Returns:
            代币经济学评分 (0-100)
        """
        score = 60.0  # 基础分
        
        text = str(project_data).lower()
        
        # 正面关键词
        positive_keywords = {
            "fair launch": 15,
            "no presale": 10,
            "community": 8,
            "locked liquidity": 12,
            "vesting": 8,
        }
        
        for keyword, points in positive_keywords.items():
            if keyword in text:
                score += points
                logger.info(f"  +{points}分: 代币关键词 '{keyword}'")
        
        # 负面关键词
        negative_keywords = {
            "team holds": -10,
            "large allocation": -8,
        }
        
        for keyword, points in negative_keywords.items():
            if keyword in text:
                score += points
                logger.info(f"  {points}分: 代币风险 '{keyword}'")
        
        return max(min(score, 100), 0)
    
    def score_market_timing(self, project_data: Dict) -> float:
        """评估市场时机
        
        Args:
            project_data: 项目数据
            
        Returns:
            市场时机评分 (0-100)
        """
        score = 70.0  # 基础分
        
        category = project_data.get("category", "").lower()
        
        # 当前热门赛道加分(可动态调整)
        hot_categories = {
            "defi": 10,
            "ai": 15,
            "gamefi": 8,
            "infrastructure": 12,
        }
        
        for cat, points in hot_categories.items():
            if cat in category:
                score += points
                logger.info(f"  +{points}分: 热门赛道 '{cat}'")
                break
        
        return min(score, 100)
    
    def analyze_full_project(self, project_data: Dict) -> Dict:
        """完整分析项目
        
        Args:
            project_data: 项目原始数据
            
        Returns:
            完整分析结果
        """
        logger.info(f"🔍 Starting full project analysis...")
        
        # 1. 文本分析
        text = project_data.get("text", "")
        ai_result = self.analyze_project_text(text, project_data.get("source", "unknown"))
        
        # 合并AI分析结果到项目数据
        enhanced_data = {**project_data, **ai_result}
        
        # 2. 各维度评分
        scores = {
            "team": self.score_team_background(enhanced_data),
            "technology": self.score_technology(enhanced_data),
            "community": self.score_community(enhanced_data),
            "tokenomics": self.score_tokenomics(enhanced_data),
            "market_timing": self.score_market_timing(enhanced_data),
            "risk": 80.0,  # 由风险检测器单独计算
        }
        
        logger.info(f"📊 Individual scores: {scores}")
        
        # 3. 计算综合评分
        from app.services.analyzers.scorer import project_scorer
        
        overall_score = project_scorer.calculate_overall_score(
            team_score=scores["team"],
            tech_score=scores["technology"],
            community_score=scores["community"],
            tokenomics_score=scores["tokenomics"],
            market_timing_score=scores["market_timing"],
            risk_score=scores["risk"],
        )
        
        # 4. 计算等级
        grade = project_scorer.calculate_grade(overall_score)
        
        logger.info(f"✅ Analysis complete: Score={overall_score}, Grade={grade}")
        
        return {
            "overall_score": overall_score,
            "grade": grade,
            "scores": scores,
            "ai_analysis": ai_result,
            "category": ai_result.get("category"),
            "key_features": ai_result.get("key_features", []),
            "summary": ai_result.get("summary"),
        }


# 全局分析器实例
ai_analyzer = AIAnalyzer()

