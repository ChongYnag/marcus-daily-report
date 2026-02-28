#!/bin/bash
# Marcus 每日动量报告 - 快速运行脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Marcus - 每日动量报告生成器"
echo "================================"
echo ""

# 检查是否是交易日
DAY=$(date +%A)
if [[ "$DAY" == "Saturday" || "$DAY" == "Sunday" ]]; then
    echo "⚠️  今天是周末，美股休市"
    echo ""
fi

# 运行报告生成
echo "📊 正在生成报告..."
python3 marcus_enhanced.py

# 显示报告路径
echo ""
echo "📁 报告已保存至：$SCRIPT_DIR/reports/"
ls -lt reports/ | head -5
