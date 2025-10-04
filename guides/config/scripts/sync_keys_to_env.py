#!/usr/bin/env python3
"""
从 YAML 配置文件同步 API keys 到 .env 文件
使用方法: python sync_keys_to_env.py
"""

import yaml
import os
from pathlib import Path


def load_yaml_keys(yaml_path: str) -> dict:
    """加载 YAML 配置文件"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def update_env_file(env_path: str, keys_config: dict):
    """更新 .env 文件中的 API keys"""
    
    # 读取现有的 .env 文件
    env_lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_lines = f.readlines()
    
    # 准备需要更新的环境变量映射
    env_updates = {}
    
    # AI服务密钥
    ai_services = keys_config.get('ai_services', {})
    if ai_services.get('openai', {}).get('api_key'):
        env_updates['OPENAI_API_KEY'] = ai_services['openai']['api_key']
    if ai_services.get('anthropic', {}).get('api_key'):
        env_updates['ANTHROPIC_API_KEY'] = ai_services['anthropic']['api_key']
    if ai_services.get('deepseek', {}).get('api_key'):
        env_updates['DEEPSEEK_API_KEY'] = ai_services['deepseek']['api_key']
    
    # 数据源API
    data_sources = keys_config.get('data_sources', {})
    if data_sources.get('twitter', {}):
        twitter = data_sources['twitter']
        if twitter.get('api_key'):
            env_updates['TWITTER_API_KEY'] = twitter['api_key']
        if twitter.get('api_secret'):
            env_updates['TWITTER_API_SECRET'] = twitter['api_secret']
        if twitter.get('bearer_token'):
            env_updates['TWITTER_BEARER_TOKEN'] = twitter['bearer_token']
        if twitter.get('access_token'):
            env_updates['TWITTER_ACCESS_TOKEN'] = twitter['access_token']
        if twitter.get('access_token_secret'):
            env_updates['TWITTER_ACCESS_TOKEN_SECRET'] = twitter['access_token_secret']
    
    if data_sources.get('telegram', {}):
        telegram = data_sources['telegram']
        if telegram.get('bot_token'):
            env_updates['TELEGRAM_BOT_TOKEN'] = telegram['bot_token']
        if telegram.get('api_id'):
            env_updates['TELEGRAM_API_ID'] = str(telegram['api_id'])
        if telegram.get('api_hash'):
            env_updates['TELEGRAM_API_HASH'] = telegram['api_hash']
    
    if data_sources.get('coingecko', {}).get('api_key'):
        env_updates['COINGECKO_API_KEY'] = data_sources['coingecko']['api_key']
    
    if data_sources.get('youtube', {}).get('api_key'):
        env_updates['YOUTUBE_API_KEY'] = data_sources['youtube']['api_key']
    
    # 云服务密钥
    cloud_services = keys_config.get('cloud_services', {})
    if cloud_services.get('cloudflare_r2', {}):
        r2 = cloud_services['cloudflare_r2']
        if r2.get('account_id'):
            env_updates['R2_ACCOUNT_ID'] = r2['account_id']
        if r2.get('access_key_id'):
            env_updates['R2_ACCESS_KEY_ID'] = r2['access_key_id']
        if r2.get('secret_access_key'):
            env_updates['R2_SECRET_ACCESS_KEY'] = r2['secret_access_key']
    
    # 监控服务
    monitoring = keys_config.get('monitoring', {})
    if monitoring.get('sentry', {}).get('dsn'):
        env_updates['SENTRY_DSN'] = monitoring['sentry']['dsn']
    if monitoring.get('logtail', {}).get('source_token'):
        env_updates['LOGTAIL_TOKEN'] = monitoring['logtail']['source_token']
    
    # 更新 .env 文件
    updated_lines = []
    updated_keys = set()
    
    for line in env_lines:
        stripped = line.strip()
        # 跳过注释和空行
        if not stripped or stripped.startswith('#'):
            updated_lines.append(line)
            continue
        
        # 解析环境变量
        if '=' in stripped:
            key = stripped.split('=')[0].strip()
            if key in env_updates:
                # 更新现有的key
                updated_lines.append(f"{key}={env_updates[key]}\n")
                updated_keys.add(key)
            else:
                # 保留其他行
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    
    # 添加新的keys (如果 .env 中不存在)
    if updated_keys != set(env_updates.keys()):
        updated_lines.append("\n# ===== 从 YAML 同步的新增配置 =====\n")
        for key, value in env_updates.items():
            if key not in updated_keys:
                updated_lines.append(f"{key}={value}\n")
    
    # 写回 .env 文件
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    print(f"✅ 已更新 {len(env_updates)} 个环境变量到 {env_path}")
    print(f"   更新的变量: {', '.join(env_updates.keys())}")


def main():
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # 文件路径
    yaml_path = project_root / "guides/config/keys/api-keys.yaml"
    env_path = project_root / "backend/.env"
    
    print("🔄 开始同步 API keys...")
    print(f"   YAML源: {yaml_path}")
    print(f"   目标ENV: {env_path}")
    
    # 检查文件是否存在
    if not yaml_path.exists():
        print(f"❌ 错误: YAML配置文件不存在: {yaml_path}")
        print("   请先创建配置文件:")
        print(f"   cp {yaml_path.parent}/api-keys.example.yaml {yaml_path}")
        return 1
    
    # 加载并同步
    try:
        keys_config = load_yaml_keys(str(yaml_path))
        update_env_file(str(env_path), keys_config)
        print("\n✅ 同步完成!")
        return 0
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

