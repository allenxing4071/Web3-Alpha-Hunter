# 🚀 快速启动指南

## 一键启动命令

### 1️⃣ 启动后端 (终端1)

```bash
cd /Users/xinghailong/Documents/soft/faxianjihui/backend
python3 -m uvicorn app.main:app --reload --port 8000
```

✅ 启动成功标志: 看到 `Application startup complete`

### 2️⃣ 启动前端 (终端2)

```bash
cd /Users/xinghailong/Documents/soft/faxianjihui/frontend
npm run dev
```

✅ 启动成功标志: 看到 `Ready in XXXms`

### 3️⃣ 访问应用

- 🌐 前端地址: http://localhost:3000
- 📡 后端API: http://localhost:8000
- 📚 API文档: http://localhost:8000/docs

### 4️⃣ 登录系统

```
用户名: admin
密码: admin123
```

## 📋 可选:启动自动采集(需要Celery)

### 终端3: 启动Celery Worker

```bash
cd /Users/xinghailong/Documents/soft/faxianjihui/backend
celery -A app.tasks.celery_app worker --loglevel=info
```

### 终端4: 启动Celery Beat (定时任务)

```bash
cd /Users/xinghailong/Documents/soft/faxianjihui/backend
celery -A app.tasks.celery_app beat --loglevel=info
```

## 🎯 功能页面

- **首页**: http://localhost:3000/
- **项目列表**: http://localhost:3000/projects
- **项目对比**: http://localhost:3000/compare
- **系统管理**: http://localhost:3000/admin (手动采集控制)
- **用户管理**: http://localhost:3000/users
- **API文档**: http://localhost:3000/api-docs.html

## ⚠️ 常见问题

### 后端启动失败?

1. 检查Python版本: `python3 --version` (需要3.11+)
2. 检查依赖: `pip3 install -r requirements.txt`
3. 检查端口: `lsof -ti:8000` (如果占用,kill掉)

### 前端启动失败?

1. 检查Node版本: `node --version` (需要18+)
2. 重新安装依赖: `rm -rf node_modules && npm install`
3. 清理缓存: `rm -rf .next`

### 登录失败?

1. 打开浏览器控制台
2. 执行: `localStorage.clear()`
3. 刷新页面重新登录

---

**开发愉快!** 🎉

