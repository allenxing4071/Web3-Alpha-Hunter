# AI 配置快速开始

> **5分钟配置完成** | 最后更新: 2025-10-04

---

## ✅ 当前状态

```
✅ WildCard API Key 已配置
✅ OpenAI 已配置 (通过 WildCard 中转)
✅ Claude 已配置 (通过 WildCard 中转)
⏳ DeepSeek 待配置 (推荐)
```

---

## 🚀 立即测试

### 1. 测试 API 连接

```bash
cd backend
python3 test_wildcard_api.py
```

**预期结果**:
```
✅ OpenAI 响应成功!
✅ Claude 响应成功!
✅ AI 分析器测试通过!
🎉 所有测试通过! WildCard API 配置成功!
```

### 2. 启动后端服务

```bash
cd backend
uvicorn app.main:app --reload
```

访问: http://localhost:8000/docs

### 3. 测试 AI 分析功能

```bash
# 方式 1: 通过 API 测试
curl http://localhost:8000/api/v1/test/ai

# 方式 2: 使用现有测试脚本
python3 backend/test_ai_analyzer.py
```

---

## 📋 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| **YAML 配置** | `guides/config/keys/api-keys.yaml` | 集中管理所有 API keys |
| **环境变量** | `backend/.env` | 后端实际读取的配置 |
| **配置说明** | `guides/config/CONFIG_KEYS.md` | API keys 管理文档 |
| **WildCard 文档** | `guides/ai/WILDCARD_CONFIG.md` | WildCard 详细配置 |

---

## 🔑 API Key 信息

```yaml
服务: WildCard/GPTsAPI
API Key: sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB
Base URL: https://api.gptsapi.net/v1
```

**特点**:
- 🌐 国内直连,无需梯子
- 💰 按量付费
- 🔄 同时支持 OpenAI 和 Claude
- 🔑 一个 Key 通用

---

## 💡 快速修改配置

### 方式 1: 编辑 YAML (推荐)

```bash
# 编辑配置
vi guides/config/keys/api-keys.yaml

# 同步到 .env
python3 guides/config/scripts/sync_keys_to_env.py

# 重启服务
cd backend && uvicorn app.main:app --reload
```

### 方式 2: 直接编辑 .env

```bash
# 编辑环境变量
vi backend/.env

# 重启服务
cd backend && uvicorn app.main:app --reload
```

---

## 🎯 使用建议

### AI 模型选择策略

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 🔥 **日常分析** | `claude-3-5-sonnet` | 性能好、速度快、成本中等 |
| 💰 **大量调用** | `gpt-3.5-turbo` | 成本最低 |
| 🎓 **复杂分析** | `gpt-4` | 性能最强 |
| ⚡ **快速响应** | `claude-3-haiku` | 速度最快 |

### 当前配置

系统优先级: **Claude 3.5 Sonnet** > OpenAI GPT

可在 `backend/app/services/analyzers/ai_analyzer.py` 中调整

---

## 🔧 常见操作

### 查看当前配置

```bash
cd backend
python3 -c "
from app.core.config import settings
print('OpenAI Key:', settings.OPENAI_API_KEY[:20] + '...')
print('Claude Key:', settings.ANTHROPIC_API_KEY[:20] + '...')
print('DeepSeek Key:', settings.DEEPSEEK_API_KEY or 'NOT SET')
"
```

### 更新 API Key

```bash
# 1. 编辑 YAML 配置
vi guides/config/keys/api-keys.yaml

# 2. 同步到 .env
python3 guides/config/scripts/sync_keys_to_env.py

# 3. 验证配置
cd backend && python3 test_wildcard_api.py
```

### 添加 DeepSeek (推荐)

DeepSeek 是国内 AI 服务,性价比极高:

```bash
# 1. 访问 https://platform.deepseek.com/ 获取 API Key

# 2. 编辑配置
vi guides/config/keys/api-keys.yaml

# 在 deepseek 部分填入:
# deepseek:
#   api_key: "sk-your-deepseek-key"

# 3. 同步配置
python3 guides/config/scripts/sync_keys_to_env.py

# 4. 重启服务
cd backend && uvicorn app.main:app --reload
```

---

## 📊 成本监控

### 查看 WildCard 用量

1. 登录 WildCard 后台
2. 查看 API 使用统计
3. 设置用量告警

### 成本优化技巧

```python
# 在代码中控制 token 使用
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[...],
    max_tokens=1000,  # 限制最大输出
    temperature=0.7   # 降低随机性
)
```

---

## ⚠️ 故障排查

### 问题: API 调用失败

```bash
# 检查网络连接
curl https://api.gptsapi.net/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 检查配置
cd backend && python3 -c "from app.core.config import settings; print(settings.OPENAI_API_KEY)"

# 重新测试
python3 backend/test_wildcard_api.py
```

### 问题: 配置未生效

```bash
# 强制重新加载环境变量
cd backend
export $(cat .env | xargs)
uvicorn app.main:app --reload
```

---

## 📚 更多文档

- 📘 [WildCard 配置详解](./WILDCARD_CONFIG.md)
- 🔑 [API Keys 管理](../config/CONFIG_KEYS.md)
- 🤖 [DeepSeek 配置指南](./DEEPSEEK_GUIDE.md)
- 📖 [API 接口文档](../../docs/02-技术实现/02-API接口文档.md)

---

## 🎉 下一步

1. ✅ 运行测试验证配置
2. 💰 在 WildCard 后台充值
3. 🚀 启动后端服务
4. 🧪 测试 AI 分析功能
5. 📊 监控 API 使用情况

---

**需要帮助?** 查看详细文档或联系开发团队

