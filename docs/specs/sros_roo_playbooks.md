# SROS Roo Playbooks (Execution Specs)

> 目的：把“可执行的伪代码/验收标准/测试要求”放在 `docs/specs/`，让 `.roomodes` 保持为“角色定位与流程约束”。
>
> 使用方式：Builder 在实现前必须阅读并遵守本文，并按“验收”条目添加/运行自动化测试。

## Playbooks 的作用（为什么要有它）

Playbook 的定位是“可执行合同（execution contract）”，专门用来把口号式需求落地成：
- 需要复制的仓库参考实现（避免发明协议/自创结构）
- 传输协议/接口约束（例如：SSE 用 GET，JSON-RPC 用 POST）
- 验收标准（必须能写成自动化测试）

它的价值是：让 Builder 少做主观判断、少试错；让 Inspector 有明确的证据化验收依据；同时避免把伪代码塞进 `.roomodes` 导致“角色定位文件变成实现手册”。

## MVP 是否已达成？（你现在的项目状态怎么判）

结论：在“能跑起来 + Roo 能连上 + 至少 1 个工具可调用”这个严格意义的 MVP 上，你现在已经具备达成条件（并且你仓库里已经有自动化集成测试覆盖这条链路）。

但请注意：MVP 达成 ≠ 可以停止演进。下面列出的“下一步计划”不是为了堆功能，而是为了把 MVP 从“勉强可用”提升到“稳定可用、可扩展、Roo 自动调用成功率高”。

MVP 只要求：
- Gateway 支持 `initialize/tools/list/tools/call`
- `tools/list` 至少包含 `manuscript.find_gaps`
- `tools/call` 能跑通 1 个工具返回结构化结果

MVP 不要求（但强烈建议尽快做）：
- `tools/list` 的 `inputSchema` 精确描述每个工具参数（本仓库已实现）
- 所有 draft IO 严格绑定 `SROS_WORKSPACE_DIR`（本仓库已实现）
- 更强的错误分类、可观测性、对 Roo 的诊断友好性（可持续增强）

## 当前仓库进度标定（让系统/人都能看懂）

> 目的：把“已完成 / 部分完成 / 未完成”显式标出来，避免系统在阅读 playbook 时误判项目进度。
>
> 更新时间：2026-02-16（如后续实现发生变化，请同步更新本节）。

结论（以自动化测试为准）：截至 2026-02-16，本 playbook 的 A/B/C 以及文内列出的 Post-MVP 增强均已在本仓库实现并通过测试；当前无阻塞性待办。

### Legend
- ✅ DONE：实现已落地，且有自动化测试覆盖关键验收链路

> 注：本仓库当前不再使用 🟡/⬜ 标记；若未来引入新的 playbook 条目或发生回退，可恢复使用它们。

### Status Matrix

- ✅ DONE Playbook A（Gateway as MCP SSE Hub）
  - 证据：已存在集成测试覆盖 `GET /sse` + `POST /sse initialize/tools/list/tools/call`（见 `tests/integration/test_mcp_sse_hub.py`）

- ✅ DONE Playbook B（`sros init` 创建真实 DuckDB 文件）
  - 证据：`duckdb.connect(<workspace>/.sros/graph.db)` 可连接的自动化测试已覆盖（见 `tests/integration/test_mcp_sse_hub.py::test_duckdb_file_creation`）
  - 证据：`sros init` 生成 `.roo/mcp.json` 的集成测试已覆盖（见 `tests/integration/test_port_binding.py::test_mcp_json_schema`）

- ✅ DONE Playbook C（Manuscript draft IO 严格绑定 workspace + 路径安全）
  - 证据：`file_path` 按 workspace 相对路径解析 + 禁止绝对路径/`..` + 边界校验实现已落地（见 `src/sros/servers/manuscript/handler.py` 的 `resolve_workspace_path`）
  - 证据：集成测试以 workspace 内相对路径调用 `manuscript.find_gaps`（`file_path: "test_document.md"`）已覆盖（见 `tests/integration/test_mcp_sse_hub.py`）

- ✅ DONE Post-MVP 1：`tools/list` 的 `inputSchema` 精确化
  - 证据：Gateway `tools/list` 为主要 tools 提供了 `properties/required/additionalProperties`（见 `src/sros/gateway/main.py:mcp_list_tools`）

- ✅ DONE Post-MVP 2：`tools/call` 参数错误返回 -32602
  - 证据：缺少 tool 名、参数缺失、路径不安全等场景返回 -32602，且 message 含示例 params（见 `src/sros/gateway/main.py:dispatch_jsonrpc`）
  - 可选增强（非阻塞）：将 `inputSchema.required` 与运行时校验完全对齐（例如对声明 required 的 `file_path` 在 `tools/call` 侧也做缺失判定），进一步提升客户端自动修复能力

## Playbook A: Gateway as MCP SSE Hub (V2.3.2 core)

### Goal
- Roo 通过 workspace 的 `.roo/mcp.json` 连接 `http://localhost:<port>/sse`
- Gateway 支持 MCP JSON-RPC：至少 `initialize` + `tools/list` + `tools/call`（1 个 tool 调用即可）

### Transport Contract（严格约束）

必须严格复制并兼容现有 SSE 传输形态（见下方 References）：

1) SSE Stream
- `GET /sse` 必须返回 `text/event-stream`
- SSE payload 使用 `data: <json>\n\n`（与 [mcp_servers/common/sse_server.py](mcp_servers/common/sse_server.py) 一致）
- 连接后应尽快发送 endpoint discovery/connected/heartbeat 类事件（不要求字段完全一致，但必须是可解析 JSON）

2) JSON-RPC over HTTP
- `POST /sse` 接收 JSON body（JSON-RPC envelope）
- 返回 JSON-RPC response：`{"jsonrpc":"2.0","id":<same>,"result":...}` 或 `{"error":...}`

建议至少兼容以下 request 形态（与仓库里的 `MCPSSEServer` 一致：它只依赖 `method/params/id`）：

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
```

### Required JSON-RPC Methods（严格约束）

Gateway 作为 Roo 的 MCP Hub，至少实现：
- `initialize`
- `tools/list`
- `tools/call`

说明：仓库里部分旧 server 使用自定义方法名（如 `detect_gaps`），但 Gateway 作为 Hub 必须提供标准 tools 语义，避免 Roo 侧适配成本。

### References to Copy (in-repo)
- `mcp_servers/common/sse_server.py`（SSE transport 形态）
- `mcp_servers/manuscript_manager/main_sse.py`（SSE 入口组织方式）
- `mcp_servers/duckdb_memory/main.py`（`list_tools`/`call_tool`/错误返回结构）
- `mcp_servers/sros_gateway/main.py`（聚合网关的历史行为，可作为对照）

### Pseudo-code (structure, not final code)
```python
# src/sros/gateway/main.py

# Build registry
manuscript = ManuscriptHandler(workspace_dir=...)
scholar = ScholarHandler(...)
memory = MemoryHandler(workspace_dir=...)
zotero = ZoteroHandler(workspace_dir=...)

TOOLS = {
  "manuscript.find_gaps": manuscript.find_gaps,
  "manuscript.get_outline_tree": manuscript.get_outline_tree,
  "manuscript.insert_section": manuscript.insert_section,
  "manuscript.patch_draft": manuscript.patch_draft,
  "scholar.brainstorm_perspectives": scholar.brainstorm_perspectives,
  "memory.store_knowledge": memory.store_knowledge,
  "memory.query_knowledge": memory.query_knowledge,
  "zotero.add_citation": zotero.add_citation,
  "zotero.search_citations": zotero.search_citations,
}

def mcp_list_tools():
  # Return MCP tool definitions with inputSchema (JSON Schema)
  ...

def dispatch_jsonrpc(request: dict) -> dict:
  # Validate JSON-RPC envelope
  # method == "initialize" -> return capabilities
  # method == "tools/list" -> return mcp_list_tools()
  # method == "tools/call" -> lookup TOOLS[name] and call
  # Return {"jsonrpc":"2.0","id":...,"result":...} or {"error":...}
  ...

# Expose via SSE transport; endpoint must be GET /sse
# Use existing SSE server helper pattern rather than inventing a new protocol.
```

### Request/Response Examples（用于写测试，不是文档装饰）

1) 初始化

Request:
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
```

Response (example shape):
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"SROS Gateway","version":"..."},"capabilities":{}}}
```

2) 列出工具

Request:
```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

Response (example shape):
```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"manuscript.find_gaps","description":"...","inputSchema":{"type":"object","properties":{},"required":[]}}]}}
```

3) 调用工具

Request:
```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"manuscript.find_gaps","arguments":{}}}
```

Response (example shape):
```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"..."}]}}
```

### Acceptance (must be automated)
- `GET /sse` 返回 `text/event-stream`（测试可用短超时读取首个 `data:`）
- `POST /sse` 发送最小 `initialize` 请求能得到合法 JSON-RPC 响应（`jsonrpc=2.0`、`id` 对应）
- `POST /sse` 的 `tools/list` 返回包含至少 1 个工具
- `POST /sse` 的 `tools/call` 调用 `manuscript.find_gaps` 返回结构化结果

### Post-MVP 增强（不改协议，但提升 Roo 成功率）

1) `tools/list` 返回更精确的 `inputSchema`
- 目标：Roo 在没有人工提示的情况下也能构造正确参数
- 做法：为每个 tool 提供 JSON Schema（至少：properties + required + type + description）

2) `tools/call` 参数校验更严格
- 目标：当参数缺失/类型错误时返回 -32602，并给出下一步建议

3) 文档/一致性
- `.roo/mcp.json` 中的 description/version 与实际实现保持一致（避免误导）

## Playbook B: `sros init` must create a real DuckDB file

### Goal
- `sros init <workspace>` 后，`<workspace>/.sros/graph.db` 是有效 DuckDB 文件（不是空文本）

### Pseudo-code
```python
# src/sros/cli.py (init)
(workspace / ".sros").mkdir(parents=True, exist_ok=True)
import duckdb
duckdb.connect(str(workspace / ".sros" / "graph.db")).close()
```

### Acceptance
- `duckdb.connect(<workspace>/.sros/graph.db)` 不报错
- （可选）初始化一遍 Memory/Zotero handler 以创建表结构

## Playbook C: Manuscript draft IO must respect workspace

### Goal
- 所有草稿读写严格绑定 workspace（`$SROS_WORKSPACE_DIR`），绝不使用当前工作目录（cwd）推导路径
- **任何** file/path 参数都必须被解释为 **workspace 内相对路径**（默认推荐 `draft.md`），禁止绝对路径与路径穿越（`..`）

### Contract（精细化约束）

1) Workspace 必填
- 读取/写入 draft 的工具必须以 `SROS_WORKSPACE_DIR` 为唯一根目录
- 若未设置 `SROS_WORKSPACE_DIR`：
  - CLI 启动链路必须设置它（`sros start --workspace <x>`）
  - 工具侧必须返回可诊断错误（建议走 JSON-RPC -32602 或 tool error，包含“需要先设置 SROS_WORKSPACE_DIR”）

2) 路径语义（强约束）
- 若工具提供 `file_path`（或等价字段）：它的语义是“workspace 内的相对路径”
- 禁止：
  - 绝对路径（如 `/tmp/a.md`、`C:\\...`）
  - 路径穿越（如 `../draft.md`、`a/../../b`）
- 允许并推荐：`draft.md`、`notes/draft.md`

3) 默认值策略（与 Roo 自动调用兼容）
- 如果某 tool 的 `inputSchema` 把 `file_path` 标为 required：客户端必须提供（推荐值 `draft.md`）
- 如果某 tool 允许省略 `file_path`：服务端默认使用 `draft.md`

4) 结果可验证性
- 所有读写必须只影响 workspace 内文件；无论进程 cwd 为何，都必须一致

### Pseudo-code
```python
workspace = Path(os.environ["SROS_WORKSPACE_DIR"])  # required
def resolve_workspace_path(file_path: str) -> Path:
  # file_path is workspace-relative only
  rel = Path(file_path)
  if rel.is_absolute() or ".." in rel.parts:
    raise ValueError("file_path must be workspace-relative")
  return (workspace / rel).resolve()

path = resolve_workspace_path("draft.md")

def read_draft() -> str:
  return path.read_text(encoding="utf-8") if path.exists() else ""

def write_draft(text: str) -> None:
  path.write_text(text, encoding="utf-8")
```

### Acceptance
- 在不同 cwd 下调用 tool，仍然只影响 workspace 内的 `draft.md`
- `sros start --workspace <x>` 后，工具行为与 workspace 绑定
- 尝试 `file_path: "../draft.md"` 或绝对路径时，必须被拒绝（返回清晰错误，且不能读写到 workspace 外）

### Suggested tests（建议新增自动化验收）
- 单测：给 `resolve_workspace_path`（或等价 helper）喂入 `draft.md`、`notes/draft.md`、`../x`、`/tmp/x`，断言允许/拒绝逻辑正确
- 集成测试：在非 workspace 的 cwd 下启动 gateway，调用 manuscript 相关 tool，断言最终只修改 `<workspace>/draft.md`

## 简易 Builder 指令（只看这一段也能完成开发）

你现在是 `sros-builder`。按顺序做，不要自由发挥：

1) 先读（只读不改）
- @docs/specs/sros_roo_playbooks.md
- @docs/specs/sros_v232_implementation_spec.md

2) 先跑基线测试（必须全绿）
- `python -m pytest -q`

3) 按 playbook 做改动（先写 failing test，再实现）
- 做 MVP：实现/核对 Playbook A/B/C，并为每条 Acceptance 添加/完善自动化测试
- 做 Post-MVP：补齐 `tools/list` 的 `inputSchema` + 强化 `tools/call` 参数校验（-32602）+ 为新增行为补测试

4) 收尾回归（必须）
- `python -m pytest -q`
- 用简短文本输出：变更点 + 覆盖了哪些 Acceptance + 测试是否全绿

## Roo Code Builder 指令：Post-MVP（copy/paste）

当 Playbook A/B/C 已通过（MVP 已达成）后，用下面指令让 Roo Builder 做“成功率增强”而不是加新功能。

---

你现在是 `sros-builder`。

先加载：
- @docs/specs/sros_roo_playbooks.md
- @docs/specs/sros_v232_implementation_spec.md
- @src/sros/gateway/main.py

任务 1：提升 `tools/list` 的 inputSchema 精度（不改变现有 tool 名称）。
要求：
- `manuscript.find_gaps` 的 schema 至少包含 `file_path`（string, required）
- 对其他常用工具也补齐最小 schema（properties/required/type/description）
- 保持 `POST /sse tools/list` 的响应 shape 不变

任务 2：强化 `tools/call` 参数错误处理。
要求：
- 缺少必填参数时返回 JSON-RPC error code -32602
- 错误 message 必须包含：tool 名、缺失字段、示例 params

测试：
- 为 `tools/list` 增加断言：`manuscript.find_gaps` 的 `inputSchema.properties.file_path.type == "string"` 且 required 包含 `file_path`
- 为 `tools/call` 增加 1 个负例：缺少 `file_path` 返回 -32602

完成后运行：`python -m pytest -q`

---

## Roo Code Builder 指令（copy/paste）

把下面整段作为 Roo Code 的 Builder 输入即可（目标：减少模式跳转与自由发挥）。

---

你现在是 `sros-builder`。请严格按本文档实现 Playbook A/B/C。

重要：你必须使用 Roo 的真实工具调用能力（execute_command），而不是把类似 `[execute_command ...]` 当作纯文本输出。
如果你当前模型/Provider 不支持工具调用，立刻停止并向用户说明“当前模型无法 tool-call”，请求用户切换到支持 tool-calling 的模型或开启工具权限。

必须先加载并模仿这些参考实现（不要自创协议/自写 transport）：
- @docs/specs/sros_roo_playbooks.md
- @mcp_servers/common/sse_server.py
- @mcp_servers/manuscript_manager/main_sse.py
- @mcp_servers/duckdb_memory/main.py

任务：实现 Gateway 作为 MCP SSE Hub。
约束：
1) SSE：`GET /sse` 返回 `text/event-stream`，payload 采用 `data: <json>\n\n`。
2) JSON-RPC：`POST /sse` 支持 `initialize`、`tools/list`、`tools/call`。
3) 工具列表至少包含 `manuscript.find_gaps`，并可被 `tools/call` 成功调用。
4) 全量类型标注；每个 handler try/except，错误信息可诊断（包含关键参数和下一步建议）。

测试（先写 failing test 再实现）：
- 新增一个集成测试文件，启动 gateway 后：
  - GET /sse 断言 `text/event-stream`
  - POST /sse initialize 断言 JSON-RPC 响应
  - POST /sse tools/list 断言包含 manuscript.find_gaps
  - POST /sse tools/call 调用 manuscript.find_gaps 断言返回结构化内容

完成后运行：`pytest -q` 并确保全绿。

收尾规则（避免卡在 attempt_completion）
- 如果 Roo 运行时提供 `attempt_completion` 工具：
  - 先 `execute_command` 跑完最终回归（例如 `python -m pytest -q`）
  - 然后立刻调用 `attempt_completion` 作为最后一步
  - 调用后不要再输出任何额外文本（否则可能触发 “failed to use any tools” 的循环校验）
- 如果当前运行时没有 `attempt_completion`（例如一些普通 Chat/IDE 环境）：
  - 最后一次 `execute_command` 运行 `pytest -q`
  - 用普通文本总结“证据 + 结论”即可

## 针对你截图配置的结论（qwen3-coder-plus / OpenAI Compatible）

你现在的 Provider 是 DashScope 的 OpenAI Compatible 端点 + `qwen3-coder-plus`。从现象看，主要风险不是 tokens 或上下文窗口，而是：
- Roo 的“工具调用”需要模型输出结构化 tool-call；如果 provider/model 的 tool-calling 支持不完整、或 Roo 没能正确注入 tools schema，模型就会退化成把 `[execute_command ...]` 当文本写出来。
- Roo 的错误提示 “Model Response Incomplete / failed to use any tools” 正是这个退化的表现：Roo 在某些阶段强制要求 tool-call（常见是要求最后用 `attempt_completion` 收尾），但模型给了纯文本。

建议你在 Roo 的 provider/profile 里确认是否有类似选项：
- 启用 Function Calling / Tools
- 使用 `tools`（新格式）而不是仅 `function_call`（旧格式）
- 或者启用“强制工具模式 / tool_choice=required”（如果 Roo 提供）

---
