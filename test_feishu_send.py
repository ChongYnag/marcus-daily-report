#!/usr/bin/env python3
"""
测试发送 Marcus 报告到飞书（修复版）
"""

import json
import urllib.request
from datetime import datetime

# 加载配置
with open('feishu_config.json', 'r') as f:
    config = json.load(f)

webhook_url = config['webhook_url']

# 构建 Marcus 报告卡片
report_date = "2026-02-28 (演示测试)"
stance = "Conservative Buy"
reason = "VIX=18.5 中性，市场震荡格局"

# 构建交互式卡片（使用飞书支持的元素）
card = {
    "config": {
        "wide_screen_mode": True
    },
    "header": {
        "template": "yellow",
        "title": {
            "tag": "plain_text",
            "content": f"📈 Marcus 每日动量报告 | {report_date}"
        }
    },
    "elements": [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**🟡 市场立场：{stance}**\n**理由：** {reason}"
            }
        },
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**📊 VIX 指数：** {18.5}\n**📈 市场趋势：** +0.2%"
            }
        },
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": """**📋 5% 观察名单：**

1. **NVDA** - AI 芯片龙头
   入场：$145 | 止损：$138 | 成功率：68%

2. **TSLA** - 高 Beta 特性
   入场：$250 | 止损：$235 | 成功率：55%

3. **AMD** - 半导体复苏
   入场：$125 | 止损：$118 | 成功率：62%

4. **META** - 广告增长
   入场：$580 | 止损：$550 | 成功率：65%

5. **COIN** - 加密货币联动
   入场：BTC>$95K | 止损：-12% | 成功率：52%"""
            }
        },
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": """**⚠️ 风险提示**

• 仓位建议：30-50%
• 分散配置，不超过 3 支股票
• 单笔亏损 < 2%
• 关注 PCE 通胀数据发布"""
            }
        },
        {
            "tag": "hr"
        },
        {
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": f"🧪 测试消息 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Marcus"
                }
            ]
        }
    ]
}

# 发送请求
data = {
    "msg_type": "interactive",
    "card": card
}

print("🚀 正在发送 Marcus 报告到飞书...")
print(f"Webhook: {webhook_url[:50]}...")
print("")

try:
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        if result.get('code') == 0 or result.get('StatusCode') == 0:
            print("✅ 发送成功！")
            print("")
            print("请检查飞书群聊，应该能看到 Marcus 报告卡片。")
        else:
            print(f"❌ 发送失败：{result}")
            
except urllib.error.HTTPError as e:
    print(f"❌ HTTP 错误：{e.code} - {e.reason}")
    try:
        print(f"响应内容：{e.read().decode('utf-8')}")
    except:
        pass
except Exception as e:
    print(f"❌ 发送失败：{e}")
