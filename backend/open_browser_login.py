#!/usr/bin/env python3
"""
使用 Selenium 打开浏览器访问登录页面
自动化测试登录功能
"""

import time
import sys

def open_with_selenium():
    """使用 Selenium 打开浏览器"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
    except ImportError:
        print("❌ Selenium 未安装!")
        print("\n安装命令:")
        print("  pip install selenium")
        print("\n还需要下载 ChromeDriver:")
        print("  https://chromedriver.chromium.org/downloads")
        return False
    
    print("="*60)
    print("🌐 使用 Selenium 打开浏览器")
    print("="*60)
    
    url = "http://web3.guandongfang.cn/login"
    
    # 配置 Chrome 选项
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式(不显示浏览器窗口)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        print("\n🚀 启动 Chrome 浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"📍 访问: {url}")
        driver.get(url)
        
        print("⏳ 等待页面加载...")
        time.sleep(3)
        
        # 获取页面标题
        print(f"\n📄 页面标题: {driver.title}")
        print(f"📍 当前 URL: {driver.current_url}")
        
        # 检查页面元素
        print("\n🔍 检查页面元素...")
        
        # 等待 React 应用加载
        try:
            # 查找登录相关元素
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("✅ 页面 body 已加载")
            
            # 截图
            screenshot_path = "/tmp/login_page_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 页面截图已保存: {screenshot_path}")
            
            # 获取页面源代码
            page_source = driver.page_source
            print(f"📏 页面源代码长度: {len(page_source)} 字符")
            
            # 检查是否有 React 根元素
            if '__next' in page_source or 'next-page' in page_source:
                print("✅ 检测到 Next.js 应用")
            
            # 查找常见的登录元素
            elements_to_find = [
                ("input[type='email']", "邮箱输入框"),
                ("input[type='password']", "密码输入框"),
                ("button[type='submit']", "提交按钮"),
                ("form", "表单"),
                ("input", "输入框"),
                ("button", "按钮"),
            ]
            
            print("\n🔍 查找登录元素:")
            for selector, name in elements_to_find:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"  ✅ 找到 {len(elements)} 个 {name}")
                    else:
                        print(f"  ❌ 未找到 {name}")
                except Exception as e:
                    print(f"  ⚠️  {name} 查找失败: {e}")
            
            # 等待用户查看
            print("\n" + "="*60)
            print("ℹ️  浏览器已打开,按 Enter 关闭浏览器...")
            print("="*60)
            input()
            
        except Exception as e:
            print(f"⚠️  等待页面元素时出错: {e}")
            
            # 即使出错也保存截图
            try:
                driver.save_screenshot("/tmp/login_page_error.png")
                print("📸 错误截图已保存: /tmp/login_page_error.png")
            except:
                pass
        
        finally:
            print("\n🔒 关闭浏览器...")
            driver.quit()
            print("✅ 浏览器已关闭")
            
        return True
        
    except Exception as e:
        print(f"\n❌ 浏览器启动失败: {e}")
        print("\n可能的原因:")
        print("  1. ChromeDriver 未安装或版本不匹配")
        print("  2. Chrome 浏览器未安装")
        print("  3. 需要使用 webdriver-manager 自动管理驱动")
        print("\n解决方案:")
        print("  pip install webdriver-manager")
        print("  然后使用: from webdriver_manager.chrome import ChromeDriverManager")
        return False


def open_with_playwright():
    """使用 Playwright 打开浏览器 (备选方案)"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright 未安装!")
        print("\n安装命令:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return False
    
    print("="*60)
    print("🎭 使用 Playwright 打开浏览器")
    print("="*60)
    
    url = "http://web3.guandongfang.cn/login"
    
    try:
        with sync_playwright() as p:
            print("\n🚀 启动 Chromium 浏览器...")
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            print(f"📍 访问: {url}")
            page.goto(url)
            
            print("⏳ 等待页面加载...")
            page.wait_for_load_state("networkidle")
            
            # 获取页面标题
            print(f"\n📄 页面标题: {page.title()}")
            print(f"📍 当前 URL: {page.url}")
            
            # 截图
            screenshot_path = "/tmp/login_page_playwright.png"
            page.screenshot(path=screenshot_path)
            print(f"📸 页面截图已保存: {screenshot_path}")
            
            # 检查页面元素
            print("\n🔍 检查页面元素...")
            
            elements_to_check = [
                ("input[type='email']", "邮箱输入框"),
                ("input[type='password']", "密码输入框"),
                ("button[type='submit']", "提交按钮"),
                ("input", "输入框"),
                ("button", "按钮"),
            ]
            
            for selector, name in elements_to_check:
                count = page.locator(selector).count()
                if count > 0:
                    print(f"  ✅ 找到 {count} 个 {name}")
                else:
                    print(f"  ❌ 未找到 {name}")
            
            # 等待用户查看
            print("\n" + "="*60)
            print("ℹ️  浏览器已打开,按 Enter 关闭浏览器...")
            print("="*60)
            input()
            
            browser.close()
            print("\n✅ 浏览器已关闭")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Playwright 执行失败: {e}")
        return False


def open_with_webbrowser():
    """使用系统默认浏览器打开 (最简单)"""
    import webbrowser
    
    print("="*60)
    print("🌐 使用系统默认浏览器打开")
    print("="*60)
    
    url = "http://web3.guandongfang.cn/login"
    
    print(f"\n📍 打开 URL: {url}")
    webbrowser.open(url)
    
    print("✅ 已在默认浏览器中打开登录页面")
    return True


def main():
    print("\n🔧 Web3 Alpha Hunter 登录页面浏览器打开工具")
    print("="*60)
    
    print("\n请选择打开方式:")
    print("  1. Selenium (推荐,功能最强)")
    print("  2. Playwright (现代化工具)")
    print("  3. 系统默认浏览器 (最简单)")
    print("  4. 全部尝试")
    
    choice = input("\n请输入选项 (1-4, 默认 3): ").strip() or "3"
    
    if choice == "1":
        open_with_selenium()
    elif choice == "2":
        open_with_playwright()
    elif choice == "3":
        open_with_webbrowser()
    elif choice == "4":
        print("\n📋 依次尝试所有方法...\n")
        
        if not open_with_webbrowser():
            print("\n⏭️  尝试下一个方法...\n")
            
        time.sleep(2)
        
        if not open_with_selenium():
            print("\n⏭️  尝试下一个方法...\n")
            
        if not open_with_playwright():
            print("\n❌ 所有方法都失败了")
    else:
        print("❌ 无效的选项")
        sys.exit(1)


if __name__ == "__main__":
    main()

