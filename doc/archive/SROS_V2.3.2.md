SROS V2.3.2 架构白皮书：稿件驱动与原生解耦

版本: V2.3.2 (Productized Draft-Driven Edition)
发布日期: 2026-02-10
核心哲学: Draft is State (稿件即状态) + CLI is Interface (命令行即入口)

---

## Executive Snapshot（2026-03-10）

**一句话结论**：V2.3.2 的“可安装 + 可启动 + 可验收”的产品骨架已稳定；MCP SSE transport 已对齐 reference client；验收脚本可产出 JSON 证据；Scholar 已支持 OpenAlex 真后端并提供可控 fallback；下一阶段进入 Growing Doc Loop 后半段（定位插入 + 引用映射落库 + 最小闭环回归）。

**已完成（✅，有自动化证据）**

- Gateway：`GET /sse` + `POST /messages` 的 MCP SSE transport 语义闭环（`event: endpoint` + `session_id` + SSE `event: message` 回传响应）。
- 本地可重复验收：`scripts/verify_production.py` 端到端通过并写入 `logs/production_verification.json`。
- Scholar：默认 mock（离线确定性），可选 OpenAlex 真后端；支持 `SROS_SCHOLAR_FALLBACK=mock` 作为网络波动时的可控降级。
- Zotero：历史 `.sros/graph.db` 的最小 schema migration（缺列自愈）已落地并有单测。

**部分完成（🟡，可用但尚未闭环产品化）**

- Growing Doc Loop：Gap 检测与写回工具已存在，但“定位插入语义 + 引用映射落库 + 可复现闭环测试”仍需补齐。
- Federated Search：工具已暴露，但联邦检索质量/数据源迁移仍以 MVP 为主。

**下一步（⬜，建议按顺序落地）**

1) `manuscript.insert_section`：从“仅追加”升级为“可定位插入”（基于 heading/anchor/line）。
2) 引用映射落库：在 `.sros/graph.db` 写入 DraftSection → CITES → Paper（复用 memory 的 `nodes/edges` 表）。
3) 最小闭环回归：从 draft.md TODO 出发，跑通 gap→检索(mock)→写回→映射可查询。

0. 背景与动机：从原型到产品 (Prototype → Product)

当前 SROS 正处于从“原型开发期”向“产品发布期”过渡的关键阶段。V2.2 的主要耦合点在于：工具源码（mcp_servers/）与用户数据（workspace/、draft.md）混在一个代码仓库里，导致新用户上手成本高、维护成本高、并且 IDE/Agent 上下文噪音巨大。

必须解耦的痛点对比（Coupled → Decoupled）：

- 目录结构：论文(draft.md)埋在源码仓库深处，Git 历史混杂 → 用户在任意磁盘位置创建论文目录，论文可独立 Git 管理。
- 环境依赖：需要手动 pip install -r requirements.txt，易冲突 → 用户只需 pip install sros，依赖随包安装并保持一致。
- 启动方式：必须在源码根目录运行 python run_servers.py → 任意终端输入 sros start 即可启动后台。
- 上下文干扰：打开源码根目录会索引大量 Python 代码，浪费 Token/易误改 → 只打开论文目录，写作体验更专注。

1. 核心战略升级

1.1 从“代码库”到“产品包”(Decoupling)

目标状态（产品化三件套）：

- SROS Core：封装为标准 Python Package（pip install sros）。
- User Space：通过 CLI 初始化项目工作区，与源码彻底隔离。
- Gateway：作为后台守护进程运行，对用户透明（Roo Code/Agent 只需连接 SSE）。

1.2 从“搜索驱动”到“稿件驱动”(Draft-Driven Discovery)

目标：实现 Gap Analysis Loop（空白填充循环），让研究/检索/引用/写作围绕 draft.md 自动闭环。

- 状态中心：draft.md 作为单一真理来源（Single Source of Truth）。
- 生长感交互：左侧“生长中的大纲”，右侧“检索与引用动态”。
- 局部扩展：选中一句话 → 扩充论据 → 检索 → 引用 → 增量写入。

2. 系统架构视图

2.1 物理部署架构（The Package）

安装后位于 Python 环境：

/System_Python_Path/site-packages/sros/
├── cli.py               # 命令行入口（Typer/Click）
├── gateway/             # MCP Hub（Starlette + FastMCP）
├── servers/             # 内置 MCP 服务能力
│   ├── manuscript/      # [核心] 稿件解析与 Gap 检测
│   ├── scholar/         # [核心] 联邦搜索 + Co-STORM 视角生成
│   ├── memory/          # DuckDB 知识图谱
│   └── zotero/          # 引用管理
└── utils/               # 进程管理、健康检查、端口检测等

2.2 用户工作区架构（The Workspace）

用户执行 sros init my_paper 后生成：

/User/Documents/my_paper/
├── .roo/
│   └── mcp.json         # [自动生成] 指向 http://localhost:8000/sse
├── .roomodes            # [可选/自动生成] Roo Code 自定义模式定义（JSON）
├── .sros/
│   ├── graph.db         # DuckDB（私有知识图谱）
│   └── gap_log.json     # Gap 检测记录（可选）
├── materials/           # 原始素材（Deep Research Reports）
├── references/          # 可选：导出引用/缓存 BibTeX 等
├── draft.md             # [单一真理来源] 正在撰写的稿件
└── ideas.md             # 核心论点备忘录

2.3 源码仓库结构（面向打包的标准形态）

为了支持“pip install sros”，仓库需要向 PyPI 标准靠拢：

/sros-repo/
├── pyproject.toml       # [核心] 包定义与 CLI 入口点
├── src/
│   └── sros/
│       ├── __init__.py
│       ├── cli.py       # CLI 入口（init/start/doctor）
│       ├── gateway/     # 原 mcp_servers/sros_gateway
│       ├── servers/     # 原 mcp_servers/*（子服务聚合）
│       └── utils/       # 原 scripts/ 与 run_servers.py 的可复用逻辑
└── README.md

2.4 pyproject.toml 最小模板（示意）

这是实现 sros 命令的关键配置：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sros"
version = "2.3.2"
description = "Scientific Research Operating System"
dependencies = [
	"mcp>=1.0.0",
	"starlette",
	"uvicorn",
	"typer[all]",
	"rich",
	"duckdb",
	"pandas",
]

[project.scripts]
sros = "sros.cli:app"
```

3. 核心业务流：The Growing Doc Loop

Step 1：动态大纲与空白检测（Gap Analysis）

- Trigger：用户在 draft.md 写入 [TODO: ...] 或选中一段文字点击“扩充”。
- Action：Roo Code/Agent 调用 mcp-manuscript.find_gaps(file_path=...) 或对选中文本做定向 gap 识别。
- Output：产出 Gap 列表与类型（Evidence Needed / Elaboration Needed / Citation Needed 等）。

Step 2：视角发散（Co-STORM Perspective）

- Decision：Agent 调用 mcp-scholar.brainstorm_perspectives(query=...) 生成多维研究视角。
- Interaction：系统提示“可从 A/B/C 视角展开，你希望侧重哪个？”。
- Execution：针对选定视角触发联邦搜索与证据收集。

Step 3：实时引文映射（Live Citation Mapping）

- Ingest：高质量论文自动入库（Zotero 或内部引用库）。
- Map：在 .sros/graph.db 中建立 DraftSection → [CITES] → Paper 的引用关系。

Step 4：增量写入（Incremental Writing）

- Action：Agent 调用 mcp-manuscript.insert_section(...) 或 patch_draft(...)。
- Result：draft.md 实时更新，并附带标准引用标记（例如 [@citekey]）。

4. MCP 工具链升级规划

4.1 mcp-manuscript（重构）

- find_gaps(file_path)：基于规则（[TODO] 标记、段落长度、引用密度等）识别待办。
- get_outline_tree(file_path)：返回 Markdown/AST 的树状结构，支撑“生长中的大纲”。
- insert_section(target, content, citations)：带引用的增量写入。

4.2 mcp-scholar（增强）

- brainstorm_perspectives(query)：Co-STORM 核心，生成多维研究视角。
- find_critiques(paper_id)：CiTO 逻辑，主动寻找反驳/质疑类文献，强化论文对抗性。

4.3 sros-cli（新增，产品入口）

CLI 负责初始化工作区、启动后台、环境自检与配置生成：

- sros init：生成工作区结构 + 自动写入 .roo/mcp.json（指向 localhost:8000/sse）+ 初始化 .sros/；并可复制/生成项目级 .roomodes（JSON）。
- sros start：启动 Gateway（对齐现 run_servers.py 的能力，但运行在安装包中）。
- sros doctor / sros status：依赖自检、端口占用检查、DuckDB 文件健康检查。

5. 新用户使用流程（User Journey）

完成解耦后，新用户上手路径应当稳定且可复制：

1) 安装

```bash
pip install sros
```

2) 创建项目

```bash
sros init my-transformer-paper
cd my-transformer-paper
```

3) 启动后台

```bash
sros start
```

4) 开始写作

- 在项目目录打开 VS Code（只打开论文目录）。
- Roo Code 通过 .roo/mcp.json 自动识别并连接 http://localhost:8000/sse。
- 用户在 draft.md 继续写作并插入 [TODO]，系统进入 Growing Doc Loop。

6. 建议的落地步骤（Implementation Next）

- 标准化打包：将当前仓库逐步调整为 src/ 布局，补齐 pyproject.toml。
- CLI 开发：优先实现 sros init 与 sros start（随后补 doctor/status）。
- 发布策略：可发布到 PyPI，或先支持 pip install git+<repo_url> 进行内测分发。

7. SROS 开发准确率提升指南（V2.3.5）

目的：解决 Agent 开发结果不准确、需要反复手动矫正的问题；通过“Reference-Augmented Generation（参考增强生成）”把开发过程从“猜测生成”升级为“参考复刻 + 可验证迭代”。

7.1 核心原则

- Don't Guess, Copy（不要猜，去抄）：优先复用/模仿仓库中已验证可运行的实现模式（例如 duckdb_memory、manuscript_manager），而不是凭空发明。
- 先证据、后修改：任何修复都以可复现的失败（测试/脚本）为依据，避免“拍脑袋 patch”。
- Spec 是契约：Architect 输出的 Spec 必须可直接驱动 TDD，且明确边界与数据结构。

7.2 修正后的工作流（三阶段）

Phase 1：Architecture（Architect Mode）

- 指令模板：设计某能力的接口与数据结构，并明确“参考对象”（例如：设计 Context Ingester 的接口。参考 manuscript_manager 的设计模式）。
- 质量门槛：如果 Spec 缺少伪代码（Pseudo-Code）或只是口号式描述（例如“解析 PDF”“提取标题”），必须驳回重写。
- 输出要求：必须产出 docs/specs/*.md 作为交接产物（包含 Protocols + Pydantic Schemas + 复杂逻辑伪代码）。

Phase 2：Context Loading（Builder Mode）

原则：切换到 Builder 后，不要立刻写代码；先把 Spec 与“可抄的参考实现”加载进上下文。

Context 注入清单（示例）：

- @docs/specs/feature.md（需求/契约）
- @mcp_servers/duckdb_memory/main.py（代码模板：FastMCP/Lazy Loading/stdio 结构）
- @mcp_servers/duckdb_memory/server.py（逻辑模板：类结构、错误处理风格）

执行要求：

- 严格模仿参考代码结构（初始化方式、装饰器写法、错误处理模式、Lazy Loading 位置），优先“形似再神似”。
- 全量类型标注；对每个 MCP tool 做 try/except，错误信息可诊断（包含关键参数与下一步建议）。

Phase 3：The “Gemini Check”（可选但推荐）

触发条件：Phase 2 的实现运行报错，且两次修复仍未稳定通过（或 Roo Code 的修复质量不达标）。

操作：将“报错信息 + 相关代码片段 + 期望行为（来自 Spec）”提交给外部强推理模型进行原因分析与修复建议（例如 Gemini 1.5 Pro / 其他高推理模型）。

回填策略：把修复后的代码与解释回填到当前仓库，并立刻运行测试/脚本验证，确保修复可复现、可持续。

7.3 伪代码门槛（示例：把口号变成算法步骤）

以下是“好伪代码”的最低标准：明确库、步骤、错误分支与产物结构。

```python
def ingest_pdf(file_path: str) -> IngestResult:
	# 1) validate
	assert file_path.endswith(".pdf")
	if not exists(file_path):
		return IngestResult(error="file_not_found")

	# 2) extract text (pypdf)
	reader = pypdf.PdfReader(file_path)
	pages_text = []
	for page in reader.pages:
		pages_text.append(page.extract_text() or "")
	text = "\n".join(pages_text)

	# 3) normalize
	text = normalize_whitespace(text)

	# 4) heuristic structure
	# - find headings: regex like r"^(\d+(\.\d+)*)\s+.+$" per line
	# - split into sections
	outline = build_outline_from_headings(text)

	# 5) output
	return IngestResult(text=text, outline=outline)
```

8. Roadmap Update（对齐 V2.3.5）

8.1 Dynamic Skill Loader

目标：允许 Builder 动态生成并挂载简单脚本/技能（借鉴 OpenClaw 的“动态加载”思路），用于快速试验与回归验证，但必须受控（可追踪、可移除、默认关闭）。

8.2 Simulation Interface

目标：增加 mcp-simulator 接口（借鉴 DeepModeling）。提供最小可复现的“模拟器”能力，用于：

- 快速复现工具链调用（不用起全套服务）。
- 在 Inspector 阶段稳定复现 bug（作为回归测试前置）。

9. 当前实现进度与里程碑（Progress vs V2.3.2）

更新时间：2026-03-10

9.1 当前进度（以自动化测试为证据）

已达成（✅）

- 产品化基本形态：`pyproject.toml` + `src/` 包结构 + `sros` CLI 入口点。
- 解耦工作区：`sros init <project>` 生成 `.roo/mcp.json`、`.sros/graph.db`、`draft.md`、`ideas.md`、`materials/`、`references/`。
- Gateway SSE Hub：
  - `GET /sse` (event-stream) + `POST /sse` (JSON-RPC) + Roo 兼容 `POST /messages`。
  - **MCP SSE Transport 兼容性**：SSE 首包提供 `event: endpoint`，并使用 `session_id` 将 JSON-RPC 响应通过 SSE `event: message` 回传（兼容 Python MCP reference client）。
  - 支持 `initialize` / `tools/list` / `tools/call`。
- Manuscript MVP：`manuscript.find_gaps(file_path)` 能基于 `[TODO: ...]` 与简单启发式返回结构化 gap；并严格绑定 workspace 相对路径（禁止绝对路径与 `..`）。
- Growing Doc Loop（最小后半段✅）：`manuscript.insert_section` 已支持按 target 定位插入（heading/line/append），且当提供 citations 时会将 DraftSection → CITES → Paper 写入 `.sros/graph.db`（复用 memory 的 `nodes/edges` 表），并可通过 `memory.get_citation_map(section_id)` 查询。
- Scholar 工具暴露（MVP）：Gateway 已暴露 `scholar.brainstorm_perspectives`、`scholar.find_critiques`、`scholar.federated_search`，并通过集成测试验证可调用。
- 生产验证链路（E2E）：`verify_production.py --port 8000 --query "..."` 可稳定完成 `initialize → tools/list → tools/call`（manuscript/scholar/memory），并产出 `logs/production_verification.json` 作为 machine-readable 证据。
- 稳定性修复：
  - DuckDB 锁冲突导致的测试不稳定已解决（单测使用临时 workspace 隔离 DB）。
  - `sros start` 的端口占用检测已修正，避免 TIME_WAIT 误判（提升可重启性）。

证据（可复现）

- 集成测试：`python -m pytest -q`（tests 下已覆盖 SSE + JSON-RPC + tools/list + tools/call 最小链路）。
- Growing Doc Loop 最小回归：新增单测覆盖 `find_gaps → insert_section(定位插入+citations) → graph.db 映射可查询`。
- 一次性 SSE（便于探测）：`GET /sse?once=1` 返回 `text/event-stream` 且响应会结束（避免脚本超时）。

部分完成（🟡）

- Scholar/Memory/Zotero 的“真实业务能力”：当前实现以 MVP/示例为主（非完整联邦搜索/非完整 CiTO 证据链）。
  - Scholar：已支持 OpenAlex 真实后端（默认仍可走 mock，避免测试依赖外网）；OpenAlex `select` 参数已修复，可真实返回结果。
	- Zotero：已补齐最小 schema migration（旧 `citations` 表缺列会 best-effort `ALTER TABLE` 自愈），避免历史 `.sros/graph.db` 阻塞初始化；并有单元测试覆盖。
- Growing Doc Loop 的后半段：已落地“定位插入 + 引用映射落库 + 可查询”的最小闭环；仍待产品化项包括 `gap_log.json` 的标准化与更强的定位插入策略（多 anchor/offset/冲突处理）。

未完成（⬜）

- Federated Search 的产品化迁移：将现有 `mcp_servers/federal_academic_search` 的可运行能力迁入安装包路径并作为 `scholar.federated_search` 的真实后端（目前 Gateway 暴露已完成，但数据源/质量仍为 MVP）。
- 更强的稿件增量写入语义：`insert_section(target, ...)` 需要从“追加”升级为“可定位插入”。

9.2 里程碑规划（1-2 周可执行）

Milestone 1（本周）：契约一致性与可诊断性（Contract Consistency)

- 目标：让 `tools/list` 的 `inputSchema` 与实际 handler 签名/数据结构一致；让 Roo 能基于 schema 自主构造正确请求。
- 验收：
  - `tools/list` 中 `scholar.brainstorm_perspectives` 要求 `query`；`memory.store_knowledge` 要求 `nodes/edges`；`zotero.add_citation` 要求 citekey/title/authors/year/journal/url/bibtex。
  - 通过集成测试验证 `tools/call` 真实可调用上述工具。
  - SSE 传输满足 MCP reference client：SSE 首包 `event: endpoint`，并能通过该 endpoint 完成 JSON-RPC 往返。
  - `scripts/final_verification.py` 全绿（含 `/sse?once=1` 探测）。
  - `verify_production.py` 能在本机端到端通过（不要求外网）。

Milestone 2（下周）：Scholar 联邦搜索产品化（Federated Search)

- 目标：将联邦检索能力迁入 `site-packages/sros/servers/scholar`，并在 Gateway 暴露 `scholar.federated_search`/`scholar.find_critiques`。
- 当前进展：
  - Gateway 暴露与集成测试已完成。
  - 已提供 OpenAlex 可选真实后端（默认 mock，避免 pytest 依赖外网）。
  - OpenAlex 请求参数与字段映射已修复（避免 400 Bad Request）。
- 验收：提供最小可用的数据源（如 OpenAlex/Semantic Scholar）与可重复的集成测试（可 mock 外部网络）。
	- 推荐验收方式（不把外网塞进 pytest）：在工作区 `.env` 中配置 `SROS_SCHOLAR_BACKEND=openalex` + `OPENALEX_EMAIL`（可选再加 `SROS_SCHOLAR_FALLBACK=mock` 用于 OpenAlex 临时失败时的可控降级），启动 `sros start` 后运行 [scripts/verify_openalex_live.py](scripts/verify_openalex_live.py)；产物写入 `logs/openalex_live_verification.json` 作为可追溯证据。

Milestone 3（两周内）：Growing Doc Loop 闭环（写作→检索→引用→写回）

- 目标：在 `.sros/graph.db` 建立最小引用映射结构；`manuscript.insert_section` 支持定位写入；可选写出 `gap_log.json`。
- 验收：从 draft.md 中的 TODO 出发，能走通“gap→检索→写回并带引用标记”的自动化回归测试。

9.3 下一步建议（按优先级）

1) **Zotero schema migration（已完成✅）**
	- 行为：旧 `citations` 表缺列会 best-effort `ALTER TABLE` 自愈；索引创建失败不阻塞启动。
	- 验收：历史 `.sros/graph.db` 不再因缺列阻塞 Zotero 初始化；单元测试覆盖 legacy→migrate→写入。

2) **Gateway/CLI 可诊断性增强（让“真实可用”更像产品）**
  - `sros doctor` / `sros status`：输出端口占用、当前 workspace、DuckDB 文件锁、OpenAlex 配置是否齐全、以及 SSE endpoint/消息 endpoint 的连通性。
	- 为 `verify_production.py` 输出一份 machine-readable JSON（写入 `logs/production_verification.json`）（已实现✅），作为发布前证据。

3) **Scholar 联邦搜索“质量与确定性”**
	- 增强失败回退策略：当 OpenAlex 临时失败时可降级到 mock（可控开关 `SROS_SCHOLAR_FALLBACK=mock`），避免把网络波动误判为系统不可用。
  - 统一返回结构（id/doi/journal/url/abstract 等字段）并写入文档契约，减少 Agent 端适配成本。

4) **Growing Doc Loop 后半段落地（最小闭环）**
  - `manuscript.insert_section` 增加“定位插入”能力（基于 heading/anchor/offset）。
  - 在 `.sros/graph.db` 写入 DraftSection → CITES → Paper 的最小关系（与 `memory.store_knowledge` 对齐）。