#!/usr/bin/env python3
"""
测试登录页面访问
检查 Web3 Alpha Hunter 登录页面状态
"""

import requests
from urllib.parse import urljoin

def test_login_page():
    """测试登录页面"""
    base_url = "http://web3.guandongfang.cn"
    login_url = urljoin(base_url, "/login")
    
    print("="*60)
    print("🌐 测试 Web3 Alpha Hunter 登录页面")
    print("="*60)
    print(f"\n📍 URL: {login_url}")
    
    try:
        print("\n📡 发送 HTTP 请求...")
        response = requests.get(login_url, timeout=10)
        
        print(f"\n✅ 响应状态码: {response.status_code}")
        print(f"📦 Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"📏 响应大小: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("\n✅ 登录页面可访问!")
            
            # 检查是否是 HTML 页面
            if 'text/html' in response.headers.get('Content-Type', ''):
                print("✅ 页面类型: HTML")
                
                # 检查页面内容
                content = response.text.lower()
                
                checks = {
                    "包含 'login' 关键字": 'login' in content,
                    "包含表单元素": '<form' in content or 'form' in content,
                    "包含输入框": '<input' in content or 'input' in content,
                    "包含按钮": '<button' in content or 'button' in content,
                    "可能是 React 应用": 'react' in content or '__next' in content,
                }
                
                print("\n📊 页面内容检查:")
                for check, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"  {status} {check}")
                
                # 保存页面内容供查看
                with open('/tmp/login_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"\n💾 页面内容已保存到: /tmp/login_page.html")
            else:
                print(f"⚠️  页面类型不是 HTML: {response.headers.get('Content-Type')}")
        else:
            print(f"\n❌ 页面返回错误状态码: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("\n❌ 请求超时!")
        print("   可能的原因:")
        print("   - 服务器响应慢")
        print("   - 网络连接问题")
        
    except requests.exceptions.ConnectionError as e:
        print("\n❌ 连接失败!")
        print(f"   错误: {e}")
        print("   可能的原因:")
        print("   - 服务器未启动")
        print("   - 域名解析失败")
        print("   - 防火墙阻止")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


def test_backend_api():
    """测试后端 API"""
    api_url = "http://web3.guandongfang.cn/api/v1"
    
    print("\n" + "="*60)
    print("🔌 测试后端 API")
    print("="*60)
    
    endpoints = [
        "/",
        "/health",
        "/api/v1",
    ]
    
    for endpoint in endpoints:
        url = f"http://web3.guandongfang.cn{endpoint}"
        print(f"\n📍 测试: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"  {status} 状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  📊 响应数据: {data}")
                except:
                    print(f"  📝 响应文本: {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")


def check_dns():
    """检查域名解析"""
    import socket
    
    print("\n" + "="*60)
    print("🌐 DNS 解析检查")
    print("="*60)
    
    domain = "web3.guandongfang.cn"
    
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"\n✅ 域名: {domain}")
        print(f"✅ IP地址: {ip_address}")
        
        # 检查是否是预期的 IP
        expected_ip = "47.253.226.250"
        if ip_address == expected_ip:
            print(f"✅ IP 匹配预期值: {expected_ip}")
        else:
            print(f"⚠️  IP 不匹配预期值: {expected_ip}")
            
    except socket.gaierror:
        print(f"\n❌ 域名解析失败: {domain}")
        print("   可能的原因:")
        print("   - 域名未配置或已过期")
        print("   - DNS 服务器问题")


def main():
    print("\n🧪 Web3 Alpha Hunter 登录页面诊断")
    print("="*60)
    
    # DNS 检查
    check_dns()
    
    # 测试登录页面
    test_login_page()
    
    # 测试后端 API
    test_backend_api()
    
    print("\n" + "="*60)
    print("✅ 诊断完成!")
    print("="*60)
    
    print("\n💡 如果需要使用浏览器自动化:")
    print("   1. 安装 Selenium: pip install selenium")
    print("   2. 下载 ChromeDriver")
    print("   3. 运行浏览器自动化脚本")
    print("\n   或者配置 Browserbase API key 使用 MCP 工具")


if __name__ == "__main__":
    main()

