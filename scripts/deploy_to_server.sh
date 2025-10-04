#!/bin/bash

# Web3 Alpha Hunter 部署脚本
# 将本地更新部署到生产服务器

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SERVER_HOST="47.253.226.250"
SERVER_USER="root"
SSH_KEY="guides/config/keys/VPNKEY.pem"
REMOTE_PATH="/app/web3-alpha-hunter"
LOCAL_PATH="$(pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 Web3 Alpha Hunter 部署工具${NC}"
echo -e "${BLUE}========================================${NC}"

# 检查 SSH 密钥
if [ ! -f "$SSH_KEY" ]; then
    echo -e "${RED}❌ SSH 密钥不存在: $SSH_KEY${NC}"
    exit 1
fi

# 确保密钥权限正确
chmod 600 "$SSH_KEY"

# 检查服务器连接
echo -e "\n${YELLOW}📡 测试服务器连接...${NC}"
if ! ssh -i "$SSH_KEY" -o ConnectTimeout=5 "$SERVER_USER@$SERVER_HOST" "echo '连接成功'" > /dev/null 2>&1; then
    echo -e "${RED}❌ 无法连接到服务器${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 服务器连接正常${NC}"

# 检查本地 Git 状态
echo -e "\n${YELLOW}🔍 检查本地 Git 状态...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  有未提交的更改:${NC}"
    git status --short
    read -p "是否继续部署? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}部署已取消${NC}"
        exit 0
    fi
fi

# 显示最近的提交
echo -e "\n${YELLOW}📝 最近的提交:${NC}"
git log --oneline -5

# 选择部署内容
echo -e "\n${YELLOW}📦 选择要部署的内容:${NC}"
echo "1. 只部署后端代码"
echo "2. 只部署前端代码"
echo "3. 部署后端和前端"
echo "4. 部署配置文件 (API keys, .env)"
echo "5. 完整部署 (所有文件)"
echo "6. 只部署文档和脚本"
read -p "请选择 (1-6, 默认 3): " DEPLOY_CHOICE
DEPLOY_CHOICE=${DEPLOY_CHOICE:-3}

# 备份服务器现有文件
echo -e "\n${YELLOW}💾 备份服务器现有文件...${NC}"
BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_HOST" << EOF
    if [ -d "$REMOTE_PATH" ]; then
        mkdir -p $REMOTE_PATH/backups
        cd $REMOTE_PATH
        tar -czf backups/${BACKUP_NAME}.tar.gz \
            --exclude='backups' \
            --exclude='node_modules' \
            --exclude='__pycache__' \
            --exclude='.next' \
            --exclude='logs' \
            . 2>/dev/null || true
        echo "✅ 备份已创建: ${BACKUP_NAME}.tar.gz"
    fi
EOF

# 根据选择执行部署
case $DEPLOY_CHOICE in
    1)
        echo -e "\n${YELLOW}📤 部署后端代码...${NC}"
        rsync -avz --delete \
            -e "ssh -i $SSH_KEY" \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.env' \
            --exclude='*.json' \
            --exclude='test_*.py' \
            backend/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/backend/"
        ;;
    2)
        echo -e "\n${YELLOW}📤 部署前端代码...${NC}"
        rsync -avz --delete \
            -e "ssh -i $SSH_KEY" \
            --exclude='node_modules' \
            --exclude='.next' \
            --exclude='*.log' \
            frontend/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/frontend/"
        ;;
    3)
        echo -e "\n${YELLOW}📤 部署后端和前端代码...${NC}"
        
        # 后端
        rsync -avz --delete \
            -e "ssh -i $SSH_KEY" \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.env' \
            --exclude='*.json' \
            --exclude='test_*.py' \
            backend/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/backend/"
        
        # 前端
        rsync -avz --delete \
            -e "ssh -i $SSH_KEY" \
            --exclude='node_modules' \
            --exclude='.next' \
            --exclude='*.log' \
            frontend/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/frontend/"
        ;;
    4)
        echo -e "\n${YELLOW}📤 部署配置文件...${NC}"
        echo -e "${RED}⚠️  这将更新 API keys 和环境变量!${NC}"
        read -p "确认继续? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}部署已取消${NC}"
            exit 0
        fi
        
        # 部署 .env 文件
        scp -i "$SSH_KEY" backend/.env "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/backend/.env"
        
        # 部署 API keys (如果需要的话)
        # scp -i "$SSH_KEY" guides/config/keys/api-keys.yaml "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/guides/config/keys/"
        ;;
    5)
        echo -e "\n${YELLOW}📤 完整部署所有文件...${NC}"
        rsync -avz --delete \
            -e "ssh -i $SSH_KEY" \
            --exclude='.git' \
            --exclude='node_modules' \
            --exclude='__pycache__' \
            --exclude='.next' \
            --exclude='*.log' \
            --exclude='backups' \
            --exclude='.env.backup' \
            ./ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/"
        ;;
    6)
        echo -e "\n${YELLOW}📤 部署文档和脚本...${NC}"
        rsync -avz \
            -e "ssh -i $SSH_KEY" \
            docs/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/docs/"
        
        rsync -avz \
            -e "ssh -i $SSH_KEY" \
            guides/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/guides/"
        
        rsync -avz \
            -e "ssh -i $SSH_KEY" \
            scripts/ "$SERVER_USER@$SERVER_HOST:$REMOTE_PATH/scripts/"
        ;;
    *)
        echo -e "${RED}❌ 无效的选项${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}✅ 文件部署完成${NC}"

# 询问是否重启服务
echo -e "\n${YELLOW}🔄 是否需要重启服务?${NC}"
echo "1. 重启后端 (Docker)"
echo "2. 重启前端"
echo "3. 重启所有服务"
echo "4. 不重启"
read -p "请选择 (1-4, 默认 4): " RESTART_CHOICE
RESTART_CHOICE=${RESTART_CHOICE:-4}

case $RESTART_CHOICE in
    1)
        echo -e "\n${YELLOW}🔄 重启后端服务...${NC}"
        ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_HOST" << 'EOF'
            cd /app/web3-alpha-hunter
            docker-compose restart api
            echo "✅ 后端已重启"
EOF
        ;;
    2)
        echo -e "\n${YELLOW}🔄 重建前端...${NC}"
        ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_HOST" << 'EOF'
            cd /app/web3-alpha-hunter/frontend
            npm run build
            pm2 restart web3-frontend || echo "⚠️  请手动重启前端"
            echo "✅ 前端已重建"
EOF
        ;;
    3)
        echo -e "\n${YELLOW}🔄 重启所有服务...${NC}"
        ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_HOST" << 'EOF'
            cd /app/web3-alpha-hunter
            docker-compose restart
            cd frontend
            npm run build
            pm2 restart all || echo "⚠️  请手动重启前端"
            echo "✅ 所有服务已重启"
EOF
        ;;
    4)
        echo -e "${BLUE}ℹ️  跳过服务重启${NC}"
        ;;
esac

# 检查服务状态
echo -e "\n${YELLOW}🔍 检查服务状态...${NC}"
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_HOST" << 'EOF'
    echo "Docker 容器状态:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "磁盘使用:"
    df -h /app | tail -1
    echo ""
    echo "内存使用:"
    free -h | grep Mem
EOF

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ 部署完成!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${BLUE}📋 后续操作:${NC}"
echo "1. 访问前端: http://web3.guandongfang.cn"
echo "2. 访问 API 文档: http://web3.guandongfang.cn/api/v1/docs"
echo "3. 查看日志: ssh -i $SSH_KEY root@47.253.226.250 'docker logs -f web3_api'"
echo "4. 恢复备份: ssh -i $SSH_KEY root@47.253.226.250 'cd $REMOTE_PATH/backups && tar -xzf ${BACKUP_NAME}.tar.gz'"

echo -e "\n${YELLOW}💡 提示:${NC}"
echo "- 备份保存在: $REMOTE_PATH/backups/${BACKUP_NAME}.tar.gz"
echo "- 如有问题可随时恢复备份"

