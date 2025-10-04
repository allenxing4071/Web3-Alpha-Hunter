# API 接口文档

## 📋 接口概览

**Base URL (开发)**: `http://localhost:8000/api/v1`
**Base URL (生产)**: `https://api.web3alphahunter.com/v1`
**认证方式**: Bearer Token (JWT)
**数据格式**: JSON
**字符编码**: UTF-8
**API文档**: `http://localhost:8000/docs` (Swagger UI)

## 🎯 已实现接口

以下标记 ✅ 的接口已完全实现并可用,标记 🚧 的接口部分实现,标记 📋 的接口待实现。

---

## 🔐 认证接口 ✅

### 1. 用户注册 ✅

```http
POST /api/v1/auth/register
```

**实现状态**: ✅ 已完成

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "username": "crypto_hunter"
}
```

**响应** (201 Created):
```json
{
  "success": true,
  "data": {
    "user_id": "usr_abc123",
    "email": "user@example.com",
    "username": "crypto_hunter",
    "tier": "free",
    "created_at": "2025-10-02T10:30:00Z"
  },
  "message": "Registration successful"
}
```

---

### 2. 用户登录 ✅

```http
POST /api/v1/auth/login
```

**实现状态**: ✅ 已完成

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "dGhpc2lz...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "user_id": "usr_abc123",
      "email": "user@example.com",
      "tier": "pro"
    }
  }
}
```

---

### 3. 刷新Token ✅

```http
POST /api/v1/auth/refresh
```

**实现状态**: ✅ 已完成

**请求头**:
```
Authorization: Bearer {refresh_token}
```

**响应** (200 OK):
```json
{
  "access_token": "eyJhbGc...",
  "expires_in": 3600
}
```

---

## 📊 项目接口 ✅

### 1. 获取项目列表 ✅

```http
GET /api/v1/projects
```

**实现状态**: ✅ 已完成

**查询参数**:
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| grade | string | 否 | 项目等级 | S, A, B, C |
| category | string | 否 | 项目分类 | DeFi, NFT, GameFi |
| blockchain | string | 否 | 区块链 | Ethereum, Solana |
| min_score | number | 否 | 最低评分 | 80 |
| date_from | string | 否 | 开始日期 | 2025-10-01 |
| date_to | string | 否 | 结束日期 | 2025-10-02 |
| sort_by | string | 否 | 排序字段 | score, discovered_at |
| order | string | 否 | 排序方向 | asc, desc |
| page | number | 否 | 页码 | 1 |
| limit | number | 否 | 每页数量 | 20 (最大100) |

**请求示例**:
```http
GET /projects?grade=S&sort_by=score&order=desc&limit=10
```

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "projects": [
      {
        "project_id": "proj_xyz789",
        "name": "XXX Protocol",
        "symbol": "XXX",
        "grade": "S",
        "overall_score": 92.5,
        "category": "DeFi",
        "blockchain": "Ethereum",
        "description": "跨链流动性聚合协议...",
        "logo_url": "https://cdn.example.com/logos/xxx.png",
        "website": "https://xxx-protocol.io",
        "social_links": {
          "twitter": "https://twitter.com/xxx_protocol",
          "telegram": "https://t.me/xxx_community",
          "discord": "https://discord.gg/xxx"
        },
        "key_highlights": [
          "a16z领投 $50M A轮",
          "团队来自Uniswap核心开发",
          "已获得3个主网审计报告"
        ],
        "risk_flags": [
          {
            "type": "tokenomics",
            "severity": "medium",
            "message": "团队代币占比25%偏高"
          }
        ],
        "metrics": {
          "twitter_followers": 45000,
          "telegram_members": 12000,
          "tvl_usd": 5000000,
          "holder_count": 8500
        },
        "first_discovered_at": "2025-10-01T08:30:00Z",
        "last_updated_at": "2025-10-02T10:15:00Z"
      }
      // ... 更多项目
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_items": 47,
      "items_per_page": 10
    }
  }
}
```

---

### 2. 获取项目详情 ✅

```http
GET /api/v1/projects/{project_id}
```

**实现状态**: ✅ 已完成

**路径参数**:
- `project_id`: 项目ID

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "project_id": "proj_xyz789",
    "name": "XXX Protocol",
    "symbol": "XXX",
    "contract_address": "0x1234567890abcdef...",
    "blockchain": "Ethereum",
    "category": "DeFi",
    
    // 基础信息
    "description": "详细描述...",
    "whitepaper_url": "https://xxx.io/whitepaper.pdf",
    "website": "https://xxx-protocol.io",
    "github_repo": "https://github.com/xxx/protocol",
    
    // 评分详情
    "scores": {
      "overall": 92.5,
      "team": 95.0,
      "technology": 90.0,
      "community": 88.0,
      "tokenomics": 85.0,
      "market_timing": 92.0,
      "risk": 90.0
    },
    "grade": "S",
    
    // AI分析
    "ai_analysis": {
      "summary": "XXX Protocol是一个...",
      "key_features": [
        "特性1",
        "特性2",
        "特性3"
      ],
      "similar_projects": [
        {
          "name": "Solana",
          "similarity_score": 0.85,
          "matching_features": ["高性能", "技术团队强"]
        }
      ],
      "sentiment": {
        "score": 0.75,
        "label": "positive"
      },
      "risk_assessment": {
        "scam_probability": 5.2,
        "risk_flags": [...]
      },
      "investment_suggestion": {
        "recommendation": "强烈推荐",
        "position_size": "3-5%",
        "entry_timing": "立即小仓位埋伏",
        "stop_loss": 30.0
      }
    },
    
    // 当前指标
    "current_metrics": {
      "market_cap": 50000000,
      "price_usd": 0.25,
      "volume_24h": 2500000,
      "tvl_usd": 5000000,
      "holder_count": 8500,
      "twitter_followers": 45000,
      "telegram_members": 12000,
      "github_stars": 320,
      "github_commits_last_week": 48
    },
    
    // 发现来源
    "discovery": {
      "source": "twitter",
      "discovered_at": "2025-10-01T08:30:00Z",
      "discovered_from": "@VitalikButerin 转发"
    },
    
    "created_at": "2025-10-01T08:30:00Z",
    "updated_at": "2025-10-02T10:15:00Z"
  }
}
```

---

### 3. 获取项目历史数据 🚧

```http
GET /api/v1/projects/{project_id}/history
```

**实现状态**: 🚧 接口已定义,数据待完善

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| metric | string | 是 | 指标类型: social, onchain, score |
| days | number | 否 | 天数 (默认7, 最大90) |

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "project_id": "proj_xyz789",
    "metric_type": "social",
    "time_series": [
      {
        "timestamp": "2025-10-01T00:00:00Z",
        "twitter_followers": 30000,
        "telegram_members": 8000
      },
      {
        "timestamp": "2025-10-02T00:00:00Z",
        "twitter_followers": 45000,
        "telegram_members": 12000
      }
    ]
  }
}
```

---

## 📄 报告接口

### 1. 获取每日报告

```http
GET /reports/daily
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 否 | 日期 (默认今天) YYYY-MM-DD |

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "report_id": "rpt_20251002",
    "date": "2025-10-02",
    "statistics": {
      "total_scanned": 127,
      "new_discovered": 18,
      "s_grade": 3,
      "a_grade": 8,
      "b_grade": 5,
      "risk_warnings": 2
    },
    "sections": {
      "s_grade_projects": [
        {
          "project_id": "proj_xyz789",
          "name": "XXX Protocol",
          "score": 92.5,
          "summary": "简要介绍...",
          "highlights": [...],
          "risks": [...]
        }
      ],
      "a_grade_projects": [...],
      "risk_warnings": [
        {
          "project_id": "proj_scam123",
          "name": "Scam Token",
          "warning_type": "potential_scam",
          "reason": "团队匿名 + 不合理承诺"
        }
      ],
      "market_overview": {
        "trending_categories": ["DeFi", "AI"],
        "hot_blockchains": ["Ethereum", "Solana"],
        "sentiment": "bullish"
      }
    },
    "content_markdown": "# Web3 Alpha Daily Report\n...",
    "generated_at": "2025-10-02T09:00:00Z"
  }
}
```

---

### 2. 获取项目深度报告

```http
GET /reports/deep/{project_id}
```

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "report_id": "deep_proj_xyz789",
    "project_id": "proj_xyz789",
    "sections": {
      "executive_summary": "...",
      "background": "...",
      "technology_analysis": "...",
      "team_investors": "...",
      "tokenomics": "...",
      "competitor_analysis": [...],
      "risk_assessment": "...",
      "investment_recommendation": "..."
    },
    "content_markdown": "完整报告内容...",
    "pdf_url": "https://cdn.example.com/reports/deep_proj_xyz789.pdf",
    "generated_at": "2025-10-02T11:30:00Z"
  }
}
```

**权限**: 需要 Pro 或更高等级

---

## 🔔 监控接口

### 1. 添加到监控列表

```http
POST /watchlist
```

**请求体**:
```json
{
  "project_id": "proj_xyz789",
  "alert_settings": {
    "price_change": true,
    "community_growth": true,
    "major_events": true
  }
}
```

**响应** (201 Created):
```json
{
  "success": true,
  "data": {
    "watchlist_id": "wtc_abc123",
    "project_id": "proj_xyz789",
    "added_at": "2025-10-02T12:00:00Z"
  }
}
```

---

### 2. 获取监控列表

```http
GET /watchlist
```

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "watchlist": [
      {
        "watchlist_id": "wtc_abc123",
        "project": {
          "project_id": "proj_xyz789",
          "name": "XXX Protocol",
          "current_price": 0.25,
          "price_change_24h": 15.3
        },
        "alert_settings": {...},
        "added_at": "2025-10-02T12:00:00Z"
      }
    ]
  }
}
```

---

### 3. 移除监控

```http
DELETE /watchlist/{watchlist_id}
```

**响应** (204 No Content)

---

## 🔍 搜索接口

### 1. 搜索项目

```http
GET /search
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |
| category | string | 否 | 分类筛选 |
| limit | number | 否 | 结果数量 (默认10) |

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "query": "defi",
    "results": [
      {
        "project_id": "proj_xyz789",
        "name": "XXX Protocol",
        "description": "...",
        "score": 92.5,
        "grade": "S",
        "relevance": 0.95
      }
    ],
    "total": 15
  }
}
```

---

## 📊 统计接口

### 1. 获取平台统计

```http
GET /stats
```

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "total_projects": 1247,
    "s_grade_projects": 45,
    "projects_discovered_today": 18,
    "average_score": 68.5,
    "trending_categories": [
      {
        "category": "DeFi",
        "project_count": 450,
        "avg_score": 72.0
      }
    ],
    "top_blockchains": [
      {
        "blockchain": "Ethereum",
        "project_count": 520
      }
    ]
  }
}
```

---

## 👤 用户接口

### 1. 获取用户信息

```http
GET /users/me
```

**请求头**:
```
Authorization: Bearer {access_token}
```

**响应** (200 OK):
```json
{
  "success": true,
  "data": {
    "user_id": "usr_abc123",
    "email": "user@example.com",
    "username": "crypto_hunter",
    "tier": "pro",
    "subscription": {
      "plan": "pro",
      "status": "active",
      "started_at": "2025-09-01T00:00:00Z",
      "expires_at": "2025-10-01T00:00:00Z",
      "auto_renew": true
    },
    "usage": {
      "api_calls_today": 150,
      "api_calls_limit": 1000,
      "deep_reports_this_month": 5,
      "deep_reports_limit": 20
    },
    "created_at": "2025-09-01T10:00:00Z"
  }
}
```

---

### 2. 更新用户设置

```http
PATCH /users/me/settings
```

**请求体**:
```json
{
  "email_notifications": true,
  "telegram_notifications": true,
  "notification_preferences": {
    "daily_report": true,
    "s_grade_alerts": true,
    "price_alerts": false
  },
  "timezone": "Asia/Shanghai"
}
```

**响应** (200 OK):
```json
{
  "success": true,
  "message": "Settings updated successfully"
}
```

---

## 🔌 WebSocket 接口

### 实时数据流

**连接**:
```
wss://api.web3alphahunter.com/v1/ws
```

**认证**:
```json
{
  "type": "auth",
  "token": "your_access_token"
}
```

**订阅频道**:
```json
{
  "type": "subscribe",
  "channels": ["new_projects", "s_grade_alerts", "price_updates"]
}
```

**接收消息**:
```json
{
  "type": "new_project",
  "data": {
    "project_id": "proj_new123",
    "name": "New Protocol",
    "grade": "S",
    "score": 95.0,
    "discovered_at": "2025-10-02T14:30:00Z"
  },
  "timestamp": "2025-10-02T14:30:05Z"
}
```

---

## ❌ 错误响应

### 标准错误格式

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Invalid grade parameter. Must be one of: S, A, B, C",
    "details": {
      "field": "grade",
      "provided": "X"
    }
  },
  "request_id": "req_xyz123"
}
```

### 错误代码

| HTTP状态 | 错误代码 | 说明 |
|----------|----------|------|
| 400 | INVALID_PARAMETER | 参数无效 |
| 401 | UNAUTHORIZED | 未认证 |
| 403 | FORBIDDEN | 权限不足 |
| 404 | NOT_FOUND | 资源不存在 |
| 429 | RATE_LIMIT_EXCEEDED | 超过速率限制 |
| 500 | INTERNAL_ERROR | 服务器错误 |
| 503 | SERVICE_UNAVAILABLE | 服务不可用 |

---

## 🚦 速率限制

| 用户等级 | 限制 |
|----------|------|
| 免费版 | 100 请求/小时 |
| 基础版 | 1,000 请求/小时 |
| 专业版 | 10,000 请求/小时 |
| 企业版 | 无限制 |

**响应头**:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1696248000
```

---

## 📦 SDK示例

### Python
```python
from web3_alpha_hunter import Client

client = Client(api_key="your_api_key")

# 获取S级项目
projects = client.projects.list(grade="S", limit=10)

# 搜索项目
results = client.search("defi protocol")

# 添加到监控
client.watchlist.add("proj_xyz789")
```

### JavaScript
```javascript
import { Web3AlphaHunter } from '@web3-alpha-hunter/sdk'

const client = new Web3AlphaHunter({ apiKey: 'your_api_key' })

// 获取每日报告
const report = await client.reports.getDaily()

// 监听实时数据
client.ws.on('new_project', (project) => {
  console.log('New S-grade project:', project.name)
})
```

---

**文档版本**: v1.0  
**最后更新**: 2025-10-02  
**API版本**: v1

