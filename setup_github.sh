#!/bin/bash
# Marcus GitHub Actions 快速配置脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Marcus GitHub Actions 配置向导"
echo "=================================="
echo ""

# 检查是否已安装 Git
if ! command -v git &> /dev/null; then
    echo "❌ 未检测到 Git，请先安装 Git"
    echo "   安装：brew install git"
    exit 1
fi

# 检查是否已初始化 Git
if [ ! -d ".git" ]; then
    echo "📂 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit: Marcus daily report"
    echo "✅ Git 仓库已初始化"
    echo ""
fi

# 显示配置说明
echo "📋 接下来需要你在 GitHub 上操作："
echo ""
echo "1️⃣  打开 GitHub：https://github.com"
echo "2️⃣  创建新仓库（Private）："
echo "    名称：marcus-daily-report"
echo "3️⃣  复制仓库地址，格式："
echo "    https://github.com/YOUR_USERNAME/marcus-daily-report.git"
echo ""

read -p "请输入 GitHub 仓库地址: " repo_url

# 验证 URL 格式
if [[ ! "$repo_url" =~ ^https://github\.com/ ]]; then
    echo ""
    echo "❌ URL 格式不正确！"
    exit 1
fi

# 添加远程仓库
echo ""
echo "🔗 添加远程仓库..."
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
echo "✅ 远程仓库已配置：$repo_url"
echo ""

# 推送代码
echo "📤 推送代码到 GitHub..."
git branch -M main 2>/dev/null
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功！"
else
    echo "⚠️  推送失败，可能需要认证"
    echo ""
    echo "请使用以下命令手动推送："
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "=================================="
echo "📬 下一步：配置 GitHub Secrets"
echo ""
echo "1. 打开仓库页面：$repo_url"
echo "2. 点击 Settings → Secrets and variables → Actions"
echo "3. 点击 New repository secret"
echo "4. 添加："
echo "   Name: FEISHU_WEBHOOK"
echo "   Secret: [你的飞书 Webhook URL]"
echo ""
echo "5. 回到 Actions 标签，手动触发一次测试"
echo ""
echo "详细步骤请查看：GITHUB_ACTIONS_SETUP.md"
echo ""
echo "=================================="
echo ""
echo "✅ GitHub Actions 配置完成！"
echo ""
echo "📅 自动发送时间：周一到周五 07:00（北京时间）"
echo "🎯 下次运行：下周一早上 7 点"
echo ""
