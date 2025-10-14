#!/bin/bash

# Chrome 远程调试启动脚本
# 用法: ./start-chrome-debug.sh [端口号]

PORT=${1:-9222}
USER_DATA_DIR="/tmp/chrome-debug-$PORT"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  启动 Chrome 远程调试${NC}"
echo -e "${BLUE}======================================${NC}\n"

# 检查端口是否被占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  端口 $PORT 已被占用${NC}"
    echo -e "${YELLOW}   正在终止占用端口的进程...${NC}\n"
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    sleep 1
fi

# 创建用户数据目录
mkdir -p "$USER_DATA_DIR"

# 启动 Chrome
echo -e "${GREEN}🚀 启动参数:${NC}"
echo -e "   端口: ${BLUE}$PORT${NC}"
echo -e "   用户目录: ${BLUE}$USER_DATA_DIR${NC}"
echo -e "   访问: ${BLUE}http://127.0.0.1:$PORT${NC}\n"

# macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if [ ! -f "$CHROME_PATH" ]; then
        echo -e "${YELLOW}⚠️  未找到 Chrome，请确认已安装${NC}"
        exit 1
    fi
    
    "$CHROME_PATH" \
        --remote-debugging-port=$PORT \
        --user-data-dir="$USER_DATA_DIR" \
        --no-first-run \
        --no-default-browser-check \
        > /tmp/chrome-debug-$PORT.log 2>&1 &
    
    CHROME_PID=$!
    echo -e "${GREEN}✅ Chrome 已启动 (PID: $CHROME_PID)${NC}"
    echo -e "${YELLOW}📝 日志文件: /tmp/chrome-debug-$PORT.log${NC}\n"
    
# Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v google-chrome &> /dev/null; then
        CHROME_CMD="google-chrome"
    elif command -v chromium-browser &> /dev/null; then
        CHROME_CMD="chromium-browser"
    else
        echo -e "${YELLOW}⚠️  未找到 Chrome/Chromium${NC}"
        exit 1
    fi
    
    $CHROME_CMD \
        --remote-debugging-port=$PORT \
        --user-data-dir="$USER_DATA_DIR" \
        --no-first-run \
        --no-default-browser-check \
        > /tmp/chrome-debug-$PORT.log 2>&1 &
    
    CHROME_PID=$!
    echo -e "${GREEN}✅ Chrome 已启动 (PID: $CHROME_PID)${NC}"
    echo -e "${YELLOW}📝 日志文件: /tmp/chrome-debug-$PORT.log${NC}\n"
else
    echo -e "${YELLOW}⚠️  不支持的操作系统: $OSTYPE${NC}"
    exit 1
fi

# 等待 Chrome 启动
echo -e "${BLUE}⏳ 等待 Chrome 启动...${NC}"
sleep 2

# 检查是否启动成功
if ps -p $CHROME_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Chrome 远程调试已就绪！${NC}\n"
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  连接信息${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo -e "调试端口: ${GREEN}http://127.0.0.1:$PORT${NC}"
    echo -e "进程 PID: ${GREEN}$CHROME_PID${NC}"
    echo -e "用户目录: ${GREEN}$USER_DATA_DIR${NC}"
    echo -e "\n${YELLOW}💡 在 MCP 配置中使用:${NC}"
    echo -e '   "args": ["chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:'$PORT'"]'
    echo -e "\n${YELLOW}🛑 停止 Chrome:${NC}"
    echo -e "   kill $CHROME_PID"
    echo -e "   或运行: ./stop-chrome-debug.sh $PORT"
    echo ""
else
    echo -e "${YELLOW}⚠️  Chrome 启动失败，请查看日志: /tmp/chrome-debug-$PORT.log${NC}"
    exit 1
fi





