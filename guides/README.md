# 📚 Web3 Alpha Hunter - 指南文档

本目录包含项目的所有配置指南、教程和操作手册。

## 📂 目录结构

### ⚙️ [`config/`](./config/) - 配置中心
项目配置参数统一管理（服务器、域名、数据库、API密钥等）

- **[README.md](./config/README.md)** - 配置中心完整指南
- **servers/production.yaml** - 阿里云服务器配置
- **domains/domains.yaml** - 域名和DNS配置
- **database/database.yaml** - PostgreSQL/Redis配置
- **keys/api-keys.example.yaml** - API密钥模板
- **keys/VPNKEY.pem** - SSH密钥 (受Git保护)
- **scripts/setup_env.sh** - 环境变量设置脚本
- **scripts/start_with_env.sh** - 一键启动脚本

### 🤖 [`ai/`](./ai/) - AI配置指南
AI模型和数据采集相关文档

- **AI_API_GUIDE.md** - AI API密钥配置指南
- **DEEPSEEK_GUIDE.md** - DeepSeek AI 集成指南
- **DEEPSEEK_V3_INFO.md** - DeepSeek v3 详细信息
- **DEEPSEEK_启动说明.md** - DeepSeek 启动说明
- **DATA_COLLECTION_LOGIC.md** - 数据采集逻辑说明

### 👥 [`admin/`](./admin/) - 管理员指南
系统管理和权限配置相关文档

- **ADMIN_FULL_ACCESS.md** - 管理员权限说明
- **ADMIN_IMPROVEMENTS.md** - 管理后台改进说明
- **ADMIN_ROLE_FIX_GUIDE.md** - 管理员角色修复指南
- **ROLE_MANAGEMENT_GUIDE.md** - 角色管理系统指南

## 🚀 快速开始

### 1. 服务器和配置
```bash
# 查看配置中心
cat guides/config/README.md

# SSH连接服务器
ssh -i guides/config/keys/VPNKEY.pem root@47.253.226.250

# 使用一键配置脚本
bash guides/config/scripts/setup_env.sh
```

### 2. AI配置
```bash
# 配置DeepSeek AI
cat guides/ai/DEEPSEEK_GUIDE.md

# 查看数据采集逻辑
cat guides/ai/DATA_COLLECTION_LOGIC.md
```

### 3. 管理员设置
```bash
# 配置管理员权限
cat guides/admin/ROLE_MANAGEMENT_GUIDE.md

# 管理员角色修复
cat guides/admin/ADMIN_ROLE_FIX_GUIDE.md
```

## 📖 更多文档

- **项目主文档**: [`../README.md`](../README.md)
- **快速启动**: [`../START.md`](../START.md)
- **技术文档**: [`../docs/`](../docs/)
- **历史记录**: [`../archive/`](../archive/)

## 💡 提示

1. 所有配置文件模板在 `config/` 目录
2. AI相关配置在 `ai/` 目录
3. 管理员操作指南在 `admin/` 目录
4. 遇到问题先查看对应目录的文档

