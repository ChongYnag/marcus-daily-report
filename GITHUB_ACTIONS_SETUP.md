# 🚀 Marcus GitHub Actions 部署指南

## 概述

使用 GitHub Actions 免费运行 Marcus，**无需电脑开机**，24 小时自动发送报告！

**成本：** ¥0（GitHub 免费额度足够）  
**稳定性：** ⭐⭐⭐⭐⭐（GitHub 托管）  
**配置难度：** ⭐⭐（10 分钟搞定）

---

## 📋 配置步骤

### 步骤 1️⃣：创建 GitHub 仓库

1. **打开 GitHub**：https://github.com
2. **创建新仓库**：
   - 名称：`marcus-daily-report`（或你喜欢的名字）
   - 可见性：**Private**（私有，保护 Webhook）
   - 初始化：可以勾选 "Add a README file"
3. **点击 "Create repository"**

---

### 步骤 2️⃣：上传代码到 GitHub

#### 方法 A：使用 Git 命令行（推荐）

```bash
# 进入 Marcus 目录
cd /Users/jiangchongyang/.openclaw/workspace/agents/marcus

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Marcus daily report"

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/marcus-daily-report.git

# 推送
git push -u origin main
```

#### 方法 B：手动上传

1. 在 GitHub 仓库页面点击 "Add file" → "Upload files"
2. 拖入以下文件：
   - `send_feishu_github.py`
   - `.github/workflows/marcus_daily.yml`
   - `feishu_notifier.py`
   - `README.md`
3. 点击 "Commit changes"

---

### 步骤 3️⃣：配置 GitHub Secrets（重要！）

**保存飞书 Webhook URL（加密存储）**

1. **打开 GitHub 仓库** → 点击 **"Settings"**
2. **左侧菜单** → **"Secrets and variables"** → **"Actions"**
3. **点击 "New repository secret"**
4. **填写：**
   - **Name:** `FEISHU_WEBHOOK`
   - **Secret:** 粘贴你的飞书 Webhook URL
     ```
     https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-...
     ```
5. **点击 "Add secret"**

✅ 现在 Webhook 已安全存储，不会泄露！

---

### 步骤 4️⃣：测试运行

#### 手动触发测试

1. **在 GitHub 仓库页面** → 点击 **"Actions"** 标签
2. **左侧点击 "Marcus Daily Momentum Report"**
3. **点击 "Run workflow" 按钮**
4. **选择分支（main）** → 点击 "Run workflow"

#### 查看运行结果

```
✅ 绿色勾 = 成功
❌ 红色叉 = 失败（点击查看详情）
```

**如果成功：** 飞书会收到测试报告！

---

### 步骤 5️⃣：确认定时任务

**已配置的发送时间：**

```yaml
schedule:
  - cron: '0 23 * * 1-5'  # UTC 23:00 = 北京时间 07:00
```

**发送时间：**
- 周一到周五：早上 7:00（北京时间）
- 周末：自动跳过

---

## 📊 查看运行日志

### 在 GitHub 查看

1. **Actions** 标签 → 点击任意一次运行
2. **点击 "run-marcus"** 查看详细信息
3. **查看输出日志**

### 日志内容示例

```
🚀 Marcus 正在生成每日动量报告...

# 📈 Marcus 每日动量报告 | 2026-02-28
...

==================================================
✅ 飞书通知发送成功！

✅ 报告已生成并发送到飞书！
```

---

## 🔧 修改发送时间

编辑 `.github/workflows/marcus_daily.yml`：

### 常用时间配置

| 时间 | Cron 表达式 | 说明 |
|------|-----------|------|
| **07:00** | `0 23 * * 1-5` | 早上 7 点（当前配置） |
| **08:30** | `30 0 * * 1-5` | 早上 8:30 |
| **09:00** | `0 1 * * 1-5` | 早上 9 点 |
| **06:00** | `0 22 * * 1-5` | 早上 6 点 |

**Cron 格式说明：**
```
分 时 日 月 周
↑  ↑  ↑  ↑  ↑
|  |  |  |  └─ 星期 (0-6, 1=周一)
|  |  |  └──── 月份 (1-12)
|  |  └─────── 日期 (1-31)
|  └────────── 小时 (0-23, UTC 时间)
└───────────── 分钟 (0-59)
```

**修改后推送：**
```bash
git add .github/workflows/marcus_daily.yml
git commit -m "Update schedule to 8:30 AM"
git push
```

---

## 📬 同时支持本地 + GitHub

**可以两边都配置：**

- **本地 cron**：电脑开机时运行
- **GitHub Actions**：电脑关机时运行

**互不冲突，双重保障！**

---

## ⚠️ 注意事项

### 1. GitHub 免费额度

- **每月 2000 分钟** 免费额度
- Marcus 每次运行约 1-2 分钟
- 每月运行 22 天（交易日）× 2 分钟 = 44 分钟
- ✅ **完全够用！**

### 2. 代码隐私

- **建议用 Private 仓库**（保护 Webhook）
- Webhook 已加密存储在 Secrets
- 不会泄露到公开网络

### 3. 失败通知

可以配置失败时邮件通知：

```yaml
on:
  workflow_run:
    workflows: ["Marcus Daily Momentum Report"]
    types: [completed]

jobs:
  notify-failure:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - name: Send email
        uses: dawidd6/action-send-mail@v3
        with:
          to: your@email.com
          subject: Marcus 运行失败
          body: 请检查 GitHub Actions 日志
```

---

## 🔍 故障排查

### 问题 1：Workflow 不运行

**检查：**
```bash
# 确认 cron 表达式正确
cat .github/workflows/marcus_daily.yml
```

**GitHub Actions 可能延迟：**
- GitHub 调度可能有 1-5 分钟延迟
- 属于正常现象

### 问题 2：发送失败

**查看日志：**
1. Actions → 点击失败的运行
2. 查看错误信息

**常见原因：**
- ❌ 未配置 `FEISHU_WEBHOOK` Secret
- ❌ Webhook URL 错误
- ❌ 飞书机器人权限问题

### 问题 3：想重新运行

**手动触发：**
1. Actions → Marcus Daily Momentum Report
2. 点击 "Run workflow"

---

## 💡 进阶用法

### 1. 添加更多市场数据

可以集成免费 API：
- Alpha Vantage（免费）
- Yahoo Finance（通过 `yfinance`）
- Finnhub（免费层级）

### 2. 发送详细报告

修改 `send_feishu_github.py` 生成更详细的分析

### 3. 多群发送

配置多个 Webhook，同时发送到多个群

### 4. 添加错误通知

失败时发送通知给你

---

## 📞 需要帮助？

**遇到问题可以：**

1. 查看 GitHub Actions 日志
2. 检查 Secrets 配置
3. 手动触发测试
4. 查看飞书机器人状态

---

## ✅ 配置完成清单

- [ ] 创建 GitHub 仓库
- [ ] 上传代码
- [ ] 配置 `FEISHU_WEBHOOK` Secret
- [ ] 手动测试运行
- [ ] 确认飞书收到消息
- [ ] 等待下周一自动运行

---

**配置完成后，Marcus 将 24 小时在线，电脑关机也能发送报告！** 🎉

**下次运行时间：** 下周一 07:00（北京时间）
