#!/bin/bash

# 🚀 彻底修复部署脚本
# 直接在服务器上修改文件并重启服务

SERVER="root@web3.guandongfang.cn"
FRONTEND_DIR="/root/projects/web3/frontend"

echo "🔧 开始彻底修复..."
echo "================================"

# 1. 备份当前文件
echo "📦 1. 备份当前文件..."
ssh $SERVER "cd $FRONTEND_DIR && \
  mkdir -p backups && \
  cp src/store/authStore.ts backups/authStore.ts.bak 2>/dev/null || true && \
  cp src/store/userStore.ts backups/userStore.ts.bak 2>/dev/null || true && \
  cp src/app/login/page.tsx backups/login.tsx.bak 2>/dev/null || true"

# 2. 上传修复后的文件
echo "📤 2. 上传修复文件..."
scp frontend/src/store/authStore.ts $SERVER:$FRONTEND_DIR/src/store/
scp frontend/src/store/userStore.ts $SERVER:$FRONTEND_DIR/src/store/
scp frontend/src/app/login/page.tsx $SERVER:$FRONTEND_DIR/src/app/login/

# 3. 清理并重新构建
echo "🏗️  3. 清理并重新构建..."
ssh $SERVER "cd $FRONTEND_DIR && \
  rm -rf .next && \
  echo '清理完成,开始构建...' && \
  npm run build"

# 4. 重启服务
echo "🔄 4. 重启前端服务..."
ssh $SERVER "pm2 restart web3-frontend"

# 5. 检查服务状态
echo "✅ 5. 检查服务状态..."
ssh $SERVER "pm2 info web3-frontend | grep -E 'status|uptime|restarts'"

echo ""
echo "================================"
echo "✅ 部署完成!"
echo ""
echo "🧪 测试地址:"
echo "   登录页: http://web3.guandongfang.cn/login"
echo ""
echo "🔐 测试账号:"
echo "   用户名: admin"
echo "   密码: admin123"
echo ""
echo "⏳ 请等待 10 秒让服务完全启动..."

