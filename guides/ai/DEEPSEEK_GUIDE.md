# 🚀 DeepSeek API 配置指南

## 为什么选择 DeepSeek?

### ✅ 优势

1. **🇨🇳 国内服务** - 访问速度快,无需科学上网
2. **💰 价格便宜** - 比Claude/GPT便宜10-100倍
3. **🎯 效果优秀** - 中文理解能力强,适合Web3分析
4. **🔓 门槛低** - 容易注册,支持支付宝/微信支付

### 💰 价格对比

| 服务 | 价格 (每百万tokens) | 说明 |
|------|-------------------|------|
| **DeepSeek** | ¥1 (输入) / ¥2 (输出) | 🏆 最便宜 |
| Claude 3 Haiku | ~$0.25 / $1.25 | 约¥1.8 / ¥9 |
| GPT-3.5 Turbo | $0.5 / $1.5 | 约¥3.6 / ¥10.8 |
| GPT-4 Turbo | $10 / $30 | 约¥72 / ¥216 |

**DeepSeek性价比极高!** 💎

## 📝 获取API密钥

### 步骤1: 注册账号

1. 访问官网: https://platform.deepseek.com/
2. 点击"注册"
3. 使用手机号注册(支持国内手机号)

### 步骤2: 获取API密钥

1. 登录后进入控制台
2. 点击左侧"API Keys"
3. 点击"创建API Key"
4. 复制密钥(格式: `sk-...`)

### 步骤3: 充值

1. 进入"账户管理"
2. 点击"充值"
3. 支持支付宝/微信支付
4. 建议充值¥10-50即可使用很久

## 🔧 配置到项目

### 方法1: 环境变量文件 (推荐)

创建或编辑 `backend/.env`:

```bash
# DeepSeek AI (国内,推荐)
DEEPSEEK_API_KEY="sk-your-deepseek-api-key-here"

# 基础配置
SECRET_KEY="web3-alpha-hunter-secret-key"
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/1"
CORS_ORIGINS="http://localhost:3000,http://localhost:3001"

# 可选: 其他AI服务 (备用)
# ANTHROPIC_API_KEY="sk-ant-..."
# OPENAI_API_KEY="sk-proj-..."
```

### 方法2: 系统环境变量

```bash
# macOS/Linux
export DEEPSEEK_API_KEY="sk-your-key-here"

# Windows
set DEEPSEEK_API_KEY=sk-your-key-here
```

## 🎯 AI优先级顺序

系统会按以下顺序选择AI服务:

```
1. DeepSeek (优先,国内快速)
   ↓ 未配置时
2. Claude (备用,海外)
   ↓ 未配置时
3. OpenAI (备用,海外)
   ↓ 都未配置时
4. Mock分析 (模拟数据)
```

## 🔍 验证配置

### 1. 启动后端并查看日志

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**成功时会看到**:
```
✅ DeepSeek client initialized (优先使用)
```

**未配置时会看到**:
```
(没有DeepSeek相关日志)
```

### 2. 测试AI分析

访问: http://localhost:8000/api/v1/analyze/test

或在系统管理页面点击采集,查看是否有AI分析结果。

## 📊 使用场景

### DeepSeek可以做什么?

1. **项目文本分析**
   - 从Twitter/Telegram提取项目信息
   - 识别项目名称、代币、描述

2. **情感分析**
   - 分析社区情绪(积极/消极)
   - 评估项目热度

3. **风险识别**
   - 识别高风险词汇
   - 检测诈骗模式

4. **投资建议生成**
   - 基于多维度评分
   - 生成投资分析报告

## 💡 最佳实践

### 1. 控制Token使用

```python
# 在代码中已经设置
max_tokens=1024  # 限制输出长度
temperature=0.7  # 平衡创造性和准确性
```

### 2. 成本优化

- 只对新发现的项目做分析
- 批量分析降低API调用次数
- 缓存分析结果

### 3. 监控使用

定期检查API使用量:
1. 登录 https://platform.deepseek.com/
2. 查看"用量统计"
3. 设置预算提醒

## 🔒 安全建议

1. **不要提交密钥到Git**
   ```bash
   # .gitignore 已配置
   .env
   *.env
   ```

2. **定期轮换密钥**
   - 每月更换一次
   - 泄露后立即更换

3. **设置使用限额**
   - 在DeepSeek控制台设置
   - 避免意外消费

## 📈 成本估算

### 实际使用场景

假设每天分析100个项目:

```
每个项目分析:
- 输入: ~500 tokens (项目信息)
- 输出: ~1000 tokens (分析结果)

每天成本:
- 输入: 100 × 500 = 50,000 tokens ≈ ¥0.05
- 输出: 100 × 1000 = 100,000 tokens ≈ ¥0.20
- 合计: ¥0.25/天

每月成本: ¥0.25 × 30 = ¥7.5
```

**非常便宜!** 💰

## 🆚 与其他AI对比

### DeepSeek vs Claude

| 对比项 | DeepSeek | Claude |
|--------|----------|--------|
| 价格 | ¥1-2/百万tokens | ¥1.8-216/百万tokens |
| 速度 | 快(国内) | 慢(需科学上网) |
| 中文能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 注册难度 | 简单 | 需要海外卡 |

### DeepSeek vs GPT

| 对比项 | DeepSeek | GPT-4 |
|--------|----------|-------|
| 价格 | ¥1-2/百万tokens | ¥72-216/百万tokens |
| 速度 | 快 | 中等 |
| Web3理解 | 很好 | 很好 |
| 可用性 | 稳定 | 需科学上网 |

## 🎓 DeepSeek模型介绍

### deepseek-chat

- **用途**: 通用对话和分析
- **上下文**: 32K tokens
- **特点**: 中文优秀,推理能力强
- **适用**: Web3项目分析 ✅

### deepseek-coder

- **用途**: 代码分析
- **特点**: 代码理解强
- **适用**: 智能合约分析

## 🚀 快速开始

### 完整流程

```bash
# 1. 获取DeepSeek API密钥
访问: https://platform.deepseek.com/

# 2. 配置环境变量
echo 'DEEPSEEK_API_KEY="sk-your-key"' >> backend/.env

# 3. 启动后端
cd backend
uvicorn app.main:app --reload --port 8000

# 4. 查看日志确认
# 应该看到: ✅ DeepSeek client initialized (优先使用)

# 5. 测试采集
# 访问前端系统管理页面,点击采集按钮
```

## 📞 技术支持

- 官方文档: https://platform.deepseek.com/docs
- API文档: https://platform.deepseek.com/api-docs
- Discord: https://discord.gg/Tc7c45Zzu5

## 📝 示例配置文件

`backend/.env` 完整示例:

```bash
# ===== 基础配置 =====
PROJECT_NAME="Web3 Alpha Hunter"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true
SECRET_KEY="web3-alpha-hunter-secret-key-change-in-production"
API_V1_PREFIX="/api/v1"

# ===== 数据库 =====
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/web3hunter"

# ===== Redis =====
REDIS_URL="redis://localhost:6379/0"

# ===== Celery =====
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/1"

# ===== CORS =====
CORS_ORIGINS="http://localhost:3000,http://localhost:3001"

# ===== AI服务 (DeepSeek优先) =====
DEEPSEEK_API_KEY="sk-your-deepseek-key-here"

# 备用AI (可选)
# ANTHROPIC_API_KEY="sk-ant-your-key"
# OPENAI_API_KEY="sk-proj-your-key"

# ===== 数据采集API (可选) =====
# TWITTER_BEARER_TOKEN="your-twitter-token"
# TELEGRAM_BOT_TOKEN="your-telegram-token"
# COINGECKO_API_KEY="your-coingecko-key"
```

---

**推荐**: DeepSeek是国内最佳选择,性价比极高! 🚀

