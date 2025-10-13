#!/bin/bash

# Chrome 远程调试停止脚本
# 用法: ./stop-chrome-debug.sh [端口号]

PORT=${1:-9222}

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🛑 停止端口 $PORT 上的 Chrome 进程...${NC}\n"

# 查找并终止进程
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    PIDS=$(lsof -ti:$PORT)
    echo -e "${YELLOW}找到进程: $PIDS${NC}"
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    sleep 1
    
    # 验证是否成功
    if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${GREEN}✅ Chrome 已停止${NC}\n"
    else
        echo -e "${RED}❌ 停止失败，请手动终止进程${NC}\n"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  端口 $PORT 上没有运行的进程${NC}\n"
fi

# 清理用户数据目录（可选）
USER_DATA_DIR="/tmp/chrome-debug-$PORT"
if [ -d "$USER_DATA_DIR" ]; then
    read -p "是否删除临时数据目录? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$USER_DATA_DIR"
        echo -e "${GREEN}✅ 已清理: $USER_DATA_DIR${NC}\n"
    fi
fi




