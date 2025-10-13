# 闹钟 UI 设计指南

> **目标**: 在 Figma 中设计一个现代化的闹钟应用界面
> **风格**: 简洁、现代、易用

---

## 🎨 设计方案

### 方案 1: 简约风格闹钟（推荐）

#### 主要功能界面
1. **主屏幕 - 时间显示**
   - 大号数字时钟
   - 当前日期和星期
   - 闹钟列表

2. **添加闹钟界面**
   - 时间选择器（滚轮或拨盘）
   - 重复设置（每天、工作日、周末、自定义）
   - 铃声选择
   - 标签/备注
   - 震动开关

3. **闹钟列表**
   - 闹钟卡片（时间、标签、重复规则）
   - 开关切换
   - 编辑/删除操作

---

## 📐 设计规范

### 1. 画布设置
- **设备**: iPhone 14 Pro (393 x 852)
- **背景色**:
  - 浅色模式: #FFFFFF
  - 深色模式: #000000

### 2. 颜色系统
```
主色调:
- Primary: #007AFF (iOS 蓝)
- Secondary: #5856D6 (紫色)
- Success: #34C759 (绿色)
- Danger: #FF3B30 (红色)

中性色:
- Background Light: #FFFFFF
- Background Dark: #000000
- Surface Light: #F2F2F7
- Surface Dark: #1C1C1E
- Text Primary: #000000 / #FFFFFF
- Text Secondary: #8E8E93
- Border: #C6C6C8 / #38383A
```

### 3. 字体系统
```
标题:
- H1: SF Pro Display, Bold, 64px (时间显示)
- H2: SF Pro Display, Semibold, 34px (页面标题)
- H3: SF Pro Display, Semibold, 20px (闹钟时间)

正文:
- Body Large: SF Pro Text, Regular, 17px
- Body: SF Pro Text, Regular, 15px
- Caption: SF Pro Text, Regular, 13px
```

### 4. 间距系统
```
基础单位: 8px
常用间距:
- 4px (极小)
- 8px (小)
- 12px (中小)
- 16px (中)
- 24px (大)
- 32px (特大)
- 48px (超大)
```

### 5. 圆角系统
```
- 小圆角: 8px (按钮、输入框)
- 中圆角: 12px (卡片)
- 大圆角: 20px (模态框)
- 圆形: 50% (头像、图标按钮)
```

---

## 🎯 具体设计步骤

### 步骤 1: 创建主屏幕 (Home Screen)

#### 1.1 创建画板
```
Frame 名称: iPhone 14 Pro - Home
尺寸: 393 x 852
背景: #FFFFFF (浅色) / #000000 (深色)
```

#### 1.2 顶部状态栏
```
高度: 44px
内容: 时间、信号、电池
颜色: #000000 (浅色模式) / #FFFFFF (深色模式)
```

#### 1.3 大号时间显示
```
位置: 顶部下方 80px
字体: SF Pro Display, Bold, 64px
颜色: #000000 / #FFFFFF
示例: "09:41"

日期显示:
字体: SF Pro Text, Regular, 17px
颜色: #8E8E93
示例: "星期一, 1月13日"
```

#### 1.4 闹钟列表卡片
```
卡片样式:
- 背景: #F2F2F7 / #1C1C1E
- 圆角: 12px
- 内边距: 16px
- 间距: 12px

卡片内容:
┌─────────────────────────────────┐
│ 07:00              [开关]       │
│ 工作日闹钟         ▷           │
│ 周一至周五                      │
└─────────────────────────────────┘

元素:
- 时间: SF Pro Display, Semibold, 28px
- 标签: SF Pro Text, Regular, 15px
- 重复: SF Pro Text, Regular, 13px, #8E8E93
- 开关: Toggle Switch, 51 x 31
```

#### 1.5 底部添加按钮
```
位置: 底部安全区上方 16px
样式:
- 圆形按钮: 56 x 56
- 背景: #007AFF
- 图标: + (加号), 24px, #FFFFFF
- 阴影: 0 4px 12px rgba(0,122,255,0.3)
```

---

### 步骤 2: 创建添加闹钟界面 (Add Alarm)

#### 2.1 创建画板
```
Frame 名称: iPhone 14 Pro - Add Alarm
尺寸: 393 x 852
背景: #FFFFFF / #000000
```

#### 2.2 导航栏
```
高度: 44px
位置: 状态栏下方

左侧: "取消" 按钮, #007AFF
中间: "添加闹钟" 标题, SF Pro Display, Semibold, 17px
右侧: "保存" 按钮, #007AFF, Bold
```

#### 2.3 时间选择器
```
样式: iOS 滚轮选择器 (Picker Wheel)
位置: 顶部
高度: 216px
列:
- 小时: 00-23
- 分钟: 00-59
- 上午/下午 (可选)

选中行:
- 背景: #F2F2F7 / #1C1C1E
- 高度: 36px
- 字体: SF Pro Display, Regular, 23px
```

#### 2.4 设置列表
```
分组列表:

┌─────────────────────────────────┐
│ 重复           ▷  每天           │
├─────────────────────────────────┤
│ 标签           ▷  闹钟           │
├─────────────────────────────────┤
│ 铃声           ▷  雷达           │
├─────────────────────────────────┤
│ 稍后提醒       [开关]           │
└─────────────────────────────────┘

项目样式:
- 高度: 44px
- 背景: #FFFFFF / #1C1C1E
- 分隔线: #C6C6C8 / #38383A, 0.5px
- 文字: SF Pro Text, Regular, 17px
- 图标: ▷ (右箭头), #C6C6C8
```

---

### 步骤 3: 创建闹钟响铃界面 (Alarm Ringing)

#### 3.1 全屏显示
```
Frame 名称: iPhone 14 Pro - Ringing
背景: 渐变色或模糊背景

顶部日期:
字体: SF Pro Text, Regular, 17px
颜色: #FFFFFF
示例: "星期一, 1月13日"

中央时间:
字体: SF Pro Display, Bold, 96px
颜色: #FFFFFF
示例: "07:00"

闹钟标签:
字体: SF Pro Text, Regular, 20px
颜色: #FFFFFF, 80% opacity
示例: "工作日闹钟"
```

#### 3.2 操作按钮
```
稍后提醒按钮:
- 位置: 底部上方 120px
- 尺寸: 120 x 120 (圆形)
- 背景: #FF9500
- 图标: 月亮/时钟
- 文字: "稍后提醒", SF Pro Text, 15px
- 副文字: "9分钟", SF Pro Text, 13px

停止按钮:
- 位置: 底部安全区上方 32px
- 尺寸: 120 x 120 (圆形)
- 背景: #FF3B30
- 图标: X (叉号)
- 文字: "停止", SF Pro Text, 15px
```

---

## 🎨 设计组件库

### 1. 按钮组件

#### Primary Button
```
尺寸: 自适应宽度 x 44px
背景: #007AFF
圆角: 10px
文字: SF Pro Text, Semibold, 17px, #FFFFFF
内边距: 16px 24px

状态:
- Default: #007AFF
- Hover: #0051D5
- Pressed: #004399
- Disabled: #007AFF, 50% opacity
```

#### Icon Button
```
尺寸: 44 x 44 (圆形)
背景: #F2F2F7 / #1C1C1E
图标: 20px, #007AFF
```

### 2. 卡片组件

#### Alarm Card
```
尺寸: 361 x 自适应
背景: #F2F2F7 / #1C1C1E
圆角: 12px
内边距: 16px

内容:
- 时间: SF Pro Display, Semibold, 28px
- 标签: SF Pro Text, Regular, 15px
- 详情: SF Pro Text, Regular, 13px, #8E8E93
- 开关: Toggle Switch
```

### 3. 输入组件

#### List Item
```
高度: 44px
背景: #FFFFFF / #1C1C1E
内边距: 16px

左侧: 标签, SF Pro Text, Regular, 17px
右侧: 值 + 箭头, SF Pro Text, Regular, 17px, #8E8E93
```

#### Toggle Switch
```
尺寸: 51 x 31
开启: #34C759
关闭: #E5E5EA / #39393D
```

---

## 📱 响应式考虑

### iPhone SE (375 x 667)
- 缩小字体: H1 56px → 48px
- 减少间距: 16px → 12px

### iPad (834 x 1194)
- 使用侧边栏布局
- 左侧: 闹钟列表
- 右侧: 详情/编辑

---

## 🎯 Figma 设计检查清单

完成设计后，确保:

- ✅ 所有元素使用 Auto Layout
- ✅ 颜色使用 Variables
- ✅ 文字使用 Styles
- ✅ 组件放入 Components
- ✅ 命名规范: ComponentName/Variant/State
- ✅ 定义所有交互状态 (Default, Hover, Active, Disabled)
- ✅ 深色模式和浅色模式
- ✅ 响应式约束设置正确

---

## 🚀 设计完成后

### 1. 组织图层
```
📁 iPhone 14 Pro - Home
  📁 Status Bar
  📁 Header
    - Time Display
    - Date Display
  📁 Alarm List
    - Alarm Card 1
    - Alarm Card 2
    - ...
  📁 Bottom Navigation
    - Add Button
```

### 2. 创建组件
- Button/Primary
- Button/Secondary
- Card/Alarm
- ListItem/Default
- Toggle/On
- Toggle/Off

### 3. 导出准备
- 命名每个 Frame
- 使用 Auto Layout
- 设置正确的约束

### 4. 复制链接
- 选中 Frame
- 右键 → Copy link to selection
- 得到包含 node-id 的链接

---

## 💡 设计灵感参考

### iOS 原生闹钟应用
- 简洁的界面
- 大号时间显示
- 清晰的层级结构

### 现代设计趋势
- 毛玻璃效果 (Glassmorphism)
- 新拟态风格 (Neumorphism)
- 渐变色背景
- 微交互动画

---

## 🎨 快速开始

1. **打开您的 Figma 文件**:
   https://www.figma.com/design/5W7Bf1lRFf8kIWOjEEE5Ar/结合cursor测试

2. **创建新 Frame**:
   - 按 `F` 键
   - 选择 iPhone 14 Pro
   - 重命名为 "Clock - Home"

3. **开始设计**:
   - 添加背景色
   - 创建大号时间显示
   - 添加闹钟卡片
   - 添加底部按钮

4. **完成后**:
   - 选中 Frame
   - 右键 → Copy link to selection
   - 在 Cursor 中使用 @figma + 链接生成代码

---

## 📚 相关资源

- [Apple Design Resources](https://developer.apple.com/design/resources/)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Figma Design System](https://www.figma.com/community/file/1034054267089734146)

---

**现在开始在 Figma 中设计您的闹钟 UI 吧！** 🎨✨
