#!/bin/bash

# 🚀 Web3 Alpha Hunter - 环境配置脚本

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Web3 Alpha Hunter 环境配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ===== 核心配置 (必需) =====
export DEEPSEEK_API_KEY="sk-71165bff309a400293c2af2372164d60"
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"
export REDIS_URL="redis://localhost:6379/0"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/1"
export CORS_ORIGINS="http://localhost:3000,http://localhost:3001"

echo "✅ 核心配置已加载"
echo "  - DeepSeek API: ${DEEPSEEK_API_KEY:0:10}..."
echo "  - Database: $DATABASE_URL"
echo "  - Redis: $REDIS_URL"
echo ""

# ===== 可选配置 (数据采集API) =====
# 如果需要真实数据采集,请取消下面的注释并填入真实密钥

# Twitter API
# export TWITTER_BEARER_TOKEN="YOUR_TWITTER_BEARER_TOKEN"
# echo "⏳ Twitter API: 未配置 (使用Mock数据)"

# Telegram API
# export TELEGRAM_API_ID="YOUR_API_ID"
# export TELEGRAM_API_HASH="YOUR_API_HASH"
# echo "⏳ Telegram API: 未配置 (使用Mock数据)"

# CoinGecko API
# export COINGECKO_API_KEY="YOUR_COINGECKO_KEY"
# echo "⏳ CoinGecko API: 未配置"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 环境变量已设置完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 使用方法:"
echo "  source setup_env.sh"
echo ""
echo "🚀 然后启动服务:"
echo "  cd backend && uvicorn app.main:app --reload --port 8000"
echo ""
