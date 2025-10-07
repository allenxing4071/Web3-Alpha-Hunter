#!/usr/bin/env python3
"""
Telegram授权脚本
用于首次授权Telegram API，生成session文件
"""

import asyncio
from telethon import TelegramClient

# Telegram API配置
API_ID = 21480897
API_HASH = '6100e61192b430089e66d047dc9d6bce'
SESSION_NAME = 'web3_alpha_hunter'

async def main():
    print('=' * 60)
    print('🔐 Telegram API 授权工具')
    print('=' * 60)
    print()
    print('📱 请准备好您的手机，准备接收Telegram验证码')
    print()
    print('授权步骤:')
    print('1. 输入手机号 (带国际区号，例如: +8613800138000)')
    print('2. Telegram会发送验证码到您的手机')
    print('3. 输入收到的验证码')
    print('4. (如果有两步验证) 输入密码')
    print()
    print('=' * 60)
    print()
    
    # 创建客户端
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        # 启动授权流程
        await client.start()
        
        print()
        print('=' * 60)
        print('✅ 授权成功！')
        print('=' * 60)
        print()
        print(f'💾 Session文件已保存: {SESSION_NAME}.session')
        print()
        print('现在您可以:')
        print('1. 重启Celery服务: cd .. && ./stop-celery.sh && ./start-celery.sh')
        print('2. Telegram采集器将自动开始工作')
        print()
        
        # 断开连接
        await client.disconnect()
        
    except Exception as e:
        print()
        print('=' * 60)
        print(f'❌ 授权失败: {e}')
        print('=' * 60)
        print()
        print('常见问题:')
        print('- 手机号格式: 必须带国际区号 (+86开头)')
        print('- 验证码: 检查Telegram消息')
        print('- 网络: 确保能访问Telegram服务器')
        print()

if __name__ == '__main__':
    asyncio.run(main())

