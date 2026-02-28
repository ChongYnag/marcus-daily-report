#!/usr/bin/env python3
"""
飞书通知模块 - 发送 Marcus 报告到飞书
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

class FeishuNotifier:
    """飞书机器人通知器"""
    
    def __init__(self, webhook_url):
        """
        初始化飞书通知器
        
        Args:
            webhook_url: 飞书机器人 webhook URL
        """
        self.webhook_url = webhook_url
    
    def send_text(self, content):
        """发送纯文本消息"""
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        return self._send(data)
    
    def send_post(self, title, content_lines):
        """发送 Post 消息（富文本）"""
        elements = []
        for line in content_lines:
            if line.startswith('###'):
                elements.append({
                    "tag": "hr"
                })
                elements.append({
                    "tag": "text",
                    "text": line.replace('###', '').strip(),
                    "text_style": {"bold": True}
                })
            else:
                elements.append({
                    "tag": "text",
                    "text": line + "\n"
                })
        
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [elements]
                    }
                }
            }
        }
        return self._send(data)
    
    def send_interactive(self, card):
        """发送交互式卡片消息"""
        data = {
            "msg_type": "interactive",
            "card": card
        }
        return self._send(data)
    
    def send_market_report(self, report_data):
        """
        发送市场报告（交互式卡片）
        
        Args:
            report_data: 报告数据字典
                - date: 日期
                - stance: 市场立场
                - reason: 理由
                - vix: VIX 指数
                - watchlist: 观察名单列表
                - risk_tips: 风险提示
        """
        # 根据立场设置颜色
        stance = report_data.get('stance', 'Conservative Buy')
        if 'Aggressive' in stance:
            template = "blue"
            emoji = '🟢'
        elif 'Hold' in stance:
            template = "red"
            emoji = '🔴'
        else:
            template = "yellow"
            emoji = '🟡'
        
        # 构建卡片
        card = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": template,
                "title": {
                    "tag": "plain_text",
                    "content": f"📈 Marcus 每日动量报告 | {report_data.get('date', 'N/A')}"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{emoji} 市场立场：{stance}**\n**理由：** {report_data.get('reason', 'N/A')}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**📊 VIX 指数：** {report_data.get('vix', 'N/A')}\n**📈 市场趋势：** {report_data.get('trend', 'N/A')}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": self._format_watchlist(report_data.get('watchlist', []))
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**⚠️ 风险提示**\n{report_data.get('risk_tips', 'N/A')}"
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
                            "content": f"📅 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 交易员：Marcus"
                        }
                    ]
                }
            ]
        }
        
        return self.send_interactive(card)
    
    def _format_watchlist(self, watchlist):
        """格式化观察名单"""
        if not watchlist:
            return "**📋 观察名单：** 暂无数据"
        
        lines = ["**📋 5% 观察名单：**"]
        for i, stock in enumerate(watchlist[:5], 1):
            symbol = stock.get('symbol', 'N/A')
            logic = stock.get('logic', 'N/A')
            entry = stock.get('entry', 'N/A')
            stop = stock.get('stop', 'N/A')
            prob = stock.get('probability', 'N/A')
            
            lines.append(f"{i}. **{symbol}** - {logic}")
            lines.append(f"   入场：{entry} | 止损：{stop} | 成功率：{prob}")
        
        return "\n".join(lines)
    
    def _send(self, data):
        """发送请求到飞书"""
        try:
            req = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('code') == 0 or result.get('StatusCode') == 0:
                    return {'success': True, 'message': '发送成功'}
                else:
                    return {'success': False, 'message': f"飞书返回错误：{result}"}
                    
        except urllib.error.HTTPError as e:
            return {'success': False, 'message': f"HTTP 错误：{e.code} - {e.reason}"}
        except Exception as e:
            return {'success': False, 'message': f"发送失败：{str(e)}"}


def send_report_to_feishu(webhook_url, report_text, report_data=None):
    """
    快捷函数：发送报告到飞书
    
    Args:
        webhook_url: 飞书 webhook URL
        report_text: 完整报告文本
        report_data: 结构化报告数据（可选）
    
    Returns:
        dict: 发送结果
    """
    notifier = FeishuNotifier(webhook_url)
    
    # 如果有结构化数据，发送交互式卡片
    if report_data:
        result = notifier.send_market_report(report_data)
    else:
        # 否则发送文本消息
        title = "📈 Marcus 每日动量报告"
        result = notifier.send_text(f"{title}\n\n{report_text[:2000]}")  # 限制长度
    
    return result


if __name__ == '__main__':
    # 测试示例
    print("飞书通知模块测试")
    print("使用方法：")
    print("1. 在飞书群中添加自定义机器人")
    print("2. 获取 webhook URL")
    print("3. 调用 send_report_to_feishu(webhook_url, report)")
