#!/bin/bash

echo "🛑 停止 Web3 Alpha Hunter 开发环境"
echo "===================================="

# 停止后端
if [ -f /tmp/web3hunter-backend.pid ]; then
    BACKEND_PID=$(cat /tmp/web3hunter-backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "🛑 停止后端服务 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm /tmp/web3hunter-backend.pid
        echo "   ✅ 后端已停止"
    else
        echo "   ℹ️  后端进程不存在"
        rm /tmp/web3hunter-backend.pid
    fi
else
    echo "   ℹ️  未找到后端PID文件"
fi

# 停止前端
if [ -f /tmp/web3hunter-frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/web3hunter-frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "🛑 停止前端服务 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm /tmp/web3hunter-frontend.pid
        echo "   ✅ 前端已停止"
    else
        echo "   ℹ️  前端进程不存在"
        rm /tmp/web3hunter-frontend.pid
    fi
else
    echo "   ℹ️  未找到前端PID文件"
fi

# 清理Next.js端口占用（如果有）
echo ""
echo "🧹 清理端口占用..."
lsof -ti:3000 | xargs kill -9 2>/dev/null && echo "   ✅ 端口3000已释放" || echo "   ℹ️  端口3000未被占用"
lsof -ti:8000 | xargs kill -9 2>/dev/null && echo "   ✅ 端口8000已释放" || echo "   ℹ️  端口8000未被占用"

echo ""
echo "===================================="
echo "✅ 所有服务已停止！"
echo "===================================="

