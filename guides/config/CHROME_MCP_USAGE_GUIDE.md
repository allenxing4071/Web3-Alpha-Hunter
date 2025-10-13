# Chrome DevTools MCP 完全使用指南

## 📚 目录

1. [快速开始](#快速开始)
2. [参数详解](#参数详解)
3. [配置场景](#配置场景)
4. [使用脚本](#使用脚本)
5. [实战案例](#实战案例)
6. [常见问题](#常见问题)

---

## 🚀 快速开始

### 方法一：使用自动配置脚本（推荐）

```bash
cd guides/config
./chrome-mcp-quick-setup.sh
```

选择您需要的场景，脚本会自动配置 `~/.cursor/mcp.json`。

### 方法二：手动配置

编辑 `~/.cursor/mcp.json`，在 `mcpServers` 中添加配置：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browserUrl", "http://127.0.0.1:9222"
      ],
      "env": {}
    }
  }
}
```

---

## 📖 参数详解

### 核心参数

| 参数 | 说明 | 示例 | 使用场景 |
|------|------|------|----------|
| `--browserUrl` | 连接已运行的 Chrome | `http://127.0.0.1:9222` | 开发调试，可见操作过程 |
| `--headless` | 无头模式（无界面） | `--headless` | CI/CD，自动化测试 |
| `--isolated` | 临时用户目录（自动清理） | `--isolated` | 测试环境隔离 |
| `--viewport` | 设置视口大小 | `1920x1080` | 响应式测试 |
| `--channel` | Chrome 版本 | `stable/beta/dev/canary` | 测试新特性 |
| `--logFile` | 日志文件路径 | `/tmp/chrome.log` | 调试问题 |
| `--proxyServer` | 代理服务器 | `http://127.0.0.1:8888` | 网络调试 |
| `--acceptInsecureCerts` | 忽略证书错误 | `--acceptInsecureCerts` | 开发环境 HTTPS |
| `--executablePath` | 自定义 Chrome 路径 | `/path/to/chrome` | 使用特定版本 |

### 常用视口尺寸

#### 桌面端
- `1920x1080` - 全高清（最常见）
- `1366x768` - 笔记本常见尺寸
- `1280x720` - 高清
- `2560x1440` - 2K 显示器

#### 移动端
- `375x667` - iPhone 8/SE
- `390x844` - iPhone 12/13/14
- `414x896` - iPhone XR/11
- `360x640` - Android 小屏
- `412x915` - Android 大屏

#### 平板
- `768x1024` - iPad
- `810x1080` - iPad Air
- `1024x1366` - iPad Pro 12.9"

---

## 🎯 配置场景

### 场景 1: 日常开发（推荐）

**特点**: 可见浏览器窗口，方便调试

```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--browserUrl", "http://127.0.0.1:9222"
    ],
    "env": {}
  }
}
```

**启动 Chrome**:
```bash
# 使用脚本
./guides/config/scripts/start-chrome-debug.sh

# 或手动启动
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug
```

**适用于**: 
- ✅ 开发调试
- ✅ 手动测试
- ✅ 学习使用

---

### 场景 2: 自动化测试

**特点**: 无界面运行，环境隔离

```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--headless",
      "--isolated"
    ],
    "env": {}
  }
}
```

**适用于**:
- ✅ CI/CD 流水线
- ✅ 批量测试
- ✅ 定时任务

---

### 场景 3: 性能测试

**特点**: 固定视口，详细日志

```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--isolated",
      "--viewport", "1920x1080",
      "--logFile", "/tmp/chrome-mcp-perf.log"
    ],
    "env": {
      "DEBUG": "*"
    }
  }
}
```

**适用于**:
- ✅ 性能监控
- ✅ LCP/FCP 分析
- ✅ 网络请求分析

---

### 场景 4: 移动端测试

**特点**: 小屏幕，触摸模拟

```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--viewport", "375x667",
      "--isolated"
    ],
    "env": {}
  }
}
```

**适用于**:
- ✅ 响应式设计测试
- ✅ 移动端交互测试
- ✅ 触摸事件测试

---

### 场景 5: 网络调试

**特点**: 使用代理，查看所有请求

```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": [
      "chrome-devtools-mcp@latest",
      "--proxyServer", "http://127.0.0.1:8888"
    ],
    "env": {}
  }
}
```

**配合工具**:
- Charles Proxy
- Fiddler
- Wireshark

**适用于**:
- ✅ API 调试
- ✅ 网络问题排查
- ✅ 安全测试

---

### 场景 6: 多配置共存

**特点**: 为不同场景准备多个配置

```json
{
  "mcpServers": {
    "chrome-devtools-remote": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9222"],
      "env": {}
    },
    "chrome-devtools-headless": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--headless", "--isolated"],
      "env": {}
    },
    "chrome-devtools-mobile": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--viewport", "375x667", "--isolated"],
      "env": {}
    },
    "chrome-devtools-desktop": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--viewport", "1920x1080", "--isolated"],
      "env": {}
    }
  }
}
```

**使用方式**: 在 Cursor 中选择不同的 MCP 服务

---

## 🛠️ 使用脚本

### 1. 启动 Chrome 远程调试

```bash
./guides/config/scripts/start-chrome-debug.sh [端口号]
```

**默认端口**: 9222

**示例**:
```bash
# 使用默认端口 9222
./guides/config/scripts/start-chrome-debug.sh

# 使用自定义端口 9223
./guides/config/scripts/start-chrome-debug.sh 9223
```

### 2. 停止 Chrome 远程调试

```bash
./guides/config/scripts/stop-chrome-debug.sh [端口号]
```

### 3. 快速配置 MCP

```bash
./guides/config/chrome-mcp-quick-setup.sh
```

**命令行参数**:
- `dev` - 日常开发
- `test` - 自动化测试
- `perf` - 性能测试
- `mobile` - 移动端测试
- `proxy` - 网络调试
- `multi` - 多配置
- `minimal` - 最小配置
- `help` - 显示帮助

**示例**:
```bash
# 交互式选择
./chrome-mcp-quick-setup.sh

# 直接配置开发模式
./chrome-mcp-quick-setup.sh dev

# 显示帮助
./chrome-mcp-quick-setup.sh help
```

---

## 💼 实战案例

### 案例 1: 测试管理后台登录流程

```typescript
// 使用场景：日常开发配置

// 1. 启动 Chrome 调试
// $ ./guides/config/scripts/start-chrome-debug.sh

// 2. 在 Cursor 中使用 MCP 工具
// - 打开新页面
// - 导航到登录页
// - 填充表单
// - 点击登录按钮
// - 验证跳转
// - 截图保存

// 工具调用示例：
mcp_chrome-devtools_new_page({url: "http://localhost:3000/login"})
mcp_chrome-devtools_fill({uid: "username-input", value: "admin"})
mcp_chrome-devtools_fill({uid: "password-input", value: "password"})
mcp_chrome-devtools_click({uid: "login-button"})
mcp_chrome-devtools_take_screenshot({name: "login-success"})
```

### 案例 2: 性能测试项目列表页

```json
// 使用配置：性能测试模式

// 1. 启动性能追踪
mcp_chrome-devtools_performance_start_trace({
  reload: true,
  autoStop: true
})

// 2. 导航到项目列表
mcp_chrome-devtools_navigate_page({
  url: "http://localhost:3000/projects"
})

// 3. 等待加载完成
mcp_chrome-devtools_wait_for({
  text: "项目列表",
  timeout: 5000
})

// 4. 停止追踪并分析
mcp_chrome-devtools_performance_stop_trace()

// 5. 查看性能洞察
mcp_chrome-devtools_performance_analyze_insight({
  insightName: "LCPBreakdown"
})
```

### 案例 3: 网络请求监控

```typescript
// 使用配置：网络调试模式

// 1. 导航到页面
mcp_chrome-devtools_navigate_page({
  url: "http://localhost:3000/dashboard"
})

// 2. 等待加载
await new Promise(resolve => setTimeout(resolve, 2000))

// 3. 获取所有网络请求
const requests = mcp_chrome-devtools_list_network_requests({
  resourceTypes: ["xhr", "fetch"],
  pageSize: 50
})

// 4. 分析特定请求
const apiRequest = mcp_chrome-devtools_get_network_request({
  url: "http://localhost:8000/api/v1/projects"
})

// 5. 检查响应
console.log("状态码:", apiRequest.status)
console.log("响应时间:", apiRequest.responseTime)
```

### 案例 4: 移动端响应式测试

```typescript
// 使用配置：移动端测试模式

// 1. 打开页面
mcp_chrome-devtools_navigate_page({
  url: "http://localhost:3000"
})

// 2. 截图对比
mcp_chrome-devtools_take_screenshot({
  name: "mobile-homepage",
  fullPage: true
})

// 3. 测试触摸交互
mcp_chrome-devtools_click({uid: "menu-button"})
mcp_chrome-devtools_take_screenshot({
  name: "mobile-menu-open"
})

// 4. 测试滚动
mcp_chrome-devtools_evaluate_script({
  function: "() => window.scrollTo(0, 1000)"
})
```

---

## ❓ 常见问题

### Q1: Chrome 启动失败怎么办？

**检查步骤**:
1. 确认 Chrome 已安装
2. 检查端口是否被占用: `lsof -i:9222`
3. 查看日志: `cat /tmp/chrome-debug-9222.log`
4. 尝试其他端口: `./start-chrome-debug.sh 9223`

### Q2: 连接不上远程 Chrome？

**解决方案**:
1. 确认 Chrome 已启动并监听正确端口
2. 访问 `http://127.0.0.1:9222/json` 查看是否返回页面列表
3. 检查防火墙设置
4. 确认配置中的 URL 正确

### Q3: 如何在无头模式下调试？

**方法**:
1. 启用日志: `--logFile /tmp/chrome.log`
2. 设置环境变量: `"env": {"DEBUG": "*"}`
3. 使用截图功能查看页面状态
4. 使用 `take_snapshot` 获取页面结构

### Q4: 如何同时测试多个浏览器实例？

**方案**:
1. 使用不同端口启动多个 Chrome:
   ```bash
   ./start-chrome-debug.sh 9222
   ./start-chrome-debug.sh 9223
   ./start-chrome-debug.sh 9224
   ```

2. 配置多个 MCP 服务:
   ```json
   {
     "chrome-1": {
       "command": "npx",
       "args": ["chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9222"]
     },
     "chrome-2": {
       "command": "npx",
       "args": ["chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9223"]
     }
   }
   ```

### Q5: 性能测试结果如何解读？

**核心指标**:
- **LCP** (Largest Contentful Paint): 最大内容绘制，< 2.5s 为优秀
- **FID** (First Input Delay): 首次输入延迟，< 100ms 为优秀
- **CLS** (Cumulative Layout Shift): 累积布局偏移，< 0.1 为优秀
- **FCP** (First Contentful Paint): 首次内容绘制，< 1.8s 为优秀

**分析命令**:
```typescript
mcp_chrome-devtools_performance_analyze_insight({
  insightName: "LCPBreakdown"  // 或 "DocumentLatency"
})
```

### Q6: 如何处理 HTTPS 证书错误？

**方法 1**: 使用参数（不推荐生产环境）
```json
{
  "args": [
    "chrome-devtools-mcp@latest",
    "--acceptInsecureCerts"
  ]
}
```

**方法 2**: 添加证书到系统信任列表

### Q7: 如何保存会话状态？

**方法**:
1. 不使用 `--isolated` 参数
2. 指定固定的用户数据目录:
   ```bash
   --user-data-dir=/path/to/persistent/dir
   ```

### Q8: 如何模拟网络条件？

**工具调用**:
```typescript
// 模拟慢速 3G
mcp_chrome-devtools_emulate_network({
  throttlingOption: "Slow 3G"
})

// 模拟 CPU 节流（4倍减速）
mcp_chrome-devtools_emulate_cpu({
  throttlingRate: 4
})

// 恢复正常
mcp_chrome-devtools_emulate_network({
  throttlingOption: "No emulation"
})
```

---

## 🔗 相关资源

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Chrome Remote Debugging](https://developer.chrome.com/docs/devtools/remote-debugging/)
- [项目配置文件](./chrome-mcp-configs.json)
- [自动配置脚本](./chrome-mcp-quick-setup.sh)

---

## 📝 下一步

1. ✅ 选择适合的配置场景
2. ✅ 运行配置脚本或手动配置
3. ✅ 重启 Cursor 使配置生效
4. ✅ 开始使用 Chrome DevTools MCP 工具
5. ✅ 查看实战案例学习具体用法

**需要帮助？** 查看 [常见问题](#常见问题) 或查阅项目文档。

