#!/bin/bash

# 🚀 彻底修复部署脚本 (使用SSH密钥)
# 直接在服务器上修改文件并重启服务

SERVER="root@47.253.226.250"
SSH_KEY="guides/config/keys/VPNKEY.pem"
FRONTEND_DIR="/root/projects/web3/frontend"
LOCAL_DIR="/Users/xinghailong/Documents/soft/faxianjihui/frontend"

echo "🔧 开始彻底修复..."
echo "================================"

# 0. 测试连接
echo "🔍 0. 测试服务器连接..."
if ! ssh -i $SSH_KEY -o ConnectTimeout=5 $SERVER "echo '✅ 连接成功'" 2>/dev/null; then
    echo "❌ 无法连接到服务器"
    exit 1
fi

# 1. 备份当前文件
echo "📦 1. 备份当前文件..."
ssh -i $SSH_KEY $SERVER "cd $FRONTEND_DIR && \
  mkdir -p backups && \
  cp src/store/authStore.ts backups/authStore.ts.bak 2>/dev/null || true && \
  cp src/store/userStore.ts backups/userStore.ts.bak 2>/dev/null || true && \
  cp src/app/login/page.tsx backups/login.tsx.bak 2>/dev/null || true && \
  echo '✅ 备份完成'"

# 2. 上传修复后的文件
echo "📤 2. 上传修复文件..."
scp -i $SSH_KEY $LOCAL_DIR/src/store/authStore.ts $SERVER:$FRONTEND_DIR/src/store/
scp -i $SSH_KEY $LOCAL_DIR/src/store/userStore.ts $SERVER:$FRONTEND_DIR/src/store/
scp -i $SSH_KEY $LOCAL_DIR/src/app/login/page.tsx $SERVER:$FRONTEND_DIR/src/app/login/
echo "✅ 上传完成"

# 3. 清理并重新构建
echo "🏗️  3. 清理并重新构建..."
ssh -i $SSH_KEY $SERVER "cd $FRONTEND_DIR && \
  rm -rf .next && \
  echo '清理完成,开始构建...' && \
  npm run build 2>&1 | tail -20"

# 4. 重启服务
echo "🔄 4. 重启前端服务..."
ssh -i $SSH_KEY $SERVER "pm2 restart web3-frontend"

# 5. 等待服务启动
echo "⏳ 5. 等待服务启动..."
sleep 5

# 6. 检查服务状态
echo "✅ 6. 检查服务状态..."
ssh -i $SSH_KEY $SERVER "pm2 info web3-frontend | grep -E 'status|uptime|restarts'"

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

