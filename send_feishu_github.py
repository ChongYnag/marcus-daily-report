#!/usr/bin/env python3
"""
Marcus - GitHub Actions 版本
发送飞书通知（从环境变量读取 Webhook）
"""

import json
import urllib.request
import os
from datetime import datetime

def generate_report():
    """生成 Marcus 报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    weekday = datetime.now().strftime('%A')
    
    # 周末检查（可以通过环境变量跳过，用于测试）
    skip_weekend = os.environ.get('SKIP_WEEKEND', 'true').lower() == 'true'
    if weekday in ['Saturday', 'Sunday'] and skip_weekend:
        return None, "周末休市"
    
    # 如果是周末但不跳过（测试模式），添加标记
    if weekday in ['Saturday', 'Sunday']:
        today += " (周末测试)"
    
    # 市场数据（简化版，实际可接入 API）
    vix = 18.5
    trend = "+0.2%"
    stance = "Conservative Buy"
    reason = "VIX=18.5 中性，市场震荡格局"
    
    # 观察名单
    watchlist = [
        {"symbol": "NVDA", "logic": "AI 芯片龙头", "entry": "$145", "stop": "$138", "prob": "68%"},
        {"symbol": "TSLA", "logic": "高 Beta 特性", "entry": "$250", "stop": "$235", "prob": "55%"},
        {"symbol": "AMD", "logic": "半导体复苏", "entry": "$125", "stop": "$118", "prob": "62%"},
        {"symbol": "META", "logic": "广告增长", "entry": "$580", "stop": "$550", "prob": "65%"},
        {"symbol": "COIN", "logic": "加密货币联动", "entry": "BTC>$95K", "stop": "-12%", "prob": "52%"},
    ]
    
    # 构建飞书卡片
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "yellow",
            "title": {
                "tag": "plain_text",
                "content": f"📈 Marcus 每日动量报告 | {today}"
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
                    "content": f"**📊 VIX 指数：** {vix}\n**📈 市场趋势：** {trend}"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**📋 5% 观察名单：**\n\n" + 
                    "\n".join([
                        f"{i}. **{s['symbol']}** - {s['logic']}\n   入场：{s['entry']} | 止损：{s['stop']} | 成功率：{s['prob']}"
                        for i, s in enumerate(watchlist, 1)
                    ])
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": """**⚠️ 风险提示**

• 仓位建议：30-50%
• 分散配置，不超过 3 支股票
• 单笔亏损 < 2%"""
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
                        "content": f"🤖 GitHub Actions 自动发送 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Marcus"
                    }
                ]
            }
        ]
    }
    
    report_text = f"""# 📈 Marcus 每日动量报告 | {today}

## 市场立场：{stance}
{reason}

## 5% 观察名单
- NVDA: AI 芯片龙头，入场${145}, 止损${138}
- TSLA: 高 Beta 特性，入场${250}, 止损${235}
- AMD: 半导体复苏，入场${125}, 止损${118}
- META: 广告增长，入场${580}, 止损${550}
- COIN: 加密货币联动，BTC>$95K 介入

## 风险提示
仓位建议：30-50%，单笔亏损<2%
"""
    
    # 保存报告
    os.makedirs('reports', exist_ok=True)
    with open(f'reports/{today}_report.md', 'w') as f:
        f.write(report_text)
    
    return card, report_text


def send_to_feishu(card):
    """发送报告到飞书"""
    webhook_url = os.environ.get('FEISHU_WEBHOOK')
    
    if not webhook_url:
        print("❌ 错误：未配置 FEISHU_WEBHOOK 环境变量")
        print("请在 GitHub Secrets 中配置 FEISHU_WEBHOOK")
        return False
    
    data = {
        "msg_type": "interactive",
        "card": card
    }
    
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
                print("✅ 飞书通知发送成功！")
                return True
            else:
                print(f"❌ 发送失败：{result}")
                return False
                
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False


if __name__ == '__main__':
    print("🚀 Marcus 正在生成每日动量报告...")
    print("")
    
    card, report_text = generate_report()
    
    if card is None:
        print(f"ℹ️  {report_text}，跳过发送")
        exit(0)
    
    print(report_text)
    print("")
    print("="*50)
    
    success = send_to_feishu(card)
    
    if success:
        print("")
        print("✅ 报告已生成并发送到飞书！")
        exit(0)
    else:
        print("")
        print("❌ 发送失败，请检查配置")
        exit(1)
