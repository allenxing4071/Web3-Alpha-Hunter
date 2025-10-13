# 🚀 Web3 Alpha Hunter - 快速启动指南

## 📋 系统要求

### 必须
- **Node.js** 18+ (前端)
- **Python** 3.9+ (后端)
- **PostgreSQL** 14+ (数据库)
- **Redis** 6+ (Celery任务队列)

### 可选
- **Git** (代码管理)

---

## 🎬 一键启动（推荐）

### 1. 克隆项目
```bash
git clone <repository-url>
cd faxianjihui
```

### 2. 环境准备
```bash
# 确保PostgreSQL和Redis正在运行
# macOS (使用Homebrew)
brew services start postgresql@14
brew services start redis

# Linux
sudo systemctl start postgresql
sudo systemctl start redis

# 检查服务状态
pg_isready
redis-cli ping
```

### 3. 初始化数据库
```bash
# 创建数据库
createdb web3_alpha_hunter

# 执行迁移
cd backend
python3 scripts/run_migration.py

# 添加测试数据
python3 scripts/seed_pending_projects.py
cd ..
```

### 4. 安装依赖
```bash
# 后端依赖
cd backend
pip3 install -r requirements.txt
cd ..

# 前端依赖
cd frontend
npm install
cd ..
```

### 5. 启动开发服务
```bash
# 一键启动前后端
./start-dev.sh

# 或手动启动：
# 终端1: 后端
cd backend && python3 -m uvicorn app.main:app --reload

# 终端2: 前端
cd frontend && npm run dev
```

### 6. 访问系统
- 🌐 前端: http://localhost:3000
- 🔧 后端API: http://localhost:8000
- 📚 API文档: http://localhost:8000/docs

---

## 🧪 系统测试

```bash
# 自动测试所有API
./test-system.sh
```

测试内容：
- ✅ 后端健康检查
- ✅ 数据库连接
- ✅ 平台管理API
- ✅ 待审核项目API
- ✅ AI工作配置API
- ✅ Celery状态
- ✅ 前端服务

---

## 👤 默认账号

### 管理员账号
- 用户名: `admin`
- 密码: `admin123`
- 权限: 完整管理权限

### 普通用户
- 用户名: `user`
- 密码: `user123`
- 权限: 查看项目

---

## 🎯 核心功能测试

### 1. 系统管理 (`/admin`)
- 查看平台状态（Twitter/Telegram/Discord）
- 配置AI工作参数
- 启用/停用平台
- 手动触发数据采集
- 查看今日统计

### 2. 项目审核 (`/review`)
- 查看5个AI推荐的测试项目
- 查看AI评分和推荐理由
- 批准/拒绝项目
- 填写拒绝理由（AI会学习）

### 3. 数据库管理 (`/database`)
- 查看所有数据表
- 查看表结构
- 查看数据统计

---

## 🤖 启动Celery（可选）

Celery用于自动化数据采集和AI分析：

```bash
# 启动Celery Worker和Beat
./start-celery.sh

# 停止Celery
./stop-celery.sh

# 查看日志
tail -f /tmp/celery-worker.log
tail -f /tmp/celery-beat.log
```

---

## 🛑 停止服务

```bash
# 停止前后端
./stop-dev.sh

# 停止Celery
./stop-celery.sh
```

---

## 📊 数据库状态检查

```bash
cd backend
python3 -c "
from app.db.session import get_db
from sqlalchemy import text

db = next(get_db())

# 检查关键表
print('📊 数据库状态:')
result = db.execute(text('SELECT COUNT(*) FROM projects_pending'))
print(f'   待审核项目: {result.scalar()}')

result = db.execute(text('SELECT COUNT(*) FROM kols'))
print(f'   KOL数量: {result.scalar()}')

result = db.execute(text('SELECT COUNT(*) FROM twitter_keywords'))
print(f'   关键词数量: {result.scalar()}')
"
```

---

## 🔧 常见问题

### Q: 端口已被占用？
```bash
# 查找占用进程
lsof -ti:3000
lsof -ti:8000

# 杀死进程
kill -9 <PID>
```

### Q: PostgreSQL连接失败？
```bash
# 检查PostgreSQL状态
pg_isready -h localhost -p 5432

# 检查数据库是否存在
psql -l | grep web3_alpha_hunter
```

### Q: Redis连接失败？
```bash
# 检查Redis状态
redis-cli ping

# 启动Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### Q: 前端显示API连接错误？
检查 `frontend/.env.local` 是否存在：
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## 📚 更多文档

- **完整实施文档**: `AI_SYSTEM_IMPLEMENTATION.md`
- **API文档**: http://localhost:8000/docs（启动后端后访问）
- **项目说明**: `docs/` 目录

---

## 🎉 快速体验流程

1. **启动服务** → `./start-dev.sh`
2. **访问登录页** → http://localhost:3000/login
3. **使用管理员登录** → admin / admin123
4. **查看系统管理** → http://localhost:3000/admin
   - 查看3个平台状态
   - 配置AI工作参数
5. **审核AI推荐项目** → http://localhost:3000/review
   - 查看5个测试项目
   - 批准/拒绝项目
   - 查看评分详情
6. **查看数据库** → http://localhost:3000/database
   - 查看所有表
   - 查看数据统计

---

**🎊 完成！您已成功启动Web3 Alpha Hunter系统！**

如有问题，请查看：
- 后端日志: `tail -f /tmp/backend.log`
- 前端日志: `tail -f /tmp/frontend.log`
- 或运行测试脚本: `./test-system.sh`

