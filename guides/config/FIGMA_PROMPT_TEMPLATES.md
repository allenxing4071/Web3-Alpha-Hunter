# Figma 转代码提示词模板

本文档提供各种场景下的 Figma 转代码提示词模板，帮助您快速生成高质量的 UI 组件。

---

## 📝 基础模板

### 通用组件生成

```
@figma [Figma URL]

请根据这个 Figma 设计生成 [组件名称] 组件:

技术栈:
- React + TypeScript
- Tailwind CSS
- shadcn/ui

要求:
- 完整的 TypeScript 类型定义
- 响应式设计 (mobile-first)
- 支持深色模式 (dark:)
- 包含所有交互状态 (hover, active, disabled)
- 无障碍性支持 (ARIA labels, 键盘导航)

请生成:
1. 组件代码 (完整文件)
2. 使用示例
3. Props 文档说明
```

---

## 🎯 具体场景模板

### 1. 按钮组件

```
@figma [Figma URL]

请生成一个高级 Button 组件:

技术要求:
- TypeScript + React
- 使用 shadcn/ui Button 作为基础
- CVA (class-variance-authority) 管理 variants

Variants 需求:
- variant: default, destructive, outline, ghost, link
- size: sm, md, lg, icon
- 支持 loading 状态 (显示 spinner)
- 支持 disabled 状态

额外功能:
- asChild 支持 (Radix UI Slot)
- leftIcon 和 rightIcon props
- 完整的 TypeScript 类型
- ForwardRef 支持

请包含:
1. 组件完整代码
2. 所有 variants 的使用示例
3. Storybook stories (可选)
```

### 2. 表单输入框

```
@figma [Figma URL]

请生成表单输入组件集:

组件列表:
- Input (文本输入)
- Textarea (多行文本)
- Select (下拉选择)
- Checkbox (复选框)
- Radio (单选框)
- Switch (开关)

技术栈:
- React Hook Form 集成
- Zod 验证集成
- shadcn/ui 基础组件
- 错误状态显示

每个组件需要:
- label, placeholder, helperText
- 错误状态和错误消息
- disabled 和 readOnly 支持
- 完整的 TypeScript 类型
- ForwardRef (与 React Hook Form 兼容)

示例用法:
包含一个完整的登录表单示例
```

### 3. 卡片组件

```
@figma [Figma URL]

请生成高级 Card 组件:

组件结构:
- Card (容器)
- CardHeader (头部)
- CardTitle (标题)
- CardDescription (描述)
- CardContent (内容)
- CardFooter (底部)

设计要求:
- 精确匹配 Figma 的圆角、阴影、间距
- 支持 variant: default, elevated, outlined
- Hover 状态 (可选的悬浮效果)
- 可点击卡片 (整个卡片作为链接)

高级功能:
- 加载骨架屏 (CardSkeleton)
- 响应式网格布局支持
- 图片卡片 variant (CardImage)

使用场景:
- 项目展示卡片
- 用户资料卡片
- 统计数据卡片
```

### 4. 导航菜单

```
@figma [Figma URL]

请生成响应式导航菜单:

桌面端导航:
- 横向菜单栏
- 下拉子菜单 (Radix UI Dropdown)
- 高亮当前页面
- 用户头像菜单

移动端导航:
- 汉堡菜单按钮
- 侧边抽屉 (Sheet)
- 可折叠子菜单
- 平滑动画过渡

技术实现:
- Next.js App Router (usePathname)
- Radix UI Navigation Menu
- Framer Motion 动画
- 响应式断点: lg 切换

额外功能:
- 深色模式切换器
- 搜索框 (可选)
- 通知徽章
- 用户登录/登出状态
```

### 5. 数据表格

```
@figma [Figma URL]

请生成高级数据表格组件:

技术栈:
- TanStack Table v8
- React + TypeScript
- Tailwind CSS

功能需求:
- 排序 (单列和多列)
- 筛选 (每列独立筛选)
- 分页 (前端或后端)
- 行选择 (复选框)
- 列可见性切换
- 响应式 (移动端卡片视图)

UI 特性:
- 加载状态 (骨架屏)
- 空状态显示
- 错误状态
- 行 hover 效果
- 斑马纹 (可选)

导出功能:
- 导出 CSV
- 导出 Excel
- 打印视图

请提供:
1. Table 组件代码
2. 示例数据和类型定义
3. 使用示例 (完整页面)
```

### 6. 模态框/对话框

```
@figma [Figma URL]

请生成模态框组件集:

组件类型:
1. Dialog (基础对话框)
2. AlertDialog (确认对话框)
3. Sheet (侧边抽屉)
4. Popover (弹出框)

基于技术:
- Radix UI Dialog/AlertDialog
- shadcn/ui 样式
- Framer Motion 动画

功能要求:
- 可控和非可控模式
- 嵌套支持
- 关闭按钮和 ESC 键
- 点击外部关闭 (可配置)
- Focus trap (无障碍)

对话框组成:
- DialogTrigger (触发器)
- DialogContent (内容容器)
- DialogHeader (头部)
- DialogTitle (标题)
- DialogDescription (描述)
- DialogFooter (底部按钮区)

动画效果:
- 淡入淡出
- 从下向上滑动
- 背景遮罩动画

使用示例:
- 删除确认对话框
- 表单编辑对话框
- 侧边筛选器
```

### 7. 仪表板页面

```
@figma [Figma URL]

请生成完整的仪表板页面:

页面布局:
- 侧边栏导航 (可折叠)
- 顶部导航栏 (面包屑、搜索、用户菜单)
- 主内容区域 (网格布局)
- 底部信息栏 (可选)

数据卡片:
- 统计数据卡片 (数值、趋势、图标)
- 图表卡片 (Recharts)
- 最近活动列表
- 快速操作按钮

图表类型:
- 折线图 (趋势)
- 柱状图 (对比)
- 饼图 (占比)
- 面积图 (累积)

技术栈:
- Next.js 14 Server Components
- Recharts 数据可视化
- shadcn/ui 组件
- TanStack Query (数据获取)

响应式:
- 桌面: 3-4 列网格
- 平板: 2 列网格
- 移动: 单列堆叠

数据状态:
- 加载中 (骨架屏)
- 空数据提示
- 错误处理
- 实时数据更新 (可选)

请生成:
1. 完整页面组件
2. 所有子组件
3. Mock 数据
4. API 集成示例
```

### 8. 登录/注册页面

```
@figma [Figma URL]

请生成认证页面:

页面包含:
1. 登录页面
2. 注册页面
3. 忘记密码页面
4. 重置密码页面

表单功能:
- React Hook Form + Zod 验证
- 实时表单验证
- 错误消息显示
- 提交 loading 状态
- 成功/失败反馈

设计要求:
- 左右分栏 (左侧表单，右侧品牌展示)
- 或中央卡片式设计
- 深色模式支持
- 响应式 (移动端单栏)

额外功能:
- 社交登录按钮 (Google, GitHub)
- "记住我" 复选框
- 密码显示/隐藏切换
- 密码强度指示器
- reCAPTCHA 集成 (可选)

技术集成:
- Next-Auth 或 Supabase Auth
- 加密存储 (httpOnly cookies)
- CSRF 保护
- 路由保护示例

请生成:
1. 所有页面组件
2. 表单验证 schema
3. API 路由示例
4. 认证上下文 Provider
```

### 9. 定价页面

```
@figma [Figma URL]

请生成定价页面:

定价卡片功能:
- 3 个定价层级 (Free, Pro, Enterprise)
- 高亮推荐方案
- 功能列表 (勾选/叉号图标)
- CTA 按钮 (不同状态)
- 年付/月付切换

动画效果:
- 卡片 hover 上浮
- 切换按钮滑动动画
- 功能列表渐入

高级功能:
- 功能对比表格
- FAQ 折叠面板
- 客户评价轮播
- "联系销售" 表单

技术实现:
- Framer Motion 动画
- Radix UI Accordion (FAQ)
- 价格计算逻辑
- Stripe 支付集成准备

响应式:
- 桌面: 3 列并排
- 平板: 2 列 + 1 列
- 移动: 单列堆叠

SEO 优化:
- 结构化数据 (JSON-LD)
- 语义化 HTML
- Meta 标签

请生成:
1. 完整定价页面
2. 价格卡片组件
3. FAQ 组件
4. 功能对比表格组件
```

### 10. 设置页面

```
@figma [Figma URL]

请生成设置页面:

页面布局:
- 侧边标签导航
- 主内容区域 (表单)
- 保存/取消按钮栏

设置分类:
1. 个人资料 (头像上传、姓名、邮箱)
2. 账户设置 (密码修改、两步验证)
3. 通知偏好 (邮件、推送、应用内)
4. 外观 (主题、语言、字体大小)
5. 隐私 (数据导出、删除账户)
6. 计费 (支付方式、发票历史)

表单功能:
- 分步保存 (每部分独立保存)
- 实时验证
- 自动保存草稿 (可选)
- 修改确认对话框
- 成功/失败 toast 提示

特殊组件:
- 头像上传 (裁剪功能)
- 密码强度指示器
- 双重验证二维码
- 主题切换器 (预览)
- 数据导出进度条

技术栈:
- React Hook Form
- Zod 验证
- TanStack Query (数据同步)
- 文件上传 (uploadthing 或 S3)

请生成:
1. 设置页面主框架
2. 所有设置分类组件
3. 共享表单组件
4. API 集成示例
```

---

## 🚀 高级提示词技巧

### 技巧 1: 分层生成

```
第一步 - 先生成基础结构:
@figma [URL]
请先分析这个设计的组件层次结构，列出所有需要创建的组件。

第二步 - 生成核心组件:
现在请生成 [组件名] 组件的代码。

第三步 - 优化和增强:
请为这个组件添加 [具体功能]。
```

### 技巧 2: 指定设计系统

```
@figma [URL]

请使用我们的设计系统生成组件:

颜色:
- Primary: #3B82F6
- Secondary: #8B5CF6
- Success: #10B981
- Warning: #F59E0B
- Danger: #EF4444

间距: 4px 基础单位 (4, 8, 16, 24, 32, 48, 64)
圆角: sm(6px), md(8px), lg(12px), xl(16px)
阴影: 使用 Tailwind 默认阴影

请严格遵循这些设计令牌。
```

### 技巧 3: 性能优化

```
@figma [URL]

请生成性能优化的组件:

优化要求:
- 使用 React.memo 防止不必要的重渲染
- 大列表使用虚拟滚动 (react-virtual)
- 图片使用 Next.js Image 组件
- 懒加载非关键组件
- 代码分割 (动态导入)

请在代码中添加性能注释说明。
```

### 技巧 4: 测试代码

```
@figma [URL]

请生成组件及其测试代码:

组件代码:
- React + TypeScript
- 完整功能实现

测试代码:
- Jest + React Testing Library
- 单元测试 (组件渲染、props)
- 交互测试 (点击、输入)
- 无障碍测试 (axe-core)
- 快照测试

测试覆盖率目标: 80%+
```

### 技巧 5: Storybook 集成

```
@figma [URL]

请生成组件和 Storybook stories:

组件代码:
- [具体要求]

Storybook Stories:
- 所有 variants 的 stories
- 不同状态的 stories (loading, error, empty)
- 交互测试 (play function)
- Controls 配置
- 完整的文档注释

使用 Storybook 7+ 格式 (CSF 3.0)
```

---

## 📚 参考资源

- [shadcn/ui 组件](https://ui.shadcn.com/)
- [Radix UI 文档](https://www.radix-ui.com/)
- [Tailwind CSS 文档](https://tailwindcss.com/)
- [Figma Best Practices](https://www.figma.com/best-practices/)

---

## 💡 提示词优化建议

1. **具体明确**: 详细描述需求，避免模糊表达
2. **分步进行**: 复杂组件拆分成多个步骤
3. **提供上下文**: 说明使用场景和技术栈
4. **指定标准**: 明确设计系统、代码规范
5. **要求示例**: 让 AI 提供使用示例和文档
6. **迭代优化**: 基于生成结果不断调整提示词

---

最后更新: 2025-01-13
