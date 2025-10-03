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
├── docs/                 # 项目文档
├── docker-compose.yml    # Docker配置
└── README.md
```

## 🔧 开发指南

详细开发文档请查看 [README_DEV.md](./README_DEV.md)

## 📚 文档

- [项目概述](./docs/01-需求与设计/01-项目概述.md)
- [功能需求](./docs/01-需求与设计/02-功能需求清单.md)
- [技术选型](./docs/02-技术实现/01-技术选型.md)
- [API接口文档](./docs/02-技术实现/02-API接口文档.md)
- [部署指南](./docs/04-部署与运维/01-部署指南.md)

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
