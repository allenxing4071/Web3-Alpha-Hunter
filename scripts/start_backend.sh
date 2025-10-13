#!/bin/bash
# 启动后端服务（使用PostgreSQL数据库）

cd "$(dirname "$0")/backend"

echo "🚀 启动Web3 Alpha Hunter后端..."
echo "🐘 使用PostgreSQL数据库: web3_alpha_hunter@localhost:5432"

# 停止现有进程
pkill -9 -f "uvicorn.*app.main:app" 2>/dev/null || true
sleep 2

# 启动后端（使用配置文件中的PostgreSQL）
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &

echo "✅ 后端已启动"
echo "📡 API地址: http://localhost:8000"
echo "📖 API文档: http://localhost:8000/docs"
echo "📋 查看日志: tail -f /tmp/backend.log"

