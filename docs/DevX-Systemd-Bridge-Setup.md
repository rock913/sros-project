# DevX-Systemd-Bridge-Setup — 手动配置指南

> 目标：部署飞书桥接 systemd 服务 (`lark-channel-bridge`) + 配置 Tmux 别名 (`cauto` / `cdo`)
> 阻塞原因：systemd 服务安装 + 飞书 Bot 凭证配置需要用户手动操作（含飞书开放平台后台配置）
> 预计耗时：30 分钟（含飞书 Bot 创建）

## 架构概览

```
飞书群聊 ──Webhook──▶ lark-channel-bridge (systemd) ──stdin──▶ claude -p (headless)
                          │                                          │
                          │ 监听飞书 @消息                            │ 执行任务
                          │ 按会话隔离上下文                           │ 返回纯文本
                          │                                          │
                          ◀────────── 轮询结果 ──────────────────────┘
                          │
                          ▼
飞书群聊 ◀──Webhook── 回复消息（含代码块/文件链接）
```

- **交互式通道 (Tmux)**：`cauto` — 完整 Claude Code 对话界面，用于深度开发
- **非交互式通道 (飞书)**：`cdo` — 无头模式，飞书 @机器人 触发碎片化异步任务

## 前置条件

### 1. 飞书开放平台 — 创建 Bot 应用

1. 打开 [飞书开放平台](https://open.feishu.cn/app) 并登录
2. 点击 **创建企业自建应用**（或 **创建应用** → **企业自建应用**）
3. 填写应用名称：`SROS DevX Bridge`（或你喜欢的名字）
4. 创建完成后进入应用详情页，记录以下凭证：

| 凭证 | 位置 | 用途 |
|------|------|------|
| **App ID** | 应用详情 → 凭证与基础信息 | 飞书 API 身份标识 |
| **App Secret** | 应用详情 → 凭证与基础信息 | 飞书 API 密钥（需点击"查看"获取） |
| **Verification Token** | 事件订阅 → 加密策略 | 事件回调验签（可选，如用长轮询则不需要） |

5. **添加应用能力**（左侧边栏）：
   - ✅ **机器人** — 开启并配置默认回复（可先留空）
   - ✅ **读取群消息** — `im:message` 权限
   - ✅ **获取群信息** — `im:chat` 权限
   - ✅ **发送群消息** — `im:message:send_as_bot` 权限
   - ✅ **获取用户信息** — `contact:user` 权限（可选，用于 @ 识别）
6. 点击 **创建版本** → **申请线上发布**（需要管理员审批）
7. 审批通过后，在目标飞书群中添加该 Bot：群设置 → 群机器人 → 添加机器人

### 2. 系统依赖安装

```bash
# Python 3.10+
python3 --version

# 飞书 SDK
pip install lark-oapi

# Tmux（通常已安装）
sudo apt-get install -y tmux

# jq（JSON 解析）
sudo apt-get install -y jq
```

## Step 1 — 创建桥接脚本

将以下脚本保存为 `/home/hyf/bin/lark-channel-bridge`：

```bash
sudo mkdir -p /home/hyf/bin
```

然后创建脚本文件 `/home/hyf/bin/lark-channel-bridge`：

```python
#!/usr/bin/env python3
"""
lark-channel-bridge — 飞书群聊 ↔ Claude Code 桥接服务

监听飞书群中 @机器人 的消息，转发给 claude -p 执行，将结果回复到群聊。
每个群聊会话独立维护上下文（通过 chat_id 隔离临时工作目录）。

环境变量：
  LARK_APP_ID          — 飞书应用 App ID
  LARK_APP_SECRET      — 飞书应用 App Secret
  CLAUDE_WORKSPACE     — Claude 执行的工作根目录（默认 ~/AI4S_Workspace）
  POLL_INTERVAL        — 轮询间隔秒数（默认 5）
"""

import os
import sys
import json
import time
import subprocess
import logging
import tempfile
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [lark-bridge] %(levelname)s: %(message)s",
)
logger = logging.getLogger("lark-bridge")

# ── Config ──────────────────────────────────────────────
APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
WORKSPACE = Path(os.environ.get("CLAUDE_WORKSPACE", os.path.expanduser("~/AI4S_Workspace")))
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))

# Per-chat working directories (sandboxed under /tmp/lark-sessions/<chat_hash>)
SESSIONS_DIR = Path("/tmp/lark-sessions")


def get_client() -> lark.Client:
    return (lark.Client.builder()
            .app_id(APP_ID)
            .app_secret(APP_SECRET)
            .log_level(lark.LogLevel.INFO)
            .build())


def get_chat_workspace(chat_id: str) -> Path:
    """每个群聊独立工作目录，避免上下文污染"""
    chat_hash = hashlib.sha256(chat_id.encode()).hexdigest()[:12]
    workspace = SESSIONS_DIR / chat_hash
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


def list_unread_messages(client: lark.Client) -> list[dict]:
    """拉取未读消息列表（简化版：轮询最近消息）"""
    # 注意：飞书服务端 API 需要先获取 chat list，再逐 chat 拉消息
    # 这里用简化逻辑：列出所有群，拉每个群最近一条消息
    messages = []
    try:
        req = ListChatRequest.builder().page_size(50).build()
        resp = client.im.v1.chat.list(req)
        if not resp.success():
            logger.error(f"List chats failed: {resp.msg}")
            return messages

        for chat in resp.data.items:
            # 跳过非群聊
            if hasattr(chat, "chat_type") and chat.chat_type != "group":
                continue

            # 拉最近消息
            msg_req = (ListMessageRequest.builder()
                       .container_id_type("chat")
                       .container_id(chat.chat_id)
                       .page_size(5)
                       .sort_type("ByCreateTimeDesc")
                       .build())
            msg_resp = client.im.v1.message.list(msg_req)
            if not msg_resp.success():
                continue

            for msg in msg_resp.data.items:
                if not hasattr(msg, "msg_type") or msg.msg_type != "text":
                    continue
                # 解析消息内容，提取 @ 提及
                content = json.loads(msg.content) if msg.content else {}
                text = content.get("text", "")
                if not text:
                    continue
                messages.append({
                    "message_id": msg.message_id,
                    "chat_id": chat.chat_id,
                    "text": text,
                    "sender": getattr(msg, "sender", {}),
                    "create_time": msg.create_time,
                })

    except Exception as e:
        logger.error(f"Error listing messages: {e}")

    return messages


def reply_to_message(client: lark.Client, message_id: str, content: str):
    """回复消息到飞书群"""
    reply_content = json.dumps({"text": content})
    req = (ReplyMessageRequest.builder()
           .message_id(message_id)
           .request_body(
               ReplyMessageRequestBody.builder()
               .content(reply_content)
               .msg_type("text")
               .build())
           .build())
    resp = client.im.v1.message.reply(req)
    if not resp.success():
        # 降级：直接发送新消息到群
        logger.warning(f"Reply failed: {resp.msg}, trying send")
        send_to_chat(client, message_id, content)


def send_to_chat(client: lark.Client, chat_id: str, content: str):
    """发送新消息到群聊"""
    msg_content = json.dumps({"text": content})
    req = (CreateMessageRequest.builder()
           .receive_id_type("chat_id")
           .request_body(
               CreateMessageRequestBody.builder()
               .receive_id(chat_id)
               .msg_type("text")
               .content(msg_content)
               .build())
           .build())
    resp = client.im.v1.message.create(req)
    if not resp.success():
        logger.error(f"Send failed: {resp.msg}")


def process_message(client: lark.Client, msg: dict, processed_ids: set):
    """处理单条消息：交给 Claude 执行，回复结果"""
    if msg["message_id"] in processed_ids:
        return

    text = msg["text"]
    # 去除 @机器人 前缀（简化：取第一个空格后的内容作为 prompt）
    # 飞书 @mention 格式：@_user_1 或 @机器人名称
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        prompt = text  # 整个消息作为 prompt
    else:
        prompt = parts[1] if parts[0].startswith("@") else text

    if not prompt.strip():
        return

    # 简单去重：跳过命令类短消息
    if len(prompt.strip()) < 2:
        return

    logger.info(f"Processing [{msg['chat_id'][:8]}...]: {prompt[:100]}")

    # 在独立 workspace 中执行 claude
    workspace = get_chat_workspace(msg["chat_id"])

    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=300,  # 5 分钟超时
            cwd=str(workspace),
            env={
                **os.environ,
                "HOME": os.environ.get("HOME", "/home/hyf"),
            },
        )

        if result.returncode == 0:
            response = result.stdout.strip()
        else:
            response = f"[错误] claude 返回码 {result.returncode}\n{result.stderr[:500]}"

        # 飞书消息 20000 字符截断
        if len(response) > 18000:
            response = response[:18000] + "\n\n... [消息过长，已截断]"

        reply_to_message(client, msg["message_id"], response)
        logger.info(f"Replied to {msg['message_id'][:8]}... ({len(response)} chars)")

    except subprocess.TimeoutExpired:
        reply_to_message(client, msg["message_id"], "[超时] 任务执行超过 5 分钟，已终止")
    except Exception as e:
        logger.error(f"Process error: {e}")
        reply_to_message(client, msg["message_id"], f"[错误] {str(e)[:500]}")

    processed_ids.add(msg["message_id"])


def main():
    if not APP_ID or not APP_SECRET:
        logger.fatal("LARK_APP_ID and LARK_APP_SECRET must be set")
        sys.exit(1)

    client = get_client()
    processed_ids: set[str] = set()

    logger.info(f"Bridge started. Workspace={WORKSPACE}, Poll={POLL_INTERVAL}s")

    while True:
        try:
            messages = list_unread_messages(client)
            for msg in reversed(messages):  # 按时间正序处理
                process_message(client, msg, processed_ids)
        except Exception as e:
            logger.error(f"Poll cycle error: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
```

赋予执行权限：

```bash
chmod +x /home/hyf/bin/lark-channel-bridge
```

## Step 2 — 创建 systemd 服务

创建 `/etc/systemd/system/lark-channel-bridge.service`：

```bash
sudo tee /etc/systemd/system/lark-channel-bridge.service <<'SYSTEMD'
[Unit]
Description=SROS DevX Lark Channel Bridge
Documentation=https://github.com/anthropics/claude-code
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=hyf
Group=hyf
EnvironmentFile=/home/hyf/.config/lark-bridge/env
ExecStart=/home/hyf/bin/lark-channel-bridge
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=lark-channel-bridge

# 安全加固（可选）
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/tmp/lark-sessions /home/hyf/.claude
WorkingDirectory=/home/hyf/AI4S_Workspace

[Install]
WantedBy=multi-user.target
SYSTEMD
```

## Step 3 — 配置环境变量

```bash
mkdir -p /home/hyf/.config/lark-bridge

cat > /home/hyf/.config/lark-bridge/env <<'ENVFILE'
# 从飞书开放平台获取
LARK_APP_ID=cli_xxxxxxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxx

# Claude 工作根目录
CLAUDE_WORKSPACE=/home/hyf/AI4S_Workspace

# 轮询间隔（秒），按需调整
POLL_INTERVAL=5
ENVFILE

# 保护凭证文件权限
chmod 600 /home/hyf/.config/lark-bridge/env
```

> **务必**将 `cli_xxxxxxxxxxxx` 和 `xxxxxxxxxxxxxxxxxxxxxxxxxx` 替换为前置条件中获取的真实 App ID 和 App Secret。

## Step 4 — 启动服务

```bash
# 重载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start lark-channel-bridge

# 设置开机自启
sudo systemctl enable lark-channel-bridge

# 检查状态
sudo systemctl status lark-channel-bridge

# 查看日志
sudo journalctl -u lark-channel-bridge -f
```

预期输出：

```
● lark-channel-bridge.service - SROS DevX Lark Channel Bridge
   Loaded: loaded (/etc/systemd/system/lark-channel-bridge.service; enabled)
   Active: active (running) since ...
   ...
   [lark-bridge] Bridge started. Workspace=/home/hyf/AI4S_Workspace, Poll=5s
```

## Step 5 — 配置 Tmux 别名

编辑 `~/.bashrc` 或 `~/.zshrc`，添加以下别名：

```bash
cat >> ~/.bashrc <<'ALIASES'

# ── SROS DevX 双通道别名 ─────────────────────────────

# cauto: 交互式 Claude Code（Tmux 会话，断线保护）
alias cauto='tmux new-session -A -s claude-auto \; send-keys "cd ~/AI4S_Workspace && claude" Enter'

# cdo: 无头 Claude 单次执行（非交互式，飞书桥接同款模式）
cdo() {
    if [ -z "$1" ]; then
        echo "Usage: cdo <prompt>"
        return 1
    fi
    claude -p "$*"
}

# sros-tmux: 快速进入项目 Tmux 环境
alias sros-tmux='tmux new-session -A -s sros \; send-keys "cd ~/AI4S_Workspace/01-Core_Infra/SROS && clear" Enter'
ALIASES

source ~/.bashrc
```

### 别名说明

| 别名 | 功能 | 典型场景 |
|------|------|---------|
| `cauto` | 进入/附着 Claude Code Tmux 会话 | 日常深度开发，SSH 断线后可 `tmux attach` 恢复 |
| `cdo "任务描述"` | 无头模式单次执行 | 快速问答、脚本调用、CI/CD 集成 |
| `sros-tmux` | 进入 SROS 项目专属 Tmux 会话 | SROS 专项开发，窗口保持工作目录上下文 |

## Step 6 — 端到端烟雾测试

### 测试 1：systemd 服务存活

```bash
sudo systemctl is-active lark-channel-bridge
# 预期输出：active
```

### 测试 2：cdo 无头模式

```bash
cdo "echo hello from cdo"
# 预期输出：hello from cdo（由 Claude 返回）
```

### 测试 3：cauto Tmux 会话

```bash
# 启动 cauto（在新终端或 Tmux 中运行）
cauto
# 预期：进入 Claude Code 交互界面

# 从另一个终端附着同一会话
tmux attach -t claude-auto
# 预期：看到相同的 Claude Code 界面
```

### 测试 4：飞书群聊桥接

1. 在飞书目标群聊中发送 `@SROS DevX Bridge echo hello world`
2. 等待 5-15 秒
3. 预期：Bot 回复包含 "hello world" 的消息
4. 查看日志确认处理成功：

```bash
sudo journalctl -u lark-channel-bridge --since "2 min ago" | grep -i "replied\|error"
```

## 故障排查

| 症状 | 可能原因 | 解决 |
|------|---------|------|
| `active (exited)` | Python 异常退出 | `sudo journalctl -u lark-channel-bridge -n 50` 查看堆栈 |
| Bot 不回复 | 飞书 Token 过期 | 检查飞书开放平台 → 凭证与基础信息 → App Secret 是否变动 |
| `403 Forbidden` | 权限不足 | 确认应用已发布 + Bot 已加入目标群聊 |
| `claude: command not found` | PATH 未继承 | 在 env 文件中加 `PATH=/home/hyf/.local/bin:/usr/local/bin:$PATH` |
| `ProtectSystem=strict` 导致权限错误 | systemd 沙箱过严 | 临时注释掉 `ProtectSystem` 和 `ProtectHome` 排查，定位后调整 `ReadWritePaths` |

## 待完成后的更新

1. 更新 `ROADMAP.md` 第 79 行：

```markdown
| DevX Systemd Bridge | 飞书桥接 systemd 服务 + Tmux 别名 | P2 | ✅ |
```

2. （可选）将 `/home/hyf/bin/lark-channel-bridge` 脚本纳入 SROS 仓库版本管理：

```bash
cp /home/hyf/bin/lark-channel-bridge /home/hyf/AI4S_Workspace/01-Core_Infra/SROS/scripts/lark-channel-bridge
```

3. （可选）将 systemd unit 文件纳入版本管理：

```bash
cp /etc/systemd/system/lark-channel-bridge.service \
   /home/hyf/AI4S_Workspace/01-Core_Infra/SROS/config/systemd/lark-channel-bridge.service
```

## 安全注意事项

- **凭证隔离**：`/home/hyf/.config/lark-bridge/env` 包含 App Secret，权限必须是 `600`，**禁止**提交到 Git
- **飞书消息内容**：所有群聊消息由 `claude -p` 在工作目录下处理，敏感数据可能写入 `/tmp/lark-sessions/`。定期清理：`rm -rf /tmp/lark-sessions/*`
- **Bot 权限最小化**：仅申请必要权限（im:message, im:chat），不申请通讯录全量读取等高危权限
- **systemd 沙箱**：`ProtectSystem=strict` + `ProtectHome=read-only` 限制了桥接进程的文件系统访问范围，如需调整请评估影响
