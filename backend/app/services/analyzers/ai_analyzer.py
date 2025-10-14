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
    
    def analyze_project_text(self, text: str, source: str = "twitter", retry_with_fallback: bool = True) -> Dict:
        """分析项目文本内容（支持自动降级到备用AI）

        Args:
            text: 项目相关文本(推文、公告等)
            source: 来源(twitter, telegram等)
            retry_with_fallback: 失败时是否自动尝试其他AI提供商

        Returns:
            分析结果字典
        """
        if not self.active_provider:
            logger.warning("No AI client available, using mock analysis")
            return self._mock_analysis(text)

        prompt = f"""分析以下Web3项目相关信息,提供专业评估:

来源: {source}
内容: {text}

请分析并评分(0-100分制):
1. 项目类型/分类
2. 团队实力 (team_score)
3. 技术创新 (tech_score)  
4. 社区活跃度 (community_score)
5. 代币经济学 (tokenomics_score)
6. 市场时机 (market_timing_score)
7. 风险评估 (risk_score, 越低越好)

返回JSON格式(必须包含所有字段):
{{
  "category": "DeFi/NFT/GameFi/Infrastructure/AI/Layer2",
  "overall_score": 75.0,
  "team_score": 70.0,
  "tech_score": 80.0,
  "community_score": 75.0,
  "tokenomics_score": 70.0,
  "market_timing_score": 80.0,
  "risk_score": 30.0,
  "grade": "A",
  "reasoning": "分析理由",
  "key_features": ["特点1", "特点2"],
  "risks": ["风险1"],
  "summary": "一句话总结"
}}

评分规则: overall_score>=90为S级, >=80为A级, >=70为B级, >=60为C级, <60为D级
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
            
            # 解析JSON（处理Markdown代码块）
            import json
            import re
            
            # 移除可能的Markdown代码块标记
            if "```json" in result_text:
                # 提取```json和```之间的内容
                match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
                if match:
                    result_text = match.group(1)
            elif "```" in result_text:
                # 提取```和```之间的内容
                match = re.search(r'```\s*(.*?)\s*```', result_text, re.DOTALL)
                if match:
                    result_text = match.group(1)
            
            result_text = result_text.strip()
            
            # 尝试解析JSON
            try:
                result = json.loads(result_text)
                logger.info(f"✅ AI analysis completed: {result.get('category', 'Unknown')}")
                return result
            except json.JSONDecodeError as je:
                logger.error(f"JSON解析失败: {je}")
                logger.error(f"原始响应: {result_text[:500]}")
                # 如果JSON解析失败，尝试从文本中提取信息
                return self._extract_from_text(result_text, text)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._mock_analysis(text)
    
    def _extract_from_text(self, ai_response: str, original_text: str) -> Dict:
        """从AI文本响应中提取结构化信息"""
        # 基础结构
        result = {
            "category": "Unknown",
            "key_features": [],
            "team_info": "",
            "funding": "",
            "tech_highlights": "",
            "risks": [],
            "score_estimate": 5,
            "summary": ai_response[:200] if ai_response else "AI分析失败",
            "overall_score": 50.0,
            "team_score": 50.0,
            "tech_score": 50.0,
            "community_score": 50.0,
            "tokenomics_score": 50.0,
            "market_timing_score": 50.0,
            "risk_score": 50.0,
            "grade": "C",
            "reasoning": ai_response[:500] if ai_response else "无法生成分析"
        }
        
        # 尝试从文本中提取分类
        categories = ["DeFi", "NFT", "GameFi", "Infrastructure", "AI", "Layer2", "DEX"]
        for cat in categories:
            if cat.lower() in ai_response.lower() or cat.lower() in original_text.lower():
                result["category"] = cat
                break
        
        return result
    
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
    
    def generate_detailed_analysis(self, project_data: Dict) -> Dict:
        """生成详细AI分析（基于真实数据，避免虚假信息）

        Args:
            project_data: 项目完整数据（包含真实指标）

        Returns:
            详细分析结果（summary, key_features, investment_suggestion等）
        """
        logger.info(f"🔍 Generating detailed AI analysis for {project_data.get('name', 'Unknown')}...")

        if not self.active_provider:
            logger.warning("No AI client available")
            return self._mock_detailed_analysis()

        # 构建基于真实数据的prompt
        project_name = project_data.get("name", "Unknown")
        description = project_data.get("description", "无描述")
        category = project_data.get("category", "Unknown")
        blockchain = project_data.get("blockchain", "Unknown")

        # 提取真实指标
        metrics = project_data.get("metrics", {})
        twitter_followers = metrics.get("twitter_followers", 0)
        telegram_members = metrics.get("telegram_members", 0)
        github_stars = metrics.get("github_stars", 0)

        # 评分数据（如果有）
        scores = project_data.get("scores", {})
        overall_score = scores.get("overall", 0)

        prompt = f"""你是Web3项目分析专家。请基于以下**真实数据**分析项目，严禁编造任何不存在的信息。

**项目信息（真实数据）：**
- 项目名称: {project_name}
- 分类: {category}
- 区块链: {blockchain}
- 描述: {description}

**社交媒体数据（真实指标）：**
- Twitter粉丝: {twitter_followers if twitter_followers > 0 else "未知"}
- Telegram成员: {telegram_members if telegram_members > 0 else "未知"}
- GitHub Stars: {github_stars if github_stars > 0 else "未知"}

**评分：**
- 综合评分: {overall_score}/100

**分析要求（必须遵守）：**
1. 只基于上述真实数据进行分析
2. 如果某项数据缺失，明确说明"数据不足"，不要编造
3. 技术特性只描述该项目类型的通用特征，不编造具体技术细节
4. 投资建议要保守谨慎，强调风险

请返回JSON格式（严格遵守格式）：
{{
  "summary": "100-150字的项目摘要，只基于已知信息",
  "key_features": [
    "特性1（基于真实类型特征）",
    "特性2",
    "特性3",
    "特性4",
    "特性5"
  ],
  "investment_suggestion": {{
    "action": "投资建议文字（80-120字，强调风险和数据不足）",
    "position_size": "建议仓位（如：1-3%）",
    "entry_timing": "入场时机建议",
    "stop_loss": 止损百分比数字（如：25）
  }}
}}

**重要提醒：不要编造团队成员、融资信息、合作伙伴等未提供的数据！**"""

        try:
            # 调用AI（优先DeepSeek）
            if self.deepseek_client:
                response = self.deepseek_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是专业的Web3分析师。你必须只基于提供的真实数据进行分析，严禁编造任何信息。如果数据不足，必须明确说明。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2048,
                    temperature=0.3,  # 降低温度，减少创造性，增加准确性
                    top_p=0.9,
                    stream=False
                )
                result_text = response.choices[0].message.content
                logger.info(f"✅ DeepSeek detailed analysis generated")

            elif self.claude_client:
                response = self.claude_client.chat.completions.create(
                    model="claude-3-5-sonnet-20241022",
                    messages=[
                        {"role": "system", "content": "你是专业的Web3分析师。必须只基于真实数据分析，不编造信息。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2048,
                    temperature=0.3
                )
                result_text = response.choices[0].message.content
                logger.info(f"✅ Claude detailed analysis generated")

            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是专业的Web3分析师。只基于真实数据分析。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.3
                )
                result_text = response.choices[0].message.content
                logger.info(f"✅ OpenAI detailed analysis generated")
            else:
                logger.warning("No AI provider available")
                return self._mock_detailed_analysis()

            # 解析JSON
            import json
            import re

            # 移除Markdown代码块
            if "```json" in result_text:
                match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
                if match:
                    result_text = match.group(1)
            elif "```" in result_text:
                match = re.search(r'```\s*(.*?)\s*```', result_text, re.DOTALL)
                if match:
                    result_text = match.group(1)

            result_text = result_text.strip()
            result = json.loads(result_text)

            logger.info(f"✅ Detailed analysis parsed successfully")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to generate detailed analysis: {e}")
            return self._mock_detailed_analysis()

    def _mock_detailed_analysis(self) -> Dict:
        """模拟详细分析（当AI不可用时）"""
        return {
            "summary": "暂无详细分析摘要，AI服务不可用",
            "key_features": [
                "数据采集中",
                "分析生成中",
                "请稍后查看"
            ],
            "investment_suggestion": {
                "action": "数据不足，暂无投资建议",
                "position_size": "0%",
                "entry_timing": "等待更多数据",
                "stop_loss": 0
            }
        }

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

