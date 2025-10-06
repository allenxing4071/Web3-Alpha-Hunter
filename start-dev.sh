#!/bin/bash

echo "🚀 启动 Web3 Alpha Hunter 开发环境"
echo "===================================="

# 检查PostgreSQL
echo ""
echo "1️⃣ 检查PostgreSQL..."
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "   ✅ PostgreSQL 正在运行"
else
    echo "   ❌ PostgreSQL 未运行，请先启动PostgreSQL"
    exit 1
fi

# 检查Redis
echo ""
echo "2️⃣ 检查Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "   ✅ Redis 正在运行"
else
    echo "   ❌ Redis 未运行，请先启动Redis"
    exit 1
fi

# 启动后端
echo ""
echo "3️⃣ 启动后端服务 (端口8000)..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "   ✅ 后端已启动 (PID: $BACKEND_PID)"
echo "   📄 日志: tail -f /tmp/backend.log"
cd ..

# 等待后端启动
echo ""
echo "   ⏳ 等待后端就绪..."
sleep 3

# 检查后端健康
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ 后端健康检查通过"
else
    echo "   ⚠️  后端可能未完全启动，请检查日志"
fi

# 启动前端
echo ""
echo "4️⃣ 启动前端服务 (端口3000)..."
cd frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   ✅ 前端已启动 (PID: $FRONTEND_PID)"
echo "   📄 日志: tail -f /tmp/frontend.log"
cd ..

# 保存PID
echo "$BACKEND_PID" > /tmp/web3hunter-backend.pid
echo "$FRONTEND_PID" > /tmp/web3hunter-frontend.pid

echo ""
echo "===================================="
echo "✅ 所有服务已启动！"
echo ""
echo "📱 访问地址:"
echo "   前端: http://localhost:3000"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "🛑 停止服务:"
echo "   ./stop-dev.sh"
echo ""
echo "📊 查看日志:"
echo "   后端: tail -f /tmp/backend.log"
echo "   前端: tail -f /tmp/frontend.log"
echo "===================================="

