"""Telegram数据采集服务"""

import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from telethon import TelegramClient, events
from telethon.tl.types import Channel, User
from app.core.config import settings


class TelegramCollector:
    """Telegram数据采集器"""
    
    # 优质加密货币频道列表
    CHANNELS = [
        "@cryptonewsflash",
        "@whale_alert",
        "@CryptoInsiderNews",
        "@binance_announcements",
        "@coinbase",
        "@CryptoGemAlerts",
        "@DeFiPulse",
        "@TheCryptoMonitor",
        "@AltcoinBuzz",
        "@ICOdrops",
    ]
    
    def __init__(self):
        """初始化Telegram采集器（延迟初始化client以避免fork问题）"""
        self._client = None
        self._credentials_available = bool(settings.TELEGRAM_API_ID and settings.TELEGRAM_API_HASH)
        
        if not self._credentials_available:
            logger.warning("Telegram API credentials not configured")
        else:
            logger.info("✅ Telegram collector initialized (client will be created on demand)")
    
    def _get_client(self):
        """懒加载：每次使用时创建新的client实例（避免Celery fork问题）"""
        if not self._credentials_available:
            return None
        
        try:
            # 每次都创建新实例，避免fork后的文件描述符问题
            client = TelegramClient(
                'web3_alpha_hunter',
                settings.TELEGRAM_API_ID,
                settings.TELEGRAM_API_HASH
            )
            logger.debug("🔌 Created new Telegram client instance")
            return client
        except Exception as e:
            logger.error(f"Failed to create Telegram client: {e}")
            return None
    
    @property
    def client(self):
        """兼容性属性：返回client（懒加载）"""
        if self._client is None:
            self._client = self._get_client()
        return self._client
    
    async def start_client(self):
        """启动Telegram客户端（每次采集时重新创建client）"""
        # 获取新的client实例
        client = self._get_client()
        if not client:
            return False
        
        try:
            await client.start()
            logger.info("✅ Telegram client connected")
            self._client = client  # 保存已连接的client
            return True
        except Exception as e:
            logger.error(f"Failed to start Telegram client: {e}")
            if client:
                try:
                    await client.disconnect()
                except:
                    pass
            return False
    
    async def get_channel_messages(
        self,
        channel: str,
        limit: int = 100,
        hours: int = 24
    ) -> List[Dict]:
        """获取频道最新消息
        
        Args:
            channel: 频道用户名 (如 @cryptonewsflash)
            limit: 最大消息数
            hours: 获取过去N小时的消息
            
        Returns:
            消息列表
        """
        if not self.client:
            return []
        
        try:
            # 获取频道实体
            entity = await self.client.get_entity(channel)
            
            # 计算时间范围
            offset_date = datetime.utcnow() - timedelta(hours=hours)
            
            # 获取消息
            messages = []
            async for message in self.client.iter_messages(
                entity,
                limit=limit,
                offset_date=offset_date
            ):
                if not message.text:
                    continue
                
                msg_data = {
                    "message_id": message.id,
                    "channel": channel,
                    "text": message.text,
                    "date": message.date,
                    "views": message.views or 0,
                    "forwards": message.forwards or 0,
                    "replies": message.replies.replies if message.replies else 0,
                    "has_media": message.media is not None,
                    "entities": [],
                }
                
                # 提取实体(链接、提及等)
                if message.entities:
                    for entity in message.entities:
                        entity_type = type(entity).__name__
                        msg_data["entities"].append({
                            "type": entity_type,
                            "offset": entity.offset,
                            "length": entity.length,
                        })
                
                messages.append(msg_data)
            
            logger.info(f"✅ Collected {len(messages)} messages from {channel}")
            return messages
            
        except Exception as e:
            logger.error(f"Error collecting from {channel}: {e}")
            return []
    
    async def monitor_all_channels(self, hours: int = 1) -> List[Dict]:
        """监控所有频道
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            所有频道的消息列表
        """
        if not await self.start_client():
            return []
        
        all_messages = []
        
        for channel in self.CHANNELS:
            messages = await self.get_channel_messages(
                channel=channel,
                limit=50,
                hours=hours
            )
            all_messages.extend(messages)
        
        logger.info(f"✅ Total Telegram messages collected: {len(all_messages)}")
        return all_messages
    
    def extract_project_info(self, message: Dict) -> Optional[Dict]:
        """从消息中提取项目信息
        
        Args:
            message: 消息数据
            
        Returns:
            项目信息字典 or None
        """
        text = message["text"]
        
        # 提取URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        
        # 提取合约地址
        contract_pattern = r"0x[a-fA-F0-9]{40}"
        contracts = re.findall(contract_pattern, text)
        
        # 提取Telegram链接
        telegram_pattern = r't\.me/([a-zA-Z0-9_]+)'
        telegram_links = re.findall(telegram_pattern, text)
        
        # 关键词检测
        keywords = [
            "launch", "presale", "airdrop", "testnet", "mainnet",
            "IDO", "ICO", "token sale", "fair launch", "whitelist"
        ]
        
        found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
        
        # 如果没有找到关键信息，返回None
        if not urls and not contracts and not found_keywords:
            return None
        
        return {
            "message_id": message["message_id"],
            "discovered_at": message["date"],
            "source": "telegram",
            "source_channel": message["channel"],
            "text": text,
            "urls": urls,
            "contracts": contracts,
            "telegram_links": telegram_links,
            "keywords": found_keywords,
            "engagement": {
                "views": message["views"],
                "forwards": message["forwards"],
                "replies": message["replies"],
            }
        }
    
    async def collect_and_extract(self, hours: int = 1) -> List[Dict]:
        """采集消息并提取项目信息（每次都创建新client避免fork问题）
        
        Args:
            hours: 监控过去N小时
            
        Returns:
            项目信息列表
        """
        if not self._credentials_available:
            logger.error("Telegram API credentials not configured")
            return []
        
        logger.info(f"🔍 Starting Telegram collection (last {hours} hours)...")
        
        # 创建并启动新的客户端（避免复用旧的client）
        self._client = None  # 重置client
        if not await self.start_client():
            logger.error("Failed to start Telegram client")
            return []
        
        try:
            # 1. 监控所有频道
            messages = await self.monitor_all_channels(hours=hours)
        
            # 2. 提取项目信息
            projects = []
            for message in messages:
                project_info = self.extract_project_info(message)
                if project_info:
                    projects.append(project_info)
            
            logger.info(f"✅ Extracted {len(projects)} potential projects from Telegram")
            return projects
        
        finally:
            # 确保client被正确关闭
            if self._client:
                try:
                    await self._client.disconnect()
                    logger.debug("🔌 Telegram client disconnected")
                except Exception as e:
                    logger.warning(f"Error disconnecting Telegram client: {e}")
                finally:
                    self._client = None


# 全局采集器实例
telegram_collector = TelegramCollector()

