#!/usr/bin/env python3
"""
测试 WildCard/GPTsAPI 配置
验证 OpenAI 和 Claude 的 API 连接
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_openai():
    """测试 OpenAI (通过 WildCard)"""
    print("\n" + "="*50)
    print("测试 OpenAI (via GPTsAPI/WildCard)")
    print("="*50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY 未设置")
        return False
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.gptsapi.net/v1"
        )
        
        print(f"✅ API Key: {api_key[:20]}...")
        print("📡 发送测试请求...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "请用一句话介绍什么是Web3"}
            ],
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f"✅ OpenAI 响应成功!")
        print(f"📝 回复: {result}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI 测试失败: {e}")
        return False


def test_claude():
    """测试 Claude (通过 WildCard,使用 OpenAI 格式)"""
    print("\n" + "="*50)
    print("测试 Claude (via GPTsAPI/WildCard)")
    print("="*50)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 未设置")
        return False
    
    try:
        # 注意: WildCard 的 Claude 也使用 OpenAI 客户端
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.gptsapi.net/v1"
        )
        
        print(f"✅ API Key: {api_key[:20]}...")
        print("📡 发送测试请求...")
        
        response = client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",  # WildCard 支持的 Claude 模型
            messages=[
                {"role": "user", "content": "请用一句话介绍什么是DeFi"}
            ],
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f"✅ Claude 响应成功!")
        print(f"📝 回复: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Claude 测试失败: {e}")
        return False


def test_ai_analyzer():
    """测试 AI 分析器"""
    print("\n" + "="*50)
    print("测试 AI 分析器")
    print("="*50)
    
    try:
        from app.services.analyzers.ai_analyzer import AIAnalyzer
        
        analyzer = AIAnalyzer()
        
        if not analyzer.active_provider:
            print("❌ 没有可用的 AI provider")
            return False
        
        print(f"✅ 激活的 provider: {analyzer.active_provider}")
        
        # 测试分析
        test_text = """
        新项目 AlphaSwap 刚刚宣布完成 500万美元种子轮融资,
        由 Paradigm 领投。该项目是一个跨链 DEX 聚合器,
        支持以太坊、Solana、BSC 等多条链。
        """
        
        print("📡 测试项目分析...")
        result = analyzer.analyze_project_text(test_text, "twitter")
        
        print(f"✅ 分析完成!")
        print(f"📊 项目类型: {result.get('category')}")
        print(f"💡 核心特点: {result.get('key_features')}")
        print(f"⭐ 评分: {result.get('score_estimate')}/10")
        return True
        
    except Exception as e:
        print(f"❌ AI 分析器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n🔧 WildCard/GPTsAPI 配置测试")
    print("=" * 60)
    
    results = []
    
    # 测试 OpenAI
    results.append(("OpenAI", test_openai()))
    
    # 测试 Claude
    results.append(("Claude", test_claude()))
    
    # 测试 AI 分析器
    results.append(("AI Analyzer", test_ai_analyzer()))
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{name:20s} : {status}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n🎉 所有测试通过! WildCard API 配置成功!")
    else:
        print("\n⚠️  部分测试失败,请检查配置")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())

