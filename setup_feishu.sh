#!/bin/bash
# Marcus 飞书通知快速配置脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📬 Marcus 飞书通知配置向导"
echo "================================"
echo ""

# 检查配置文件是否存在
if [ -f "feishu_config.json" ]; then
    echo "⚠️  检测到已存在的配置文件"
    echo ""
    read -p "是否覆盖现有配置？(y/N): " overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo "取消配置"
        exit 0
    fi
fi

echo ""
echo "请按照以下步骤获取飞书 Webhook URL："
echo ""
echo "1️⃣  打开飞书，进入要接收报告的群聊"
echo "2️⃣  点击右上角群设置 ⚙️"
echo "3️⃣  选择「群机器人」→「添加机器人」"
echo "4️⃣  选择「自定义机器人」"
echo "5️⃣  填写名称（如：Marcus 交易助手）"
echo "6️⃣  复制生成的 Webhook URL"
echo ""
echo "Webhook URL 格式："
echo "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
echo ""

read -p "请输入飞书 Webhook URL: " webhook_url

# 验证 URL 格式
if [[ ! "$webhook_url" =~ ^https://open\.feishu\.cn/open-apis/bot/v2/hook/ ]]; then
    echo ""
    echo "❌ URL 格式不正确！请确认是从飞书复制的 Webhook 地址"
    exit 1
fi

# 创建配置文件
cat > feishu_config.json << EOF
{
  "enabled": true,
  "webhook_url": "$webhook_url",
  "send_mode": "interactive",
  "notify_time": "08:30",
  "timezone": "Asia/Shanghai",
  "skip_weekends": true,
  "skip_holidays": false
}
EOF

echo ""
echo "✅ 配置文件已创建：feishu_config.json"
echo ""

# 测试发送
read -p "是否立即测试发送？(y/N): " test_now

if [[ "$test_now" =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 正在发送测试消息..."
    echo ""
    
    # 创建测试消息
    python3 -c "
import json
import urllib.request

with open('feishu_config.json', 'r') as f:
    config = json.load(f)

webhook_url = config['webhook_url']

# 发送测试消息
data = {
    'msg_type': 'text',
    'content': {
        'text': '🎉 Marcus 飞书通知测试成功！\\n\\n配置完成，每个交易日早上 8:30 自动接收《每日动量报告》。'
    }
}

req = urllib.request.Request(
    webhook_url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        if result.get('code') == 0 or result.get('StatusCode') == 0:
            print('✅ 测试消息发送成功！请在飞书中查看')
        else:
            print(f'❌ 发送失败：{result}')
except Exception as e:
    print(f'❌ 发送失败：{e}')
"
fi

echo ""
echo "================================"
echo "📋 下一步："
echo ""
echo "1. 在飞书群中查看测试消息"
echo "2. 设置定时任务（crontab）："
echo ""
echo "   crontab -e"
echo "   添加：30 8 * * 1-5 cd $SCRIPT_DIR && python3 marcus_enhanced.py >> reports/cron.log 2>&1"
echo ""
echo "3. 或手动运行测试："
echo "   python3 marcus_enhanced.py"
echo ""
echo "详细说明请查看：FEISHU_SETUP.md"
echo ""
