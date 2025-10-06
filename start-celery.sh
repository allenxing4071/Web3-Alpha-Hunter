#!/bin/bash
# Celery 启动脚本

cd "$(dirname "$0")/backend"

echo "🚀 启动 Celery Worker..."
python3 -m celery -A app.tasks.celery_app worker --loglevel=info > /tmp/celery-worker.log 2>&1 &
WORKER_PID=$!
echo "✅ Celery Worker 已启动 (PID: $WORKER_PID)"

sleep 2

echo "🚀 启动 Celery Beat..."
python3 -m celery -A app.tasks.celery_app beat --loglevel=info > /tmp/celery-beat.log 2>&1 &
BEAT_PID=$!
echo "✅ Celery Beat 已启动 (PID: $BEAT_PID)"

sleep 2

echo ""
echo "📊 检查服务状态..."
if curl -s http://localhost:8000/api/v1/admin/celery-status | grep -q "true"; then
    echo "✅ 所有 Celery 服务运行正常！"
    echo ""
    echo "📝 日志文件:"
    echo "  - Worker: /tmp/celery-worker.log"
    echo "  - Beat:   /tmp/celery-beat.log"
    echo ""
    echo "🛑 停止服务: ./stop-celery.sh"
else
    echo "⚠️  服务状态检查失败，请查看日志"
fi

