# 脚本工具目录

> **目录说明**: 项目启动和管理脚本
> **最后更新**: 2025-10-13

本目录包含项目开发和部署所需的各种脚本工具。

---

## 📂 脚本列表

### 🤖 上下文记忆系统脚本 (新增)

#### 1. init-context-system.sh ⭐
**用途**: 为新项目自动创建 Claude Code 上下文记忆系统

**功能**:
- 自动创建 `.claudecontext` (项目记忆核心)
- 自动创建 `.clinerules` (AI工作规范)
- 自动创建 `AI_START_HERE.md` (AI入口指南)
- 自动创建 `CONTEXT_SYSTEM_README.md` (系统说明)
- 支持交互式初始化（收集项目信息）

**使用方法**:
```bash
# 基本用法：在当前目录初始化
./scripts/init-context-system.sh

# 交互式初始化（推荐）
./scripts/init-context-system.sh -i

# 在指定目录初始化
./scripts/init-context-system.sh /path/to/project

# 强制覆盖已存在的文件
./scripts/init-context-system.sh -f

# 查看帮助
./scripts/init-context-system.sh --help
```

**详细文档**: [README_CONTEXT_SYSTEM.md](./README_CONTEXT_SYSTEM.md)

---

#### 2. install-globally.sh
**用途**: 全局安装上下文系统初始化工具

**功能**:
- 安装到 `/usr/local/bin` (系统级)
- 安装到 `~/.local/bin` (用户级)
- 创建 shell alias
- 自动配置 PATH

**使用方法**:
```bash
./scripts/install-globally.sh

# 然后在任何地方使用
claude-init              # 初始化当前目录
claude-init -i           # 交互式初始化
claude-init /path/to/dir # 初始化指定目录
```

**优势**:
- ✅ 一次安装，全局使用
- ✅ 新建项目自动包含上下文系统
- ✅ 提升开发效率 80%+

---

### 开发环境脚本

#### 1. start-dev.sh
**用途**: 启动完整开发环境

**功能**:
- 启动PostgreSQL数据库 (Docker)
- 启动Redis (Docker)
- 启动后端服务 (FastAPI)
- 启动前端服务 (Next.js)
- 启动Celery Worker
- 启动Celery Beat

**使用方法**:
```bash
./scripts/start-dev.sh
```

**依赖检查**:
- Docker Desktop 运行中
- Python 3.11+ 已安装
- Node.js 18+ 已安装
- 虚拟环境已创建

---

#### 2. stop-dev.sh
**用途**: 停止开发环境所有服务

**功能**:
- 停止前端 (Next.js)
- 停止后端 (FastAPI)
- 停止Celery Worker
- 停止Celery Beat
- 停止Docker容器 (PostgreSQL/Redis)

**使用方法**:
```bash
./scripts/stop-dev.sh
```

**安全提示**:
- 会保存数据库数据 (Docker卷持久化)
- 会终止所有Python进程 (谨慎使用)

---

### 后端服务脚本

#### 3. start_backend.sh
**用途**: 单独启动后端服务

**功能**:
- 检查虚拟环境
- 启动Uvicorn服务器
- 监听端口: 8000

**使用方法**:
```bash
./scripts/start_backend.sh
```

**前提条件**:
- 数据库已启动
- Redis已启动
- 虚拟环境已激活

---

### Celery任务队列脚本

#### 4. start-celery.sh
**用途**: 启动Celery异步任务服务

**功能**:
- 启动Celery Worker (执行异步任务)
- 启动Celery Beat (定时任务调度)

**使用方法**:
```bash
./scripts/start-celery.sh
```

**日志位置**:
- Worker日志: `logs/celery_worker.log`
- Beat日志: `logs/celery_beat.log`

**监控命令**:
```bash
# 查看Worker状态
celery -A app.tasks.celery inspect active

# 查看定时任务
celery -A app.tasks.celery inspect scheduled
```

---

#### 5. stop-celery.sh
**用途**: 停止Celery服务

**功能**:
- 优雅停止Celery Worker
- 优雅停止Celery Beat
- 清理PID文件

**使用方法**:
```bash
./scripts/stop-celery.sh
```

---

## 🚀 快速使用指南

### 首次启动完整环境

```bash
# 1. 确保Docker Desktop运行中
# 2. 进入项目目录
cd /path/to/faxianjihui

# 3. 启动完整开发环境
./scripts/start-dev.sh

# 4. 等待所有服务启动完成
# - 后端: http://localhost:8000
# - 前端: http://localhost:3000
# - API文档: http://localhost:8000/docs
```

### 停止所有服务

```bash
./scripts/stop-dev.sh
```

### 单独启动某个服务

```bash
# 只启动后端
./scripts/start_backend.sh

# 只启动Celery
./scripts/start-celery.sh
```

---

## 📝 脚本说明

### start-dev.sh 详细流程

```bash
#!/bin/bash
# 1. 检查Docker状态
# 2. 启动数据库和Redis容器
# 3. 等待数据库就绪
# 4. 启动后端服务 (后台)
# 5. 启动前端服务 (后台)
# 6. 启动Celery服务
# 7. 显示服务状态
```

**关键参数**:
- 后端端口: `8000`
- 前端端口: `3000`
- PostgreSQL端口: `5432`
- Redis端口: `6379`

---

### stop-dev.sh 详细流程

```bash
#!/bin/bash
# 1. 停止前端进程 (pkill node)
# 2. 停止后端进程 (pkill python)
# 3. 停止Celery进程
# 4. 停止Docker容器
# 5. 清理临时文件
```

**警告**:
- `pkill python` 会终止所有Python进程
- 如果系统有其他Python应用在运行,请谨慎使用

---

## 🔧 自定义配置

### 修改端口

编辑 `start_backend.sh`:
```bash
# 修改这一行
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# 改为
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 修改日志路径

编辑 `start-celery.sh`:
```bash
# 修改这些行
WORKER_LOG="logs/celery_worker.log"
BEAT_LOG="logs/celery_beat.log"
```

---

## ⚠️ 常见问题

### 1. 端口被占用

**问题**: `Address already in use: 8000`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000

# 终止进程
kill -9 <PID>

# 或使用stop-dev.sh停止所有服务
./scripts/stop-dev.sh
```

---

### 2. Docker未启动

**问题**: `Cannot connect to Docker daemon`

**解决**:
```bash
# macOS: 打开Docker Desktop应用
open -a Docker

# Linux: 启动Docker服务
sudo systemctl start docker
```

---

### 3. 虚拟环境未激活

**问题**: `No module named 'fastapi'`

**解决**:
```bash
# 进入backend目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

### 4. 数据库连接失败

**问题**: `could not connect to server`

**解决**:
```bash
# 检查PostgreSQL容器状态
docker ps | grep postgres

# 如果未运行,启动容器
docker start web3-postgres

# 检查连接
docker exec web3-postgres pg_isready
```

---

## 📊 服务健康检查

### 检查所有服务状态

```bash
# 后端
curl http://localhost:8000/api/health

# 前端
curl http://localhost:3000

# PostgreSQL
docker exec web3-postgres pg_isready

# Redis
docker exec web3-redis redis-cli ping

# Celery Worker
celery -A app.tasks.celery inspect ping
```

---

## 🔄 脚本维护

### 添加新脚本

1. 在 `scripts/` 目录创建新脚本
2. 添加执行权限: `chmod +x scripts/new-script.sh`
3. 更新本README文档

### 脚本规范

- 使用 `#!/bin/bash` shebang
- 添加脚本说明注释
- 使用有意义的变量名
- 添加错误处理
- 输出清晰的状态信息

**示例模板**:
```bash
#!/bin/bash

# 脚本名称: example.sh
# 用途: 示例脚本说明
# 作者: 技术团队
# 日期: 2025-10-13

set -e  # 遇到错误立即退出

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始执行...${NC}"

# 脚本逻辑
...

echo -e "${GREEN}执行完成!${NC}"
```

---

## 📚 相关文档

- [快速启动指南](../docs/快速指南/快速启动.md)
- [部署指南](../docs/04-部署与运维/01-部署指南.md)
- [开发规范](../docs/03-开发规范/01-代码规范.md)

---

**维护者**: 技术团队
**最后更新**: 2025-10-13
**目录位置**: `/scripts/`
