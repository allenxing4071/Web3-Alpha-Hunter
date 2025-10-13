# Telegram 配置说明

## 您提供的Bot Token

**Bot用户名**: @iqiq007_bot  
**Bot Token**: `7999542138:AAHaBdI2pwrRUXdqRMv6dNw9BNONSa-FTCA`

---

## ⚠️ 重要说明

您提供的是 **Telegram Bot Token**，这个用于机器人功能（如发送通知、接收命令）。

但是，**数据采集需要的是 Telegram API (MTProto)**，需要以下两个参数：
- `TELEGRAM_API_ID` (数字)
- `TELEGRAM_API_HASH` (32位字符串)

---

## 📋 需要注册Telegram API

### 步骤1: 访问注册页面
打开浏览器访问: https://my.telegram.org/

### 步骤2: 登录
使用您的手机号登录（接收验证码）

### 步骤3: 创建应用
1. 点击 "API development tools"
2. 填写表单:
   - **App title**: `Web3 Alpha Hunter`
   - **Short name**: `web3hunter`
   - **URL**: 可以留空或填写 `https://github.com/yourusername/web3-alpha-hunter`
   - **Platform**: 选择 `Other`
3. 点击 "Create application"

### 步骤4: 获取密钥
页面会显示:
```
App api_id: 12345678
App api_hash: abcdef1234567890abcdef1234567890
```

复制这两个值！

---

## 🔧 配置方式

### 方案A: 数据采集 (主要功能)

```bash
# backend/.env
TELEGRAM_API_ID=12345678  # 从 my.telegram.org 获取
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890  # 从 my.telegram.org 获取
```

**用途**: 监听Telegram频道消息，采集Web3项目信息

---

### 方案B: Bot通知 (可选功能)

```bash
# backend/.env
TELEGRAM_BOT_TOKEN=7999542138:AAHaBdI2pwrRUXdqRMv6dNw9BNONSa-FTCA
```

**用途**: 向用户发送通知（如新项目提醒）

---

## ✅ 推荐配置

**同时配置两者**，实现完整功能:

```bash
# backend/.env

# === Telegram数据采集 (必须) ===
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890

# === Telegram Bot通知 (可选) ===
TELEGRAM_BOT_TOKEN=7999542138:AAHaBdI2pwrRUXdqRMv6dNw9BNONSa-FTCA
```

---

## 📝 下一步操作

1. 访问 https://my.telegram.org/
2. 登录并创建应用
3. 复制 `api_id` 和 `api_hash`
4. 配置到 `backend/.env` 文件
5. 重启Celery服务

---

## 🧪 验证配置

配置完成后，运行测试:

```bash
cd /Users/xinghailong/Documents/soft/faxianjihui/backend
python3 -c "
import asyncio
from app.services.collectors.telegram import telegram_collector

async def test():
    success = await telegram_collector.start_client()
    if success:
        print('✅ Telegram采集器配置成功！')
        messages = await telegram_collector.get_channel_messages('@cryptonewsflash', limit=5)
        print(f'✅ 采集到 {len(messages)} 条消息')
    else:
        print('❌ 配置失败，请检查API ID和Hash')

asyncio.run(test())
"
```

---

## 常见问题

**Q: Bot Token和API有什么区别？**  
A: 
- **Bot Token**: 机器人功能（发送消息、命令交互）
- **API ID/Hash**: 作为客户端读取频道消息（数据采集）

**Q: 必须都配置吗？**  
A: 
- 数据采集（核心功能）: 必须配置 `API_ID` 和 `API_HASH`
- Bot通知（辅助功能）: 可选配置 `BOT_TOKEN`

**Q: 注册API需要付费吗？**  
A: 完全免费，无调用次数限制
