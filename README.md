# Web3 Alpha Hunter

> AI驱动的Web3项目早期发现与分析平台 🚀

通过智能化爬虫和AI分析,从全球社交媒体、开发者社区、链上数据中发现早期优质Web3项目,帮助投资者捕获百倍千倍增长机会。

## ✨ 核心功能

- 🌍 **全球情报采集**: 覆盖 Twitter/X、Telegram、Discord、Reddit、GitHub、CoinGecko等多源数据
- 🤖 **AI智能分析**: 多维度评分系统(团队、技术、社区、代币经济、市场时机、风险)
- 📊 **项目分级**: S/A/B/C 四级评分,快速识别高潜力项目
- 🔍 **风险检测**: 自动识别高风险项目、诈骗模式、团队透明度问题
- 📈 **实时监控**: 项目动态追踪、价格预警、巨鲸地址监控
- 📝 **每日Alpha报告**: 结构化日报,投资建议和风险提示

## 🤖 AI 增强开发

### 🚀 AI助手：请先看这里！

**新对话开始时**，AI助手请先阅读：
1. **[AI_START_HERE.md](./AI_START_HERE.md)** ⭐ **← 从这里开始！**
2. [`.claudecontext`](./.claudecontext) - 项目核心记忆（必读）
3. [`.clinerules`](./.clinerules) - 工作规范（必读）

### AI 助手协作系统

本项目配备了**跨对话记忆系统**，让AI助手能够在每次新对话中保持项目上下文：

**核心文件**：
- 📋 [`.claudecontext`](./.claudecontext) - 项目上下文记忆（战略层/董事会）
- 📜 [`.clinerules`](./.clinerules) - AI助手工作规范
- 🚀 [`AI_START_HERE.md`](./AI_START_HERE.md) - AI助手入口指南

**完整文档**：
- 📖 [`docs/AI助手使用指南.md`](./docs/AI助手使用指南.md) - 详细使用指南
- 💡 [`docs/快速指南/AI助手协作示例.md`](./docs/快速指南/AI助手协作示例.md) - 实战案例
- 📋 [`跨对话记忆-快速开始.md`](./跨对话记忆-快速开始.md) - 5分钟快速了解

**使用说明**：
- **给AI助手**: 每次新对话请先阅读 `AI_START_HERE.md` 和 `.claudecontext`
- **给开发者**: 重大变更后请更新 `.claudecontext` 文件
- **快捷命令**: 新对话可以说"读取上下文，准备工作"

### 🎨 Figma 转代码 (新功能)

**AI 驱动的设计到代码工作流**，使用 Figma MCP + Cursor + Claude 4.5 快速生成高质量 UI 组件。

#### 快速配置
```bash
cd guides/config
./figma-quick-setup.sh
```

#### 主要特性
- ✅ 从 Figma 设计直接生成 React + TypeScript 组件
- ✅ 自动匹配 Tailwind CSS + shadcn/ui 样式
- ✅ 生成响应式和无障碍代码
- ✅ 支持完整页面和复杂布局
- ✅ 与项目设计系统深度集成

#### 文档资源
- 📖 [完整配置指南](./guides/config/FIGMA_MCP_SETUP.md)
- 🎯 [提示词模板库](./guides/config/FIGMA_PROMPT_TEMPLATES.md) - 10+ 种组件模板
- 🎉 [配置完成总结](./FIGMA_SETUP_COMPLETE.md) - 快速开始使用

#### 快速示例
```
@figma https://www.figma.com/file/xxx/Design

请根据这个设计生成 Dashboard 页面:
- Next.js 14 + TypeScript
- Tailwind CSS + shadcn/ui
- 响应式布局 + 深色模式
```

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd faxianjihui
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问应用

- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 默认登录账号

- 用户名: `admin`
- 密码: `admin123`

## 📁 项目结构

```
faxianjihui/
├── backend/              # FastAPI后端
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── db/          # 数据库
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # 业务逻辑
│   │   └── tasks/       # Celery任务
│   └── requirements.txt
├── frontend/             # Next.js前端
│   ├── src/
│   │   ├── app/         # 页面路由
│   │   ├── components/  # React组件
│   │   ├── lib/         # 工具函数
│   │   ├── store/       # Zustand状态管理
│   │   └── types/       # TypeScript类型
│   └── package.json
├── scripts/              # ⭐ 脚本工具目录
│   ├── start-dev.sh     # 开发环境启动
│   ├── stop-dev.sh      # 开发环境停止
│   └── README.md        # 脚本使用说明
├── docs/                 # 项目技术文档
│   ├── 快速指南/         # ⭐ 快速上手文档
│   ├── 01-需求与设计/
│   ├── 02-技术实现/
│   ├── 03-功能模块/     # ⭐ 功能模块文档
│   └── 99-归档/         # 历史文档归档
├── guides/               # 📚 配置和操作指南
│   ├── config/          # 配置指南
│   ├── ai/              # AI配置指南
│   └── admin/           # 管理员指南
├── docker-compose.yml    # Docker配置
└── README.md             # 项目主文档
```

## 🔧 开发指南

详细开发文档请查看 [README_DEV.md](./README_DEV.md)

## 📚 文档导航

### 🚀 快速上手
- [📘 快速启动](./docs/快速指南/快速启动.md) - 5分钟快速启动 ⭐
- [📗 数据补全](./docs/快速指南/快速启动-数据补全.md) - 初始化数据
- [🔧 脚本说明](./scripts/README.md) - 启动脚本使用指南

### 📖 技术文档 (`docs/`)
- [📚 文档中心](./docs/README.md) - 完整文档导航 v2.0
- [🔍 系统分析报告](./docs/系统分析报告.md) - 文档vs实际差异分析
- [📊 已实现功能清单](./docs/02-技术实现/03-已实现功能清单-完整版.md) - 22表完整记录 ⭐
- [🗄️ 数据库设计文档](./docs/02-技术实现/04-数据库设计文档-完整版.md) - 22表详细设计 ⭐
- [🤖 KOL管理系统](./docs/03-功能模块/01-KOL管理系统.md) - 3表完整文档
- [✅ 项目审核系统](./docs/03-功能模块/02-项目审核系统.md) - AI推荐评分
- [🔮 AI预测系统](./docs/03-功能模块/03-AI预测与行动计划系统.md) - 发币预测/空投估值
- [🌐 平台监控系统](./docs/03-功能模块/04-平台监控系统.md) - 多平台数据采集
- [📋 API接口文档](./docs/02-技术实现/02-API接口文档.md) - RESTful API规范
- [🏗️ 技术选型](./docs/02-技术实现/01-技术选型.md) - 技术栈说明
- [🚀 部署指南](./docs/04-部署与运维/01-部署指南.md) - 生产环境部署

### 🔧 配置和操作指南 (`guides/`)
- [📚 指南中心](./guides/README.md) - 所有指南索引
- [⚙️ 配置中心](./guides/config/README.md) - 服务器/域名/数据库/API密钥配置
- [🤖 AI配置](./guides/ai/DEEPSEEK_GUIDE.md) - DeepSeek AI模型配置
- [👥 管理员指南](./guides/admin/ROLE_MANAGEMENT_GUIDE.md) - 用户权限管理

## 🎯 核心技术栈

### 后端
- FastAPI - 高性能Python Web框架
- SQLAlchemy - ORM
- Celery - 任务队列
- Redis - 缓存和消息队列
- PostgreSQL - 主数据库

### 前端
- Next.js 14 - React框架
- TypeScript - 类型安全
- Tailwind CSS - 样式
- Zustand - 状态管理
- Recharts - 数据可视化

### AI & 数据
- OpenAI GPT-4 / Anthropic Claude - AI分析
- LangChain - AI工作流
- Playwright - 网页爬虫
- Web3.py - 链上数据

## 📊 评分体系

### 六维评分模型

1. **团队背景** (20%) - 创始人经历、顾问团队、开发者活跃度
2. **技术创新** (25%) - 代码质量、架构设计、技术壁垒
3. **社区热度** (15%) - 社交媒体增长、KOL关注、社区参与
4. **代币经济** (15%) - 分配机制、释放曲线、实用性
5. **市场时机** (15%) - 赛道热度、竞品分析、发展阶段
6. **风险评估** (10%) - 审计状态、团队透明度、潜在风险

### 项目分级

- **S级 (85-100分)**: 极具潜力,强烈推荐关注
- **A级 (70-84分)**: 优质项目,值得深入研究  
- **B级 (55-69分)**: 有一定潜力,谨慎观察
- **C级 (<55分)**: 风险较高,不建议关注

## 🔐 安全提示

- ⚠️ 本系统仅供研究学习使用
- ⚠️ 所有分析结果仅供参考,不构成投资建议
- ⚠️ 请勿将API密钥提交到Git仓库
- ⚠️ 生产环境请修改默认密钥和密码

## 📝 开发进度

- [x] 项目架构设计
- [x] 后端API开发
- [x] 前端UI开发
- [x] 数据采集模块
- [x] AI分析引擎
- [x] 用户认证系统
- [x] 系统管理后台
- [ ] 自动化部署
- [ ] 性能优化
- [ ] 监控告警

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📄 许可证

MIT License

## 📧 联系方式

如有问题或建议,请通过Issue联系。

---

**免责声明**: 本项目仅用于技术研究和学习,任何投资决策请自行承担风险。
