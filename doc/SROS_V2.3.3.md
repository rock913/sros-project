SROS V2.3.3 升级目标：稳健写回 + 并发安全 + 生态接入（TDD 驱动）

版本: V2.3.3 (Robust Loop Edition)
目标发布日期: 2026-03
核心哲学延续: Draft is State + CLI is Interface

---

## 0) 对标基线（来自 V2.3.2 进展）

V2.3.2 已稳定提供“可安装 + 可启动 + 可验收”的骨架，并具备可复现证据链：

- MCP SSE transport 对齐 reference client（`event: endpoint` → `/messages?session_id=...` → SSE `event: message` 回传响应）。
- 本地生产验收脚本可落盘 machine-readable 证据：`logs/production_verification.json`。
- Scholar 支持 OpenAlex 真后端 + 可控 fallback（`SROS_SCHOLAR_FALLBACK=mock`）。
- Growing Doc Loop 后半段已落地最小闭环（定位插入 + 引用映射落库 + 可查询）。

V2.3.3 在此基线之上，重点解决两类“产品级风险”：

1) **写回定位不稳**（模型幻觉/标题轻微偏差导致插入错位）。
2) **并发脏写**（用户手动编辑与 Agent 写回冲突）。

---

## 1) 总体评估（What’s good / What’s risky）

### 1.1 核心亮点 (Strengths)

彻底的物理与逻辑解耦：将系统封装为 pip install sros 标准包，将用户态数据隔离在由 sros init 创建的独立 Workspace 中。这解决了 AI Agent 工具链最常见的“工具代码与用户数据混杂”的痛点，极大降低了上下文噪音（Token 消耗）。

坚守行业标准协议 (MCP)：全面拥抱 Model Context Protocol (MCP)，并标准实现了 SSE (Server-Sent Events) + JSON-RPC。这意味着 SROS 不是一个封闭的系统，而是一个可以被任何现代 AI 编程辅助工具即插即用的后台能力引擎。

Draft is State（稿件即状态）理念：放弃了复杂的中间状态管理，将 Markdown 文件 (draft.md) 作为单一真理来源 (Single Source of Truth)。这种极简主义设计极其适合大模型阅读和修改。

工程健壮性设计：支持 OpenAlex 真后端与 Mock 的无缝切换、Zotero Schema 的自愈能力（Best-effort ALTER TABLE），以及 verify_production.py 提供机器可读 JSON 证据。

### 1.2 潜在风险与改进建议 (Risks & Recommendations)

Markdown/行级操纵的脆弱性：依靠 `heading:<Title>` 进行定位插入容易受模型幻觉/大小写/轻微拼写误差影响导致内容错位。

- V2.3.3 建议：引入 **可验证锚点** 与 **fuzzy match 限界策略**：
    - 锚点哈希（anchor-hash）：由 `get_outline_tree` 返回并用于 `insert_section(target="anchor:<hash>")`。
    - fuzzy match：仅在相似度阈值内自动匹配，否则返回可诊断错误（列出当前 headings + 候选建议）。

并发与冲突控制：用户与 Agent 同时修改 draft.md 易造成脏写。

- V2.3.3 建议：引入 **乐观并发控制**：工具调用携带 `expected_sha256`，若文件已变更则拒绝写入并返回 Version Mismatch 指引。

---

## 2) V2.3.3 升级目标（Definition of Done）

### 2.1 写回定位更稳（Anchors)

- `manuscript.get_outline_tree` 返回每个 heading 的稳定锚点（anchor hash）。
- `manuscript.insert_section` 新增 target：
    - `anchor:<hash>`：精确锚点（推荐）。
    - `heading:<Title>`：支持大小写不敏感 + 可控 fuzzy（有阈值）。
    - 当无法匹配时：返回可诊断错误（列出 headings + 相似候选）。

### 2.2 并发安全（Optimistic Concurrency）

- `insert_section` / `patch_draft` 支持可选参数 `expected_sha256`。
- 若 `expected_sha256` 与当前文件 hash 不一致：拒绝写入，返回包含 `current_sha256` 的错误，并建议客户端重新读取大纲/文件后重试。

### 2.3 防御性编程（Agent 友好错误）

- 任何参数错误或目标缺失，不再静默失败；错误信息必须包含：
    - 失败原因
    - 当前可用选项（如 headings 列表）
    - 下一步建议（如“先调用 get_outline_tree 获取 anchor 后再写回”）

### 2.4 生态接入模板化（可选但推荐）

- `sros init --target roo|claude-code` 生成对接配置（`.roo/mcp.json`、`.clauderc`、`.roomodes`/指南）。

---

## 3) 里程碑与研发计划（TDD-First）

Milestone A（已完成）：定位稳健 + 并发安全（核心）

1) TDD：新增单测覆盖（已落地）
    - `heading:` 大小写不敏感匹配
    - `heading:` 可控 fuzzy（拼写轻微偏差可匹配，偏差过大必须报错）
    - `anchor:` hash 精确匹配
    - `expected_sha256` mismatch 拒绝写入并返回可诊断错误
2) 实现：manuscript handler 增强（已落地）
    - `get_outline_tree` 为每个 heading 返回可验证 `anchor`（hash）
    - `insert_section` 支持 `target="anchor:<hash>"` 并返回结构化结果（`ok/error/current_sha256/...`）
    - `insert_section`/`patch_draft` 支持 `expected_sha256` 乐观并发控制
3) Gateway：tools/list schema 扩展（已落地）
    - `manuscript.insert_section`/`manuscript.patch_draft` 增加可选 `expected_sha256`
    - 新增 `manuscript.get_file_sha256` 工具（便于客户端做并发保护）

Milestone B（下一步）：冲突提示与可恢复（UX + 可恢复策略）

目标：把“失败”变成“可恢复的下一步动作”，减少 Agent 反复试错。

建议 TDD 用例（优先级从高到低）：
1) `anchor:` 前缀歧义时：返回结构化错误，包含可选候选列表（title/anchor/line），并提示“用更长前缀”。
2) `heading:` 不存在且 fuzzy 也失败时：错误中必须包含 headings 列表 + 最相似候选（Top-N）+ 推荐改用 `anchor:`。
3) `expected_sha256` mismatch 时：错误中必须包含 `current_sha256`，并建议客户端先 `get_file_sha256/get_outline_tree` 刷新后重试。
4) （可选）提供 `dry_run=true`：只解析 target 并返回将插入的位置/锚点信息，不写入文件。

Milestone C（可选）：生态模板化

- `sros init --target ...` 自动生成对接配置与 playbook。

---

## 4) 验收证据（Artifacts）

- 状态更新（2026-03-10）：`python -m pytest -q` 全绿（覆盖 V2.3.3 anchors + 并发安全 + Claude Code MVP CLI/verify），当前为 `23 passed`。
- `python scripts/verify_production.py ...` 产出 `logs/production_verification.json`。
- `sros verify --port 8000` 产出 `logs/claude_mvp_verification.json`（验证 initialize/tools/list/tools/call）。
- （可选）对接脚本/模板可在新 workspace 一键生效。

2. 核心机制技术实现细节 (Technical Implementation)

为了让系统能够快速、稳定地被开发和复现，以下提供 SROS 核心链路的实现流程与准生产级伪代码。

2.1 MCP Gateway SSE 通讯闭环

实现流程：

客户端发起 GET /sse，Gateway 生成唯一 session_id。

Gateway 下发首个 SSE Event，类型为 endpoint，告知客户端后续的 JSON-RPC 请求应发往何处（如 POST /messages?session_id=xxx）。

客户端发起 POST /messages 调用工具。

Gateway 处理请求后，将结果通过刚才建立的 SSE 连接以 event: message 的形式异步推给客户端。

FastAPI 核心伪代码：

from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import uuid

app = FastAPI()
sessions = {} # 内存管理 SSE 发送队列

@app.get("/sse")
async def sse_handshake(request: Request):
    session_id = str(uuid.uuid4())
    queue = asyncio.Queue()
    sessions[session_id] = queue

    async def event_generator():
        # 1. 发送 MCP 规范要求的 endpoint 事件
        yield {
            "event": "endpoint",
            "data": f"http://localhost:8000/messages?session_id={session_id}"
        }
        # 2. 持续监听当前 session 的消息队列
        while True:
            msg = await queue.get()
            yield {"event": "message", "data": msg}

    return EventSourceResponse(event_generator())

@app.post("/messages")
async def handle_rpc(request: Request, session_id: str):
    if session_id not in sessions:
        return {"error": "Invalid session"}
    
    payload = await request.json()
    # 解析 JSON-RPC (如 method: "tools/call", params: {"name": "manuscript.find_gaps"})
    response_data = await dispatch_mcp_call(payload) 
    
    # 异步推回 SSE 管道
    await sessions[session_id].put(json.dumps(response_data))
    return "Accepted" # POST 请求立刻返回


2.2 Growing Doc Loop：定位插入与引用落库

这是 SROS 的核心业务流。Agent 根据返回的大纲，选择特定的锚点（如 heading-12），调用 insert_section 写入内容，并关联引用。

实现流程：

解析 Target 参数，将 Markdown 转化为行数组。

找到对应行号进行 List Insert。

如果携带了 citations，生成唯一 section_id。

连接 DuckDB，将引用关系（DraftSection -> CITES -> Paper）持久化。

伪代码契约 (manuscript_manager.py)：

import duckdb

def insert_section(target: str, content: str, citations: list, file_path: str, workspace_dir: str):
    # 1. 相对路径安全校验
    assert ".." not in file_path and not file_path.startswith("/")
    full_path = Path(workspace_dir) / file_path
    
    lines = full_path.read_text().splitlines()
    insert_idx = len(lines) # 默认追加
    
    # 2. 解析 Target 定位
    if target.startswith("heading:"):
        title = target.split(":", 1)[1].strip()
        for i, line in enumerate(lines):
            if line.startswith("#") and title in line:
                insert_idx = i + 1
                break
    elif target.startswith("line:"):
        insert_idx = int(target.split(":")[1])

    # 3. 增量写入
    lines.insert(insert_idx, f"\n{content}\n")
    full_path.write_text("\n".join(lines))
    
    # 4. 图谱落库 (DuckDB)
    if citations:
        section_id = f"draft_section:{file_path}#line-{insert_idx}"
        db_path = Path(workspace_dir) / ".sros/graph.db"
        conn = duckdb.connect(str(db_path))
        
        # 写入节点与边
        conn.execute("INSERT OR IGNORE INTO nodes VALUES (?, ?)", (section_id, 'DraftSection'))
        for cite in citations:
            citekey = cite.get('citekey')
            conn.execute("INSERT OR IGNORE INTO nodes VALUES (?, ?)", (citekey, 'Paper'))
            conn.execute("INSERT INTO edges (source, target, relation) VALUES (?, ?, ?)", 
                         (section_id, citekey, 'CITES'))
        conn.close()

    return {"status": "success", "inserted_at": insert_idx, "section_id": section_id}


2.3 Scholar 联邦搜索降级策略

为了保证自动化回归测试的稳定性，Scholar 工具必须具备环境感知能力：网络好时走 OpenAlex，网络差或测试环境中退化为离线确定性的 Mock 数据。

实现流程与伪代码：

import os

def federated_search(query: str, max_results: int = 5):
    backend = os.getenv("SROS_SCHOLAR_BACKEND", "mock")
    fallback = os.getenv("SROS_SCHOLAR_FALLBACK", "mock")
    
    if backend == "openalex":
        try:
            return call_openalex_api(query, max_results)
        except Exception as e:
            if fallback == "mock":
                print(f"[Warn] OpenAlex failed, gracefully degrading to mock. Error: {e}")
                return get_mock_search_results(query)
            raise e
    
    return get_mock_search_results(query)


3. 生态对接与实战使用指南

SROS 作为底座，其最大的价值在于能够与各类前端 Agent 完美结合。以下是主流 Agent 的对接指南。

3.1 基础项目初始化 (所有 Agent 共享)

无论使用什么 Agent，第一步始终是通过 SROS CLI 初始化并启动守护进程：

# 1. 安装 SROS 核心包
pip install -e .  # 或 pip install sros

# 2. 初始化工作区
sros init my-transformer-paper  # 默认生成 Roo 配置

# 可选：同时生成 Claude Code + Roo 配置
# sros init my-transformer-paper --target both

# 可选：仅生成 Claude Code 配置
# sros init my-transformer-paper --target claude-code

cd my-transformer-paper

# 3. 启动后台服务 (默认暴露 8000 端口)
sros start -w . -p 8000


启动后，系统会在 .sros/graph.db 初始化 DuckDB，并在工作区生成标准的 draft.md。

3.2 与 Claude Code 结合

Claude Code 极擅长执行 CLI 命令与复杂文件分析，将其设定为“研究员”模式效果极佳。

对接步骤：

推荐用 CLI 一键生成对接文件（MVP）：

```
sros init my-transformer-paper --target claude-code
cd my-transformer-paper
sros start -w . -p 8000

# 不运行 Claude 也能先验证 MCP 是否可用
sros verify --port 8000
```

MVP 开发状态（2026-03-10）：已完成 ✅

已交付能力（仓库内可复现）：

- `sros init --target claude-code|both`：生成 `.clauderc` + `CLAUDE.md`
- `sros start ...`：在端口/URL 变化时可同步更新 `.clauderc` 的 Gateway SSE URL
- `sros verify --port 8000`：不运行 Claude 也能验证 MCP SSE 工具链可用，并落盘 `logs/claude_mvp_verification.json`
- 回归测试：`python -m pytest -q` 全绿（当前 `23 passed`）

仍建议补齐的工作（不阻塞 MVP，但利于产品化）：

1) 真实 Claude Code 端到端验收脚本：在本机 Claude 中确认能发现 MCP server、能实际调用 `manuscript.*` 工具并写回（含常见报错排查）
2) 远程/端口转发场景的更强指引：建议配置 `--gateway-url`、何时需要 `sros start --auto-port`/更新 URL
3) 失败可恢复 UX（对应 Milestone B）：anchor 前缀歧义候选列表、heading 失败 Top-N 推荐、并发冲突的下一步建议更标准化

这会生成：

- `.clauderc`：Claude Code 对接配置（包含 MCP SSE URL 与 custom instructions）
- `CLAUDE.md`：工作区提示词/流程指南（人类可读）

在工作区根目录创建 .clauderc 配置文件：

（若用上面的 `sros init --target claude-code`，则无需手写）

{
    "custom_instructions": "...（见 CLAUDE.md / .clauderc 生成内容）...",
    "mcp_servers": {"sros-gateway": {"url": "http://localhost:8000/sse"}}
}


在终端启动 Claude Code：claude

发送提示词：“请扫描 draft.md 里的所有空白部分，帮我找两篇关于 Transformer 的最新文献补充进去。”

3.3 与 Roo Code (VS Code Extension) 结合

Roo Code 非常适合在 IDE 内边看边改，SROS 甚至在 init 阶段就为其做了自动适配。

对接步骤：

运行 sros init 时，系统会自动生成 .roo/mcp.json：

{
    "mcpServers": {
        "sros-gateway": {
            "name": "SROS Gateway",
            "url": "http://localhost:8000/sse",
            "type": "sse",
            "disabled": false,
            "alwaysAllow": []
        }
    }
}


(注：Remote-SSH/端口转发场景建议用 `sros init ... --gateway-url http://127.0.0.1:<forwarded>/sse`，或在 `sros start --auto-port` 时启用自动更新 url。)

在 VS Code 中打开 my-transformer-paper 文件夹。

点击 Roo Code 面板，你会看到 manuscript.find_gaps, scholar.brainstorm_perspectives 等工具已亮起并可用。

3.4 与 OpenClaw 结合 (高级/动态 Agent)

OpenClaw 可作为 SROS 的“大脑”，通过动态下发技能脚本强化 SROS。

对接步骤：

启动 SROS 时，配置动态技能挂载点：sros start -w . --plugin-dir .sros/skills/

在 OpenClaw 中配置 Agent 的 TaskPlan：

Step 1: 调用 SROS 获取 draft.md 的当前状态。

Step 2 (Reasoning): 在 OpenClaw 内部进行 Co-STORM 多智能体辩论。

Step 3: 动态生成一个专门针对某种特定 PDF 格式解析的 Python 脚本，写入 .sros/skills/custom_parser.py。

Step 4: SROS Gateway 自动热加载该工具，OpenClaw 随即调用此新工具提取数据，并存入 .sros/graph.db。

4. 演进路线总结 (Next Steps for Ecosystem)

为了最大化与各种 Agent 的兼容性并保证工程稳定性，建议 SROS 按照以下优先级推进：

巩固 MCP 基座（已提供伪代码基础）：确保 SSE event: endpoint 握手协议完全符合 Reference Client 的规范。

规范化 Prompt/Playbook 分发：利用 sros init --target claude-code 或 sros init --target roo 自动生成本指南中提及的 .clauderc 和 .roomodes，实现开箱即用。

增强防御性编程（容错提示）：Agent 频繁犯错（幻觉、参数传错）。SROS 被暴露的 MCP Tool 必须具备容错性，对于异常调用必须返回明确的自然语言指导。
例如：{"error": "Target heading 'Methodology' not found in draft.md. Current headings are ['Intro', 'Background']. Please re-read outline_tree."}，利用此机制引导 Agent 闭环自我纠正。