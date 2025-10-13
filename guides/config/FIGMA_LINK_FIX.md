# Figma 链接问题修复指南

> 您的链接: `https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled?t=1eZR365YZ2evJ99A-0`

---

## ⚠️ 问题诊断

您提供的链接**缺少 node-id 参数**，这意味着：
- ❌ 链接指向整个文件，而不是具体的设计元素
- ❌ AI 无法知道要生成哪个组件
- ❌ 需要重新获取正确的链接

---

## 🔧 修复步骤

### 方法 1: 正确复制链接（推荐）

#### 步骤 1: 打开并选中元素
1. 访问您的 Figma 文件：
   ```
   https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled
   ```

2. 在左侧图层面板或画布中，**点击选中**您要转换的 Frame
   - 例如：Button、Card、Header 等
   - 选中后该元素会有蓝色边框

#### 步骤 2: 复制选区链接
**方式 A: 右键菜单**
1. 保持元素选中状态
2. 右键点击该元素
3. 点击 **"Copy link to selection"** 或 **"复制选区链接"**

**方式 B: 快捷键**
1. 保持元素选中状态
2. 按 `Cmd + Shift + .` (Mac) 或 `Ctrl + Shift + .` (Windows)

#### 步骤 3: 验证新链接
新链接应该包含 `node-id` 参数：

```
✅ 正确格式:
https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled?node-id=1:2

❌ 错误格式（您当前的链接）:
https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled?t=1eZR365YZ2evJ99A-0
                                                          ↑
                                                    没有 node-id
```

---

### 方法 2: 手动添加 node-id（需要知道节点ID）

如果您知道具体的节点ID，可以手动添加：

1. 在 Figma 中选中元素
2. 查看右侧属性面板顶部的节点信息
3. 找到类似 `1:2` 的ID
4. 手动添加到链接：
   ```
   https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled?node-id=1:2
   ```

---

## 📋 使用示例

获取正确链接后，在 Cursor 中这样使用：

### 示例 1: 生成按钮
```
@figma https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled?node-id=1:2

请生成这个 Button 组件:
- React + TypeScript
- Tailwind CSS
- 支持 primary, secondary variants
- 包含 hover 和 disabled 状态
```

### 示例 2: 生成卡片
```
@figma https://www.figma.com/design/24h1viVbjs6vcqyZxLzJPt/Untitled?node-id=3:4

请生成这个 Card 组件:
- Next.js 14 + TypeScript
- Tailwind CSS + shadcn/ui
- 响应式设计
- 支持深色模式
```

---

## 🎯 图解说明

### 错误操作流程
```
❌ 只打开文件 → 直接复制浏览器地址栏 → 得到错误链接
   （缺少 node-id）
```

### 正确操作流程
```
✅ 打开文件 → 选中具体元素 → 右键复制选区链接 → 得到正确链接
   （包含 node-id）
```

---

## 💡 常见问题

### Q1: 为什么必须选中元素？

**答**:
- Figma 文件可能包含几十个甚至上百个设计元素
- AI 需要知道具体要生成哪一个
- `node-id` 参数告诉 AI 要处理哪个元素

### Q2: 如何找到文件中的所有元素？

**答**:
- 查看左侧的图层面板（Layers）
- 所有 Frame、组件都会列在那里
- 点击任意一个即可选中

### Q3: 可以一次生成多个组件吗？

**答**:
- 可以，但需要多次操作
- 每个组件复制一次链接
- 分别向 AI 发送请求

**示例**:
```
# 第一个组件
@figma [Button 的链接 + node-id]
请生成 Button 组件...

# 第二个组件
@figma [Card 的链接 + node-id]
请生成 Card 组件...
```

### Q4: 我的文件是空的怎么办？

**答**:
- 如果是新建的空文件，需要先在 Figma 中创建设计
- 或者找一个已有设计的文件进行测试
- 可以从 Figma Community 复制示例设计

---

## 🎨 快速测试

如果您想快速测试功能，可以：

1. **使用 Figma Community 的设计**
   - 访问 [Figma Community](https://www.figma.com/community)
   - 搜索 "Button" 或 "UI Kit"
   - 复制一个设计到您的文件
   - 选中并复制链接

2. **创建简单的测试设计**
   - 在您的文件中创建一个简单的矩形
   - 添加文字
   - 使用 Auto Layout
   - 选中后复制链接进行测试

---

## 📚 相关文档

- [Figma 使用教程](./FIGMA_USAGE_TUTORIAL.md) - 完整的使用流程
- [Figma AI 使用指南](./FIGMA_AI_USAGE_GUIDE.md) - 唤醒和使用方法
- [提示词模板库](./FIGMA_PROMPT_TEMPLATES.md) - 各种场景示例

---

## 🆘 需要帮助？

如果您：
1. 已经获取了包含 `node-id` 的新链接
2. 想测试 Figma 转代码功能
3. 有任何疑问

请把新的链接发给我，我会帮您生成代码！

---

**记住**: 一定要**选中具体元素**后再复制链接！
