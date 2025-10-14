#!/bin/bash

# 🚀 增强的项目创建工具 - 自动包含上下文记忆系统
#
# 用途: 创建新项目并自动初始化上下文系统
# 使用: mkproject my-new-project
# 版本: v1.0

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
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 显示帮助
show_help() {
    cat << EOF
🚀 增强的项目创建工具

用途:
  创建新项目并自动初始化 Claude Code 上下文记忆系统

使用方法:
  mkproject <项目名称> [选项]

示例:
  mkproject my-awesome-app           # 创建项目
  mkproject my-app --git             # 创建项目 + 初始化 git
  mkproject my-app --full            # 完整初始化（git + 上下文系统）
  mkproject my-app -i                # 交互式初始化

选项:
  -h, --help              显示帮助信息
  -g, --git               初始化 git 仓库
  -f, --full              完整初始化（git + 上下文 + .gitignore）
  -i, --interactive       交互式初始化上下文系统
  -t, --template <类型>   使用项目模板（web/api/cli/lib）
  --no-context            不初始化上下文系统

模板类型:
  web                     Web 应用（Next.js/React/Vue）
  api                     API 服务（FastAPI/Express）
  cli                     CLI 工具
  lib                     库/包项目
  full                    全栈项目（前端 + 后端）

EOF
}

# 创建 .gitignore 文件
create_gitignore() {
    local project_dir=$1

    print_info "创建 .gitignore..."

    cat > "$project_dir/.gitignore" << 'EOF'
# 依赖
node_modules/
venv/
__pycache__/
*.pyc
.Python

# 环境变量
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# 构建输出
dist/
build/
*.log

# 测试
coverage/
.pytest_cache/

# 其他
*.bak
.cache/
EOF

    print_success ".gitignore 创建完成"
}

# 创建 README.md
create_readme() {
    local project_dir=$1
    local project_name=$(basename "$project_dir")

    print_info "创建 README.md..."

    cat > "$project_dir/README.md" << EOF
# $project_name

> 项目简介

## 🚀 快速开始

\`\`\`bash
# 安装依赖
npm install  # 或 pip install -r requirements.txt

# 启动开发服务器
npm run dev  # 或 python main.py
\`\`\`

## 📖 文档

- [项目上下文](./.claudecontext) - AI 助手项目记忆
- [开发规范](./.clinerules) - 开发规范和约束
- [AI 入口](./AI_START_HERE.md) - AI 助手快速开始

## 🤖 AI 协作

本项目配备了完整的 AI 上下文记忆系统。新对话时：

\`\`\`bash
# AI 助手请先阅读
cat .claudecontext
cat .clinerules
\`\`\`

## 🔧 开发

\`\`\`bash
# 开发命令
npm run dev

# 构建
npm run build

# 测试
npm test
\`\`\`

## 📝 许可证

MIT

---

📅 创建时间: $(date +%Y-%m-%d)
🤖 使用 [mkproject](https://github.com) 创建
EOF

    print_success "README.md 创建完成"
}

# 根据模板创建项目结构
create_project_structure() {
    local project_dir=$1
    local template=$2

    case $template in
        web)
            print_info "创建 Web 应用结构..."
            mkdir -p "$project_dir/src"
            mkdir -p "$project_dir/public"
            mkdir -p "$project_dir/components"
            ;;
        api)
            print_info "创建 API 服务结构..."
            mkdir -p "$project_dir/app"
            mkdir -p "$project_dir/tests"
            mkdir -p "$project_dir/docs"
            ;;
        cli)
            print_info "创建 CLI 工具结构..."
            mkdir -p "$project_dir/src"
            mkdir -p "$project_dir/bin"
            mkdir -p "$project_dir/tests"
            ;;
        lib)
            print_info "创建库项目结构..."
            mkdir -p "$project_dir/src"
            mkdir -p "$project_dir/tests"
            mkdir -p "$project_dir/examples"
            ;;
        full)
            print_info "创建全栈项目结构..."
            mkdir -p "$project_dir/frontend"
            mkdir -p "$project_dir/backend"
            mkdir -p "$project_dir/docs"
            mkdir -p "$project_dir/scripts"
            ;;
    esac
}

# 主函数
main() {
    print_header "🚀 创建新项目"

    # 参数解析
    PROJECT_NAME=""
    INIT_GIT=false
    FULL_INIT=false
    INTERACTIVE=false
    NO_CONTEXT=false
    TEMPLATE=""

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -g|--git)
                INIT_GIT=true
                shift
                ;;
            -f|--full)
                FULL_INIT=true
                INIT_GIT=true
                shift
                ;;
            -i|--interactive)
                INTERACTIVE=true
                shift
                ;;
            --no-context)
                NO_CONTEXT=true
                shift
                ;;
            -t|--template)
                TEMPLATE=$2
                shift 2
                ;;
            *)
                if [ -z "$PROJECT_NAME" ]; then
                    PROJECT_NAME=$1
                else
                    print_error "未知参数: $1"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # 检查项目名称
    if [ -z "$PROJECT_NAME" ]; then
        print_error "请提供项目名称"
        echo ""
        show_help
        exit 1
    fi

    # 检查目录是否已存在
    if [ -d "$PROJECT_NAME" ]; then
        print_error "目录已存在: $PROJECT_NAME"
        exit 1
    fi

    print_info "项目名称: $PROJECT_NAME"
    if [ -n "$TEMPLATE" ]; then
        print_info "项目模板: $TEMPLATE"
    fi
    echo ""

    # 创建项目目录
    print_info "创建项目目录..."
    mkdir -p "$PROJECT_NAME"
    PROJECT_DIR=$(cd "$PROJECT_NAME" && pwd)
    print_success "目录创建完成: $PROJECT_DIR"

    # 创建项目结构（如果指定了模板）
    if [ -n "$TEMPLATE" ]; then
        create_project_structure "$PROJECT_DIR" "$TEMPLATE"
        print_success "项目结构创建完成"
    fi

    # 初始化 git
    if [ "$INIT_GIT" = true ] || [ "$FULL_INIT" = true ]; then
        print_header "📦 初始化 Git"
        cd "$PROJECT_DIR"
        git init
        print_success "Git 仓库初始化完成"
    fi

    # 创建 .gitignore 和 README
    if [ "$FULL_INIT" = true ]; then
        create_gitignore "$PROJECT_DIR"
        create_readme "$PROJECT_DIR"
    fi

    # 初始化上下文系统
    if [ "$NO_CONTEXT" = false ]; then
        print_header "🤖 初始化上下文记忆系统"

        # 获取 init-context-system.sh 的路径
        SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
        INIT_SCRIPT="$SCRIPT_DIR/init-context-system.sh"

        if [ ! -f "$INIT_SCRIPT" ]; then
            # 尝试使用全局命令
            if command -v claude-init &> /dev/null; then
                if [ "$INTERACTIVE" = true ]; then
                    claude-init -i "$PROJECT_DIR"
                else
                    claude-init "$PROJECT_DIR"
                fi
            else
                print_warning "找不到 init-context-system.sh 脚本"
                print_info "跳过上下文系统初始化"
            fi
        else
            if [ "$INTERACTIVE" = true ]; then
                "$INIT_SCRIPT" -i "$PROJECT_DIR"
            else
                "$INIT_SCRIPT" "$PROJECT_DIR"
            fi
        fi
    fi

    # 完成提示
    print_header "🎉 项目创建完成！"

    echo ""
    print_success "项目位置: $PROJECT_DIR"
    echo ""
    print_info "下一步："
    echo "  1. cd $PROJECT_NAME"
    echo "  2. 查看项目文件: ls -la"
    if [ "$NO_CONTEXT" = false ]; then
        echo "  3. 编辑上下文: vim .claudecontext"
        echo "  4. 开始开发 🚀"
    else
        echo "  3. 开始开发 🚀"
    fi
    echo ""

    # 显示项目结构
    print_info "项目结构:"
    cd "$PROJECT_DIR"
    if command -v tree &> /dev/null; then
        tree -L 2 -a
    else
        ls -la
    fi
}

# 执行主函数
main "$@"
