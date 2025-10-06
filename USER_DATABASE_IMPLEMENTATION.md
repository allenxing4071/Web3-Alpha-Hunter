# 用户数据库系统实现文档

## 📋 概述

本文档记录了将用户管理系统从浏览器 localStorage 迁移到 PostgreSQL 数据库的完整实现过程（方案A）。

---

## 🎯 实现目标

### 方案A选择原因
- ✅ 生产环境级别的安全性
- ✅ 数据持久化（不会因清除缓存丢失）
- ✅ 支持多端登录
- ✅ 便于审计和管理
- ✅ 符合行业最佳实践

### 对比方案B（localStorage）
- ❌ 数据不安全（明文存储在浏览器）
- ❌ 清除缓存即丢失
- ❌ 无法多端登录
- ❌ 仅适合demo/测试环境

---

## 🗃️ 数据库设计

### users表结构

```sql
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt加密
    role VARCHAR(20) NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

-- 索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### 默认数据

**管理员账号:**
- 用户名: `admin`
- 密码: `admin123`
- 邮箱: `admin@web3hunter.com`
- 角色: `admin`

---

## 🔧 技术实现

### 后端实现

#### 1. 数据模型
```python
# backend/app/models/user.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    last_login_at = Column(TIMESTAMP, nullable=True)
```

#### 2. Schema定义
```python
# backend/app/schemas/user.py
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "user"

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
```

#### 3. API端点
```python
# backend/app/api/v1/users.py

POST   /api/v1/users/login        # 用户登录
GET    /api/v1/users              # 获取用户列表
GET    /api/v1/users/{id}         # 获取单个用户
POST   /api/v1/users              # 创建用户
PUT    /api/v1/users/{id}         # 更新用户
DELETE /api/v1/users/{id}         # 删除用户
POST   /api/v1/users/init-default # 初始化默认用户
```

#### 4. 密码加密
使用 `bcrypt` 进行密码哈希：
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

### 前端实现

#### 1. API封装
```typescript
// frontend/src/lib/api.ts
export const usersApi = {
  login: (username: string, password: string) => 
    api.post('/users/login', { username, password }),
  list: () => api.get('/users'),
  create: (data: any) => api.post('/users', data),
  update: (id: string, data: any) => api.put(`/users/${id}`, data),
  delete: (id: string) => api.delete(`/users/${id}`),
}
```

#### 2. 认证状态管理
```typescript
// frontend/src/store/authStore.ts
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (username: string, password: string) => {
    const response = await usersApi.login(username, password)
    if (response.success && response.user) {
      sessionStorage.setItem('auth_user', JSON.stringify(response.user))
      sessionStorage.setItem('auth_token', response.token)
      set({ user: response.user, isAuthenticated: true })
      return true
    }
    return false
  },
  
  // ...
}))
```

#### 3. 用户管理页面
- 从数据库加载用户列表
- 支持CRUD操作
- 表单验证
- 权限控制（仅管理员可访问）

---

## 🔐 安全特性

### 1. 密码安全
- ✅ 使用bcrypt进行密码哈希
- ✅ 密码最小长度6位
- ✅ 密码不在API响应中返回
- ✅ 更新用户时密码可选（留空表示不修改）

### 2. 输入验证
- ✅ 用户名长度3-100字符
- ✅ 邮箱格式验证（使用pydantic EmailStr）
- ✅ 角色限制（admin/user）
- ✅ SQL注入防护（使用SQLAlchemy ORM）

### 3. 业务规则
- ✅ 用户名必须唯一
- ✅ 邮箱必须唯一
- ✅ 不能删除管理员账号
- ✅ 不能删除最后一个用户
- ✅ 禁用的用户无法登录

---

## 📊 数据库管理页面集成

users表已添加到数据库管理页面的表列表中：

```typescript
{ 
  id: 'users', 
  label: '👥 users', 
  name: 'users (用户表)', 
  desc: '系统用户管理' 
}
```

可在 `/database` 页面查看users表的：
- 表结构
- 实时数据
- 分页浏览
- 统计信息

---

## 🧪 测试验证

### 1. 数据库测试
```bash
# 查看users表
psql $DATABASE_URL -c "SELECT * FROM users;"

# 统计用户数
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

### 2. API测试
```bash
# 获取用户列表
curl http://localhost:8000/api/v1/users/

# 登录测试
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 创建用户
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"test123",
    "role":"user"
  }'
```

### 3. 前端测试
1. 访问 `http://web3.guandongfang.cn/login`
2. 使用 `admin` / `admin123` 登录
3. 访问用户管理页面测试CRUD功能
4. 访问 `/database` 页面查看users表数据

---

## 📦 依赖说明

### 后端新增依赖
```txt
bcrypt>=4.0.0           # 密码加密
email-validator>=2.0.0  # 邮箱验证
```

安装命令：
```bash
pip3 install bcrypt email-validator
```

---

## 🚀 部署说明

### 1. 数据库迁移
```bash
cd backend
python3 -c "
from app.db.session import get_db
from sqlalchemy import text

db = next(get_db())
with open('scripts/create_users_table.sql', 'r') as f:
    sql = f.read()
db.execute(text(sql))
db.commit()
"
```

### 2. 启动服务
```bash
# 后端
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 前端
cd frontend
npm run dev
```

### 3. 初始化默认用户
- 默认管理员会在数据库迁移时自动创建
- 也可以通过API手动初始化：
```bash
curl -X POST http://localhost:8000/api/v1/users/init-default
```

---

## 📝 使用指南

### 管理员操作

1. **登录系统**
   - 用户名: `admin`
   - 密码: `admin123`

2. **创建新用户**
   - 进入"用户管理"页面
   - 点击"+ 添加用户"
   - 填写用户信息
   - 选择角色（admin/user）
   - 点击"添加用户"

3. **编辑用户**
   - 在用户列表中点击"编辑"
   - 修改用户信息
   - 密码留空表示不修改
   - 点击"更新用户"

4. **删除用户**
   - 点击用户行的"删除"按钮
   - 确认删除
   - 注意：不能删除管理员和最后一个用户

5. **查看数据库**
   - 进入"数据库管理"页面
   - 选择"users"表
   - 查看表结构和数据
   - 支持分页浏览

---

## ⚠️ 注意事项

1. **密码安全**
   - 请立即修改默认管理员密码
   - 密码至少6位
   - 建议使用强密码

2. **角色权限**
   - admin: 完全权限
   - user: 普通权限

3. **数据备份**
   - 定期备份数据库
   - 特别是users表数据

4. **生产环境**
   - 使用环境变量管理密钥
   - 启用HTTPS
   - 配置CORS
   - 使用JWT替代简单token

---

## 🔄 后续优化建议

### 短期优化
- [ ] 实现JWT Token认证
- [ ] 添加密码强度验证
- [ ] 实现密码重置功能
- [ ] 添加用户头像
- [ ] 记录用户操作日志

### 长期优化
- [ ] 实现OAuth第三方登录
- [ ] 添加双因素认证（2FA）
- [ ] 实现会话管理
- [ ] 添加权限细分（RBAC）
- [ ] 实现用户配额限制

---

## 📚 相关文档

- [API文档](./docs/02-技术实现/02-API接口文档.md)
- [数据库设计](./docs/02-技术实现/04-数据库设计文档.md)
- [部署指南](./docs/04-部署与运维/01-部署指南.md)

---

## ✅ 完成状态

- [x] 创建users数据库表
- [x] 创建用户模型和Schema
- [x] 实现用户管理API
- [x] 修改前端连接真实API
- [x] authStore使用真实API
- [x] 用户管理页面连接数据库
- [x] 数据库管理页面添加users表
- [x] 文档编写

**实施日期:** 2025-10-06  
**版本:** v1.0.0  
**状态:** ✅ 已完成并测试通过






