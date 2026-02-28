#!/usr/bin/env python3
"""
Marcus - 每日动量报告生成器
获取市场数据并生成交易日志
"""

import json
import requests
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

# 配置
MARKET_DATA = {
    '^VIX': 'VIX 恐慌指数',
    '^GSPC': '标普 500',
    '^NDX': '纳斯达克 100',
    '^DJI': '道琼斯',
    'SPY': '标普 ETF',
    'QQQ': '纳指 ETF',
}

# 动量股票池（可根据需要调整）
MOMENTUM_STOCKS = [
    'NVDA', 'TSLA', 'AMD', 'AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN',
    'NFLX', 'COIN', 'PLTR', 'SMCI', 'AVGO', 'CRM', 'ORCL',
    'MRNA', 'BNTX', 'REGN', 'VRTX', 'GILD',
]

def get_market_sentiment():
    """获取市场情绪指标"""
    try:
        vix = yf.Ticker('^VIX')
        vix_data = vix.history(period='5d')
        current_vix = vix_data['Close'].iloc[-1]
        vix_change = ((current_vix - vix_data['Close'].iloc[0]) / vix_data['Close'].iloc[0]) * 100
        
        spy = yf.Ticker('SPY')
        spy_data = spy.history(period='5d')
        spy_change = ((spy_data['Close'].iloc[-1] - spy_data['Close'].iloc[0]) / spy_data['Close'].iloc[0]) * 100
        
        return {
            'vix': current_vix,
            'vix_change': vix_change,
            'spy_change': spy_change,
        }
    except Exception as e:
        return {'error': str(e)}

def determine_market_stance(sentiment):
    """根据市场情绪决定立场"""
    if 'error' in sentiment:
        return 'Hold/Cash', '数据获取失败，建议观望'
    
    vix = sentiment['vix']
    vix_change = sentiment['vix_change']
    spy_change = sentiment['spy_change']
    
    # VIX < 15 且市场上涨 -> 激进
    if vix < 15 and spy_change > 0.5:
        return 'Aggressive Buy', f'VIX={vix:.1f}(-{abs(vix_change):.1f}%) 低波动，SPY +{spy_change:.1f}% 放量上涨'
    # VIX > 25 或市场大跌 -> 观望
    elif vix > 25 or spy_change < -1:
        return 'Hold/Cash', f'VIX={vix:.1f}(+{vix_change:.1f}%) 高波动，SPY {spy_change:.1f}% 风险偏高'
    # 其他情况 -> 保守
    else:
        return 'Conservative Buy', f'VIX={vix:.1f} 中性，SPY {spy_change:.1f}% 震荡格局'

def analyze_stock(symbol):
    """分析单支股票"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1mo')
        
        if len(data) < 5:
            return None
        
        current = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        daily_change = ((current - prev_close) / prev_close) * 100
        
        # 计算动量指标
        ma5 = data['Close'].iloc[-5:].mean()
        ma20 = data['Close'].iloc[-20:].mean() if len(data) >= 20 else ma5
        
        volume = data['Volume'].iloc[-1]
        avg_volume = data['Volume'].iloc[-10:].mean()
        volume_ratio = volume / avg_volume if avg_volume > 0 else 1
        
        # 简单评分
        score = 0
        if daily_change > 2: score += 2
        if daily_change > 0: score += 1
        if current > ma5: score += 1
        if current > ma20: score += 1
        if volume_ratio > 1.5: score += 2
        
        return {
            'symbol': symbol,
            'price': current,
            'change': daily_change,
            'volume_ratio': volume_ratio,
            'score': score,
            'ma5': ma5,
            'ma20': ma20,
        }
    except Exception as e:
        return None

def generate_watchlist():
    """生成 5 支观察股票"""
    results = []
    for symbol in MOMENTUM_STOCKS:
        data = analyze_stock(symbol)
        if data and data['score'] >= 3:
            results.append(data)
    
    # 按评分排序，取前 5
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:5]

def generate_report():
    """生成完整报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 获取市场情绪
    sentiment = get_market_sentiment()
    stance, reason = determine_market_stance(sentiment)
    
    # 生成观察名单
    watchlist = generate_watchlist()
    
    # 构建报告
    report = f"""# 📈 每日动量报告 | Daily Momentum Report
**日期：** {today}
**交易员：** Marcus

---

## 1️⃣ Marcus 的市场立场

**{stance}**

**理由：** {reason}

---

## 2️⃣ 5% 观察名单

"""
    
    if watchlist:
        report += "| 股票代码 | 当前价 | 日涨跌 | 成交量比 | 入场条件 | 止损 | 成功概率 |\n"
        report += "|---------|-------|-------|---------|---------|------|---------|\n"
        
        for stock in watchlist:
            entry = stock['ma5'] * 1.01  # 突破 5 日线 1%
            stop = stock['ma5'] * 0.97   # 跌破 5 日线 3%
            prob = min(55 + stock['score'] * 5, 85)  # 基础 55% + 评分加成
            
            report += f"| {stock['symbol']} | ${stock['price']:.2f} | {stock['change']:+.1f}% | {stock['volume_ratio']:.1f}x | 突破 ${entry:.2f} | <${stop:.2f} | {prob}% |\n"
    else:
        report += "*今日市场动量不足，建议观望或降低选股标准*\n"
    
    # 风险提示
    report += f"""
---

## 3️⃣ 风险提示

**仓位建议：**
"""
    
    if stance == 'Aggressive Buy':
        report += "- 可使用 70-80% 仓位，集中参与高确定性机会\n"
    elif stance == 'Conservative Buy':
        report += "- 建议使用 30-50% 仓位，分散配置，严格止损\n"
    else:
        report += "- 建议现金为主（<20% 仓位），等待明确信号\n"
    
    report += f"""
**主要风险点：**
- VIX 当前 {sentiment.get('vix', 'N/A'):.1f}，"""
    
    if sentiment.get('vix', 20) > 20:
        report += "波动率偏高，注意仓位控制\n"
    else:
        report += "波动率正常，可适度参与\n"
    
    report += "- 单支股票仓位不超过总资金的 20%\n"
    report += "- 严格执行止损，亏损不超过总资金 2%\n"
    report += "- 财报季注意个股黑天鹅事件\n"
    
    report += f"""
---

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据来源：Yahoo Finance*
"""
    
    return report

if __name__ == '__main__':
    report = generate_report()
    print(report)
    
    # 保存到文件
    today = datetime.now().strftime('%Y-%m-%d')
    with open(f'/Users/jiangchongyang/.openclaw/workspace/agents/marcus/reports/{today}_report.md', 'w') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存至 reports/{today}_report.md")
