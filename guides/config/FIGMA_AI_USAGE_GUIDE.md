# Figma AI 唤醒和使用指南

> **最后更新**: 2025-01-13

本指南详细说明如何在 Cursor 中唤醒和使用 Figma AI 功能。

---

## 🚀 快速唤醒方法

### 方法 1: 使用 `@figma` 提及（推荐）

在 Cursor 聊天窗口中直接使用 `@figma` 提及：

```
@figma [您的 Figma 设计 URL]

请根据这个设计生成 [组件名称] 组件...
```

**示例**:
```
@figma https://www.figma.com/file/xxx/ProjectName?node-id=123:456

请根据这个设计生成 Button 组件:
- React + TypeScript
- Tailwind CSS
- 支持 primary, secondary, ghost variants
```

### 方法 2: 直接粘贴 Figma URL

直接粘贴 Figma 设计链接，Cursor 会自动识别：

```
https://www.figma.com/file/xxx/ProjectName?node-id=123:456

请实现这个设计...
```

### 方法 3: 使用 "测试连接" 命令

验证 Figma MCP 是否正常工作：

```
@figma 测试连接
```

---

## 📝 完整的唤醒流程

### 步骤 1: 准备 Figma 设计

1. 在 Figma 中打开您的设计文件
2. 选择要实现的 Frame 或组件
3. 复制 URL（格式：`https://www.figma.com/file/xxx/ProjectName?node-id=123:456`）

### 步骤 2: 在 Cursor 中唤醒

在 Cursor 聊天窗口中：

```
@figma [粘贴您的 Figma URL]

[您的详细需求说明]
```

### 步骤 3: 等待 AI 响应

Cursor 会：
1. 自动连接到 Figma MCP Server
2. 获取设计信息
3. 分析设计结构和样式
4. 开始生成代码

---

## 🎯 最佳唤醒提示词

### 基础模板

```
@figma [Figma URL]

请根据这个设计生成 [组件名称] 组件:

技术栈:
- React + TypeScript
- Tailwind CSS
- shadcn/ui

要求:
- 完整的 TypeScript 类型定义
- 响应式设计 (mobile-first)
- 支持深色模式
- 包含所有交互状态
- 无障碍性支持
```

### 高级模板

```
@figma [Figma URL]

请按照 .cursorrules 中的规范实现这个设计:

组件需求:
- [组件名称] - [功能描述]
- [组件名称] - [功能描述]

特殊要求:
- 使用 Framer Motion 动画
- 支持数据可视化 (Recharts)
- 表单验证 (React Hook Form + Zod)
- 性能优化 (React.memo, 懒加载)

请生成:
1. 完整的组件代码
2. 使用示例
3. Props 文档说明
```

---

## 🔧 常见唤醒场景

### 场景 1: 生成单个组件

```
@figma https://www.figma.com/file/xxx/Design?node-id=123:456

请生成这个 Button 组件:
- variant: primary, secondary, outline, ghost
- size: sm, md, lg
- 支持 loading 和 disabled 状态
- 使用 CVA (class-variance-authority)
```

### 场景 2: 生成完整页面

```
@figma https://www.figma.com/file/xxx/Dashboard

请生成完整的仪表板页面:

页面结构:
- 顶部导航栏
- 侧边菜单
- 主内容区域 (统计卡片 + 图表)
- 底部信息栏

技术要求:
- Next.js 14 App Router
- Tailwind CSS + shadcn/ui
- Recharts 数据可视化
- 响应式布局
- 深色模式支持
```

### 场景 3: 生成表单组件

```
@figma https://www.figma.com/file/xxx/Form

请生成登录表单组件:

包含:
- 邮箱输入框 (带验证)
- 密码输入框 (显示/隐藏切换)
- 记住我复选框
- 登录按钮 (loading 状态)
- 忘记密码链接
- 错误消息显示

技术集成:
- React Hook Form
- Zod 验证
- 与 Next-Auth 兼容
```

---

## 🐛 唤醒问题排查

### 问题 1: `@figma` 没有响应

**可能原因**:
- MCP 配置未生效
- Token 配置错误
- Cursor 需要重启

**解决方案**:
```bash
# 检查配置
./guides/config/figma-quick-setup.sh

# 重启 Cursor
# 完全关闭并重新打开
```

### 问题 2: "无法连接到 Figma"

**可能原因**:
- Token 无效或过期
- 网络连接问题
- Figma 文件权限问题

**解决方案**:
1. 检查 `.env.local` 中的 Token
2. 验证 Token 有效性
3. 确认 Figma 文件可访问

### 问题 3: 设计信息获取失败

**可能原因**:
- URL 格式错误
- Frame 不存在
- 设计文件权限不足

**解决方案**:
1. 确认 URL 包含 `node-id` 参数
2. 检查 Frame 是否存在于设计中
3. 确保有文件访问权限

---

## 💡 唤醒技巧

### 技巧 1: 分步唤醒

```
第一步 - 分析设计:
@figma [URL]
请先分析这个设计的组件层次结构

第二步 - 生成核心组件:
现在请生成 [组件名] 组件的代码

第三步 - 优化功能:
请为这个组件添加 [具体功能]
```

### 技巧 2: 引用项目规范

```
@figma [URL]

请按照 .cursorrules 中的规范生成代码:
- 使用项目设计系统
- 遵循代码风格指南
- 应用性能最佳实践
```

### 技巧 3: 提供上下文

```
@figma [URL]

这是用于 Web3 Alpha Hunter 项目的 [页面名称] 页面:
- 项目背景: [简要说明]
- 目标用户: [用户群体]
- 技术栈: [具体技术]

请生成符合项目需求的代码...
```

---

## 🎨 设计准备建议

### 在 Figma 中优化设计

1. **使用 Auto Layout**
   - 所有组件必须使用 Auto Layout
   - 设置合理的 padding 和 gap

2. **规范化命名**
   ```
   组件: ComponentName/Variant/State
   示例: Button/Primary/Large, Card/Elevated/Default
   ```

3. **使用设计系统**
   - 创建 Variables (颜色、间距、圆角)
   - 使用 Styles (文字、效果)
   - 组件库统一管理

4. **定义交互状态**
   - Default, Hover, Active, Disabled
   - 使用 Variants 组织状态

---

## 📚 相关资源

- [Figma MCP 配置指南](./FIGMA_MCP_SETUP.md)
- [Figma Token 创建指南](./FIGMA_TOKEN_GUIDE.md)
- [提示词模板库](./FIGMA_PROMPT_TEMPLATES.md)
- [配置完成总结](../FIGMA_SETUP_COMPLETE.md)

---

## 🆘 获取帮助

如遇到唤醒问题：
1. 查看本文档的"唤醒问题排查"部分
2. 运行配置检查脚本：`./guides/config/figma-quick-setup.sh`
3. 检查 Cursor 输出面板的错误日志
4. 查看项目 [Figma MCP 配置指南](./FIGMA_MCP_SETUP.md)

---

**祝您使用愉快！享受 AI 驱动的设计到代码工作流！** 🚀