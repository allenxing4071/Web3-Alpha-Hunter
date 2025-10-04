"""项目发现服务 - 从多平台数据中发现和聚合项目"""

import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from loguru import logger


class ProjectDiscoveryService:
    """项目发现服务"""
    
    def __init__(self):
        """初始化"""
        self.discovered_projects = {}
        logger.info("✅ Project Discovery Service initialized")
    
    def extract_project_names(self, text: str) -> List[str]:
        """从文本中提取项目名称（增强版）
        
        Args:
            text: 文本内容
            
        Returns:
            项目名称列表
        """
        projects = []
        
        # 方法1: 正则匹配大写开头的词组
        pattern1 = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        matches1 = re.findall(pattern1, text)
        projects.extend(matches1)
        
        # 方法2: 特定模式匹配
        patterns = [
            r'(?:check out|introducing|new project|announcing)\s+([A-Z][a-zA-Z\s]+?)(?:\.|,|$)',
            r'([A-Z][a-zA-Z]+)\s+(?:protocol|network|chain|finance|swap)',
            r'(?:protocol|network|chain)\s+([A-Z][a-zA-Z\s]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            projects.extend(matches)
        
        # 方法3: URL中提取
        urls = re.findall(r'https?://([a-zA-Z0-9-]+)\.[a-z]+', text)
        for url in urls:
            # 转换域名为项目名
            name = url.replace('-', ' ').title()
            if len(name) > 3:
                projects.append(name)
        
        # 方法4: 合约地址附近的文本
        contract_pattern = r"0x[a-fA-F0-9]{40}"
        contracts = re.findall(contract_pattern, text)
        if contracts:
            # 在合约地址前后找项目名
            for contract in contracts:
                idx = text.find(contract)
                before = text[max(0, idx-50):idx]
                after = text[idx:min(len(text), idx+50)]
                
                # 提取大写开头的词
                nearby = before + after
                names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', nearby)
                projects.extend(names)
        
        # 清洗和去重
        projects = list(set([p.strip() for p in projects if p.strip()]))
        
        # 过滤噪音
        noise_words = {
            "The", "This", "That", "These", "Those",
            "Twitter", "Discord", "Telegram", "Medium",
            "Http", "Https", "Com", "Org", "Io",
            "New", "Launch", "Project", "Protocol",
            "And", "For", "With"
        }
        
        projects = [
            p for p in projects
            if p not in noise_words and len(p) > 2 and len(p) < 50
        ]
        
        return projects
    
    def aggregate_multi_source_data(self, data_sources: Dict[str, List[Dict]]) -> List[Dict]:
        """聚合多平台数据
        
        Args:
            data_sources: 各平台数据，格式：{"twitter": [...], "telegram": [...], ...}
            
        Returns:
            聚合后的项目列表
        """
        logger.info("🔍 Aggregating multi-source data...")
        
        # 项目名称 -> 提及列表
        project_mentions = defaultdict(list)
        
        # 处理各平台数据
        for platform, items in data_sources.items():
            logger.info(f"  - Processing {platform}: {len(items)} items")
            
            for item in items:
                # 提取项目名称
                text = item.get("text", "") or item.get("content", "")
                
                if not text:
                    continue
                
                projects = self.extract_project_names(text)
                
                for project in projects:
                    project_mentions[project].append({
                        "platform": platform,
                        "source_item": item,
                        "discovered_at": item.get("created_at") or item.get("date") or datetime.utcnow(),
                        "text": text[:200]  # 保存上下文
                    })
        
        logger.info(f"📊 Found {len(project_mentions)} unique project names")
        
        # 构建项目数据
        aggregated_projects = []
        
        for project_name, mentions in project_mentions.items():
            # 按平台统计
            platform_counts = defaultdict(int)
            for mention in mentions:
                platform_counts[mention["platform"]] += 1
            
            # 跨平台一致性
            num_platforms = len(platform_counts)
            
            # 总提及数
            total_mentions = len(mentions)
            
            # 首次发现时间
            first_discovered = min(m["discovered_at"] for m in mentions)
            
            # 最近提及时间
            last_mentioned = max(m["discovered_at"] for m in mentions)
            
            # 计算初步信号强度
            signal_strength = min(100, (
                min(40, total_mentions * 5) +  # 提及数
                min(40, num_platforms * 13) +  # 跨平台
                20  # 基础分
            ))
            
            project_data = {
                "project_name": project_name,
                "total_mentions": total_mentions,
                "platform_mentions": dict(platform_counts),
                "num_platforms": num_platforms,
                "first_discovered_at": first_discovered,
                "last_mentioned_at": last_mentioned,
                "signal_strength": int(signal_strength),
                "mentions": mentions[:10],  # 保存前10条提及
                "discovery_status": "new"
            }
            
            aggregated_projects.append(project_data)
        
        # 按信号强度排序
        aggregated_projects.sort(key=lambda x: x["signal_strength"], reverse=True)
        
        logger.info(f"✅ Aggregated {len(aggregated_projects)} projects")
        return aggregated_projects
    
    def calculate_topic_heat(self, project_name: str, mentions: List[Dict]) -> Dict:
        """计算项目话题热度
        
        Args:
            project_name: 项目名称
            mentions: 提及列表
            
        Returns:
            热度数据
        """
        if not mentions:
            return {"heat_score": 0}
        
        # 统计不同时间段的提及数
        now = datetime.utcnow()
        
        # 处理日期格式
        def parse_date(d):
            if isinstance(d, datetime):
                return d
            elif isinstance(d, str):
                try:
                    return datetime.fromisoformat(d.replace('Z', '+00:00'))
                except:
                    return datetime.utcnow()
            else:
                return datetime.utcnow()
        
        mentions_24h = [m for m in mentions if (now - parse_date(m["discovered_at"])).total_seconds() < 86400]
        mentions_7d = [m for m in mentions if (now - parse_date(m["discovered_at"])).total_seconds() < 604800]
        
        # 计算增长率
        if len(mentions_7d) > len(mentions_24h):
            recent_rate = len(mentions_24h) / (len(mentions_7d) - len(mentions_24h))
        else:
            recent_rate = 1.0
        
        # 计算热度分
        heat_score = min(100, (
            min(50, len(mentions_24h) * 10) +  # 24小时提及
            min(30, recent_rate * 30) +  # 增长率
            min(20, len(set(m["platform"] for m in mentions_24h)) * 7)  # 平台数
        ))
        
        return {
            "project_name": project_name,
            "heat_score": int(heat_score),
            "mentions_24h": len(mentions_24h),
            "mentions_7d": len(mentions_7d),
            "growth_rate": recent_rate,
            "is_trending": heat_score > 70
        }
    
    def detect_sudden_surge(self, project_name: str, mentions: List[Dict]) -> Dict:
        """检测突然爆发
        
        Args:
            project_name: 项目名称
            mentions: 提及列表（按时间排序）
            
        Returns:
            爆发检测结果
        """
        if len(mentions) < 10:
            return {"is_surge": False}
        
        # 按小时统计
        hourly_counts = defaultdict(int)
        
        for mention in mentions:
            hour = mention["discovered_at"].replace(minute=0, second=0, microsecond=0)
            hourly_counts[hour] += 1
        
        # 转换为列表
        sorted_hours = sorted(hourly_counts.keys())
        counts = [hourly_counts[h] for h in sorted_hours]
        
        if len(counts) < 24:
            return {"is_surge": False}
        
        # 计算基线（前面的平均值）
        baseline = sum(counts[:-24]) / len(counts[:-24]) if len(counts) > 24 else 0
        
        # 最近24小时平均
        recent_avg = sum(counts[-24:]) / 24
        
        # 判断爆发
        surge_ratio = recent_avg / baseline if baseline > 0 else 0
        is_surge = surge_ratio > 3
        
        return {
            "project_name": project_name,
            "is_surge": is_surge,
            "surge_ratio": surge_ratio,
            "baseline_per_hour": baseline,
            "recent_per_hour": recent_avg
        }
    
    def filter_known_projects(self, projects: List[Dict]) -> List[Dict]:
        """过滤已知大项目
        
        Args:
            projects: 项目列表
            
        Returns:
            过滤后的项目列表
        """
        # 已知大项目列表
        known_big_projects = {
            "Bitcoin", "Ethereum", "Binance", "Coinbase",
            "Uniswap", "Aave", "Compound", "Maker",
            "Polygon", "Solana", "Avalanche", "Cardano",
            "Polkadot", "Chainlink", "Cosmos", "Tezos"
        }
        
        filtered = [
            p for p in projects
            if p["project_name"] not in known_big_projects
        ]
        
        logger.info(f"📊 Filtered out {len(projects) - len(filtered)} known big projects")
        return filtered
    
    def check_token_status(self, project_name: str) -> Dict:
        """检查项目是否已发币（简化版）
        
        Args:
            project_name: 项目名称
            
        Returns:
            代币状态
        """
        # TODO: 集成CoinGecko/CoinMarketCap API
        
        # 简单的关键词检测
        no_token_keywords = ["testnet", "coming soon", "pre-launch"]
        has_token_keywords = ["token", "launched", "live"]
        
        # 这里返回假设值，实际需要调用API
        return {
            "project_name": project_name,
            "has_token": False,  # 假设未发币
            "checked_at": datetime.utcnow()
        }
    
    def discover_projects(self, data_sources: Dict[str, List[Dict]]) -> List[Dict]:
        """完整的项目发现流程
        
        Args:
            data_sources: 各平台数据
            
        Returns:
            发现的项目列表
        """
        logger.info("🚀 Starting project discovery process...")
        
        # 1. 聚合多平台数据
        aggregated = self.aggregate_multi_source_data(data_sources)
        logger.info(f"  ✅ Step 1: Aggregated {len(aggregated)} projects")
        
        # 2. 过滤已知大项目
        filtered = self.filter_known_projects(aggregated)
        logger.info(f"  ✅ Step 2: Filtered to {len(filtered)} projects")
        
        # 3. 计算热度和爆发
        for project in filtered:
            # 话题热度
            heat = self.calculate_topic_heat(
                project["project_name"],
                project["mentions"]
            )
            project["heat_data"] = heat
            
            # 突发检测
            surge = self.detect_sudden_surge(
                project["project_name"],
                project["mentions"]
            )
            project["surge_data"] = surge
            
            # 检查代币状态
            token_status = self.check_token_status(project["project_name"])
            project["token_status"] = token_status
        
        logger.info("  ✅ Step 3: Calculated heat and surge data")
        
        # 4. 筛选高质量项目
        high_quality = [
            p for p in filtered
            if (
                p["num_platforms"] >= 2 and  # 至少2个平台
                p["total_mentions"] >= 3 and  # 至少3次提及
                not p["token_status"]["has_token"]  # 未发币
            )
        ]
        
        logger.info(f"  ✅ Step 4: {len(high_quality)} high-quality projects")
        
        # 5. 按综合信号排序
        high_quality.sort(
            key=lambda x: (
                x["heat_data"].get("heat_score", 0) * 0.6 +
                x["signal_strength"] * 0.4
            ),
            reverse=True
        )
        
        logger.info(f"✅ Discovery complete: {len(high_quality)} projects found")
        
        return high_quality


# 全局服务实例
project_discovery_service = ProjectDiscoveryService()

