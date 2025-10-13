# 您的 Figma 链接使用示例

> **您的 Figma 文件**: 结合cursor测试
> **链接**: https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

---

## ✅ 链接检查

您的链接格式正确！

```
https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1
                                                                    ↑
                                                            包含 node-id ✅
```

---

## 🎯 在 Cursor 中的使用方式

### 基础使用

在 Cursor 聊天窗口中输入：

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请根据这个设计生成组件代码
```

---

## 💡 推荐使用示例

### 示例 1: 生成按钮组件（如果设计中有 Button）

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请生成这个 Button 组件:

技术栈:
- React + TypeScript
- Tailwind CSS

功能需求:
- 支持 variant: primary, secondary, outline, ghost
- 支持 size: sm, md, lg
- 支持 loading 状态
- 支持 disabled 状态
- 支持左右图标

设计要求:
- 精确匹配 Figma 中的颜色、间距、圆角
- 响应式设计
- 支持深色模式
- 添加 hover 和 active 动画

请生成完整的 TypeScript 组件代码和使用示例
```

---

### 示例 2: 生成表单组件

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请生成这个表单组件:

技术要求:
- React Hook Form + Zod validation
- shadcn/ui 组件
- TypeScript

表单字段:
- 输入框（文本、邮箱、密码）
- 下拉选择
- 复选框
- 单选按钮

功能:
- 实时表单验证
- 错误消息显示
- 提交 loading 状态
- 响应式布局

请包含完整的类型定义和验证 schema
```

---

### 示例 3: 生成卡片组件

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请生成这个 Card 组件:

组件结构:
- CardHeader (头部)
- CardTitle (标题)
- CardDescription (描述)
- CardContent (内容区域)
- CardFooter (底部操作区)

技术栈:
- Next.js 14 + TypeScript
- Tailwind CSS + shadcn/ui

功能:
- 支持 variant: default, elevated, outlined
- 支持 hover 悬浮效果
- 可点击（整个卡片作为链接）
- 加载骨架屏

请生成所有子组件和完整的使用示例
```

---

### 示例 4: 生成完整页面

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请生成这个完整页面:

页面结构:
- 顶部导航栏
- 侧边菜单（可选）
- 主内容区域
- 底部信息

技术栈:
- Next.js 14 App Router
- TypeScript
- Tailwind CSS + shadcn/ui
- Framer Motion（动画）

功能需求:
- 响应式布局
- 深色模式支持
- 页面过渡动画
- SEO 优化

请生成:
1. 页面主文件
2. 所有子组件
3. TypeScript 类型
4. Layout 组件
```

---

### 示例 5: 按照项目规范生成

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请按照 .cursorrules 中的规范生成这个组件:

项目信息:
- 项目名: Web3 Alpha Hunter
- 技术栈: Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui

要求:
- 使用项目设计系统（颜色、间距、字体）
- 遵循项目代码风格
- 组件可复用
- 完整的 TypeScript 类型
- 响应式设计
- 无障碍性支持

请生成符合项目规范的完整代码
```

---

## 🎨 如果设计中有多个元素

如果您的 Figma 文件中有多个不同的组件，您需要：

### 步骤 1: 选中第一个组件
1. 在 Figma 中选中第一个组件（如：Button）
2. 右键 → "Copy link to selection"
3. 得到新链接（node-id 会不同）

### 步骤 2: 在 Cursor 中生成
```
@figma [第一个组件的链接]
请生成 Button 组件...
```

### 步骤 3: 选中第二个组件
1. 选中第二个组件（如：Card）
2. 复制新链接
3. 在 Cursor 中生成

---

## 🔧 通用模板

您可以使用这个通用模板：

```
@figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

请生成这个 [组件名称] 组件:

技术栈:
- [前端框架: React/Next.js/Vue/等]
- [样式方案: Tailwind CSS/CSS Modules/等]
- [UI 库: shadcn/ui/Ant Design/等]

功能需求:
- [需求1]
- [需求2]
- [需求3]

设计要求:
- 精确匹配 Figma 设计
- 响应式设计
- 支持深色模式（如需要）
- [其他要求]

请生成:
1. 完整的组件代码
2. TypeScript 类型定义
3. 使用示例
4. Props 文档说明
```

---

## 🎯 现在开始使用

### 方法 1: 立即测试（在当前项目）

1. 确保已完成全局配置（或在当前项目已配置）
2. 重启 Cursor
3. 在 Cursor 聊天窗口中输入：
   ```
   @figma https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试?node-id=0-1

   请分析这个设计的结构并生成对应的 React 组件
   ```

### 方法 2: 测试连接

先测试 Figma MCP 是否正常工作：
```
@figma 测试连接
```

如果响应正常，再使用您的链接。

---

## 💡 最佳实践建议

### 1. 提供详细上下文
```
这是一个用于 Web3 项目的 KOL 卡片组件...
目标用户是投资者...
需要展示 KOL 头像、名字、粉丝数、影响力评分...
```

### 2. 指定技术细节
```
- 使用 Next.js 14 App Router
- TypeScript strict mode
- Tailwind CSS + CSS Variables
- 响应式断点: sm(640px), md(768px), lg(1024px)
```

### 3. 说明特殊要求
```
- 支持国际化 (i18n)
- SEO 友好
- 性能优化 (memo, lazy load)
- 无障碍性 (ARIA labels)
```

---

## 📚 相关文档

- [Figma 使用教程](./FIGMA_USAGE_TUTORIAL.md)
- [Figma AI 使用指南](./FIGMA_AI_USAGE_GUIDE.md)
- [提示词模板库](./FIGMA_PROMPT_TEMPLATES.md)
- [全局配置说明](./GLOBAL_SETUP_INSTRUCTIONS.md)

---

## 🎊 准备就绪！

您的链接格式正确，现在可以：

1. ✅ 重启 Cursor（如果还没重启）
2. ✅ 在 Cursor 中测试您的链接
3. ✅ 开始生成代码！

如果遇到任何问题，随时告诉我！
