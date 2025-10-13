#!/bin/bash

# Chrome DevTools MCP 快速配置脚本
# 用法: ./chrome-mcp-quick-setup.sh [场景名称]

set -e

CONFIG_FILE="$HOME/.cursor/mcp.json"
BACKUP_FILE="$HOME/.cursor/mcp.json.backup.$(date +%Y%m%d_%H%M%S)"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Chrome DevTools MCP 配置工具${NC}"
echo -e "${BLUE}======================================${NC}\n"

# 备份现有配置
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}📦 备份现有配置到: $BACKUP_FILE${NC}"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
fi

# 配置场景
show_menu() {
    echo -e "${GREEN}请选择配置场景:${NC}\n"
    echo "1) 日常开发 - 连接已有浏览器 (推荐)"
    echo "2) 自动化测试 - 无头模式"
    echo "3) 性能测试 - 固定环境"
    echo "4) 移动端测试 - 小屏幕"
    echo "5) 网络调试 - 使用代理"
    echo "6) 多配置 - 同时安装所有场景"
    echo "7) 最小配置 - 默认设置"
    echo "0) 退出"
    echo ""
    read -p "请输入选项 [0-7]: " choice
}

# 场景 1: 日常开发
config_dev() {
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--browserUrl", "http://127.0.0.1:9222"
    ],
    "env": {}
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 日常开发模式${NC}"
    echo -e "${YELLOW}📌 使用前需要先启动 Chrome:${NC}"
    echo -e "   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug\n"
}

# 场景 2: 自动化测试
config_test() {
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--headless",
      "--isolated"
    ],
    "env": {}
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 自动化测试模式（无头模式）${NC}\n"
}

# 场景 3: 性能测试
config_perf() {
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--isolated",
      "--viewport", "1920x1080",
      "--logFile", "/tmp/chrome-mcp-perf.log"
    ],
    "env": {
      "DEBUG": "*"
    }
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 性能测试模式${NC}"
    echo -e "${YELLOW}📌 日志文件: /tmp/chrome-mcp-perf.log${NC}\n"
}

# 场景 4: 移动端测试
config_mobile() {
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--viewport", "375x667",
      "--isolated"
    ],
    "env": {}
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 移动端测试模式（iPhone 8 尺寸）${NC}\n"
}

# 场景 5: 网络调试
config_proxy() {
    read -p "请输入代理服务器地址 (默认: http://127.0.0.1:8888): " proxy
    proxy=${proxy:-http://127.0.0.1:8888}
    
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--proxyServer", "$proxy"
    ],
    "env": {}
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 网络调试模式（代理: $proxy）${NC}\n"
}

# 场景 6: 多配置
config_multi() {
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools-remote": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--browserUrl", "http://127.0.0.1:9222"
    ],
    "env": {}
  },
  "chrome-devtools-headless": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--headless",
      "--isolated"
    ],
    "env": {}
  },
  "chrome-devtools-mobile": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--viewport", "375x667",
      "--isolated"
    ],
    "env": {}
  },
  "chrome-devtools-desktop": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--viewport", "1920x1080",
      "--isolated"
    ],
    "env": {}
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 多场景配置${NC}"
    echo -e "${YELLOW}📌 可用的配置:${NC}"
    echo "   - chrome-devtools-remote (连接已有浏览器)"
    echo "   - chrome-devtools-headless (无头模式)"
    echo "   - chrome-devtools-mobile (移动端)"
    echo "   - chrome-devtools-desktop (桌面端)"
    echo ""
}

# 场景 7: 最小配置
config_minimal() {
    cat > /tmp/chrome-mcp-config.json <<EOF
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["chrome-devtools-mcp@latest"],
    "env": {}
  }
}
EOF
    echo -e "\n${GREEN}✅ 已配置: 最小配置（默认设置）${NC}\n"
}

# 合并配置到主文件
merge_config() {
    if [ -f "$CONFIG_FILE" ]; then
        # 使用 Python 合并 JSON（如果有的话）
        if command -v python3 &> /dev/null; then
            python3 <<EOF
import json
import sys

# 读取现有配置
with open('$CONFIG_FILE', 'r') as f:
    main_config = json.load(f)

# 读取新配置
with open('/tmp/chrome-mcp-config.json', 'r') as f:
    new_config = json.load(f)

# 合并 mcpServers
if 'mcpServers' not in main_config:
    main_config['mcpServers'] = {}

main_config['mcpServers'].update(new_config)

# 写回
with open('$CONFIG_FILE', 'w') as f:
    json.dump(main_config, f, indent=2)

print("配置已成功合并")
EOF
        else
            echo -e "${RED}❌ 未找到 Python3，无法自动合并配置${NC}"
            echo -e "${YELLOW}📌 请手动将 /tmp/chrome-mcp-config.json 的内容合并到 $CONFIG_FILE${NC}"
            return 1
        fi
    else
        # 创建新配置文件
        echo "{\"mcpServers\": $(cat /tmp/chrome-mcp-config.json)}" > "$CONFIG_FILE"
    fi
    
    echo -e "${GREEN}✅ 配置已写入: $CONFIG_FILE${NC}\n"
}

# 显示启动 Chrome 的帮助
show_chrome_help() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  如何启动 Chrome 远程调试${NC}"
    echo -e "${BLUE}======================================${NC}\n"
    echo -e "${GREEN}方法 1: 直接运行${NC}"
    echo '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug'
    echo ""
    echo -e "${GREEN}方法 2: 创建别名（推荐）${NC}"
    echo "在 ~/.zshrc 或 ~/.bashrc 中添加:"
    echo 'alias chrome-debug="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug &"'
    echo ""
    echo "然后运行: chrome-debug"
    echo ""
    echo -e "${GREEN}方法 3: 创建启动脚本${NC}"
    echo "查看项目中的 guides/config/scripts/start-chrome-debug.sh"
    echo ""
}

# 主流程
main() {
    if [ "$1" != "" ]; then
        case $1 in
            dev) config_dev; merge_config ;;
            test) config_test; merge_config ;;
            perf) config_perf; merge_config ;;
            mobile) config_mobile; merge_config ;;
            proxy) config_proxy; merge_config ;;
            multi) config_multi; merge_config ;;
            minimal) config_minimal; merge_config ;;
            help) show_chrome_help; exit 0 ;;
            *) echo "未知选项: $1"; exit 1 ;;
        esac
    else
        show_menu
        case $choice in
            1) config_dev; merge_config ;;
            2) config_test; merge_config ;;
            3) config_perf; merge_config ;;
            4) config_mobile; merge_config ;;
            5) config_proxy; merge_config ;;
            6) config_multi; merge_config ;;
            7) config_minimal; merge_config ;;
            0) echo "退出"; exit 0 ;;
            *) echo -e "${RED}无效选项${NC}"; exit 1 ;;
        esac
    fi
    
    echo -e "${GREEN}🎉 配置完成！${NC}"
    echo -e "${YELLOW}💡 提示: 重启 Cursor 以使配置生效${NC}\n"
    
    # 如果是远程调试配置，显示帮助
    if [ "$choice" = "1" ] || [ "$1" = "dev" ]; then
        show_chrome_help
    fi
}

main "$@"

