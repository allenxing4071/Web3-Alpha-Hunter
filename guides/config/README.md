# Config 配置目录

> **最后更新**: 2025-10-04
> **⚠️ 重要**: 此目录包含项目所有配置文件,请妥善保管API密钥和SSH密钥

---

## 📁 目录结构

```
guides/config/
├── README.md                  # 📍 你在这里
├── .gitignore                 # Git忽略规则
├── servers/                   # 服务器配置
│   └── production.yaml        # 生产服务器信息
├── domains/                   # 域名配置
│   └── domains.yaml           # 域名和DNS配置
├── database/                  # 数据库配置
│   └── database.yaml          # 数据库连接配置
├── keys/                      # 密钥管理 ⚠️ 敏感
│   ├── VPNKEY.pem             # SSH密钥
│   └── api-keys.example.yaml  # API密钥示例
├── scripts/                   # 配置脚本
│   ├── setup_env.sh           # 环境变量设置
│   └── start_with_env.sh      # 一键启动
└── examples/                  # 配置示例
```

---

## 🔐 密钥管理

### SSH密钥

**位置**: `guides/config/keys/VPNKEY.pem`

**用途**: 连接到生产服务器

**使用方法**:
```bash
# 确保权限正确
chmod 600 guides/config/keys/VPNKEY.pem

# SSH连接
ssh -i guides/config/keys/VPNKEY.pem root@47.253.226.250

# 配置SSH Config
cat >> ~/.ssh/config << 'EOF'
Host web3-server
    HostName 47.253.226.250
    User root
    IdentityFile ~/Documents/soft/faxianjihui/guides/config/keys/VPNKEY.pem
EOF
```

### API密钥

**示例文件**: `guides/config/keys/api-keys.example.yaml`

**创建真实配置**:
```bash
# 1. 复制示例文件
cp guides/config/keys/api-keys.example.yaml guides/config/keys/api-keys.yaml

# 2. 编辑并填入真实密钥
vi guides/config/keys/api-keys.yaml

# 3. 确认文件不会被Git追踪
git status  # 应该看不到 api-keys.yaml
```

---

## 🌐 域名配置

**配置文件**: `guides/config/domains/domains.yaml`

### 当前使用域名

| 域名 | 状态 | 用途 |
|------|------|------|
| `web3.guandongfang.cn` | ✅ 已解析 | 主域名 |
| `api.web3.guandongfang.cn` | ⏳ 待配置 | API接口 |
| `admin.web3.guandongfang.cn` | ⏳ 待配置 | 管理后台 |

### DNS配置建议

```yaml
# A记录
web3.guandongfang.cn  →  47.253.226.250

# CNAME记录 (建议)
api.web3.guandongfang.cn    →  web3.guandongfang.cn
admin.web3.guandongfang.cn  →  web3.guandongfang.cn
```

---

## 🖥️ 服务器配置

**配置文件**: `guides/config/servers/production.yaml`

### 生产服务器信息

| 项目 | 值 |
|------|------|
| **IP地址** | 47.253.226.250 |
| **用户名** | root |
| **SSH密钥** | config/keys/VPNKEY.pem |
| **操作系统** | Ubuntu 24.04.2 LTS |
| **配置** | 2核 / 1.6GB / 40GB |

### 部署路径

```bash
/app/web3-alpha-hunter/
├── backend/          # 后端应用
├── frontend/         # 前端应用
├── data/             # 数据文件
├── logs/             # 日志文件
└── backups/          # 备份文件
```

---

## 🗄️ 数据库配置

**配置文件**: `config/database/database.yaml`

### PostgreSQL配置

```yaml
host: postgres
port: 5432
database: web3_alpha_hunter
username: postgres
password: ${DB_PASSWORD}  # 从环境变量读取
```

### Redis配置

```yaml
host: redis
port: 6379
database: 0
```

---

## 🚀 快速使用指南

### 1. 首次配置

```bash
# 1. 复制API密钥示例文件
cp config/keys/api-keys.example.yaml config/keys/api-keys.yaml

# 2. 编辑配置文件,填入真实密钥
vi config/keys/api-keys.yaml

# 3. 确保SSH密钥权限正确
chmod 600 config/keys/VPNKEY.pem

# 4. 测试SSH连接
ssh -i config/keys/VPNKEY.pem root@47.253.226.250
```

### 2. 在代码中使用配置

#### Python (后端)

```python
import yaml

# 读取服务器配置
with open('config/servers/production.yaml') as f:
    server_config = yaml.safe_load(f)

print(server_config['server']['connection']['host'])
# 输出: 47.253.226.250

# 读取API密钥
with open('config/keys/api-keys.yaml') as f:
    api_keys = yaml.safe_load(f)

openai_key = api_keys['ai_services']['openai']['api_key']
```

#### TypeScript (前端)

```typescript
import yaml from 'js-yaml'
import fs from 'fs'

// 读取域名配置
const domainsConfig = yaml.load(
  fs.readFileSync('config/domains/domains.yaml', 'utf8')
)

const apiDomain = domainsConfig.current_domains.recommended_subdomains.api.domain
// 输出: api.web3.guandongfang.cn
```

### 3. 部署时使用配置

```bash
# 上传配置到服务器
scp -i config/keys/VPNKEY.pem \
  config/database/database.yaml \
  root@47.253.226.250:/app/web3-alpha-hunter/config/

# 从配置生成环境变量
ssh -i config/keys/VPNKEY.pem root@47.253.226.250 << 'EOF'
  cd /app/web3-alpha-hunter
  python scripts/generate_env_from_config.py
EOF
```

---

## 🔒 安全最佳实践

### ✅ 应该做的

1. **使用环境变量**
   ```bash
   # 不要在配置文件中硬编码密码
   password: ${DB_PASSWORD}
   ```

2. **定期轮换密钥**
   - SSH密钥: 每6个月
   - API密钥: 每3个月
   - 数据库密码: 每月

3. **使用密钥管理服务**
   - 生产环境建议使用AWS Secrets Manager或HashiCorp Vault
   - 开发环境可以使用`.env`文件

4. **限制权限**
   ```bash
   chmod 600 config/keys/*.pem
   chmod 600 config/keys/api-keys.yaml
   ```

### ❌ 不应该做的

1. ❌ 将真实密钥提交到Git
2. ❌ 通过聊天工具发送密钥
3. ❌ 在公共场所展示包含密钥的屏幕
4. ❌ 使用弱密码或默认密码

---

## 📋 配置清单

### 服务器配置 ✅
- [x] SSH密钥已移至`config/keys/`
- [x] 服务器信息已记录在`servers/production.yaml`
- [x] SSH权限已设置为600

### 域名配置 ✅
- [x] 主域名`web3.guandongfang.cn`已解析
- [ ] 子域名`api.web3.guandongfang.cn`待配置
- [ ] SSL证书待申请

### API密钥 ⏳
- [x] 示例文件已创建
- [ ] 填写OpenAI密钥
- [ ] 填写DeepSeek密钥
- [ ] 填写Twitter API密钥
- [ ] 填写Telegram Bot Token
- [ ] 填写CoinGecko API密钥

### 数据库配置 ✅
- [x] PostgreSQL配置已定义
- [x] Redis配置已定义
- [ ] 生产环境密码待设置

---

## 🔄 配置更新流程

1. **更新配置文件**
   ```bash
   vi config/servers/production.yaml
   ```

2. **验证配置格式**
   ```bash
   # 验证YAML语法
   python -c "import yaml; yaml.safe_load(open('config/servers/production.yaml'))"
   ```

3. **提交到Git** (仅非敏感配置)
   ```bash
   git add config/servers/production.yaml
   git commit -m "更新服务器配置"
   ```

4. **同步到服务器**
   ```bash
   rsync -avz -e "ssh -i config/keys/VPNKEY.pem" \
     config/ root@47.253.226.250:/app/web3-alpha-hunter/config/
   ```

---

## 📞 问题排查

### SSH密钥无法使用

```bash
# 检查密钥权限
ls -la config/keys/VPNKEY.pem
# 应该显示: -rw------- (600)

# 修复权限
chmod 600 config/keys/VPNKEY.pem

# 测试连接
ssh -vvv -i config/keys/VPNKEY.pem root@47.253.226.250
```

### YAML解析错误

```bash
# 使用yamllint检查
pip install yamllint
yamllint config/

# 或使用Python验证
python -c "import yaml; yaml.safe_load(open('config/domains/domains.yaml'))"
```

### Git误提交密钥

```bash
# 从Git历史中移除敏感文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/keys/api-keys.yaml" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送(谨慎!)
git push origin --force --all
```

---

## 🔗 相关文档

- [服务器连接指南](../docs/04-部署与运维/02-服务器连接指南.md)
- [服务器环境详情](../docs/04-部署与运维/03-服务器环境详情.md)
- [部署指南](../docs/04-部署与运维/01-部署指南.md)
- [配置说明](../guides/config/CONFIG_KEYS.md)

---

**维护者**: 开发团队
**最后审查**: 2025-10-04
