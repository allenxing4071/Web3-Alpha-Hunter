# API Keys 配置说明

> **最后更新**: 2025-10-04  
> **状态**: ✅ OpenAI 和 Claude 已配置

---

## 📋 配置概览

本项目使用两种方式管理 API keys:

1. **YAML配置文件** (`guides/config/keys/api-keys.yaml`) - 集中管理所有密钥
2. **环境变量文件** (`backend/.env`) - 后端应用实际读取的配置

---

## 🔑 已配置的 API Keys

### ✅ AI 服务

| 服务 | 状态 | 配置位置 | 说明 |
|------|------|---------|------|
| **OpenAI** | ✅ 已配置 | YAML + .env | GPT-4, GPT-3.5 |
| **Claude (Anthropic)** | ✅ 已配置 | YAML + .env | Claude-3 系列 |
| **DeepSeek** | ⏳ 待配置 | YAML + .env | 国内优选,便宜快速 |

### ⏳ 数据源 API (待配置)

| 服务 | 状态 | 用途 |
|------|------|------|
| Twitter/X | ⏳ 待配置 | 获取项目推文和社交数据 |
| Telegram | ⏳ 待配置 | 监控 Telegram 群组 |
| CoinGecko | ⏳ 待配置 | 获取代币价格数据 |
| YouTube | ⏳ 待配置 | 获取视频数据 |

---

## 🚀 快速开始

### 1. 查看已配置的密钥

```bash
# 查看 YAML 配置文件
cat guides/config/keys/api-keys.yaml

# 查看后端环境变量 (敏感信息)
cat backend/.env | grep API_KEY
```

### 2. 更新密钥

有两种方式:

#### 方式 A: 直接编辑 .env 文件

```bash
# 编辑后端环境变量
vi backend/.env

# 修改对应的变量
OPENAI_API_KEY=sk-your-new-key
ANTHROPIC_API_KEY=sk-ant-your-new-key
```

#### 方式 B: 通过 YAML 统一管理 (推荐)

```bash
# 1. 编辑 YAML 配置文件
vi guides/config/keys/api-keys.yaml

# 2. 运行同步脚本,自动更新 .env
python guides/config/scripts/sync_keys_to_env.py
```

### 3. 验证配置

```bash
# 检查后端是否能读取到密钥
cd backend
python -c "from app.core.config import settings; print('OpenAI:', settings.OPENAI_API_KEY[:20] + '...'); print('Claude:', settings.ANTHROPIC_API_KEY[:20] + '...')"
```

---

## 📁 文件结构

```
guides/config/
├── keys/
│   ├── api-keys.yaml          # ✅ 真实密钥 (已配置 OpenAI + Claude)
│   └── api-keys.example.yaml  # 示例文件
├── scripts/
│   └── sync_keys_to_env.py    # 同步工具脚本
└── CONFIG_KEYS.md             # 📍 你在这里

backend/
├── .env                        # ✅ 后端环境变量 (已配置)
└── .env.example                # 示例文件
```

---

## 🔄 同步机制

### 自动同步工具

`sync_keys_to_env.py` 脚本会:

1. 读取 `guides/config/keys/api-keys.yaml`
2. 提取所有 API keys
3. 更新 `backend/.env` 文件中对应的环境变量
4. 保留 .env 中的其他配置不变

### 支持的配置项

| YAML 路径 | 环境变量名 | 说明 |
|-----------|-----------|------|
| `ai_services.openai.api_key` | `OPENAI_API_KEY` | OpenAI API密钥 |
| `ai_services.anthropic.api_key` | `ANTHROPIC_API_KEY` | Claude API密钥 |
| `ai_services.deepseek.api_key` | `DEEPSEEK_API_KEY` | DeepSeek API密钥 |
| `data_sources.twitter.api_key` | `TWITTER_API_KEY` | Twitter API密钥 |
| `data_sources.telegram.bot_token` | `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `data_sources.coingecko.api_key` | `COINGECKO_API_KEY` | CoinGecko API密钥 |

---

## 🔒 安全最佳实践

### ✅ 已实施的安全措施

1. **Git 保护**
   - `api-keys.yaml` 已被 `.gitignore` 排除
   - `.env` 文件不会被提交到 Git
   - 仅提交 `.example` 示例文件

2. **文件权限**
   ```bash
   # 设置密钥文件为只读
   chmod 600 guides/config/keys/api-keys.yaml
   chmod 600 backend/.env
   ```

3. **分离配置**
   - 开发环境: 使用 `backend/.env`
   - 生产环境: 使用环境变量或密钥管理服务

### ❌ 不要这样做

1. ❌ 将真实密钥提交到 Git
2. ❌ 在代码中硬编码密钥
3. ❌ 通过聊天工具发送密钥
4. ❌ 在公共场所展示包含密钥的屏幕

---

## 🧪 测试 AI 配置

### 测试 OpenAI

```bash
cd backend
python -c "
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello!'}],
    max_tokens=10
)
print('✅ OpenAI API 工作正常:', response.choices[0].message.content)
"
```

### 测试 Claude

```bash
cd backend
python -c "
from anthropic import Anthropic
from app.core.config import settings

client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
message = client.messages.create(
    model='claude-3-haiku-20240307',
    max_tokens=10,
    messages=[{'role': 'user', 'content': 'Hello!'}]
)
print('✅ Claude API 工作正常:', message.content[0].text)
"
```

### 完整系统测试

```bash
# 启动后端并测试 AI 分析器
cd backend
python test_ai_analyzer.py
```

---

## 📊 API Keys 使用监控

### 查看 API 调用情况

```python
# 在代码中添加日志
from loguru import logger

logger.info(f"Using AI provider: {analyzer.active_provider}")
logger.info(f"API call cost: ${cost}")
```

### 成本控制

| AI 服务 | 价格 (per 1M tokens) | 推荐场景 |
|---------|---------------------|---------|
| DeepSeek | ¥1 / $0.14 | 🥇 日常使用,性价比最高 |
| GPT-3.5 | $0.50 / $1.50 | 轻量级任务 |
| GPT-4 | $30 / $60 | 复杂分析 |
| Claude-3 Haiku | $0.25 / $1.25 | 快速响应 |
| Claude-3 Sonnet | $3 / $15 | 平衡性能 |

---

## 🔧 故障排查

### 问题 1: 环境变量未生效

```bash
# 重启后端服务
cd backend
uvicorn app.main:app --reload

# 或强制重新加载环境变量
python -c "from dotenv import load_dotenv; load_dotenv(override=True)"
```

### 问题 2: API 调用失败

```bash
# 检查密钥是否正确
cd backend
python -c "
from app.core.config import settings
print('OPENAI_API_KEY:', settings.OPENAI_API_KEY[:20] + '...' if settings.OPENAI_API_KEY else 'NOT SET')
print('ANTHROPIC_API_KEY:', settings.ANTHROPIC_API_KEY[:20] + '...' if settings.ANTHROPIC_API_KEY else 'NOT SET')
"
```

### 问题 3: 同步脚本失败

```bash
# 检查 YAML 文件格式
python -c "import yaml; yaml.safe_load(open('guides/config/keys/api-keys.yaml'))"

# 手动运行同步脚本并查看详细输出
python guides/config/scripts/sync_keys_to_env.py
```

---

## 📝 配置清单

### 已完成 ✅

- [x] 创建 `api-keys.yaml` 配置文件
- [x] 配置 OpenAI API key
- [x] 配置 Claude API key
- [x] 创建 `backend/.env` 文件
- [x] 创建同步工具脚本
- [x] 设置 `.gitignore` 保护

### 待完成 ⏳

- [ ] 配置 DeepSeek API key (推荐,性价比高)
- [ ] 配置 Twitter API keys
- [ ] 配置 Telegram Bot Token
- [ ] 配置 CoinGecko API key
- [ ] 测试 AI 分析器功能
- [ ] 设置文件权限 (chmod 600)

---

## 🔗 相关文档

- [配置目录 README](./README.md)
- [DeepSeek 配置指南](../ai/DEEPSEEK_GUIDE.md)
- [API 接口文档](../../docs/02-技术实现/02-API接口文档.md)

---

**维护者**: 开发团队  
**最后审查**: 2025-10-04  
**状态**: ✅ OpenAI + Claude 已配置完成

