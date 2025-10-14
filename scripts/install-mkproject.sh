#!/bin/bash

# 🌐 全局安装 mkproject 工具
#
# 用途: 将 mkproject 安装到全局，实现自动化项目创建

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

main() {
    print_header "🚀 安装 mkproject 工具"

    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    SOURCE_MKPROJECT="$SCRIPT_DIR/mkproject.sh"
    SOURCE_INIT="$SCRIPT_DIR/init-context-system.sh"

    # 检查文件
    if [ ! -f "$SOURCE_MKPROJECT" ]; then
        print_error "找不到 mkproject.sh"
        exit 1
    fi

    print_info "请选择安装方式："
    echo "  1) 安装到 /usr/local/bin (推荐，需要 sudo)"
    echo "  2) 安装到 ~/.local/bin (用户目录)"
    echo "  3) 创建 alias (最简单) ⭐"
    echo "  4) 取消"
    echo ""
    read -p "请选择 (1-4): " choice

    case $choice in
        1)
            print_info "安装到 /usr/local/bin..."
            sudo cp "$SOURCE_MKPROJECT" /usr/local/bin/mkproject
            sudo chmod +x /usr/local/bin/mkproject

            # 同时安装 init-context-system.sh
            if [ -f "$SOURCE_INIT" ]; then
                sudo cp "$SOURCE_INIT" /usr/local/bin/claude-init
                sudo chmod +x /usr/local/bin/claude-init
                print_success "claude-init 也已安装"
            fi

            print_success "安装完成！"
            echo ""
            print_info "现在可以使用："
            echo "  mkproject my-app          # 创建项目"
            echo "  mkproject my-app --full   # 完整初始化"
            echo "  mkproject my-app -i       # 交互式"
            ;;
        2)
            LOCAL_BIN="$HOME/.local/bin"
            mkdir -p "$LOCAL_BIN"

            print_info "安装到 ~/.local/bin..."
            cp "$SOURCE_MKPROJECT" "$LOCAL_BIN/mkproject"
            chmod +x "$LOCAL_BIN/mkproject"

            if [ -f "$SOURCE_INIT" ]; then
                cp "$SOURCE_INIT" "$LOCAL_BIN/claude-init"
                chmod +x "$LOCAL_BIN/claude-init"
                print_success "claude-init 也已安装"
            fi

            # 检查 PATH
            if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
                print_warning "$LOCAL_BIN 不在 PATH 中"

                if [ -n "$ZSH_VERSION" ]; then
                    SHELL_RC="$HOME/.zshrc"
                else
                    SHELL_RC="$HOME/.bashrc"
                fi

                echo ""
                echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
                print_success "已添加到 $SHELL_RC"
                print_warning "请运行: source $SHELL_RC"
            fi

            print_success "安装完成！"
            ;;
        3)
            if [ -n "$ZSH_VERSION" ]; then
                SHELL_RC="$HOME/.zshrc"
            else
                SHELL_RC="$HOME/.bashrc"
            fi

            print_info "创建 alias..."
            echo "" >> "$SHELL_RC"
            echo "# mkproject - 增强的项目创建工具" >> "$SHELL_RC"
            echo "alias mkproject='$SOURCE_MKPROJECT'" >> "$SHELL_RC"

            if [ -f "$SOURCE_INIT" ]; then
                echo "alias claude-init='$SOURCE_INIT'" >> "$SHELL_RC"
                print_success "claude-init alias 也已创建"
            fi

            print_success "Alias 创建完成！"
            echo ""
            print_warning "请运行: source $SHELL_RC"
            echo ""
            print_info "之后可以使用："
            echo "  mkproject my-app          # 创建项目"
            echo "  mkproject my-app --full   # 完整初始化"
            ;;
        4)
            print_info "已取消"
            exit 0
            ;;
    esac

    echo ""
    print_header "🎉 安装完成！"
    echo ""
    print_info "快速测试："
    echo "  mkproject test-app --full"
    echo ""
}

main "$@"
