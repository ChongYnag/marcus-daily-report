# Marcus - 股票日报分析 Agent

## 📋 概述

Marcus 是一名拥有 15 年华尔街经验的量化日内交易策略师，每天自动生成《每日动量报告》。

**✨ 新功能：支持飞书通知！** 报告生成后自动发送到你的飞书群聊。

## 📁 文件结构

```
agents/marcus/
├── prompt.md              # Marcus 人设 prompt
├── marcus_enhanced.py     # 主程序（推荐）
├── marcus_daily.py        # 基础版报告脚本
├── marcus_report.py       # 完整版报告脚本（需 yfinance）
├── marcus_demo.py         # 演示版（生成完整示例）
├── feishu_notifier.py     # 飞书通知模块
├── feishu_config.json     # 飞书配置（需自行创建）
├── setup_feishu.sh        # 飞书配置向导
├── FEISHU_SETUP.md        # 飞书配置详细指南
├── run_marcus.sh          # 快速运行脚本
├── README.md              # 本文件
└── reports/               # 生成的报告存储目录
```

## 📬 配置飞书通知

### 快速配置（推荐）

运行配置向导：

```bash
cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus
./setup_feishu.sh
```

按照提示输入飞书 Webhook URL 即可！

### 手动配置

1. 在飞书群添加自定义机器人，获取 Webhook URL
2. 创建配置文件 `feishu_config.json`：

```json
{
  "enabled": true,
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK",
  "send_mode": "interactive"
}
```

详细说明请查看：**[FEISHU_SETUP.md](FEISHU_SETUP.md)**

---

## ⚙️ 配置自动运行

### 方法 1：使用 crontab（推荐）

在终端执行：

```bash
crontab -e
```

添加以下行（每个交易日早上 8:30 运行，美股开盘前）：

```cron
# Marcus 每日动量报告 + 飞书通知 - 交易日早上 8:30
30 8 * * 1-5 cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus && python3 marcus_enhanced.py >> /Users/jiangchongyang/.openclaw/workspace/agents/marcus/reports/cron.log 2>&1
```

**说明：**
- `1-5` 表示周一到周五
- 周末自动跳过（脚本内已处理）
- 日志保存在 `cron.log`
- 报告会自动发送到飞书（如果已配置）

### 方法 2：使用 OpenClaw Heartbeat

编辑 `HEARTBEAT.md`，添加：

```markdown
# Marcus 股票日报
- 交易日早上检查是否有新报告
- 如有新报告，发送到用户
```

### 方法 3：手动运行

```bash
cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus
python3 marcus_daily.py
```

## 📊 获取实时数据（可选）

当前版本使用模板数据。要获取实时市场数据：

### 安装 yfinance

```bash
pip3 install yfinance pandas
```

然后使用 `marcus_report.py` 替代 `marcus_daily.py`：

```bash
python3 marcus_report.py
```

### 或使用免费 API

1. **Alpha Vantage** (免费，需注册): https://www.alphavantage.co/support/#api-key
2. **Finnhub** (免费层级): https://finnhub.io/

获取 API Key 后，修改脚本中的数据来源。

## 📬 报告发送

### 配置消息发送

如果要自动发送报告到微信/Telegram/Email：

1. 修改脚本末尾，添加消息发送逻辑
2. 或使用 OpenClaw 的 `message` 工具

示例（添加到脚本末尾）：

```python
# 发送报告到 Telegram
subprocess.run([
    'openclaw', 'message', 'send',
    '--target', 'your_channel_id',
    '--message', report
])
```

## 📝 自定义股票池

编辑 `marcus_report.py` 中的 `MOMENTUM_STOCKS` 列表：

```python
MOMENTUM_STOCKS = [
    'NVDA', 'TSLA', 'AMD',  # 科技股
    'MRNA', 'BNTX',         # 生物科技
    'COIN', 'MARA',         # 加密货币相关
    # 添加你关注的股票...
]
```

## 🎯 使用建议

1. **报告仅供参考** - Marcus 的建议基于数据分析，不构成投资建议
2. **独立判断** - 交易前请自行确认市场状况
3. **风险控制** - 严格遵守止损纪律
4. **持续优化** - 根据你的交易风格调整参数

## 🔧 故障排除

### 报告未生成

```bash
# 检查 Python 版本
python3 --version

# 手动运行测试
cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus
python3 marcus_daily.py

# 查看日志
cat reports/cron.log
```

### crontab 不执行

```bash
# 检查 crontab 是否生效
crontab -l

# 检查 cron 服务状态
sudo systemctl status cron  # Linux
sudo launchctl list | grep cron  # macOS
```

---

**交易员：** Marcus  
**配置日期：** 2026-02-28  
**版本：** 1.0
