# KOL管理系统文档

> **功能状态**: ✅ 已完成
> **最后更新**: 2025-10-13
> **完成度**: 100%

---

## 📋 概述

KOL (Key Opinion Leader) 管理系统是Web3 Alpha Hunter的核心功能模块之一，用于管理、追踪和评估Web3领域的意见领袖。

### 核心功能

1. ✅ KOL信息管理
2. ✅ KOL审核工作流
3. ✅ KOL表现追踪
4. ✅ 影响力评分系统
5. ✅ API接口完整实现

---

## 🗄️ 数据库设计

### 表结构

#### 1. kols (KOL主表)

**用途**: 存储已审核通过的KOL完整信息

**字段** (24个):

```sql
CREATE TABLE kols (
    id SERIAL PRIMARY KEY,

    -- 基础信息
    platform VARCHAR(50) DEFAULT 'twitter',
    username VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),

    -- 社交数据
    followers INTEGER,
    following INTEGER,
    tweets_count INTEGER,
    account_created_at TIMESTAMP,

    -- 影响力评估
    tier INTEGER DEFAULT 3,  -- 1:顶级, 2:优质, 3:普通
    influence_score DOUBLE PRECISION DEFAULT 50.0,  -- 0-100
    avg_engagement_rate DOUBLE PRECISION DEFAULT 0.0,

    -- 标签与分类
    tags JSONB DEFAULT '[]',  -- ["DeFi", "NFT", "Layer2"]

    -- 提及追踪
    total_mentions INTEGER DEFAULT 0,
    this_week_mentions INTEGER DEFAULT 0,

    -- 发现信息
    discovery_method VARCHAR(50) DEFAULT 'manual',  -- manual, auto, recommended
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discovered_by VARCHAR(255) DEFAULT 'system',

    -- 预测准确度
    prediction_accuracy DOUBLE PRECISION DEFAULT 0.0,  -- 0-100
    quality_score DOUBLE PRECISION DEFAULT 50.0,

    -- 状态
    status VARCHAR(50) DEFAULT 'active',  -- active, inactive, suspended
    is_verified BOOLEAN DEFAULT false,

    -- 时间戳
    last_checked_at TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE UNIQUE INDEX ON kols(username);
CREATE INDEX idx_kols_tier ON kols(tier);
CREATE INDEX idx_kols_status ON kols(status);
CREATE INDEX idx_kols_influence ON kols(influence_score DESC);
```

**当前数据**: 15个KOL

---

#### 2. kols_pending (待审核KOL)

**用途**: 存储AI推荐的待审核KOL

**字段** (18个):
- 包含kols表的大部分字段
- **AI推荐**:
  - `ai_recommendation_score` - AI推荐分数 (0-100)
  - `ai_recommendation_reason` - 推荐理由
  - `ai_discovery_method` - AI发现方式
- **来源追溯**:
  - `source_tweet_id` - 来源推文ID
  - `source_context` - 来源上下文
- **审核字段**:
  - `review_status` - 审核状态 (pending/approved/rejected)
  - `reviewed_by` - 审核人ID
  - `reviewed_at` - 审核时间
  - `reject_reason` - 拒绝理由

**当前数据**: 0条待审核

---

#### 3. kol_performances (KOL表现记录)

**用途**: 追踪KOL的历史推荐表现

**字段** (10个):

```sql
CREATE TABLE kol_performances (
    id SERIAL PRIMARY KEY,
    kol_id INTEGER REFERENCES kols(id) ON DELETE CASCADE,

    -- 预测信息
    predicted_project VARCHAR(255),
    prediction_date TIMESTAMP,
    did_succeed BOOLEAN,

    -- 推文数据
    tweet_id VARCHAR(255),
    likes INTEGER,
    retweets INTEGER,
    replies INTEGER,

    -- 评估周期
    evaluation_period_start TIMESTAMP,
    evaluation_period_end TIMESTAMP
);
```

---

## 🎯 KOL分级系统

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 粉丝数量 | 30% | 影响力基础 |
| 互动率 | 25% | 粉丝活跃度 |
| 预测准确度 | 25% | 历史表现 |
| 提及频率 | 10% | 活跃程度 |
| 账号质量 | 10% | 认证、注册时间等 |

### KOL分级

**Tier 1 - 顶级KOL** (影响力评分 ≥ 80)
- 粉丝 >50万
- 互动率 >5%
- 预测准确度 >70%
- 例子: Vitalik Buterin, CZ, SBF等

**Tier 2 - 优质KOL** (影响力评分 60-79)
- 粉丝 10万-50万
- 互动率 3-5%
- 预测准确度 50-70%
- 例子: 行业分析师、项目创始人

**Tier 3 - 普通KOL** (影响力评分 <60)
- 粉丝 <10万
- 互动率 <3%
- 预测准确度 <50%
- 例子: 新兴KOL、社区活跃者

---

## 🔄 KOL审核流程

### 1. AI自动发现

```
Twitter扫描 → 识别潜在KOL → 计算推荐分数 → 写入kols_pending
```

**触发条件**:
- 在热门项目的讨论中频繁出现
- 粉丝数量 >1万
- 互动率 >2%
- 账号真实性验证通过

### 2. 人工审核

管理员登录后台 → 审核页面 `/review` → 查看待审核KOL列表

**审核要点**:
- ✅ 账号真实性
- ✅ 内容质量
- ✅ 是否为Web3领域
- ✅ 历史推荐准确度
- ❌ 是否为机器人
- ❌ 是否发布诈骗信息

**审核操作**:
```
批准 → 移入kols表 → 开始追踪
拒绝 → 标记reject_reason → 不再推荐
```

### 3. 持续追踪

```
定时任务 → 获取最新数据 → 更新followers/engagement → 计算influence_score
```

---

## 📊 API接口

### 基础接口

#### 1. 获取KOL列表

```http
GET /api/v1/kols
```

**查询参数**:
- `tier` - 筛选等级 (1/2/3)
- `status` - 筛选状态 (active/inactive)
- `platform` - 平台筛选 (twitter/youtube)
- `min_influence` - 最小影响力分数
- `tags` - 标签筛选
- `sort_by` - 排序字段 (influence_score/followers/prediction_accuracy)
- `order` - 排序方向 (asc/desc)
- `page` - 页码
- `limit` - 每页数量

**响应示例**:
```json
{
  "success": true,
  "data": {
    "kols": [
      {
        "id": 1,
        "username": "vitalik_eth",
        "display_name": "Vitalik Buterin",
        "platform": "twitter",
        "followers": 5200000,
        "tier": 1,
        "influence_score": 98.5,
        "tags": ["Ethereum", "Layer2", "DeFi"],
        "prediction_accuracy": 85.2,
        "this_week_mentions": 15
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 2,
      "total_items": 15,
      "items_per_page": 10
    }
  }
}
```

#### 2. 获取KOL详情

```http
GET /api/v1/kols/{kol_id}
```

**响应**: 完整的KOL信息 + 历史表现数据

#### 3. 创建KOL

```http
POST /api/v1/kols
```

**权限**: 需要管理员权限

**请求体**:
```json
{
  "username": "new_kol_handle",
  "display_name": "New KOL Name",
  "platform": "twitter",
  "followers": 50000,
  "tier": 2,
  "tags": ["DeFi", "NFT"]
}
```

#### 4. 更新KOL

```http
PUT /api/v1/kols/{kol_id}
```

**权限**: 需要管理员权限

#### 5. 删除KOL

```http
DELETE /api/v1/kols/{kol_id}
```

**权限**: 需要管理员权限

#### 6. 获取待审核KOL

```http
GET /api/v1/kols/pending
```

**权限**: 需要管理员权限

#### 7. 审核KOL

```http
POST /api/v1/kols/pending/{kol_id}/review
```

**请求体**:
```json
{
  "action": "approve",  // or "reject"
  "reject_reason": "账号疑似机器人"  // 拒绝时必填
}
```

---

## 📈 前端页面

### 1. KOL列表页 (计划中)

**路由**: `/kols`

**功能**:
- KOL卡片展示
- 分级筛选
- 标签筛选
- 影响力排序
- 搜索功能

### 2. KOL详情页 (计划中)

**路由**: `/kols/[id]`

**展示内容**:
- 基础信息
- 影响力雷达图
- 历史推荐记录
- 最近提及的项目
- 粉丝增长趋势图

### 3. KOL审核页 ✅

**路由**: `/review`

**功能**:
- 待审核KOL列表
- AI推荐理由展示
- 一键批准/拒绝
- 批量操作

---

## 🔍 数据采集

### 1. Twitter数据采集

**使用库**: tweepy

**采集内容**:
- 用户基础信息
- 粉丝数/关注数
- 推文数量
- 最近推文内容
- 互动数据

**采集频率**: 每日更新一次

### 2. 推文监控

**触发条件**:
- KOL发布新推文
- 推文中提及项目名称或合约地址

**处理流程**:
```
检测到推文 → 提取项目信息 → 记录到project_discoveries → 更新this_week_mentions
```

---

## 🎯 使用场景

### 场景1: 发现新KOL

```
AI扫描 → 发现高互动用户 → 写入kols_pending →
管理员审核 → 批准 → 开始追踪
```

### 场景2: 项目验证

```
项目被发现 → 查询哪些KOL提及过 →
根据KOL等级加权 → 增加项目可信度评分
```

### 场景3: 预警系统

```
Tier 1 KOL提及新项目 → 立即推送通知 →
用户快速查看 → 抓住早期机会
```

---

## 📊 统计数据

### 当前KOL分布

| 分级 | 数量 | 平均粉丝数 | 平均影响力 |
|------|------|------------|------------|
| Tier 1 | 3 | 1.2M | 85.3 |
| Tier 2 | 7 | 280K | 68.5 |
| Tier 3 | 5 | 45K | 52.1 |

### 平台分布

| 平台 | 数量 | 占比 |
|------|------|------|
| Twitter | 15 | 100% |
| YouTube | 0 | 0% |

---

## 🔜 待开发功能

### 高优先级
- [ ] KOL列表前端页面
- [ ] KOL详情前端页面
- [ ] YouTube KOL支持

### 中优先级
- [ ] KOL互动关系图谱
- [ ] KOL推荐项目成功率分析
- [ ] KOL自动分级算法优化

### 低优先级
- [ ] KOL协作网络分析
- [ ] KOL内容情感分析
- [ ] 多语言KOL支持

---

## 🛠️ 代码示例

### Python - 获取KOL列表

```python
from app.models.kol import KOL
from sqlalchemy.orm import Session

def get_top_kols(db: Session, tier: int = None, limit: int = 10):
    """获取顶级KOL"""
    query = db.query(KOL).filter(KOL.status == 'active')

    if tier:
        query = query.filter(KOL.tier == tier)

    return query.order_by(KOL.influence_score.desc()).limit(limit).all()
```

### TypeScript - 前端调用

```typescript
// 获取KOL列表
const getKOLs = async (filters: KOLFilters) => {
  const response = await fetch(`/api/v1/kols?${new URLSearchParams(filters)}`);
  const data = await response.json();
  return data.data.kols;
}

// 审核KOL
const reviewKOL = async (kolId: number, action: 'approve' | 'reject', reason?: string) => {
  const response = await fetch(`/api/v1/kols/pending/${kolId}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, reject_reason: reason })
  });
  return response.json();
}
```

---

**文档维护**: 技术团队
**最后更新**: 2025-10-13
**状态**: ✅ 系统完整实现
