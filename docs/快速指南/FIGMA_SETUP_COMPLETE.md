# 🎉 Figma MCP Server 配置完成

> **配置时间**: 2025-01-13
> **状态**: ✅ 已完成

---

## 📦 已安装的组件

### 1. Figma MCP Server
- ✅ 已安装 `figma-developer-mcp` (v0.6.1)
- 📍 位置: `node_modules/figma-developer-mcp`
- 🔧 配置文件: [.mcp.json](./.mcp.json)

### 2. 配置文件

#### [.mcp.json](./.mcp.json)
Cursor MCP 服务器配置文件，用于连接 Figma API。

#### [.cursorrules](./.cursorrules)
Cursor AI 代码生成规则，包含：
- 项目技术栈配置
- Figma 设计转代码规范
- 样式系统（Tailwind CSS）
- 组件开发标准
- 响应式设计规则
- 无障碍性要求

#### [.env.local.example](./.env.local.example)
环境变量模板文件，需要复制为 `.env.local` 并填入真实 Token。

---

## 📚 文档资源

### 主要文档

1. **[Figma MCP 配置指南](./guides/config/FIGMA_MCP_SETUP.md)**
   - 获取 Figma Access Token 的步骤
   - 完整的配置说明
   - 常见问题解决方案
   - 验证安装方法

2. **[Figma Token 创建指南](./guides/config/FIGMA_TOKEN_GUIDE.md)**
   - 详细的 Token 创建步骤
   - 截图说明和常见问题
   - Token 安全注意事项
   - 验证 Token 有效性

3. **[提示词模板库](./guides/config/FIGMA_PROMPT_TEMPLATES.md)**
   - 10+ 种常见组件的提示词模板
   - 按钮、表单、卡片、导航等
   - 完整页面模板（仪表板、登录页等）
   - 高级提示词技巧

3. **[快速启动脚本](./guides/config/figma-quick-setup.sh)**
   - 一键检查配置状态
   - 自动安装依赖
   - 引导配置 Token

---

## 🚀 下一步操作

### 步骤 1: 获取 Figma Personal Access Token

1. 访问 [Figma Settings](https://www.figma.com/settings)
2. 找到 **Personal Access Tokens** 部分
3. 点击 **Create new token**
4. 输入名称（如：`cursor-mcp-token`）
5. 复制生成的 Token（格式：`figd_xxxxx...`）

⚠️ **重要**: Token 只显示一次，请立即保存！

### 步骤 2: 配置环境变量

创建 `.env.local` 文件（如果还没有）:

```bash
# 复制示例文件
cp .env.local.example .env.local

# 编辑文件，添加您的 Token
# FIGMA_ACCESS_TOKEN=figd_your_real_token_here
```

或直接编辑 `.env.local`:

```bash
echo "FIGMA_ACCESS_TOKEN=figd_your_token_here" > .env.local
```

### 步骤 3: 验证配置

运行快速配置脚本检查一切是否就绪：

```bash
cd guides/config
./figma-quick-setup.sh
```

### 步骤 4: 重启 Cursor

关闭并重新打开 Cursor 编辑器，让 MCP 配置生效。

### 步骤 5: 测试连接

在 Cursor 聊天窗口中输入：

```
@figma 测试连接
```

如果看到 Figma 相关提示或图标，说明配置成功！

---

## 💡 快速使用示例

### 示例 1: 生成简单组件

```
@figma https://www.figma.com/file/xxx/ProjectName?node-id=123:456

请根据这个设计生成 Button 组件:
- React + TypeScript
- Tailwind CSS
- 支持 primary, secondary, outline variants
- 包含 hover 和 disabled 状态
```

### 示例 2: 生成完整页面

```
@figma https://www.figma.com/file/xxx/Dashboard

请生成仪表板页面:
- Next.js 14 + shadcn/ui
- 包含统计卡片和图表
- 响应式布局
- 深色模式支持
```

### 示例 3: 使用项目规范

```
@figma https://www.figma.com/file/xxx/Form

请按照 .cursorrules 中的规范生成登录表单:
- React Hook Form + Zod validation
- shadcn/ui 组件
- 完整的错误处理
- loading 状态
```

---

## 🔧 项目集成

### 技术栈配置

已在 [.cursorrules](./.cursorrules) 中配置:

- **前端框架**: Next.js 14 + React + TypeScript
- **样式方案**: Tailwind CSS
- **组件库**: shadcn/ui
- **表单**: React Hook Form + Zod
- **图表**: Recharts
- **图标**: Lucide React
- **动画**: Framer Motion

### 设计系统

已定义的设计令牌:

**颜色系统**:
- Primary: `#3B82F6` (blue-500)
- Secondary: `#8B5CF6` (violet-500)
- Accent: `#10B981` (emerald-500)

**间距系统**:
- 基础单位: 4px
- 常用值: 4, 8, 12, 16, 24, 32, 48, 64px

**圆角系统**:
- sm: 6px
- md: 8px
- lg: 12px
- xl: 16px

**字体**:
- 主字体: Inter (sans-serif)
- 等宽: JetBrains Mono

---

## 📖 学习资源

### Figma 最佳实践

在设计时遵循这些原则，可以获得更好的代码生成质量:

1. **使用 Auto Layout** - 所有组件必须使用 Auto Layout
2. **规范命名** - 图层命名清晰（如：`Button/Primary/Large`）
3. **设计系统** - 使用 Variables 定义颜色、间距、字体
4. **组件化** - 创建可复用的组件库
5. **状态定义** - 明确 default, hover, active, disabled 状态

### 相关链接

- [Figma API 文档](https://www.figma.com/developers/api)
- [shadcn/ui 组件库](https://ui.shadcn.com/)
- [Tailwind CSS 文档](https://tailwindcss.com/)
- [Radix UI 文档](https://www.radix-ui.com/)
- [Cursor 文档](https://docs.cursor.com/)

---

## 🐛 常见问题

### Q1: Token 无效或认证失败？

**解决方案**:
1. 检查 Token 格式是否完整（包含 `figd_` 前缀）
2. 确认 Token 未过期
3. 在 `.env.local` 中正确配置
4. 重启 Cursor

### Q2: 无法找到 Figma 文件？

**解决方案**:
1. 确认文件 URL 正确
2. 检查文件访问权限（至少需要 "Can view"）
3. 确认文件未被删除或移动

### Q3: MCP Server 无法连接？

**解决方案**:
```bash
# 检查安装
npm list figma-developer-mcp

# 重新安装
npm install --save-dev figma-developer-mcp

# 重启 Cursor
```

### Q4: 生成的代码不符合项目规范？

**解决方案**:
1. 检查 [.cursorrules](./.cursorrules) 是否存在
2. 在提示词中明确指定要遵循 `.cursorrules`
3. 提供更详细的技术栈说明

---

## 🎯 最佳实践建议

### 提示词编写技巧

1. **具体明确**
   ```
   ❌ 生成一个按钮
   ✅ 生成 TypeScript Button 组件,使用 Tailwind CSS,支持 3 种 variants
   ```

2. **提供上下文**
   ```
   这是用于 Web3 项目的 KOL 列表页面...
   使用 Next.js 14 App Router...
   ```

3. **分步进行**
   ```
   第一步: 先分析设计结构
   第二步: 生成核心组件
   第三步: 添加交互功能
   ```

4. **引用规则**
   ```
   请按照 .cursorrules 中定义的规范生成代码
   ```

### 工作流程建议

1. **设计阶段（Figma）**
   - 规范化设计（Auto Layout, Variables）
   - 整理组件库
   - 定义设计令牌

2. **开发阶段（Cursor）**
   - 复制 Figma URL
   - 使用 `@figma` 提及
   - 编写详细提示词
   - 迭代优化

3. **集成阶段**
   - 调整样式细节
   - 添加业务逻辑
   - 测试响应式和无障碍

---

## 🎉 开始使用

现在一切就绪！您可以:

1. ✅ 获取 Figma Token 并配置到 `.env.local`
2. ✅ 重启 Cursor
3. ✅ 打开您的 Figma 设计
4. ✅ 在 Cursor 中使用 `@figma` 开始生成代码

查看 [提示词模板库](./guides/config/FIGMA_PROMPT_TEMPLATES.md) 获取更多示例！

---

## 📞 获取帮助

如遇到问题:
1. 查看 [配置指南](./guides/config/FIGMA_MCP_SETUP.md) 的"常见问题"部分
2. 查看本文档的"常见问题"
3. 检查 Cursor 输出面板的错误日志
4. 访问 [figma-developer-mcp](https://www.npmjs.com/package/figma-developer-mcp) 查看最新文档

---

**祝您使用愉快！享受 AI 驱动的设计到代码工作流！** 🚀
