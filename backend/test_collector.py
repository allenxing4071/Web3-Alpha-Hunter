"""快速测试数据采集器"""
import asyncio
from app.services.collectors.test_collector import mock_twitter_collector, mock_telegram_collector

print("=== Testing Twitter Collector ===")
twitter_projects = mock_twitter_collector.collect_and_extract(hours=24)
print(f"\n✅ Found {len(twitter_projects)} Twitter projects")
for p in twitter_projects:
    print(f"  - {p['author']['username']}: {p['text'][:80]}...")

print("\n=== Testing Telegram Collector ===")
telegram_projects = asyncio.run(mock_telegram_collector.collect_and_extract(hours=24))
print(f"\n✅ Found {len(telegram_projects)} Telegram projects")
for p in telegram_projects:
    print(f"  - {p['source_channel']}: {p['text'][:80]}...")

print(f"\n🎉 Total: {len(twitter_projects) + len(telegram_projects)} projects discovered!")
