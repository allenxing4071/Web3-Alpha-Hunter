"""AI数据补全服务 - 智能推断和搜索缺失字段"""

import re
from typing import Dict, Optional
from loguru import logger
from app.services.analyzers import ai_analyzer


class DataEnricher:
    """数据增强器 - 使用AI和搜索引擎补全缺失字段"""
    
    def __init__(self):
        """初始化数据增强器"""
        logger.info("✅ DataEnricher initialized")
    
    def enrich_project(self, project_data: Dict) -> Dict:
        """补全项目所有缺失字段
        
        Args:
            project_data: 项目数据字典，包含name, description等
            
        Returns:
            增强后的项目数据，补全了blockchain, category, website, social等字段
        """
        logger.info(f"🔍 Enriching project: {project_data.get('name', 'Unknown')}")
        
        enriched = project_data.copy()
        
        # 1. 使用AI推断缺失字段
        ai_inferred = self.ai_infer_missing_fields(project_data)
        
        # 2. 从描述中提取社交链接
        social_links = self.extract_social_links_from_text(
            project_data.get('description', '')
        )
        
        # 3. 合并结果（原有数据优先）
        for key, value in ai_inferred.items():
            if not enriched.get(key) and value:
                enriched[key] = value
        
        for key, value in social_links.items():
            if not enriched.get(key) and value:
                enriched[key] = value
        
        logger.info(f"✅ Enrichment complete for {enriched.get('name')}")
        return enriched
    
    def ai_infer_missing_fields(self, project_data: Dict) -> Dict:
        """使用AI推断缺失字段
        
        Args:
            project_data: 包含name和description的项目数据
            
        Returns:
            推断出的字段字典 {blockchain, category, twitter, website等}
        """
        name = project_data.get('name', 'Unknown')
        description = project_data.get('description', '')
        
        if not description or description == 'N/A':
            logger.warning(f"⚠️ No description for {name}, skipping AI inference")
            return {}
        
        # 构建AI提示词
        prompt = f"""分析以下Web3项目信息，推断缺失的字段：

项目名称: {name}
项目描述: {description}

请推断并返回JSON格式（只返回JSON，不要其他内容）：
{{
    "blockchain": "主要运行的区块链平台(Ethereum/Solana/BSC/Polygon/Arbitrum/Base/Avalanche等，如果无法确定则为null)",
    "category": "项目分类(DeFi/NFT/GameFi/Infrastructure/DAO/Layer2/Bridge等，如果无法确定则为null)",
    "twitter": "可能的Twitter账号(格式@username，如果无法确定则为null)",
    "website": "可能的官网域名(完整URL，如果无法确定则为null)"
}}

推断规则：
1. blockchain: 从描述中识别区块链关键词(如"on Ethereum", "Solana-based", "multi-chain"等)
2. category: 从功能描述判断(如"DEX"→DeFi, "NFT marketplace"→NFT, "play-to-earn"→GameFi)
3. twitter: 如果描述中有@username或twitter.com/username，提取出来
4. website: 如果描述中有域名，提取第一个
"""
        
        try:
            # 调用AI分析
            if not ai_analyzer.active_provider:
                logger.warning("⚠️ No AI provider available, skipping inference")
                return {}
            
            # 使用AI客户端
            client = None
            model = None
            
            if ai_analyzer.active_provider == "deepseek":
                client = ai_analyzer.deepseek_client
                model = "deepseek-chat"
            elif ai_analyzer.active_provider == "claude":
                client = ai_analyzer.claude_client
                model = "claude-3-5-sonnet-20241022"
            elif ai_analyzer.active_provider == "openai":
                client = ai_analyzer.openai_client
                model = "gpt-4o-mini"
            
            if not client:
                return {}
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个Web3项目数据分析专家，擅长从描述中推断项目信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 提取JSON
            import json
            # 尝试直接解析
            try:
                result = json.loads(result_text)
            except:
                # 如果失败，尝试提取JSON部分
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    logger.warning(f"⚠️ Failed to parse AI response: {result_text[:100]}")
                    return {}
            
            # 验证并清理结果
            inferred = {}
            if result.get('blockchain') and result['blockchain'] != 'null':
                inferred['blockchain'] = result['blockchain']
            if result.get('category') and result['category'] != 'null':
                inferred['category'] = result['category']
            if result.get('twitter') and result['twitter'] != 'null':
                inferred['twitter'] = result['twitter']
            if result.get('website') and result['website'] != 'null':
                inferred['website'] = result['website']
            
            logger.info(f"🤖 AI inferred fields: {inferred}")
            return inferred
            
        except Exception as e:
            logger.error(f"❌ AI inference failed: {e}")
            return {}
    
    def extract_social_links_from_text(self, text: str) -> Dict:
        """从文本中提取社交链接
        
        Args:
            text: 项目描述或其他文本
            
        Returns:
            提取出的社交链接字典
        """
        if not text:
            return {}
        
        links = {}
        
        # 提取Twitter
        twitter_patterns = [
            r'twitter\.com/([a-zA-Z0-9_]+)',
            r'x\.com/([a-zA-Z0-9_]+)',
            r'@([a-zA-Z0-9_]+)',  # 直接的@username
        ]
        for pattern in twitter_patterns:
            match = re.search(pattern, text)
            if match:
                username = match.group(1)
                if username and len(username) > 2:  # 过滤掉太短的
                    links['twitter'] = f"@{username}" if not username.startswith('@') else username
                    break
        
        # 提取Telegram
        telegram_patterns = [
            r't\.me/([a-zA-Z0-9_]+)',
            r'telegram\.me/([a-zA-Z0-9_]+)',
        ]
        for pattern in telegram_patterns:
            match = re.search(pattern, text)
            if match:
                channel = match.group(1)
                links['telegram'] = f"@{channel}" if not channel.startswith('@') else channel
                break
        
        # 提取Discord
        discord_pattern = r'discord\.gg/([a-zA-Z0-9]+)'
        match = re.search(discord_pattern, text)
        if match:
            links['discord'] = f"https://discord.gg/{match.group(1)}"
        
        # 提取网站（http/https链接）
        website_pattern = r'https?://(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
        match = re.search(website_pattern, text)
        if match:
            links['website'] = match.group(0)
        
        return links
    
    def extract_blockchain_from_description(self, description: str) -> Optional[str]:
        """从描述中提取区块链平台
        
        Args:
            description: 项目描述
            
        Returns:
            区块链名称或None
        """
        if not description:
            return None
        
        desc_lower = description.lower()
        
        # 区块链关键词映射
        blockchain_keywords = {
            'Ethereum': ['ethereum', 'eth', 'erc-20', 'erc20', 'erc-721', 'evm'],
            'Solana': ['solana', 'sol', 'spl'],
            'BSC': ['bsc', 'binance smart chain', 'bnb chain', 'bep-20'],
            'Polygon': ['polygon', 'matic'],
            'Arbitrum': ['arbitrum', 'arb'],
            'Optimism': ['optimism', 'op mainnet'],
            'Base': ['base chain', 'base network'],
            'Avalanche': ['avalanche', 'avax'],
            'Sui': ['sui network', 'sui blockchain'],
            'Aptos': ['aptos'],
        }
        
        for blockchain, keywords in blockchain_keywords.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    return blockchain
        
        return None
    
    def extract_category_from_description(self, description: str) -> Optional[str]:
        """从描述中提取项目分类
        
        Args:
            description: 项目描述
            
        Returns:
            分类名称或None
        """
        if not description:
            return None
        
        desc_lower = description.lower()
        
        # 分类关键词映射
        category_keywords = {
            'DeFi': ['defi', 'dex', 'swap', 'liquidity', 'lending', 'staking', 'yield', 'amm'],
            'NFT': ['nft', 'non-fungible', 'collectible', 'digital art', 'pfp'],
            'GameFi': ['gamefi', 'play-to-earn', 'p2e', 'game', 'metaverse'],
            'Infrastructure': ['infrastructure', 'protocol', 'layer', 'blockchain', 'network'],
            'DAO': ['dao', 'governance', 'decentralized autonomous'],
            'Bridge': ['bridge', 'cross-chain', 'interoperability'],
            'Launchpad': ['launchpad', 'ido', 'initial dex offering'],
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    return category
        
        return None


# 全局实例
data_enricher = DataEnricher()
