# Figma MCP Server 配置指南

## 📋 概述

本指南帮助您配置 Figma MCP Server 与 Cursor + Claude 4.5 集成，实现高级 UI 代码生成。

## 🚀 快速开始

### 1. 获取 Figma Personal Access Token

1. 访问 [Figma Settings](https://www.figma.com/settings)
2. 进入 **Personal Access Tokens** 部分
3. 点击 **Create new token**
4. 输入 Token 名称（如：`cursor-mcp-token`）
5. 复制生成的 Token（格式：`figd_xxxxx...`）

⚠️ **重要**: 请立即保存此 Token，关闭后将无法再次查看！

### 2. 配置环境变量

在项目根目录创建或编辑 `.env.local` 文件：

```bash
# Figma MCP Configuration
FIGMA_ACCESS_TOKEN=figd_your_token_here
```

⚠️ 确保 `.env.local` 已添加到 `.gitignore`，不要提交到 Git！

### 3. 配置 Cursor MCP 设置

#### 方法 A: 使用 Cursor Settings UI（推荐）

1. 打开 Cursor
2. 按 `Cmd/Ctrl + Shift + P` 打开命令面板
3. 输入 `Preferences: Open User Settings (JSON)`
4. 添加以下配置：

```json
{
  "mcp": {
    "servers": {
      "figma": {
        "command": "npx",
        "args": [
          "-y",
          "figma-developer-mcp",
          "--figma-api-key",
          "YOUR_FIGMA_TOKEN_HERE",
          "--stdio"
        ],
        "disabled": false
      }
    }
  }
}
```

#### 方法 B: 使用 .mcp.json 配置文件

在项目根目录创建 `.mcp.json`：

```json
{
  "servers": {
    "figma": {
      "command": "node_modules/.bin/figma-developer-mcp",
      "args": [
        "--figma-api-key",
        "${FIGMA_ACCESS_TOKEN}",
        "--stdio"
      ],
      "env": {
        "FIGMA_ACCESS_TOKEN": "从环境变量读取"
      }
    }
  }
}
```

### 4. 验证安装

重启 Cursor 后，在聊天窗口输入：

```
@figma 测试连接
```

如果看到 Figma 图标或提示，说明配置成功！

---

## 🎯 使用方法

### 方法 1: 使用 Figma 文件 URL

```
@figma https://www.figma.com/file/xxx/ProjectName?node-id=123:456

请根据这个设计生成 React + Tailwind 组件
```

### 方法 2: 指定 Figma Frame

```
请实现 Figma 中的 "Hero Section" 设计:
https://www.figma.com/file/xxx/ProjectName?node-id=789:012

要求:
- Next.js 14 + TypeScript
- Tailwind CSS
- 响应式设计
- 深色模式支持
```

### 方法 3: 生成整个页面

```
@figma https://www.figma.com/file/xxx/Dashboard

生成完整的仪表板页面:
- 使用 shadcn/ui 组件
- 支持数据可视化 (使用 recharts)
- 响应式布局
- 加载状态和错误处理
```

---

## 📝 最佳实践

### 在 Figma 中

1. **使用 Auto Layout**
   - 所有组件必须使用 Auto Layout
   - 设置合理的 padding 和 gap

2. **规范命名**
   - 组件: `ComponentName/Variant/State`
   - 示例: `Button/Primary/Large`, `Card/Elevated/Default`

3. **使用设计系统**
   - 创建 Variables (颜色、间距、圆角)
   - 使用 Styles (文字、效果)
   - 组件库统一管理

4. **定义交互状态**
   - Default, Hover, Active, Disabled
   - 使用 Variants 组织状态

### 在 Cursor 中

1. **清晰的提示词**
   ```
   请根据 Figma 设计生成组件:
   - 技术栈: [框架/库]
   - 样式方案: [CSS方案]
   - 特殊要求: [响应式/动画/状态]
   ```

2. **指定组件库**
   ```
   使用 shadcn/ui 组件:
   - Button, Card, Dialog 等
   - 保持一致的设计语言
   ```

3. **迭代优化**
   ```
   请优化这个组件:
   - 添加 loading 状态
   - 改进无障碍性 (ARIA)
   - 性能优化 (memo, lazy load)
   ```

---

## 🔧 高级配置

### 自定义 MCP Server 参数

在 `.mcp.json` 中添加更多选项：

```json
{
  "servers": {
    "figma": {
      "command": "node_modules/.bin/figma-developer-mcp",
      "args": [
        "--figma-api-key",
        "${FIGMA_ACCESS_TOKEN}",
        "--cache-ttl",
        "3600",
        "--max-depth",
        "5",
        "--stdio"
      ]
    }
  }
}
```

参数说明:
- `--cache-ttl`: 缓存时间（秒）
- `--max-depth`: 最大遍历深度
- `--verbose`: 启用详细日志

### 配置代理（如需要）

```json
{
  "servers": {
    "figma": {
      "command": "node_modules/.bin/figma-developer-mcp",
      "args": ["--figma-api-key", "${FIGMA_ACCESS_TOKEN}", "--stdio"],
      "env": {
        "HTTP_PROXY": "http://proxy.example.com:8080",
        "HTTPS_PROXY": "https://proxy.example.com:8080"
      }
    }
  }
}
```

---

## 🐛 常见问题

### 1. Token 无效

**错误**: `Authentication failed: Invalid token`

**解决**:
- 检查 Token 是否正确复制（包含 `figd_` 前缀）
- 确认 Token 未过期
- 在 Figma Settings 中重新生成 Token

### 2. 无法找到 Figma 文件

**错误**: `File not found: 404`

**解决**:
- 确认您有文件访问权限
- 检查 URL 是否正确
- 确保文件未被删除或移动

### 3. MCP Server 连接失败

**错误**: `Failed to connect to MCP server`

**解决**:
```bash
# 检查 figma-developer-mcp 是否正确安装
npm list figma-developer-mcp

# 重新安装
npm install --save-dev figma-developer-mcp

# 重启 Cursor
```

### 4. 权限问题

**错误**: `Permission denied`

**解决**:
- 确保 Figma 文件设置为 "Can view" 或更高权限
- 检查团队/项目访问权限
- 使用个人 Access Token（非 OAuth）

---

## 📚 实用示例

### 示例 1: 生成登录表单

```
@figma https://www.figma.com/file/xxx/Auth-Screens?node-id=100:200

请生成登录表单组件:

技术栈:
- React + TypeScript
- React Hook Form + Zod validation
- Tailwind CSS + shadcn/ui

要求:
- 邮箱和密码字段
- 表单验证和错误提示
- Loading 状态
- "忘记密码" 和 "注册" 链接
- 响应式设计
```

### 示例 2: 生成数据卡片

```
@figma https://www.figma.com/file/xxx/Dashboard?node-id=200:300

请生成统计卡片组件:

要求:
- 显示标题、数值、趋势（↑↓）
- 使用 Lucide React 图标
- 支持 skeleton loading
- 响应式 grid 布局
- Props 类型安全
```

### 示例 3: 生成导航菜单

```
@figma https://www.figma.com/file/xxx/Navigation?node-id=300:400

请生成响应式导航菜单:

技术栈:
- Next.js 14 App Router
- Radix UI (Dropdown Menu)
- Tailwind CSS

功能:
- 桌面端: 横向菜单
- 移动端: 汉堡菜单
- 用户头像下拉菜单
- 支持深色模式
- 平滑动画过渡
```

---

## 🎨 推荐工作流程

### 1. 设计阶段（Figma）

```
设计师创建设计
    ↓
规范化设计（Auto Layout, Variables）
    ↓
整理组件库和样式指南
    ↓
分享文件并设置权限
```

### 2. 开发阶段（Cursor）

```
复制 Figma URL
    ↓
在 Cursor 中使用 @figma 提及
    ↓
编写详细的提示词
    ↓
Claude 生成初始代码
    ↓
迭代优化和调整
    ↓
集成到项目中
```

### 3. 协作优化

```
设计更新 → 开发快速迭代
    ↓
建立设计令牌系统
    ↓
共享组件库和样式
    ↓
持续同步和改进
```

---

## 📖 相关资源

- [Figma API 文档](https://www.figma.com/developers/api)
- [figma-developer-mcp GitHub](https://github.com/your-org/figma-developer-mcp)
- [Cursor 文档](https://docs.cursor.com/)
- [MCP 协议规范](https://modelcontextprotocol.io/)

---

## 🆘 获取帮助

如遇到问题:
1. 查看本文档的"常见问题"部分
2. 检查 Cursor 输出面板的错误日志
3. 访问项目 GitHub Issues
4. 联系团队技术支持

---

最后更新: 2025-01-13
