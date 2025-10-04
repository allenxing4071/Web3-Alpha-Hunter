# 📊 数据采集逻辑说明

## 🔄 采集流程

### 1. 触发方式

#### 方式A: 手动触发 (系统管理页面)
- 前端: `http://localhost:3000/admin`
- 点击采集按钮 → API调用 → 执行采集任务
- 支持单独采集 (Twitter/Telegram/CoinGecko) 或全部采集

#### 方式B: 定时自动采集 (Celery Beat)
- 需要启动 Celery Worker 和 Celery Beat
- 配置文件: `backend/app/tasks/celery_app.py`
- 当前定时任务:
  ```python
  - Twitter采集: 每5分钟执行一次
  - Telegram采集: 每15分钟执行一次
  - 评分更新: 每小时执行一次
  - 生成日报: 每天9:00执行
  ```

### 2. 采集步骤

```
┌─────────────────────────────────────────────────────────┐
│ 1. 手动/定时触发采集任务                                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 2. 执行数据采集                                            │
│    - Twitter: 搜索关键词,监控KOL                            │
│    - Telegram: 监控频道消息                                │
│    - CoinGecko: 获取项目数据                               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 数据清洗和提取                                          │
│    - 提取项目名称、代币、描述                                │
│    - 识别链接 (官网/Twitter/Telegram)                       │
│    - 计算初步热度                                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 检查数据库是否已存在                                     │
│    - 根据项目名称查重                                       │
│    - 如果已存在: 更新数据                                   │
│    - 如果不存在: 创建新项目                                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 5. 保存到数据库                                            │
│    - 插入 Projects 表                                      │
│    - 状态: discovered (刚发现)                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 6. 触发AI分析 (需要API密钥)                                │
│    - 如果配置了 DEEPSEEK_API_KEY                           │
│    - 调用AI分析引擎                                        │
│    - 生成多维度评分和等级                                   │
│    - 更新项目状态: analyzed (已分析)                        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 7. 返回采集结果                                            │
│    - projects_found: 发现的项目数                          │
│    - projects_saved: 保存的新项目数                        │
│    - source: 数据来源                                      │
└─────────────────────────────────────────────────────────┘
```

## 🎯 当前状态

### ✅ 已完成
1. **数据采集器**
   - `TwitterCollector`: Twitter数据采集
   - `TelegramCollector`: Telegram数据采集
   - 模拟数据生成 (无API密钥时)

2. **数据库保存**
   - 自动查重 (根据项目名称)
   - 保存新项目到 `Projects` 表
   - 返回保存数量

3. **API端点**
   - `/api/v1/admin/collect/twitter`
   - `/api/v1/admin/collect/telegram`
   - `/api/v1/admin/collect/coingecko`
   - `/api/v1/admin/collect/all`

4. **Celery集成**
   - 任务定义完成
   - 支持异步执行
   - 支持同步降级 (Celery未运行时)

### 🔧 待完成

1. **AI分析触发** (TODO标记)
   - 位置: `backend/app/tasks/collectors.py`
   - 需要: DeepSeek API密钥
   - 功能: 自动对新项目进行AI分析

2. **真实API集成**
   - Twitter API (需要申请)
   - Telegram API (需要申请)
   - CoinGecko API (可选,有免费额度)

## 🚀 启动完整采集系统

### 步骤1: 配置环境变量

编辑 `backend/.env`:
```bash
# 必需: 数据库
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"

# 必需: Redis (用于Celery)
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/1"

# 推荐: AI分析
DEEPSEEK_API_KEY="sk-your-deepseek-key"

# 可选: 真实数据采集
TWITTER_BEARER_TOKEN="your-twitter-token"
TELEGRAM_BOT_TOKEN="your-telegram-token"
```

### 步骤2: 启动依赖服务

```bash
# 启动PostgreSQL和Redis
docker-compose up -d postgres redis

# 或者使用本地服务
# PostgreSQL: brew services start postgresql
# Redis: brew services start redis
```

### 步骤3: 初始化数据库

```bash
cd backend
python -c "from app.db.session import init_db; init_db()"
```

### 步骤4: 启动后端服务

```bash
# 终端1: 启动FastAPI
cd backend
uvicorn app.main:app --reload --port 8000
```

### 步骤5: 启动Celery (可选,用于自动采集)

```bash
# 终端2: 启动Celery Worker
cd backend
celery -A app.tasks.celery_app worker --loglevel=info

# 终端3: 启动Celery Beat (定时任务)
cd backend
celery -A app.tasks.celery_app beat --loglevel=info
```

### 步骤6: 启动前端

```bash
# 终端4: 启动Next.js
cd frontend
npm run dev
```

### 步骤7: 测试采集

访问: http://localhost:3000/admin

点击采集按钮,查看结果!

## 📝 采集任务详情

### Twitter采集 (`collect_twitter_data`)

**功能**:
- 搜索Web3相关关键词
- 监控KOL账户
- 提取项目信息

**返回数据**:
```python
{
    "name": "ProjectName",
    "symbol": "TOKEN",
    "description": "项目描述",
    "twitter": "@projecthandle",
    "website": "https://...",
    "engagement": {
        "likes": 1000,
        "retweets": 500
    }
}
```

**执行频率**: 每5分钟 (可调整)

### Telegram采集 (`collect_telegram_data`)

**功能**:
- 监控Web3相关频道
- 提取项目公告
- 分析社区活跃度

**返回数据**:
```python
{
    "name": "ProjectName",
    "description": "从频道提取的信息",
    "telegram": "https://t.me/channel",
    "members": 5000
}
```

**执行频率**: 每15分钟 (可调整)

### CoinGecko采集 (`collect_coingecko_data`)

**功能**:
- 获取新上线代币
- 价格和市值数据
- 交易量数据

**执行频率**: 每小时 (可调整)

### 全部采集 (`collect_all_sources`)

**功能**:
- 依次执行所有采集器
- 汇总结果
- 返回总计数据

**触发**: 手动触发或定时执行

## 🔐 API密钥说明

### DeepSeek AI (推荐)

**作用**: AI分析项目,生成评分和等级
**获取**: https://platform.deepseek.com/
**价格**: ¥1-2/百万tokens
**必需性**: 非必需,但强烈推荐

**没有密钥时**: 使用模拟分析 (固定评分,无实际AI)

### Twitter API

**作用**: 真实Twitter数据采集
**获取**: https://developer.twitter.com/
**价格**: 有免费额度
**必需性**: 可选,无密钥时使用模拟数据

### Telegram API

**作用**: 真实Telegram数据采集
**获取**: https://my.telegram.org/apps
**价格**: 免费
**必需性**: 可选,无密钥时使用模拟数据

## 💾 数据库表结构

### Projects (主表)
```sql
- project_name: 项目名称
- symbol: 代币符号
- description: 项目描述
- discovered_from: 发现来源 (twitter/telegram/coingecko)
- status: 状态 (discovered/analyzed/archived)
- twitter_handle: Twitter账号
- telegram_group: Telegram群组
- website_url: 官网
- created_at: 创建时间
- updated_at: 更新时间
```

### AIAnalysis (AI分析结果)
```sql
- project_id: 关联的项目ID
- overall_score: 综合评分 (0-100)
- grade: 等级 (S/A/B/C)
- team_score: 团队评分
- tech_score: 技术评分
- community_score: 社区评分
- tokenomics_score: 代币经济学评分
- market_timing_score: 市场时机评分
- risk_score: 风险评分
- analysis_summary: AI分析摘要
```

## 🎯 下一步优化建议

1. **启用AI分析**
   - 配置 DeepSeek API密钥
   - 取消 TODO 注释
   - 自动分析所有新项目

2. **接入真实API**
   - 申请 Twitter API
   - 申请 Telegram API
   - 获取真实数据

3. **优化采集频率**
   - 根据实际需求调整
   - 避免API限流
   - 平衡成本和时效性

4. **添加数据源**
   - Discord监控
   - Reddit监控
   - GitHub活跃度
   - 链上数据分析

5. **增强去重逻辑**
   - 多字段匹配
   - 模糊查询
   - 合并重复项目

---

**当前系统已可以采集和保存数据,配置DeepSeek API后即可自动AI分析!** 🚀
