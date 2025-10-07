#!/usr/bin/env python3
"""
为现有CoinGecko项目补充真实数据
从CoinGecko API获取真实的市场数据和社交指标
"""

import sys
import os
from pathlib import Path
import requests
import time
from datetime import datetime
from decimal import Decimal

# 添加项目路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.project import Project, SocialMetrics, OnchainMetrics
from app.core.config import settings

# CoinGecko API配置
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
RATE_LIMIT_DELAY = 1.5  # 免费API限制: 10-30次/分钟

def fetch_coin_data(coin_id: str) -> dict:
    """从CoinGecko获取币种详细数据"""
    try:
        # 获取币种详细信息
        url = f"{COINGECKO_BASE_URL}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        time.sleep(RATE_LIMIT_DELAY)  # 避免触发限流
        
        return response.json()
    except Exception as e:
        print(f"  ❌ 获取 {coin_id} 数据失败: {e}")
        return None

def extract_social_metrics(data: dict, project_id: int) -> dict:
    """提取社交媒体指标"""
    community = data.get("community_data", {})
    
    return {
        "project_id": project_id,
        "twitter_followers": community.get("twitter_followers"),
        "telegram_members": community.get("telegram_channel_user_count"),
        "github_stars": data.get("developer_data", {}).get("stars"),
        "github_forks": data.get("developer_data", {}).get("forks"),
        "discord_members": None,  # CoinGecko不提供
    }

def extract_onchain_metrics(data: dict, project_id: int) -> dict:
    """提取链上指标"""
    market = data.get("market_data", {})
    
    return {
        "project_id": project_id,
        "market_cap": market.get("market_cap", {}).get("usd"),
        "price_usd": market.get("current_price", {}).get("usd"),
        "volume_24h": market.get("total_volume", {}).get("usd"),
        "circulating_supply": market.get("circulating_supply"),
        "total_supply": market.get("total_supply"),
        "tvl_usd": None,  # CoinGecko不直接提供TVL
        "holder_count": None,
    }

def get_coingecko_id_from_symbol(symbol: str) -> str:
    """根据symbol尝试获取CoinGecko ID"""
    # 常见映射
    mapping = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "BNB": "binancecoin",
        "XRP": "ripple",
        "USDT": "tether",
        "USDC": "usd-coin",
        "DOGE": "dogecoin",
        "ADA": "cardano",
        "MATIC": "matic-network",
        "DOT": "polkadot",
        "AVAX": "avalanche-2",
        "UNI": "uniswap",
        "LINK": "chainlink",
        "ATOM": "cosmos",
        "ARB": "arbitrum",
        "OP": "optimism",
        "PENGU": "pudgy-penguins",
        "HYPE": "hyperliquid",
    }
    
    if symbol in mapping:
        return mapping[symbol]
    
    # 尝试搜索
    try:
        url = f"{COINGECKO_BASE_URL}/search"
        params = {"query": symbol}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        coins = response.json().get("coins", [])
        if coins:
            return coins[0]["id"]
    except:
        pass
    
    return None

def update_project_real_data(db: Session, project: Project):
    """为项目补充真实数据"""
    print(f"\n处理: {project.project_name} (${project.symbol or 'N/A'})")
    
    # 获取CoinGecko ID
    coingecko_id = None
    if project.symbol:
        coingecko_id = get_coingecko_id_from_symbol(project.symbol.replace("$", "").upper())
    
    if not coingecko_id:
        # 尝试用项目名搜索
        try:
            url = f"{COINGECKO_BASE_URL}/search"
            params = {"query": project.project_name}
            response = requests.get(url, params=params, timeout=10)
            coins = response.json().get("coins", [])
            if coins:
                coingecko_id = coins[0]["id"]
        except:
            pass
    
    if not coingecko_id:
        print(f"  ⚠️  未找到CoinGecko ID，跳过")
        return False
    
    print(f"  📊 CoinGecko ID: {coingecko_id}")
    
    # 获取详细数据
    coin_data = fetch_coin_data(coingecko_id)
    if not coin_data:
        return False
    
    # 提取并保存社交指标
    social_data = extract_social_metrics(coin_data, project.id)
    # 过滤None值
    social_data_clean = {k: v for k, v in social_data.items() if v is not None or k == 'project_id'}
    if len(social_data_clean) > 1:  # 除了project_id还有其他数据
        social_metrics = SocialMetrics(**social_data_clean)
        db.add(social_metrics)
        db.flush()
        # 关联到project
        project.social_metrics_id = social_metrics.id
        print(f"  ✅ 社交数据: Twitter {social_data['twitter_followers'] or 0}, Telegram {social_data['telegram_members'] or 0}")
    
    # 提取并保存链上指标
    onchain_data = extract_onchain_metrics(coin_data, project.id)
    # 过滤None值并转换为Decimal
    onchain_data_clean = {}
    for k, v in onchain_data.items():
        if k == 'project_id':
            onchain_data_clean[k] = v
        elif v is not None:
            if k in ['market_cap', 'price_usd', 'volume_24h', 'circulating_supply', 'total_supply', 'tvl_usd']:
                onchain_data_clean[k] = Decimal(str(v))
            else:
                onchain_data_clean[k] = v
    
    if len(onchain_data_clean) > 1:  # 除了project_id还有其他数据
        onchain_metrics = OnchainMetrics(**onchain_data_clean)
        db.add(onchain_metrics)
        db.flush()
        # 关联到project
        project.onchain_metrics_id = onchain_metrics.id
        
        mc = onchain_data_clean.get('market_cap')
        price = onchain_data_clean.get('price_usd')
        print(f"  ✅ 链上数据: 市值 ${float(mc)/1e6:.1f}M, 价格 ${float(price):.4f}" if mc and price else "  ✅ 链上数据已保存")
    
    project.last_updated_at = datetime.utcnow()
    return True

def main():
    """主函数"""
    print("🚀 开始为CoinGecko项目补充真实数据")
    print("=" * 70)
    
    db = next(get_db())
    
    # 获取所有CoinGecko项目
    projects = db.query(Project).filter(
        Project.discovered_from == "coingecko"
    ).all()
    
    print(f"\n📊 找到 {len(projects)} 个CoinGecko项目")
    
    success_count = 0
    failed_count = 0
    
    for i, project in enumerate(projects, 1):
        print(f"\n[{i}/{len(projects)}]", end=" ")
        
        try:
            if update_project_real_data(db, project):
                success_count += 1
                db.commit()
            else:
                failed_count += 1
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            failed_count += 1
            db.rollback()
    
    print("\n" + "=" * 70)
    print(f"✅ 完成！成功: {success_count}, 失败: {failed_count}")
    print(f"📊 真实数据已补充到数据库")

if __name__ == "__main__":
    main()

