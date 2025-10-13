#!/bin/bash
# Celery 停止脚本

echo "🛑 停止 Celery 服务..."

# 停止 Celery Worker
echo "  停止 Celery Worker..."
pkill -f "celery.*worker" && echo "  ✅ Worker 已停止" || echo "  ℹ️  Worker 未运行"

# 停止 Celery Beat
echo "  停止 Celery Beat..."
pkill -f "celery.*beat" && echo "  ✅ Beat 已停止" || echo "  ℹ️  Beat 未运行"

sleep 1

# 检查是否还有残留进程
if pgrep -f "celery" > /dev/null; then
    echo ""
    echo "⚠️  发现残留进程，强制清理..."
    pkill -9 -f "celery"
    sleep 1
fi

echo ""
echo "✅ Celery 服务已全部停止"

