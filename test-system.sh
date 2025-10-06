#!/bin/bash

echo "🧪 Web3 Alpha Hunter 系统测试"
echo "===================================="

API_URL="http://localhost:8000"

# 测试后端健康
echo ""
echo "1️⃣ 测试后端健康..."
if curl -s ${API_URL}/health | grep -q "healthy"; then
    echo "   ✅ 后端健康检查通过"
else
    echo "   ❌ 后端健康检查失败"
    exit 1
fi

# 测试数据库连接
echo ""
echo "2️⃣ 测试数据库统计API..."
RESPONSE=$(curl -s ${API_URL}/api/v1/database/stats)
if echo $RESPONSE | grep -q "success"; then
    PROJECT_COUNT=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['project_count'])")
    TABLE_COUNT=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['table_count'])")
    echo "   ✅ 数据库连接正常"
    echo "   📊 项目数量: $PROJECT_COUNT"
    echo "   📊 业务表数量: $TABLE_COUNT"
else
    echo "   ❌ 数据库连接失败"
fi

# 测试平台API
echo ""
echo "3️⃣ 测试平台管理API..."
RESPONSE=$(curl -s ${API_URL}/api/v1/platforms/)
if echo $RESPONSE | grep -q "twitter"; then
    PLATFORM_COUNT=$(echo $RESPONSE | python3 -c "import sys, json; print(len(json.load(sys.stdin)['platforms']))")
    echo "   ✅ 平台API正常"
    echo "   🌍 已配置平台: $PLATFORM_COUNT 个"
else
    echo "   ❌ 平台API失败"
fi

# 测试待审核项目API
echo ""
echo "4️⃣ 测试待审核项目API..."
RESPONSE=$(curl -s ${API_URL}/api/v1/admin/pending-projects)
if echo $RESPONSE | grep -q "success"; then
    PENDING_COUNT=$(echo $RESPONSE | python3 -c "import sys, json; print(len(json.load(sys.stdin)['projects']))")
    STATS=$(echo $RESPONSE | python3 -c "import sys, json; stats=json.load(sys.stdin)['stats']; print(f\"待审核:{stats.get('pending',0)} 已批准:{stats.get('approved',0)} 已拒绝:{stats.get('rejected',0)}\")")
    echo "   ✅ 待审核项目API正常"
    echo "   📋 $STATS"
else
    echo "   ❌ 待审核项目API失败"
fi

# 测试AI工作配置API
echo ""
echo "5️⃣ 测试AI工作配置API..."
RESPONSE=$(curl -s ${API_URL}/api/v1/admin/ai-work-config)
if echo $RESPONSE | grep -q "success"; then
    MIN_SCORE=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['config']['min_ai_score'])")
    MAX_PROJECTS=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['config']['max_projects_per_day'])")
    echo "   ✅ AI工作配置API正常"
    echo "   🎯 最低推荐分数: $MIN_SCORE"
    echo "   📈 每日推荐上限: $MAX_PROJECTS"
else
    echo "   ❌ AI工作配置API失败"
fi

# 测试Celery状态
echo ""
echo "6️⃣ 测试Celery状态API..."
RESPONSE=$(curl -s ${API_URL}/api/v1/admin/celery-status)
if echo $RESPONSE | grep -q "worker_running"; then
    WORKER=$(echo $RESPONSE | python3 -c "import sys, json; print('运行中' if json.load(sys.stdin)['worker_running'] else '已停止')")
    BEAT=$(echo $RESPONSE | python3 -c "import sys, json; print('运行中' if json.load(sys.stdin)['beat_running'] else '已停止')")
    echo "   ✅ Celery状态API正常"
    echo "   🔧 Worker: $WORKER"
    echo "   ⏰ Beat: $BEAT"
else
    echo "   ❌ Celery状态API失败"
fi

# 测试前端
echo ""
echo "7️⃣ 测试前端服务..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "   ✅ 前端服务正常"
    echo "   🌐 访问地址: http://localhost:3000"
else
    echo "   ⚠️  前端服务未启动或无法访问"
fi

echo ""
echo "===================================="
echo "✅ 系统测试完成！"
echo ""
echo "📱 快速访问:"
echo "   登录页面: http://localhost:3000/login"
echo "   系统管理: http://localhost:3000/admin"
echo "   项目审核: http://localhost:3000/review"
echo "   API文档: http://localhost:8000/docs"
echo "===================================="

