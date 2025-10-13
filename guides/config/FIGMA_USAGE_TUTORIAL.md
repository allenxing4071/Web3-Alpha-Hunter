# Figma 转代码完整使用教程

> **最后更新**: 2025-01-13

本教程详细演示如何从 Figma 设计到 Cursor 生成代码的完整流程。

---

## 🎯 完整工作流程

### 流程图

```
Figma 设计 → 复制链接 → Cursor 使用 @figma → AI 生成代码
```

---

## 📝 详细步骤演示

### 步骤 1: 在 Figma 中准备设计

#### 1.1 打开您的 Figma 设计文件

1. 访问 [Figma](https://www.figma.com/)
2. 登录您的账户
3. 打开您想要转换为代码的设计文件

#### 1.2 选择要转换的设计元素

**选项 A: 选择单个 Frame（推荐）**
- 点击选中您想要转换的 Frame（如：Button、Card、Header 等）
- 这个 Frame 就是您想要生成代码的组件

**选项 B: 选择整个页面**
- 选择整个页面或大型布局
- 适合生成完整的页面代码

**选项 C: 选择组件**
- 选择 Figma 组件库中的组件
- 适合生成可复用的组件代码

---

### 步骤 2: 复制 Figma 链接

#### 方法 1: 使用右键菜单（推荐）

1. 在 Figma 中选中您要转换的 Frame 或组件
2. 右键点击
3. 选择 **"Copy link to selection"** 或 **"复制选区链接"**
4. 链接已复制到剪贴板！

#### 方法 2: 使用快捷键

1. 选中 Frame 或组件
2. 按快捷键：
   - Mac: `Cmd + Shift + .`
   - Windows/Linux: `Ctrl + Shift + .`
3. 链接已复制！

#### 方法 3: 从浏览器地址栏复制

1. 选中 Frame 或组件
2. 浏览器地址栏会自动更新
3. 复制浏览器地址栏的完整 URL

**链接格式示例**:
```
https://www.figma.com/file/abc123xyz/ProjectName?node-id=123:456
                          ↑                         ↑
                    文件ID                      节点ID
```

---

### 步骤 3: 在 Cursor 中使用 @figma

#### 3.1 打开 Cursor

1. 打开 Cursor 编辑器
2. 打开您的项目（任意项目，已配置全局后）
3. 打开 Cursor 聊天窗口（通常在右侧或底部）

#### 3.2 输入 @figma 命令

在聊天窗口中输入：

```
@figma https://www.figma.com/file/abc123xyz/ProjectName?node-id=123:456

请根据这个设计生成 Button 组件:
- React + TypeScript
- Tailwind CSS
- 支持 primary, secondary, ghost variants
- 包含 hover 和 disabled 状态
```

**格式说明**:
- `@figma` - 唤醒 Figma MCP
- `[空格]` - 空格分隔
- `[Figma URL]` - 粘贴您复制的 Figma 链接
- `[换行]` - 换行后输入详细需求
- `[详细需求]` - 说明您想要生成的代码

#### 3.3 等待 AI 响应

1. Cursor 会自动连接 Figma API
2. 获取设计的详细信息（尺寸、颜色、间距等）
3. 分析设计结构
4. 生成符合您要求的代码

---

## 🎨 实际使用示例

### 示例 1: 生成按钮组件

#### 在 Figma 中:
1. 打开您的设计文件
2. 找到 Button 设计
3. 选中 Button Frame
4. 右键 → "Copy link to selection"
5. 得到链接: `https://www.figma.com/file/xxx/Design?node-id=100:200`

#### 在 Cursor 中:
```
@figma https://www.figma.com/file/xxx/Design?node-id=100:200

请生成这个 Button 组件:

技术栈:
- React + TypeScript
- Tailwind CSS

功能需求:
- 支持 variant: primary, secondary, outline, ghost
- 支持 size: sm, md, lg
- 支持 loading 状态（显示 spinner）
- 支持 disabled 状态
- 支持左右图标 (leftIcon, rightIcon)

设计要求:
- 精确匹配 Figma 中的颜色、间距、圆角
- 响应式设计
- 支持深色模式 (dark:)
- 添加 hover 和 active 动画

请生成:
1. 完整的组件代码
2. TypeScript 类型定义
3. 使用示例
```

---

### 示例 2: 生成卡片组件

#### 在 Figma 中:
1. 选中 Card 设计
2. 复制链接: `https://www.figma.com/file/xxx/Dashboard?node-id=200:300`

#### 在 Cursor 中:
```
@figma https://www.figma.com/file/xxx/Dashboard?node-id=200:300

请生成这个 Card 组件:

组件结构:
- CardHeader (头部)
- CardTitle (标题)
- CardDescription (描述)
- CardContent (内容区域)
- CardFooter (底部)

技术要求:
- Next.js 14 + TypeScript
- Tailwind CSS + shadcn/ui
- 组件可组合使用

功能:
- 支持 variant: default, elevated, outlined
- 支持 hover 悬浮效果
- 可点击（整个卡片作为链接）
- 加载骨架屏 (CardSkeleton)

请包含完整的类型定义和使用示例
```

---

### 示例 3: 生成完整页面

#### 在 Figma 中:
1. 选中整个页面或主 Frame
2. 复制链接: `https://www.figma.com/file/xxx/App?node-id=300:400`

#### 在 Cursor 中:
```
@figma https://www.figma.com/file/xxx/App?node-id=300:400

请生成这个仪表板页面:

页面布局:
- 顶部导航栏（Logo、菜单、用户头像）
- 侧边栏（可折叠）
- 主内容区域（统计卡片 + 图表）

技术栈:
- Next.js 14 App Router
- TypeScript
- Tailwind CSS + shadcn/ui
- Recharts（图表）
- Lucide React（图标）

功能需求:
- 响应式布局（桌面3列、平板2列、移动1列）
- 支持深色模式
- 数据卡片显示（数值、趋势、图标）
- 交互式图表
- 加载状态和骨架屏

请生成:
1. 页面主文件
2. 所有子组件
3. TypeScript 类型
4. Mock 数据示例
```

---

## 🎯 关键要点

### 1. Figma 链接必须包含 node-id

**正确的链接格式**:
```
✅ https://www.figma.com/file/xxx/ProjectName?node-id=123:456
                                              ↑
                                          包含 node-id
```

**错误的链接格式**:
```
❌ https://www.figma.com/file/xxx/ProjectName
                                  ↑
                            没有 node-id，AI 不知道要生成哪个设计
```

**如何确保有 node-id**:
- 必须先选中具体的 Frame、组件或元素
- 然后复制链接
- 链接中会自动包含 `?node-id=xxx:xxx`

---

### 2. 提供详细的需求说明

越详细的需求，生成的代码质量越高：

```
基础需求:
@figma [URL]
请生成 Button 组件

↓ 改进为 ↓

详细需求:
@figma [URL]
请生成 Button 组件:
- 技术栈: React + TypeScript + Tailwind CSS
- Variants: primary, secondary, outline, ghost
- Sizes: sm, md, lg
- 状态: hover, active, disabled, loading
- 功能: 支持图标、完整类型定义
- 要求: 响应式、深色模式、无障碍
```

---

### 3. 引用项目规范

如果项目中有 `.cursorrules` 文件：

```
@figma [URL]

请按照 .cursorrules 中的规范生成代码:
- 使用项目的设计系统
- 遵循代码风格指南
- 应用性能最佳实践

[其他具体需求...]
```

---

## 🔧 进阶技巧

### 技巧 1: 分步生成

复杂设计可以分步生成：

```
第一步 - 分析设计:
@figma [URL]
请先分析这个设计的组件层次结构，列出所有需要创建的组件

第二步 - 生成核心组件:
现在请生成 [具体组件名] 组件的代码

第三步 - 添加功能:
请为这个组件添加 [具体功能]
```

### 技巧 2: 批量生成组件

```
@figma [URL 1]
请生成 Button 组件

@figma [URL 2]
请生成 Input 组件

@figma [URL 3]
请生成 Card 组件

技术栈统一使用: React + TypeScript + Tailwind CSS
```

### 技巧 3: 生成变体

```
@figma [URL]

请生成这个组件的所有变体:
- Button/Primary
- Button/Secondary
- Button/Outline
- Button/Ghost

使用 CVA (class-variance-authority) 管理变体
```

---

## 📋 Figma 设计准备建议

为了获得最佳的代码生成效果，在 Figma 中设计时请注意：

### 1. 使用 Auto Layout
- 所有组件必须使用 Auto Layout
- 正确设置 padding、gap、对齐方式

### 2. 规范命名
```
推荐命名格式:
- ComponentName/Variant/State
- 例如: Button/Primary/Default
        Button/Primary/Hover
        Card/Elevated/Default
```

### 3. 使用设计令牌
- 创建 Variables（颜色、间距、圆角）
- 使用 Styles（文字、效果）
- 组件库统一管理

### 4. 定义完整状态
- Default（默认）
- Hover（悬停）
- Active（激活）
- Disabled（禁用）
- Loading（加载中，如果适用）

---

## 🐛 常见问题

### Q1: 链接中没有 node-id？

**原因**: 没有选中具体的 Frame 或组件

**解决**:
1. 在 Figma 中点击选中具体的 Frame
2. 再复制链接
3. 确认链接包含 `?node-id=xxx:xxx`

### Q2: AI 说无法访问设计？

**原因**: Figma 文件权限不足

**解决**:
1. 确认文件权限至少是 "Can view"
2. 如果是私有文件，确认您的 Token 有权限访问
3. 尝试将文件设为 "Anyone with the link can view"

### Q3: 生成的代码不符合预期？

**原因**: 需求描述不够详细

**解决**:
1. 明确指定技术栈
2. 详细描述功能需求
3. 说明设计要求
4. 引用项目规范（.cursorrules）

### Q4: @figma 没有响应？

**原因**: MCP 配置未生效

**解决**:
1. 确认已配置全局设置
2. 完全重启 Cursor
3. 等待 1-2 分钟让 MCP 启动
4. 运行配置检查脚本

---

## 📚 相关文档

- [Figma MCP 配置指南](./FIGMA_MCP_SETUP.md)
- [Figma Token 创建指南](./FIGMA_TOKEN_GUIDE.md)
- [Figma AI 使用指南](./FIGMA_AI_USAGE_GUIDE.md)
- [全局配置说明](./GLOBAL_SETUP_INSTRUCTIONS.md)
- [提示词模板库](./FIGMA_PROMPT_TEMPLATES.md)

---

## 🎊 快速开始

1. 在 Figma 中选中设计
2. 复制链接（右键 → Copy link to selection）
3. 在 Cursor 中输入：
   ```
   @figma [粘贴链接]

   请生成 [组件名] 组件:
   [详细需求...]
   ```
4. 等待 AI 生成代码
5. 开始使用！

---

**现在您应该清楚如何使用了！试试看吧！** 🚀
