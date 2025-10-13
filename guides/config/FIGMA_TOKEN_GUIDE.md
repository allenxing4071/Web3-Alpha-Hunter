# Figma Personal Access Token 创建指南

> **最后更新**: 2025-01-13

本指南详细说明如何在 Figma 中创建 Personal Access Token，用于配置 Figma MCP Server。

---

## 🚀 快速步骤

### 步骤 1: 访问 Figma Settings

1. 打开浏览器，访问 [Figma Settings](https://www.figma.com/settings)
2. 登录您的 Figma 账户

### 步骤 2: 找到 Personal Access Tokens

1. 在左侧菜单中找到 **"Personal Access Tokens"** 选项
2. 点击进入该页面

### 步骤 3: 创建新 Token

1. 点击 **"Create new token"** 按钮
2. 在弹出的窗口中输入 Token 名称：
   - 建议名称：`cursor-mcp-token`
   - 或：`web3-alpha-hunter-mcp`
3. 点击 **"Create token"**

### 步骤 4: 复制 Token

1. **立即复制** 生成的 Token（格式：`figd_xxxxx...`）
2. **重要**: Token 只显示一次，关闭后将无法再次查看！
3. 将 Token 保存到安全的地方

### 步骤 5: 配置到项目

将 Token 添加到项目中的 `.env.local` 文件：

```bash
# 编辑 .env.local 文件
FIGMA_ACCESS_TOKEN=figd_your_actual_token_here
```

---

## 📸 详细截图说明

### 1. 登录 Figma Settings

访问 https://www.figma.com/settings，确保您已登录：

```
Figma Settings
├── Account
├── Teams & Projects
├── Billing & Usage
├── Security & Privacy
├── Apps & Integrations
├── Personal Access Tokens  ← 点击这里
└── Developer
```

### 2. Personal Access Tokens 页面

进入后您会看到：

```
Personal Access Tokens
├── [Create new token] 按钮
├── (如果已有 Token，会显示列表)
└── 说明文字
```

### 3. 创建 Token 对话框

点击 "Create new token" 后弹出：

```
Create a new personal access token

Token name: [cursor-mcp-token]  ← 输入名称

[Cancel] [Create token]  ← 点击创建
```

### 4. Token 生成页面

创建成功后显示：

```
Your new personal access token

figd_1a2b3c4d5e6f7g8h9i0j...  ← 立即复制这个！

⚠️  This token will only be shown once.
    Make sure to copy it now.

[I've copied the token]  ← 确认后关闭
```

---

## 🔐 Token 安全注意事项

### 保护您的 Token

1. **不要分享**: 不要将 Token 分享给他人
2. **不要提交到 Git**: 确保 `.env.local` 在 `.gitignore` 中
3. **定期轮换**: 建议每 3-6 个月更新一次 Token
4. **最小权限**: Token 具有与您账户相同的权限

### 如果 Token 泄露

1. 立即删除泄露的 Token
2. 创建新的 Token
3. 更新所有使用该 Token 的服务

---

## 🐛 常见问题

### Q1: 找不到 Personal Access Tokens 选项？

**可能原因**:
- 您使用的是团队账户而非个人账户
- 账户权限限制

**解决方案**:
- 确保使用个人账户登录
- 联系 Figma 管理员获取权限

### Q2: Token 创建失败？

**可能原因**:
- 网络连接问题
- 账户验证问题
- 浏览器插件阻止

**解决方案**:
- 刷新页面重试
- 使用无痕模式
- 检查网络连接

### Q3: 忘记复制 Token？

**解决方案**:
- **无法恢复**，必须创建新的 Token
- 删除旧的 Token，创建新的

### Q4: Token 无效？

**可能原因**:
- Token 格式错误（必须以 `figd_` 开头）
- Token 已过期或被撤销
- 复制时包含空格

**解决方案**:
- 检查 Token 格式
- 创建新的 Token
- 确保复制完整 Token

---

## 🔧 验证 Token 有效性

创建 Token 后，可以通过以下方式验证：

### 方法 1: 使用 curl 测试

```bash
# 替换 YOUR_TOKEN 为您的实际 Token
curl -H "X-Figma-Token: YOUR_TOKEN" \
     "https://api.figma.com/v1/me"
```

如果返回用户信息，说明 Token 有效。

### 方法 2: 在 Cursor 中测试

配置好 Token 并重启 Cursor 后：

```
@figma 测试连接
```

如果看到 Figma 相关提示，说明配置成功。

---

## 📋 Token 管理最佳实践

### 1. 命名规范

```
推荐命名:
- cursor-mcp-token
- project-name-mcp-token
- username-figma-token
```

### 2. 环境分离

```bash
# 开发环境
FIGMA_ACCESS_TOKEN_DEV=figd_xxx

# 生产环境
FIGMA_ACCESS_TOKEN_PROD=figd_yyy
```

### 3. 定期检查

每月检查一次：
- Token 是否仍在有效
- 是否有异常使用
- 是否需要轮换

### 4. 备份策略

- 将 Token 保存在密码管理器中
- 不要存储在明文文件中
- 团队成员共享时使用安全方式

---

## 🎯 下一步操作

### 配置完成后的验证

1. **编辑 `.env.local`**
   ```bash
   FIGMA_ACCESS_TOKEN=figd_your_actual_token_here
   ```

2. **重启 Cursor**
   - 完全关闭 Cursor
   - 重新打开

3. **测试连接**
   ```
   @figma 测试连接
   ```

4. **开始使用**
   ```
   @figma https://www.figma.com/file/xxx/Design

   请生成 Button 组件...
   ```

---

## 📚 相关资源

- [Figma API 文档](https://www.figma.com/developers/api)
- [Figma Personal Access Tokens 官方文档](https://help.figma.com/hc/en-us/articles/8085703771159)
- [Figma MCP 配置指南](../FIGMA_MCP_SETUP.md)
- [提示词模板库](../FIGMA_PROMPT_TEMPLATES.md)

---

## 🆘 获取帮助

如遇到问题：
1. 查看本文档的"常见问题"部分
2. 访问 [Figma Help Center](https://help.figma.com/)
3. 查看项目 [Figma MCP 配置指南](../FIGMA_MCP_SETUP.md)

---

**祝您配置顺利！** 🎉