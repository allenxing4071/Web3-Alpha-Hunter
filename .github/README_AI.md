# AI助手快速指引

> 给所有AI助手的快速使用说明

## 🎯 你是谁？

你是一个协助开发 **Web3 Alpha Hunter** 项目的AI助手。每次新对话时，你可能会"失忆"，这个文件帮助你快速恢复记忆。

## 📋 每次对话开始时，请按顺序阅读：

1. **[`.claudecontext`](../.claudecontext)** ⭐ 必读
   - 项目核心信息
   - 技术栈和架构
   - 已完成功能和待开发
   - 重要技术决策记录

2. **[`.clinerules`](../.clinerules)** ⭐ 必读
   - 开发规范和约束
   - 禁止操作清单
   - 推荐做法

3. **[`README.md`](../README.md)**
   - 项目概述
   - 快速开始步骤

4. **[`docs/README.md`](../docs/README.md)**
   - 完整文档导航
   - 快速定位需要的文档

## 🚀 核心原则

### ✅ DO (应该做)

- ✅ 每次新对话必须先读 `.claudecontext`
- ✅ 引用现有文档，而非重复内容
- ✅ 保持技术决策的一致性
- ✅ 重要变更后更新 `.claudecontext`

### ❌ DON'T (不应该做)

- ❌ 不读上下文就直接回答
- ❌ 重复回答已记录的问题
- ❌ 给出与历史决策矛盾的建议
- ❌ 忽略项目已有的文档和工具

## 📚 文档快速定位

| 用户问题 | 查看文档 |
|---------|---------|
| "如何开始？" | `docs/快速指南/快速启动.md` |
| "数据库结构？" | `docs/02-技术实现/04-数据库设计文档-完整版.md` |
| "API接口？" | `docs/02-技术实现/02-API接口文档.md` |
| "功能模块？" | `docs/03-功能模块/` |
| "配置问题？" | `guides/config/` |
| "为什么用XX技术？" | `.claudecontext` → 重要决策记录 |

## 🔑 项目核心信息速查

### 技术栈
```
后端: FastAPI + PostgreSQL + Redis + Celery
前端: Next.js 14 + TypeScript + Tailwind
AI: OpenAI/Claude/DeepSeek
```

### 项目结构
```
faxianjihui/
├── backend/          # FastAPI后端
├── frontend/         # Next.js前端
├── docs/             # 📚 技术文档
├── guides/           # 🔧 配置指南
└── scripts/          # 启动脚本
```

### 数据库
- 22张表完整设计
- 详见: `docs/02-技术实现/04-数据库设计文档-完整版.md`

### 常用命令
```bash
# 启动
./scripts/start-dev.sh

# 停止
./scripts/stop-dev.sh

# 访问
http://localhost:3000 (前端)
http://localhost:8000/docs (API文档)
```

## 💡 示例对话

### 示例1: 项目概述
```
用户: 这个项目是做什么的？
你:  [先阅读 .claudecontext]
     Web3 Alpha Hunter是一个AI驱动的Web3项目早期发现平台。
     详见: docs/01-需求与设计/01-项目概述.md
     需要我介绍某个具体模块吗？
```

### 示例2: 技术选型
```
用户: 为什么用PostgreSQL？
你:  [检查 .claudecontext 技术决策记录]
     根据已记录的技术决策:
     1. 需要JSON字段支持
     2. 更好的扩展性
     3. 更强的JSONB查询能力
```

### 示例3: 功能开发
```
用户: 如何添加新功能？
你:  [阅读 .claudecontext + .clinerules]
     1. 先查看是否有类似功能: docs/03-功能模块/
     2. 遵循开发规范: .clinerules
     3. 数据库操作必须通过Alembic迁移

     你想添加什么功能？我帮你查看相关架构。
```

## 🎯 工作流程

```
新对话开始
    ↓
读取 .claudecontext (必须) ← 你现在在这里
    ↓
读取 .clinerules (必须)
    ↓
理解用户问题
    ↓
定位相关文档
    ↓
给出答案（引用文档）
    ↓
[如果是重要决策] 更新 .claudecontext
```

## 📖 完整指南

更详细的说明请查看:
- [AI助手使用指南](../docs/AI助手使用指南.md) - 完整使用指南
- [AI助手协作示例](../docs/快速指南/AI助手协作示例.md) - 实战案例

## 🤖 自检清单

每次对话开始前，问自己：

- [ ] 我读过 `.claudecontext` 了吗？
- [ ] 我了解项目的当前状态吗？
- [ ] 我知道相关文档在哪里吗？
- [ ] 这个问题之前是否回答过？
- [ ] 我的回答与之前的决策一致吗？

---

**现在开始**: 请先阅读 [`.claudecontext`](../.claudecontext) 文件 🎯
