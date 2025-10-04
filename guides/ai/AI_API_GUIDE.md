# 🤖 AI分析 - API密钥配置指南

## ✅ 是的,AI分析需要API密钥!

根据代码分析,AI分析模块使用以下服务:

### 支持的AI服务

1. **Anthropic Claude** (推荐)
   - API密钥: `ANTHROPIC_API_KEY`
   - 用于文本分析、项目评估
   - 官网: https://console.anthropic.com/

2. **OpenAI GPT-4**
   - API密钥: `OPENAI_API_KEY`
   - 备用AI服务
   - 官网: https://platform.openai.com/

## 📋 当前配置状态

查看 `backend/app/core/config.py` 第43-44行:

```python
# AI服务
OPENAI_API_KEY: Optional[str] = None      # ← 默认为空
ANTHROPIC_API_KEY: Optional[str] = None   # ← 默认为空
```

**当前状态**: ⚠️ 两个都是 `None`,AI分析**不会真正运行**

## 🔧 如何配置API密钥

### 方法1: 环境变量 (推荐)

创建或编辑 `backend/.env` 文件:

```bash
# AI服务密钥
OPENAI_API_KEY="sk-proj-your-openai-key-here"
ANTHROPIC_API_KEY="sk-ant-your-anthropic-key-here"

# 其他配置...
SECRET_KEY="web3-alpha-hunter-secret-key"
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"
REDIS_URL="redis://localhost:6379/0"
```

### 方法2: 直接设置环境变量

```bash
# macOS/Linux
export ANTHROPIC_API_KEY="sk-ant-your-key"
export OPENAI_API_KEY="sk-proj-your-key"

# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key
set OPENAI_API_KEY=sk-proj-your-key
```

## 🎯 AI分析工作流程

### 1. 有API密钥时

```python
# ai_analyzer.py 第19-32行
if settings.ANTHROPIC_API_KEY:
    self.claude_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    logger.info("✅ Claude client initialized")

if settings.OPENAI_API_KEY:
    self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    logger.info("✅ OpenAI client initialized")
```

**使用真实AI分析**:
- 调用Claude/GPT进行深度分析
- 生成项目摘要
- 提取关键信息
- 风险评估
- 投资建议

### 2. 没有API密钥时

```python
# ai_analyzer.py 第44-46行
if not self.claude_client and not self.openai_client:
    logger.warning("No AI client available, using mock analysis")
    return self._mock_analysis(text)
```

**使用模拟分析**:
- 返回假数据
- 不进行真实AI分析
- 快速返回结果(用于测试)

## 💰 API密钥获取方式

### Anthropic Claude

1. 访问 https://console.anthropic.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新密钥
5. 复制密钥 (格式: `sk-ant-api03-...`)

**价格参考**:
- Claude 3.5 Sonnet: $3/1M tokens (输入), $15/1M tokens (输出)
- Claude 3 Haiku: $0.25/1M tokens (输入), $1.25/1M tokens (输出)

### OpenAI GPT-4

1. 访问 https://platform.openai.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新密钥
5. 复制密钥 (格式: `sk-proj-...`)

**价格参考**:
- GPT-4 Turbo: $10/1M tokens (输入), $30/1M tokens (输出)
- GPT-3.5 Turbo: $0.5/1M tokens (输入), $1.5/1M tokens (输出)

## 🚀 启动流程

### 完整启动命令

```bash
# 1. 设置API密钥
export ANTHROPIC_API_KEY="sk-ant-your-key"

# 2. 启动后端
cd backend
uvicorn app.main:app --reload --port 8000

# 3. (可选) 启动Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# 4. 启动前端
cd ../frontend
npm run dev
```

### 查看AI初始化日志

启动后端后,你会看到:

```
# 有密钥时:
✅ Claude client initialized
✅ OpenAI client initialized

# 无密钥时:
(没有这些日志)
```

## ⚠️ 当前采集流程

### 修复后的流程

1. **数据采集** (已修复 ✅)
   ```
   点击采集 → 调用collector → 返回项目数据
   ```

2. **数据库保存** (已修复 ✅)
   ```
   采集到的项目 → 检查重复 → 保存到数据库
   ```

3. **AI分析** (需要API密钥 ⚠️)
   ```
   - 有密钥: 真实AI分析
   - 无密钥: 跳过或使用模拟分析
   ```

## 🎯 推荐配置

### 最小可运行配置 (不需要AI)

```env
# 必需
SECRET_KEY="web3-alpha-hunter-secret"
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/1"
CORS_ORIGINS="http://localhost:3000,http://localhost:3001"
```

**功能**: 
- ✅ 数据采集
- ✅ 数据保存
- ❌ AI分析 (使用模拟)

### 完整配置 (包含AI)

```env
# 基础配置
SECRET_KEY="web3-alpha-hunter-secret"
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/1"
CORS_ORIGINS="http://localhost:3000,http://localhost:3001"

# AI服务 (二选一或都配置)
ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
OPENAI_API_KEY="sk-proj-your-openai-key"

# 可选: 数据采集API
TWITTER_BEARER_TOKEN="your-twitter-token"
TELEGRAM_BOT_TOKEN="your-telegram-token"
COINGECKO_API_KEY="your-coingecko-key"
```

**功能**:
- ✅ 数据采集
- ✅ 数据保存
- ✅ 真实AI分析
- ✅ 完整功能

## 📊 成本估算

### 保守使用场景

假设每天分析100个项目,每个项目1000 tokens:

**使用Claude 3 Haiku** (经济型):
- 每天: 100,000 tokens
- 成本: ~$0.025/天
- 月成本: ~$0.75

**使用Claude 3.5 Sonnet** (高质量):
- 每天: 100,000 tokens  
- 成本: ~$0.30/天
- 月成本: ~$9

## 🔒 安全提示

1. **不要提交.env到Git**
   - `.gitignore`已配置忽略`.env`
   - 永远不要在代码中硬编码密钥

2. **使用环境变量**
   - 生产环境使用服务器环境变量
   - 开发环境使用`.env`文件

3. **定期轮换密钥**
   - 定期更换API密钥
   - 监控API使用量

## 📝 总结

### AI分析是否必需?

**不必需,但推荐!**

- **无AI密钥**: 系统仍可采集和保存项目
- **有AI密钥**: 获得深度分析、评分、投资建议

### 当前已修复的问题

1. ✅ API调用 - 不再返回假数据
2. ✅ 数据库保存 - 采集的项目会保存
3. ✅ 重复检查 - 不会保存重复项目
4. ✅ 同步执行 - Celery未运行时仍可工作

### AI分析状态

- ⚠️ 代码已就绪
- ⚠️ 需要配置API密钥
- ⚠️ 无密钥时使用模拟分析

---

**建议**: 先测试基础采集功能,确认正常后再添加AI密钥

