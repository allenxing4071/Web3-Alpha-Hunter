"""Discord数据采集服务"""

import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
import discord
from discord.ext import commands

from app.core.config import settings


class DiscordCollector:
    """Discord数据采集器"""
    
    # 监控的服务器列表
    MONITORED_GUILDS = [
        # 稍后通过配置动态添加
    ]
    
    # 关键频道关键词
    KEY_CHANNEL_KEYWORDS = [
        "announcement", "alpha", "airdrop", "whitelist",
        "general", "partnership", "development"
    ]
    
    def __init__(self):
        """初始化Discord Bot"""
        if not settings.DISCORD_BOT_TOKEN:
            logger.warning("Discord Bot Token not configured")
            self.bot = None
            return
        
        # 创建Bot实例
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.setup_events()
        logger.info("✅ Discord Bot initialized")
    
    def setup_events(self):
        """设置事件处理器"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f'✅ Discord Bot logged in as {self.bot.user}')
            logger.info(f'监控 {len(self.bot.guilds)} 个服务器')
            
            # 分析所有服务器
            for guild in self.bot.guilds:
                await self.analyze_guild(guild)
        
        @self.bot.event
        async def on_message(message):
            """处理新消息"""
            
            # 忽略bot自己的消息
            if message.author.bot:
                return
            
            # 只处理关键频道
            if not self.is_key_channel(message.channel):
                return
            
            # 提取关键信息
            key_info = self.extract_key_information(message)
            
            if key_info and key_info.get("importance", 0) > 80:
                logger.info(f"🔥 重要消息: {message.guild.name} #{message.channel.name}")
                # TODO: 发送预警
            
            # 保存消息
            await self.save_message(message)
        
        @self.bot.event
        async def on_guild_join(guild):
            """加入新服务器"""
            logger.info(f'✅ 加入服务器: {guild.name}')
            await self.analyze_guild(guild)
    
    def is_key_channel(self, channel) -> bool:
        """判断是否为关键频道"""
        channel_name = channel.name.lower()
        
        return any(
            keyword in channel_name
            for keyword in self.KEY_CHANNEL_KEYWORDS
        )
    
    def calculate_channel_importance(self, channel) -> int:
        """计算频道重要性（0-100）"""
        score = 0
        channel_name = channel.name.lower()
        
        # 基于频道名称
        priority_map = {
            "announcement": 100,
            "alpha": 90,
            "airdrop": 85,
            "whitelist": 85,
            "general": 80,
            "partnership": 75,
            "development": 70,
        }
        
        for keyword, priority in priority_map.items():
            if keyword in channel_name:
                score = max(score, priority)
        
        return score
    
    async def analyze_guild(self, guild) -> Dict:
        """分析服务器"""
        logger.info(f"🔍 Analyzing guild: {guild.name}")
        
        # 统计成员
        total_members = guild.member_count
        online_members = sum(
            1 for m in guild.members
            if m.status != discord.Status.offline
        )
        
        # 识别关键频道
        key_channels = []
        for channel in guild.text_channels:
            if self.is_key_channel(channel):
                importance = self.calculate_channel_importance(channel)
                key_channels.append({
                    "name": channel.name,
                    "id": channel.id,
                    "importance": importance
                })
        
        logger.info(f"  - 成员: {total_members} (在线: {online_members})")
        logger.info(f"  - 关键频道: {len(key_channels)}")
        
        return {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "member_count": total_members,
            "online_count": online_members,
            "key_channels": key_channels,
            "analyzed_at": datetime.utcnow()
        }
    
    async def analyze_community_activity(self, guild_id: int) -> Dict:
        """分析社区活跃度"""
        guild = self.bot.get_guild(guild_id)
        
        if not guild:
            return {}
        
        # 统计消息（过去24小时）
        message_count = 0
        unique_authors = set()
        
        for channel in guild.text_channels:
            try:
                async for message in channel.history(
                    limit=100,
                    after=datetime.utcnow() - timedelta(hours=24)
                ):
                    message_count += 1
                    unique_authors.add(message.author.id)
            except:
                pass  # 无权限访问
        
        # 计算活跃度分数
        activity_score = min(100, (
            min(30, guild.member_count / 1000) +
            min(30, message_count / 100) +
            min(20, len(unique_authors) / 50) +
            min(20, (len(unique_authors) / message_count if message_count > 0 else 0) * 20)
        ))
        
        return {
            "guild_id": guild_id,
            "guild_name": guild.name,
            "total_members": guild.member_count,
            "daily_messages": message_count,
            "active_users": len(unique_authors),
            "activity_score": int(activity_score),
            "activity_level": "High" if activity_score > 70 else "Medium" if activity_score > 40 else "Low"
        }
    
    def extract_key_information(self, message: discord.Message) -> Optional[Dict]:
        """从消息中提取关键信息"""
        text = message.content.lower()
        
        # 检测信息类型
        info_type = None
        importance = 0
        
        # 高优先级关键词
        if any(kw in text for kw in ["snapshot", "快照", "airdrop announcement"]):
            info_type = "SNAPSHOT_ANNOUNCEMENT"
            importance = 100
        
        elif any(kw in text for kw in ["whitelist open", "白名单开放", "allowlist"]):
            info_type = "WHITELIST_OPEN"
            importance = 95
        
        elif any(kw in text for kw in ["token launch", "tge", "代币上线"]):
            info_type = "TOKEN_LAUNCH"
            importance = 90
        
        elif any(kw in text for kw in ["airdrop", "空投"]):
            info_type = "AIRDROP_ALERT"
            importance = 85
        
        elif any(kw in text for kw in ["partnership", "合作", "integration"]):
            info_type = "PARTNERSHIP"
            importance = 70
        
        elif re.search(r"0x[a-fA-F0-9]{40}", text):
            info_type = "CONTRACT_ADDRESS"
            importance = 80
        
        if info_type:
            return {
                "type": info_type,
                "guild": message.guild.name,
                "channel": message.channel.name,
                "author": message.author.name,
                "content": message.content,
                "importance": importance,
                "timestamp": message.created_at,
                "message_id": message.id
            }
        
        return None
    
    def extract_project_names(self, text: str) -> List[str]:
        """从文本中提取项目名称"""
        projects = []
        
        # 正则匹配
        pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        matches = re.findall(pattern, text)
        projects.extend(matches)
        
        # 去重和清洗
        projects = list(set([p.strip() for p in projects if len(p) > 2]))
        
        # 过滤噪音
        noise_words = ["Discord", "Twitter", "Telegram", "The", "This"]
        projects = [p for p in projects if p not in noise_words]
        
        return projects
    
    async def save_message(self, message: discord.Message):
        """保存消息到数据库"""
        # TODO: 实现数据库保存
        pass
    
    async def collect_guild_messages(
        self,
        guild_id: int,
        hours: int = 24,
        limit_per_channel: int = 100
    ) -> List[Dict]:
        """采集服务器消息
        
        Args:
            guild_id: 服务器ID
            hours: 采集过去N小时的消息
            limit_per_channel: 每个频道最大消息数
            
        Returns:
            消息列表
        """
        guild = self.bot.get_guild(guild_id)
        
        if not guild:
            logger.warning(f"Guild {guild_id} not found")
            return []
        
        all_messages = []
        after_time = datetime.utcnow() - timedelta(hours=hours)
        
        # 只采集关键频道
        key_channels = [c for c in guild.text_channels if self.is_key_channel(c)]
        
        logger.info(f"🔍 Collecting messages from {len(key_channels)} key channels in {guild.name}")
        
        for channel in key_channels:
            try:
                count = 0
                async for message in channel.history(limit=limit_per_channel, after=after_time):
                    if message.author.bot:
                        continue
                    
                    msg_data = {
                        "message_id": message.id,
                        "guild_id": guild.id,
                        "guild_name": guild.name,
                        "channel_id": channel.id,
                        "channel_name": channel.name,
                        "author_id": message.author.id,
                        "author_name": message.author.name,
                        "content": message.content,
                        "created_at": message.created_at,
                        "reactions": [
                            {"emoji": str(r.emoji), "count": r.count}
                            for r in message.reactions
                        ],
                        "attachments": [att.url for att in message.attachments],
                    }
                    
                    all_messages.append(msg_data)
                    count += 1
                
                logger.info(f"  - #{channel.name}: {count} messages")
                
            except discord.Forbidden:
                logger.warning(f"  - #{channel.name}: No permission")
            except Exception as e:
                logger.error(f"  - #{channel.name}: Error - {e}")
        
        logger.info(f"✅ Collected {len(all_messages)} messages from {guild.name}")
        return all_messages
    
    async def start(self):
        """启动Bot"""
        if not self.bot:
            logger.error("Discord Bot not initialized")
            return
        
        try:
            await self.bot.start(settings.DISCORD_BOT_TOKEN)
        except Exception as e:
            logger.error(f"Failed to start Discord Bot: {e}")
    
    async def stop(self):
        """停止Bot"""
        if self.bot:
            await self.bot.close()


# 全局采集器实例
discord_collector = DiscordCollector()

