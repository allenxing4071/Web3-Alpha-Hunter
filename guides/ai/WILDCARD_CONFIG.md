# WildCard/GPTsAPI 配置说明

> **配置时间**: 2025-10-04  
> **状态**: ✅ 已配置完成  
> **参考文档**: [WildCard API 使用教程](https://help.bewildcard.com/zh-CN/articles/9121334-gptsapi-%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B)

---

## 📋 配置概览

本项目使用 **WildCard (GPTsAPI)** 作为 AI API 中转服务,实现:

- ✅ 无需 OpenAI/Anthropic 官方账号
- ✅ 国内网络直连,无需梯子
- ✅ 统一的 API Key 管理
- ✅ 同时支持 GPT 和 Claude 模型

### 关键特性

| 特性 | 说明 |
|------|------|
| **中转地址** | `https://api.gptsapi.net/v1` |
| **API Key** | 已配置在 `guides/config/keys/api-keys.yaml` |
| **支持模型** | GPT-3.5, GPT-4, Claude-3.5-Sonnet |
| **计费方式** | 按使用量付费 |

---

## 🔑 已配置的 API Key

```yaml
API Key: sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB
Base URL: https://api.gptsapi.net/v1
```

**重要说明**:
- ⚠️ 这是 WildCard 中转 API,不是官方 API
- 🔄 OpenAI 和 Claude 使用**同一个** API Key
- 🌐 必须使用 WildCard 的 base_url

---

## 📦 支持的 AI 模型

### OpenAI 模型

| 模型 | 用途 | 成本 |
|------|------|------|
| `gpt-3.5-turbo` | 快速响应,日常分析 | 低 |
| `gpt-4` | 复杂分析 | 高 |
| `gpt-4-turbo` | 平衡性能 | 中 |

### Claude 模型 (推荐)

| 模型 | 用途 | 成本 |
|------|------|------|
| `claude-3-5-sonnet-20241022` | 🥇 最新版本,综合性能最佳 | 中 |
| `claude-3-5-sonnet-20240620` | 稳定版本 | 中 |
| `claude-3-opus-20240229` | 最强性能 | 高 |
| `claude-3-haiku-20240307` | 快速响应 | 低 |

---

## 🔧 配置方法

### 1. YAML 配置文件

位置: `guides/config/keys/api-keys.yaml`

```yaml
ai_services:
  # OpenAI (通过 GPTsAPI/WildCard 中转)
  openai:
    api_key: "sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB"
    base_url: "https://api.gptsapi.net/v1"
    models:
      - "gpt-4"
      - "gpt-3.5-turbo"

  # Anthropic Claude (通过 GPTsAPI/WildCard 中转)
  anthropic:
    api_key: "sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB"
    base_url: "https://api.gptsapi.net/v1"
    models:
      - "claude-3-5-sonnet-20241022"
```

### 2. 环境变量配置

位置: `backend/.env`

```bash
OPENAI_API_KEY=sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB
ANTHROPIC_API_KEY=sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB
```

---

## 💻 代码集成

### Python 示例

```python
from openai import OpenAI

# OpenAI 模型调用
client = OpenAI(
    api_key="sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB",
    base_url="https://api.gptsapi.net/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Claude 模型调用 (使用 OpenAI 格式!)
claude_client = OpenAI(
    api_key="sk-Zudfb63f8fcfa4e29e3265599f4562c6c404b6542eddPtbB",
    base_url="https://api.gptsapi.net/v1"
)

response = claude_client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",  # 注意使用 Claude 模型名
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 关键要点

1. **Claude 也使用 OpenAI 客户端**
   - WildCard 统一使用 OpenAI 的 API 格式
   - 只需修改 `model` 参数为 Claude 模型名

2. **Base URL 必须正确**
   - 使用 `https://api.gptsapi.net/v1`
   - 不能使用官方 API 地址

3. **同一个 API Key**
   - GPT 和 Claude 共用一个 key
   - 通过模型名区分调用哪个服务

---

## 🧪 测试配置

### 快速测试

```bash
cd backend
python3 test_wildcard_api.py
```

### 测试项目

测试脚本会验证:
- ✅ OpenAI API 连接
- ✅ Claude API 连接
- ✅ AI 分析器功能

### 预期输出

```
🔧 WildCard/GPTsAPI 配置测试
============================================================

==================================================
测试 OpenAI (via GPTsAPI/WildCard)
==================================================
✅ API Key: sk-Zudfb63f8fcfa4e...
📡 发送测试请求...
✅ OpenAI 响应成功!
📝 回复: Web3是去中心化互联网的新范式...

==================================================
测试 Claude (via GPTsAPI/WildCard)
==================================================
✅ API Key: sk-Zudfb63f8fcfa4e...
📡 发送测试请求...
✅ Claude 响应成功!
📝 回复: DeFi是去中心化金融...

🎉 所有测试通过! WildCard API 配置成功!
```

---

## 💰 成本说明

根据 [WildCard 定价](https://help.bewildcard.com/zh-CN/articles/9121334-gptsapi-%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B):

| 模型 | 输入价格 | 输出价格 |
|------|---------|---------|
| GPT-3.5-turbo | 约 ¥0.005/1K tokens | 约 ¥0.015/1K tokens |
| GPT-4 | 约 ¥0.21/1K tokens | 约 ¥0.42/1K tokens |
| Claude-3.5-Sonnet | 约 ¥0.021/1K tokens | 约 ¥0.105/1K tokens |

**成本优化建议**:
- 🥇 优先使用 GPT-3.5 或 Claude-3.5-Sonnet
- 💡 只对重要分析使用 GPT-4
- 📊 定期检查 WildCard 后台的用量统计

---

## 🔒 安全注意事项

### ✅ 已实施的保护

1. **Git 保护**
   ```bash
   # .gitignore 已排除
   guides/config/keys/api-keys.yaml
   backend/.env
   ```

2. **文件权限**
   ```bash
   chmod 600 guides/config/keys/api-keys.yaml
   chmod 600 backend/.env
   ```

3. **环境隔离**
   - 开发环境: `.env`
   - 生产环境: 环境变量或密钥管理服务

### ⚠️ 重要提醒

- ❌ 不要将 API Key 提交到 Git
- ❌ 不要在公开渠道分享 Key
- ⏰ 定期更换 API Key (建议3个月)
- 📊 监控 API 用量,防止滥用

---

## 🔧 故障排查

### 问题 1: 连接失败

```
错误: Connection timeout
```

**解决方案**:
```bash
# 检查网络连接
curl https://api.gptsapi.net/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 确认 base_url 正确
# 应该是: https://api.gptsapi.net/v1
```

### 问题 2: API Key 无效

```
错误: Invalid API key
```

**解决方案**:
1. 检查 `.env` 文件中的 key 是否正确
2. 确认 key 没有空格或换行符
3. 登录 WildCard 后台检查 key 状态

### 问题 3: 模型不支持

```
错误: Model not found
```

**解决方案**:
```python
# Claude 模型名必须完整
✅ 正确: "claude-3-5-sonnet-20241022"
❌ 错误: "claude-3-sonnet"

# 检查支持的模型列表
curl https://api.gptsapi.net/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 📚 相关文档

- [WildCard API 使用教程](https://help.bewildcard.com/zh-CN/articles/9121334-gptsapi-%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B)
- [配置管理说明](../config/CONFIG_KEYS.md)
- [API 接口文档](../../docs/02-技术实现/02-API接口文档.md)
- [AI 分析器开发指南](./AI_API_GUIDE.md)

---

## ✅ 配置检查清单

- [x] WildCard API Key 已获取
- [x] `api-keys.yaml` 已配置
- [x] `backend/.env` 已更新
- [x] AI 分析器已适配 WildCard
- [x] Base URL 已设置为 `https://api.gptsapi.net/v1`
- [x] Claude 调用方式已更新为 OpenAI 格式
- [x] 测试脚本已创建
- [ ] 已运行测试验证配置
- [ ] 已设置文件权限 (chmod 600)
- [ ] 已在 WildCard 后台充值

---

**维护者**: 开发团队  
**最后更新**: 2025-10-04  
**状态**: ✅ 配置完成,待测试验证

