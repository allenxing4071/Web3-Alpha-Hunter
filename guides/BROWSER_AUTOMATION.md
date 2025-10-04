# 浏览器自动化使用指南

> **最后更新**: 2025-10-04  
> **状态**: ✅ 可用

---

## 📋 问题诊断结果

### ✅ 登录页面状态

```
URL: http://web3.guandongfang.cn/login
状态: ✅ 可访问
类型: Next.js React 应用
DNS: ✅ 解析正常 (47.253.226.250)
响应: ✅ 200 OK
```

---

## 🚀 快速打开登录页面

### 方式 1: 使用系统默认浏览器 (推荐,最简单)

```bash
# 方法 A: 使用 Python webbrowser
python3 -c "import webbrowser; webbrowser.open('http://web3.guandongfang.cn/login')"

# 方法 B: 使用脚本
python3 backend/open_browser_login.py
# 选择选项 3
```

### 方式 2: 使用 Selenium (功能最强)

```bash
# 1. 安装 Selenium
pip install selenium webdriver-manager

# 2. 运行脚本
python3 backend/open_browser_login.py
# 选择选项 1
```

### 方式 3: 使用 Playwright (现代化)

```bash
# 1. 安装 Playwright
pip install playwright
playwright install chromium

# 2. 运行脚本
python3 backend/open_browser_login.py
# 选择选项 2
```

---

## 🔧 MCP Browserbase 配置

### 问题

MCP Browserbase 需要 API key 才能使用:

```
Error: Unauthorized. Ensure you provided a valid API key
```

### 解决方案

#### 选项 1: 获取 Browserbase API Key

1. 访问 [Browserbase](https://www.browserbase.com/)
2. 注册账号并获取 API key
3. 配置环境变量:

```bash
# 添加到 backend/.env
BROWSERBASE_API_KEY=your-api-key-here
BROWSERBASE_PROJECT_ID=your-project-id-here
```

#### 选项 2: 使用本地 Selenium/Playwright

由于 MCP Browserbase 是云服务,建议在本地开发环境使用 Selenium 或 Playwright。

---

## 📦 已创建的工具脚本

### 1. `test_login_page.py` - 页面诊断工具

```bash
cd backend
python3 test_login_page.py
```

**功能**:
- ✅ DNS 解析检查
- ✅ HTTP 连接测试
- ✅ 页面内容分析
- ✅ 保存页面截图到 `/tmp/login_page.html`

### 2. `open_browser_login.py` - 浏览器打开工具

```bash
cd backend
python3 open_browser_login.py
```

**功能**:
- 🌐 选项 1: Selenium 自动化
- 🎭 选项 2: Playwright 自动化
- 💻 选项 3: 系统默认浏览器
- 🔄 选项 4: 自动尝试所有方法

---

## 🧪 Selenium 自动化示例

### 基础使用

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置选项
options = Options()
# options.add_argument('--headless')  # 无头模式

# 启动浏览器
driver = webdriver.Chrome(options=options)

# 访问登录页面
driver.get("http://web3.guandongfang.cn/login")

# 等待页面加载
import time
time.sleep(3)

# 截图
driver.save_screenshot("login_page.png")

# 关闭浏览器
driver.quit()
```

### 使用 webdriver-manager (推荐)

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 自动下载并使用正确版本的 ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get("http://web3.guandongfang.cn/login")
# ... 其他操作
driver.quit()
```

---

## 🎭 Playwright 自动化示例

### 基础使用

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # 访问页面
    page.goto("http://web3.guandongfang.cn/login")
    
    # 等待加载
    page.wait_for_load_state("networkidle")
    
    # 截图
    page.screenshot(path="login_page.png")
    
    # 关闭浏览器
    browser.close()
```

### 异步版本

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto("http://web3.guandongfang.cn/login")
        await page.screenshot(path="login_page.png")
        
        await browser.close()

asyncio.run(main())
```

---

## 🔍 登录页面信息

### 技术栈

```
框架: Next.js
语言: React (TypeScript)
状态管理: Zustand
UI: Tailwind CSS
路由: Next.js App Router
```

### 页面特征

```html
- 使用 Next.js 服务端渲染
- 初始加载显示"正在加载..."
- React hydration 后显示完整登录表单
- 深色主题 (dark mode)
```

### API 端点

```
登录: POST /api/v1/auth/login
注册: POST /api/v1/auth/register
健康检查: 需要配置 /health (目前404)
```

---

## 💡 使用建议

### 本地开发

```bash
# 推荐使用 Selenium + webdriver-manager
pip install selenium webdriver-manager

# 或使用 Playwright (更现代)
pip install playwright
playwright install chromium
```

### CI/CD 环境

```bash
# 使用无头模式
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

### 云端自动化

```bash
# 使用 Browserbase (需要 API key)
# 或 Selenium Grid
# 或 BrowserStack
```

---

## ⚠️ 常见问题

### 问题 1: ChromeDriver 版本不匹配

```
Error: session not created: This version of ChromeDriver only supports Chrome version X
```

**解决方案**:
```bash
pip install webdriver-manager
```

然后使用:
```python
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### 问题 2: 页面加载缓慢

```python
# 设置超时
driver.set_page_load_timeout(30)

# 等待特定元素
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
```

### 问题 3: React 应用需要时间 hydrate

```python
# Next.js 应用需要等待 JavaScript 执行
time.sleep(3)  # 等待 React hydration

# 或等待特定元素出现
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
)
```

---

## 📊 性能对比

| 工具 | 启动速度 | 功能 | 学习曲线 | 推荐场景 |
|------|---------|------|---------|---------|
| **webbrowser** | ⚡⚡⚡ | ⭐ | ⭐ | 快速打开页面 |
| **Selenium** | ⚡⚡ | ⭐⭐⭐ | ⭐⭐ | 成熟稳定,生态丰富 |
| **Playwright** | ⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐ | 现代化,功能强大 |
| **Browserbase** | ⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 云端自动化 |

---

## 📚 相关文档

- [Selenium 官方文档](https://www.selenium.dev/documentation/)
- [Playwright 官方文档](https://playwright.dev/)
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
- [Browserbase](https://www.browserbase.com/)

---

## ✅ 快速命令参考

```bash
# 测试页面是否可访问
curl -I http://web3.guandongfang.cn/login

# 运行诊断工具
python3 backend/test_login_page.py

# 打开浏览器
python3 backend/open_browser_login.py

# 快速打开
python3 -c "import webbrowser; webbrowser.open('http://web3.guandongfang.cn/login')"

# 安装依赖
pip install selenium webdriver-manager
pip install playwright && playwright install chromium
```

---

**维护者**: 开发团队  
**最后更新**: 2025-10-04  
**状态**: ✅ 所有工具就绪

