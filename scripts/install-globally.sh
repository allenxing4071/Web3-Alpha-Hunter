#!/bin/bash

# 🌐 全局安装 Claude Code 上下文记忆系统初始化工具
#
# 用途: 将 init-context-system.sh 安装到全局，任何地方都可以使用
# 使用: ./install-globally.sh

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# 主函数
main() {
    print_header "🌐 全局安装 Claude Code 上下文记忆系统"

    # 获取脚本所在目录
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    SOURCE_SCRIPT="$SCRIPT_DIR/init-context-system.sh"

    # 检查源脚本是否存在
    if [ ! -f "$SOURCE_SCRIPT" ]; then
        print_error "找不到 init-context-system.sh"
        print_info "请确保在正确的目录运行此脚本"
        exit 1
    fi

    print_info "源脚本: $SOURCE_SCRIPT"
    echo ""

    # 选择安装位置
    print_info "请选择安装方式："
    echo "  1) 安装到 /usr/local/bin (推荐，需要 sudo)"
    echo "  2) 安装到 ~/.local/bin (用户目录，无需 sudo)"
    echo "  3) 创建全局 alias (最简单)"
    echo "  4) 取消安装"
    echo ""
    read -p "请选择 (1-4): " choice

    case $choice in
        1)
            install_to_usr_local
            ;;
        2)
            install_to_local_bin
            ;;
        3)
            create_alias
            ;;
        4)
            print_info "已取消安装"
            exit 0
            ;;
        *)
            print_error "无效选择"
            exit 1
            ;;
    esac
}

# 安装到 /usr/local/bin
install_to_usr_local() {
    print_header "📦 安装到 /usr/local/bin"

    TARGET="/usr/local/bin/claude-init"

    print_info "复制脚本到 $TARGET..."
    sudo cp "$SOURCE_SCRIPT" "$TARGET"
    sudo chmod +x "$TARGET"

    print_success "安装完成！"
    echo ""
    print_info "现在你可以在任何目录运行："
    echo "  claude-init              # 在当前目录初始化"
    echo "  claude-init -i           # 交互式初始化"
    echo "  claude-init /path/to/dir # 在指定目录初始化"
    echo ""
    test_installation "claude-init"
}

# 安装到 ~/.local/bin
install_to_local_bin() {
    print_header "📦 安装到 ~/.local/bin"

    LOCAL_BIN="$HOME/.local/bin"
    TARGET="$LOCAL_BIN/claude-init"

    # 创建目录（如果不存在）
    if [ ! -d "$LOCAL_BIN" ]; then
        print_info "创建目录 $LOCAL_BIN..."
        mkdir -p "$LOCAL_BIN"
    fi

    # 复制脚本
    print_info "复制脚本到 $TARGET..."
    cp "$SOURCE_SCRIPT" "$TARGET"
    chmod +x "$TARGET"

    # 检查 PATH
    if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
        print_warning "$LOCAL_BIN 不在 PATH 中"
        echo ""
        print_info "请添加以下内容到你的 shell 配置文件："

        # 检测 shell 类型
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        else
            SHELL_RC="$HOME/.profile"
        fi

        echo ""
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        print_info "添加到: $SHELL_RC"
        echo ""
        read -p "是否自动添加？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "" >> "$SHELL_RC"
            echo "# Claude Code Context System" >> "$SHELL_RC"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
            print_success "已添加到 $SHELL_RC"
            print_warning "请运行: source $SHELL_RC 或重新打开终端"
        fi
    fi

    print_success "安装完成！"
    echo ""
    print_info "现在你可以在任何目录运行："
    echo "  claude-init              # 在当前目录初始化"
    echo "  claude-init -i           # 交互式初始化"
    echo "  claude-init /path/to/dir # 在指定目录初始化"
    echo ""
    test_installation "claude-init"
}

# 创建 alias
create_alias() {
    print_header "🔗 创建全局 alias"

    # 检测 shell 类型
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
        SHELL_NAME="zsh"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
        SHELL_NAME="bash"
    else
        SHELL_RC="$HOME/.profile"
        SHELL_NAME="shell"
    fi

    print_info "将添加 alias 到: $SHELL_RC"
    echo ""

    # 添加 alias
    echo "" >> "$SHELL_RC"
    echo "# Claude Code Context System" >> "$SHELL_RC"
    echo "alias claude-init='$SOURCE_SCRIPT'" >> "$SHELL_RC"

    print_success "Alias 创建完成！"
    echo ""
    print_warning "请运行以下命令使 alias 生效："
    echo "  source $SHELL_RC"
    echo ""
    print_info "或者重新打开终端"
    echo ""
    print_info "之后你可以在任何目录运行："
    echo "  claude-init              # 在当前目录初始化"
    echo "  claude-init -i           # 交互式初始化"
    echo "  claude-init /path/to/dir # 在指定目录初始化"
}

# 测试安装
test_installation() {
    local cmd=$1
    print_info "测试安装..."

    if command -v "$cmd" &> /dev/null; then
        print_success "✓ $cmd 命令可用"
        echo ""
        $cmd --version
    else
        print_warning "命令未在 PATH 中，可能需要重新打开终端"
    fi
}

# 执行主函数
main "$@"
