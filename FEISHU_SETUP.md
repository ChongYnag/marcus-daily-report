# 📬 Marcus 飞书通知配置指南

## 快速开始

### 步骤 1️⃣：在飞书群添加机器人

1. **打开飞书**，进入你想接收报告的群聊（或创建新群）

2. **添加自定义机器人**：
   - 点击右上角群设置 ⚙️
   - 选择「群机器人」
   - 点击「添加机器人」
   - 选择「自定义机器人」

3. **配置机器人**：
   - 名称：`Marcus 交易助手`（或你喜欢的名字）
   - 头像：可以上传一个 📈 或 🤖 的图标
   - **勾选「发送消息」**权限
   - 点击「完成」

4. **获取 Webhook URL**：
   - 添加成功后，会显示一个 Webhook 地址
   - 格式：`https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - **复制这个 URL**，后面要用

---

### 步骤 2️⃣：配置 Marcus

1. **复制配置文件**：
   ```bash
   cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus
   cp feishu_config.example.json feishu_config.json
   ```

2. **编辑配置文件**：
   ```bash
   # 用你喜欢的编辑器打开
   code feishu_config.json
   # 或
   vim feishu_config.json
   # 或
   open -a TextEdit feishu_config.json
   ```

3. **填入 Webhook URL**：
   ```json
   {
     "enabled": true,
     "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的_WEBHOOK_地址",
     "send_mode": "interactive",
     "notify_time": "08:30",
     "timezone": "Asia/Shanghai",
     "skip_weekends": true,
     "skip_holidays": false
   }
   ```

   **替换 `你的_WEBHOOK_地址` 为步骤 1 中复制的 URL**

4. **保存文件**

---

### 步骤 3️⃣：测试发送

运行测试命令：

```bash
cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus
python3 marcus_enhanced.py
```

如果配置正确，你会看到：

```
🚀 Marcus 正在生成每日动量报告...

[报告内容...]

✅ 报告已保存至：reports/2026-02-28_report.md

==================================================
📬 正在发送飞书通知...
✅ 飞书通知发送成功！
```

然后在飞书群里应该能看到 Marcus 发送的报告！🎉

---

## 📋 配置选项说明

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用飞书通知 |
| `webhook_url` | string | 必填 | 飞书机器人 Webhook URL |
| `send_mode` | string | `"interactive"` | 消息格式：`interactive`(卡片) / `text`(文本) |
| `notify_time` | string | `"08:30"` | 计划发送时间（配合 cron 使用） |
| `timezone` | string | `"Asia/Shanghai"` | 时区设置 |
| `skip_weekends` | boolean | `true` | 是否跳过周末 |
| `skip_holidays` | boolean | `false` | 是否跳过节假日 |

---

## ⚙️ 设置自动发送

### 方法 1：使用 crontab（推荐）

```bash
crontab -e
```

添加以下内容（每个交易日早上 8:30）：

```cron
# Marcus 股票日报 + 飞书通知 - 交易日早上 8:30
30 8 * * 1-5 cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus && python3 marcus_enhanced.py >> reports/cron.log 2>&1
```

**说明：**
- `1-5` = 周一到周五
- 周末自动跳过（脚本内已处理）
- 日志保存在 `reports/cron.log`

---

### 方法 2：使用 OpenClaw 心跳

编辑 `HEARTBEAT.md`：

```markdown
# Marcus 股票日报
- 交易日早上 8:30 检查并发送报告
- 检查飞书通知是否成功
```

---

## 🔧 故障排查

### 问题 1：飞书没收到消息

**检查 Webhook URL 是否正确**：
```bash
cat feishu_config.json | grep webhook_url
```

**测试 Webhook**：
```bash
curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"测试消息"}}'
```

### 问题 2：提示模块导入错误

确保 `feishu_notifier.py` 在同一目录：
```bash
ls -la /Users/jiangchongyang/.openclaw/workspace/agents/marcus/feishu_notifier.py
```

### 问题 3：消息格式不对

检查 `send_mode` 配置：
- `interactive` = 精美卡片（推荐）
- `text` = 纯文本

---

## 🎨 消息样式预览

### 交互式卡片模式（推荐）

```
┌─────────────────────────────────────────┐
│ 📈 Marcus 每日动量报告 | 2026-02-28    │
├─────────────────────────────────────────┤
│ 🟡 市场立场：Conservative Buy          │
│                                         │
│ 理由：VIX=18.5 中性，震荡格局          │
├─────────────────────────────────────────┤
│ 📊 VIX 指数：18.5                       │
│ 📈 市场趋势：+0.2%                      │
├─────────────────────────────────────────┤
│ 📋 5% 观察名单：                        │
│ 1. NVDA - AI 芯片龙头                   │
│    入场：$145 | 止损：$138 | 68%       │
│ 2. TSLA - 高波动性                      │
│    ...                                  │
├─────────────────────────────────────────┤
│ ⚠️ 风险提示                             │
│ - 仓位建议：30-50%                      │
│ - 关注 PCE 数据发布                     │
├─────────────────────────────────────────┤
│ 📅 生成时间：2026-02-28 08:30:00       │
│ 交易员：Marcus                          │
└─────────────────────────────────────────┘
```

---

## 📱 手机端效果

飞书 App 会显示：

1. **推送通知**：「Marcus 每日动量报告」
2. **卡片消息**：点击可展开完整内容
3. **快速预览**：市场立场 + VIX 指数

---

## 🔒 安全提示

- ⚠️ **不要分享 Webhook URL** - 任何人拿到都能往群里发消息
- ⚠️ **不要提交到 Git** - `feishu_config.json` 已加入 `.gitignore`
- ✅ **定期检查** - 确保机器人权限正常

---

## 💡 进阶用法

### 多个群接收

创建多个配置文件：
```bash
feishu_config_team.json    # 团队群
feishu_config_personal.json # 个人群
```

修改脚本加载多个配置即可。

### 不同报告类型

可以配置不同时间发送不同内容：
- 早上 8:30 - 盘前报告
- 中午 12:00 - 午间更新
- 下午 4:00 - 收盘总结

---

## 📞 需要帮助？

遇到问题可以：
1. 查看日志：`cat reports/cron.log`
2. 手动测试：`python3 marcus_enhanced.py`
3. 检查飞书机器人状态

---

**配置完成后，每个交易日早上都能自动收到 Marcus 的报告！** 🚀
