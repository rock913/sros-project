SROS V2.3.2 架构白皮书：稿件驱动与原生解耦

版本: V2.3.2 (Productized Draft-Driven Edition)
发布日期: 2026-02-10
核心哲学: Draft is State (稿件即状态) + CLI is Interface (命令行即入口)

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

- sros init：生成工作区结构 + 自动写入 .roo/mcp.json（指向 localhost:8000/sse）+ 初始化 .sros/。
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