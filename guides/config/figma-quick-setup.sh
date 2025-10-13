#!/bin/bash

# Figma MCP Server 快速配置脚本
# 使用方法: ./figma-quick-setup.sh

set -e

echo "🎨 Figma MCP Server 快速配置工具"
echo "================================"
echo ""

# 检查是否已安装 figma-developer-mcp
if ! npm list figma-developer-mcp >/dev/null 2>&1; then
  echo "❌ 未检测到 figma-developer-mcp，正在安装..."
  npm install --save-dev figma-developer-mcp
  echo "✅ figma-developer-mcp 安装完成"
else
  echo "✅ figma-developer-mcp 已安装"
fi

echo ""

# 检查 .env.local 是否存在
if [ ! -f .env.local ]; then
  echo "📝 创建 .env.local 文件..."
  cp .env.local.example .env.local
  echo "✅ .env.local 文件已创建"
  echo ""
  echo "⚠️  请编辑 .env.local 文件，添加您的 Figma Access Token:"
  echo "   FIGMA_ACCESS_TOKEN=figd_your_token_here"
  echo ""
  echo "📖 获取 Token: https://www.figma.com/settings → Personal Access Tokens"
else
  echo "✅ .env.local 文件已存在"

  # 检查是否配置了 Token
  if grep -q "figd_your_token_here" .env.local 2>/dev/null; then
    echo "⚠️  请确保已在 .env.local 中配置真实的 Figma Token"
  elif grep -q "FIGMA_ACCESS_TOKEN=" .env.local 2>/dev/null; then
    echo "✅ Figma Token 已配置"
  else
    echo "⚠️  请在 .env.local 中添加 FIGMA_ACCESS_TOKEN"
  fi
fi

echo ""

# 检查 .mcp.json 是否存在
if [ ! -f .mcp.json ]; then
  echo "❌ 未找到 .mcp.json 配置文件"
  echo "   请参考 guides/config/FIGMA_MCP_SETUP.md 进行配置"
else
  echo "✅ .mcp.json 配置文件已存在"
fi

echo ""

# 检查 .cursorrules 是否存在
if [ ! -f .cursorrules ]; then
  echo "⚠️  未找到 .cursorrules 文件"
  echo "   建议创建此文件以优化代码生成质量"
else
  echo "✅ .cursorrules 文件已存在"
fi

echo ""
echo "================================"
echo "📚 配置完成！下一步:"
echo ""
echo "1. 获取 Figma Token:"
echo "   https://www.figma.com/settings"
echo ""
echo "2. 配置 Token 到 .env.local:"
echo "   FIGMA_ACCESS_TOKEN=figd_xxxxx"
echo ""
echo "3. 重启 Cursor 编辑器"
echo ""
echo "4. 在 Cursor 中测试:"
echo "   @figma 测试连接"
echo ""
echo "5. 查看完整文档:"
echo "   guides/config/FIGMA_MCP_SETUP.md"
echo "   guides/config/FIGMA_PROMPT_TEMPLATES.md"
echo ""
echo "🎉 祝使用愉快！"
