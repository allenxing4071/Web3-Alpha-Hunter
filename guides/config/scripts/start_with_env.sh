#!/bin/bash

# 🚀 Web3 Alpha Hunter - 一键启动脚本 (包含环境变量)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 启动 Web3 Alpha Hunter"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 加载环境变量
echo "📋 加载环境变量..."
source setup_env.sh

# 2. 检查并停止旧进程
echo ""
echo "🔍 检查现有进程..."
lsof -ti:8000 | xargs kill -9 2>/dev/null && echo "  ✅ 已停止旧的后端进程" || echo "  ℹ️ 无需停止后端"
lsof -ti:3000 | xargs kill -9 2>/dev/null && echo "  ✅ 已停止旧的前端进程" || echo "  ℹ️ 无需停止前端"

# 3. 启动后端
echo ""
echo "🔧 启动后端服务..."
cd backend
python3 -m uvicorn app.main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "  ✅ 后端已启动 (PID: $BACKEND_PID)"
echo "  📄 日志: /tmp/backend.log"

# 4. 等待后端启动
echo ""
echo "⏳ 等待后端就绪..."
sleep 5

# 检查DeepSeek初始化
if grep -q "DeepSeek v3 client initialized" /tmp/backend.log; then
    echo "  ✅ DeepSeek v3 已初始化"
else
    echo "  ⚠️ DeepSeek初始化状态未知,查看日志: tail -f /tmp/backend.log"
fi

# 5. 启动前端
echo ""
echo "🎨 启动前端服务..."
cd ../frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  ✅ 前端已启动 (PID: $FRONTEND_PID)"
echo "  📄 日志: /tmp/frontend.log"

# 6. 显示访问信息
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 启动完成!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 访问地址:"
echo "  - 前端首页: http://localhost:3000"
echo "  - 系统管理: http://localhost:3000/admin"
echo "  - 控制面板: http://localhost:3000/dashboard.html"
echo "  - 后端API: http://localhost:8000/docs"
echo ""
echo "👤 默认登录:"
echo "  - 用户名: admin"
echo "  - 密码: admin123"
echo ""
echo "📊 查看日志:"
echo "  - 后端: tail -f /tmp/backend.log"
echo "  - 前端: tail -f /tmp/frontend.log"
echo ""
echo "🛑 停止服务:"
echo "  - 后端: kill $BACKEND_PID"
echo "  - 前端: kill $FRONTEND_PID"
echo "  - 全部: lsof -ti:8000,3000 | xargs kill -9"
echo ""
