SROS V3.0 战略规划：面向 AI4S 的全链路科研操作系统

1. 重新定义生态位：SROS 的“主板与实验室”哲学

在未来的科研形态中，通用大模型（Claude、GPT-4）是**“科学家的大脑”，Claude Code / OpenClaw 等 Agent 框架是“科学家的双手（研究员）”**。

SROS 的终极生态位是：科学家的“标准化实验室（Laboratory）”与“高速数据总线（Data Bus）”。

SROS 不负责“思考”，SROS 负责“供给环境、提供仪器、管理账本”。

1.1 SROS 与通用 Agent 的共生契约

Claude Code / OpenClaw 负责：理解人类意图、分解任务、规划流水线、阅读文献、撰写文字、编写临时代码。

SROS 负责：

环境隔离：提供极其规范的物理目录（Workspace），让大模型知道数据在哪、图表在哪、草稿在哪。

高阶仪器的封装：大模型不会凭空算蛋白质或做 fMRI 预处理，SROS 将这些庞大的计算库（如 ESM3, fMRIPrep）封装成一句简单的 sros-skill 命令。

隐形图谱守护：在大模型修改 Markdown 或生成数据的同时，SROS 在底层 DuckDB 自动维护极其严谨的 知识-数据-代码-文本 有向图。

2. 覆盖“科研全流程”的系统架构设计 (V3.0)

一个完整的科研生命周期包含：Idea (洞察) -> Literature (文献) -> Experiment (实验/计算) -> Result (数据/图表) -> Writing (成文/排版)。

SROS V3 必须从“只做首尾（文献+成文）”扩展到“吞下中段（实验+数据）”。

2.1 架构升级：The "Headless Lab" Architecture (无头实验室架构)

┌───────────────────────────────────────────────────────────────┐
│  AI Agents (The Brain & Hands): Claude Code, OpenClaw, Roo    │
└───────┬───────────────────────────────┬───────────────────────┘
        │ (Terminal / CLI)              │ (MCP / JSON-RPC)
        ▼                               ▼
┌───────────────────────────────────────────────────────────────┐
│                   SROS Gateway & CLI Router                   │
└───────┬───────────────────────────────┬───────────────┬───────┘
        ▼                               ▼               ▼
┌───────────────┐               ┌───────────────┐ ┌─────────────┐
│ Core Skills   │               │ Domain Skills │ │ Custom      │
│ (原生核心技能)  │               │ (官方垂直扩展包) │ │ Plugins   │
├───────────────┤               ├───────────────┤ ├─────────────┤
│ • Gap Detect  │               │ • Neuro-Pack  │ │ • K-Dense   │
│ • Scholar Sync│               │ • Bio-Pack    │ │   Skills    │
│ • Draft Insert│               │ • Data-Viz    │ │ • User Skill│
└───────┬───────┘               └───────┬───────┘ └───────┬─────┘
        │                               │                 │
┌───────▼───────────────────────────────▼─────────────────▼─────┐
│ SROS Workspace (The Single Source of Truth)                   │
├─────────────────┬─────────────────┬─────────────┬─────────────┤
│ draft.md (稿件) │ graph.db (图谱)  │ data/ (数据) │ figs/ (图表)│
└─────────────────┴─────────────────┴─────────────┴─────────────┘


2.2 端到端 MVP 与“可视化界面”：IDE-as-UI（把反馈飞轮做成产品能力）

在 V3.0 里，“可视化界面”不等于传统 Web GUI。SROS 的主要用户是 Claude Code / OpenClaw / Roo 这类 Agent 与开发者本人。

核心结论：

- 不做传统前端面板（React/Vue 的按钮表单），避免预设交互路径束缚 Agent。
- 必须做端到端可运行的 MVP（Golden Thread），并把 VS Code 的文件树 + Markdown 预览 + 终端视作“天然可视化界面”。
- 让 `sros-skill` 命令成为 Agent 的“UI 按钮”：参数极简、输出可读、支持 `--raw` JSON、错误信息可自愈。

为什么端到端 MVP 会极大加速迭代：

- 只有端到端，才能暴露“接口衔接处”的系统性摩擦（Token 爆炸、路径约定、插入破坏排版、错误可恢复性）。
- 反馈飞轮极短：一条命令/一次工具调用即可复现与验证，而不是手动拼 JSON + 看日志。
- 可视化“体感”来自 IDE：草稿实时长出内容/图表，就是最强的 Aha Moment。

端到端 MVP 的形态（V3.0 的“新型界面”三件套）：

1) 人类研究员 UI：VS Code + 物理文件（workspace 目录规范 + draft.md 预览）
2) Agent UI：CLI Skills + 标准化输出（默认人类友好 + `--raw` 机器可读）
3) IDE 兼容壳：极简 MCP Gateway（不含业务逻辑，只做 CLI 反射代理）

黄金主线（Golden Thread）建议的迭代节奏：

- 第 1 周：只求跑通（mock search + insert-markdown），用 Claude Code 串起来
- 第 2 周：引入“数据/图表”闭环（run-script → figures/ → draft.md 引用）
- 第 3 周：把 mock 替换为真实能力（OpenAlex/真实脚本/真实图谱）


3. SROS 新版本研发思路与详细开发路径

为了实现上述宏伟蓝图，建议将开发路径分为三个阶段（Phase 1 ~ 3），逐步完成从“写作工具”到“科研 OS”的蜕变。

🚀 Phase 1: 核心重构 —— 拥抱 Unix 哲学与大一统 CLI (预计耗时: 3周)

目标：解决目前 MCP 导致的上下文污染，完成 CLI Skills 的底层重构，让 Claude Code 能够以极低的 Token 成本丝滑调用 SROS。

开发路径：

实现 sros-skill 基类：

抛弃原有的 mcp_servers 目录，建立 src/sros/skills/。

使用 typer 将所有现有能力（scholar.search, manuscript.find_gaps, manuscript.insert_section）封装为独立的命令行工具。

强制标准输出格式 (Unix Pipe Ready)：

所有的 sros-skill 必须支持 --raw (输出纯 JSON 供 jq 过滤) 和默认的人类友好输出（供 LLM 直接阅读摘要）。

极简 MCP Gateway：

重新实现一个极其轻量的 Gateway。它不包含任何业务代码，纯粹作为 CLI 的反射代理：当 IDE（如 Roo Code）通过 MCP 发送请求时，它在后台执行对应的 sros-skill 命令并返回结果。

Agent 启蒙配置自动生成：

修改 sros init，在初始化时不仅生成 .roo/mcp.json，还要生成 .clauderc (面向 Claude Code) 和 openclaw.yaml (面向 OpenClaw)，在其中用自然语言写明当前 Workspace 可用的 sros-skill 列表及用法。

🚀 Phase 2: 突破纯文本 —— 数据、计算与全息图谱 (预计耗时: 1-2个月)

目标：覆盖“Experiment (实验)”和“Result (数据)”环节，让 SROS 具备硬核科学计算的承载能力。

开发路径：

扩展 Workspace 规范：

sros init 新增目录结构：data/raw/, data/processed/, figures/, scripts/。强制科研数据管理的最佳实践。

重新设计 DuckDB 图谱 (Heterogeneous Graph)：

抛弃旧表，直接建立全新的“异构科研溯源图谱”。

Schema 设计：节点包含 Paper, Section, Dataset, Model, Figure。

Edge 设计：包含 CITES, GENERATES, ANALYZES, TRAINED_ON。

效果：当大模型插入一张图片时，DuckDB 记录 [Figure: roc.png] <- GENERATES <- [Script: svc.py] <- ANALYZES <- [Dataset: fmri.csv]。

开发 sros-skill-data 核心扩展包：

提供 sros-skill data preview <file> (用 pandas 快速返回 CSV 摘要供 LLM 理解)。

提供 sros-skill data plot <script> (执行绘图脚本并将结果注册到工作区)。

🚀 Phase 3: 开放生态与垂直领域重构 (预计耗时: 长期演进)

目标：通过插件系统接入类似 K-Dense、GraphMRI 等庞大能力，实现生态大爆发。

开发路径：

动态插件挂载系统 (Plugin Loader)：

在 .sros/ 下建立 plugins/ 目录。

允许用户或 OpenClaw 动态将 Python 脚本放入该目录，SROS 自动解析其 Docstring 并将其注册为新的 sros-skill，同时通过 MCP 暴露给前端 IDE。

官方垂直扩展包 (SROS Packs)：

SROS-Neuro-Pack：用 SROS 逻辑重构 GraphMRI。集成 fMRIPrep docker 调用命令，脑网络提取命令。

SROS-Bio-Pack：对接 ESM3, AlphaFold3，让大模型可以通过一行 sros-skill bio fold <sequence> 获得 PDB 文件。

事件驱动架构 (Event Hooks)：

科研计算往往耗时很长（如训练模型耗时 3 天）。

SROS 加入后台任务队列。当长耗时 sros-skill 执行完毕时，SROS 能够主动向 Claude Code 或 OpenClaw 发送 Webhook/系统通知，唤醒大模型继续写论文。

4. 演进策略：无历史包袱的“破坏性重构” (Breaking Changes)

鉴于目前 V2 版本尚无真实的外部生产用户依赖，这是系统演进中极其宝贵的**“架构红利期”**。

我们应该采用快刀斩乱麻的“破坏性重构”策略，坚决剔除任何为了“向后兼容（Backward Compatibility）”而存在的累赘代码，轻装上阵直奔 V3 终态。

4.1 核心清理计划（大砍刀）

废弃旧版数据库迁移脚本 (Drop Schema Migrations)：

立即移除 V2.3.2 中所有的 Zotero schema migration (如 ALTER TABLE 自愈逻辑)。

V3 策略：直接用一套干净的 DDL 初始化全新异构图谱。如果检测到旧的 .sros/graph.db，直接在 sros init 时报错并要求用户删除重建（因为目前并没有包含重要数据的旧工作区）。这能砍掉大量复杂的数据库防御性编程代码。

废弃历史通信协议兼容 (Drop Legacy APIs)：

移除为了早期客户端存在的非标准 API（例如 POST /sse 等兼容路由）。

V3 策略：Gateway 只提供符合最新规范的极简接口（或完全让位给 CLI），不再维护历史包袱。

删减硬编码的 Reasoning 代码 (Drop Hardcoded Logic)：

清理掉任何试图用 Python 编写的“自动规划流”代码（例如自己写的 Co-STORM 循环体、死板的 Gap 填补控制流）。

V3 策略：将这些复杂的流转全部剥离出 Python 代码，转而用自然语言编写成 .clauderc 提示词，交给外部的通用大脑（Claude/OpenClaw）去动态规划。

4.2 底层资产的“摘樱桃”式重用 (Cherry-picking the Good Parts)

虽然是破坏性重构，但并非推倒重来。我们要将 V2 中经过验证的纯粹算法“摘樱桃”般提取出来：

提取核心 Domain Logic：
把稳定可用的算法（如 Markdown AST 的定向解析与无损插入、OpenAlex API 的请求与降级封装）从原本的 src/sros/servers/* 目录中抽离。

重组到 core 目录：
把它们放到 src/sros/core/ 下，变成无状态的纯函数，完全独立于任何 Web 或 MCP 框架。

套上 Typer CLI 外壳：
在 src/sros/cli/skills/ 目录下，用 Typer 将上述 core 函数包装为 sros-skill 命令行，作为新系统唯一的核心接驳点。

5. 关键里程碑验收标准 (Milestones)

V3.0-Alpha (Skill-Driven Only)：完成 Phase 1 核心重构与清理。验收：旧的兼容代码全部移除。完全通过终端的 sros-skill 命令与 Claude Code 配合，走通“检索->写入”闭环。

V3.0-Beta (Data-Aware OS)：完成 Phase 2 部分。验收：Agent 能够读取 data/ 下的 CSV，编写并执行一个 Python 脚本生成图表，将图表路径插入 draft.md，并在全新的 DuckDB 中能查到这条数据溯源链路。

V3.0-GA (The AI4S Ecosystem)：完成 Phase 3 核心框架。验收：发布一套完善的 Plugin 开发文档。展示如何用 50 行 Python 代码将一个复杂的外部生信模型包装成 sros-skill，并被 OpenClaw 动态加载和调用。


5.1 当前实现状态（2026-03-16，v3.0-main）

已完成：

- `sros-skill` 已落地（支持 `--raw`），覆盖 manuscript/scholar/memory 的 MVP 工具。
- Gateway 已“变薄”：`tools/call` 不直接持有业务 Handler；统一反射到 skills 层的 RPC 派发（映射集中在 skills 模块），Gateway 只负责协议/路由。
- 已有自动化端到端验收：gap → search(mock) → insert → draft.md 更新（Golden Thread）。
- Repo 已完成大规模去噪：V2 文档/spec/旧 mcp_servers 已归档，不再干扰主线。
- Slice 0：升级 `sros init` 直接生成 V3 workspace 规范（`data/raw`、`data/processed`、`figures`、`scripts`）并生成 `openclaw.yaml`。已通过 TDD 实现并测试通过。

待完成（下一步）：

- Slice 2：数据闭环与异构图谱 schema（Dataset/Script/Figure 节点与 GENERATES/ANALYZES 边）。
  - 实现 `sros-skill data.preview <file>`：用 pandas 快速返回 CSV 摘要供 LLM 理解。
  - 实现 `sros-skill data.run-script <script>`：执行绘图脚本并将结果注册到工作区，更新 DuckDB 图谱。
  - 扩展 DuckDB schema 为异构图：添加 Dataset/Script/Figure 节点类型和 GENERATES/ANALYZES 边类型。

下一步计划：

- 基于 TDD 开始实现 Slice 2：先编写单元测试，然后实现 `data.preview` 功能（CSV 摘要），接着实现 `data.run-script`（脚本执行与图谱注册）。
- 目标：在本周内完成 Slice 2 的核心功能，确保 Agent 能读取 data/ 下的 CSV、执行脚本生成图表，并将图表路径插入 draft.md，同时在 DuckDB 中维护数据溯源链路。

6. 总结

未来的科研软件不会是堆砌无数按钮的图形界面（那是上个时代的 GraphMRI）。

未来的科研软件将是一个个高度标准化的命令行原子技能。大模型是极其出色的“命令行乐手”，而 SROS V3.0 就是那个提供全套乐器、标准乐谱格式、以及超级录音棚的操作系统。利用好“零历史包袱”的红利期进行果断重构，我们将以极低的工程成本，为未来的 AI4S 大爆发奠定最坚实的基建底座。


附录 A：端到端 MVP 与“可视化界面”需求深度分析（并入 V3.0 单一事实来源）

> 说明：本附录来自项目内部对“端到端 MVP/可视化工作流为何能加速迭代”的系统性分析。
> V3.0 的落地策略以此为约束：不做传统 Web GUI，但必须构建 IDE-as-UI + CLI Skills + 极简 MCP 壳的端到端飞轮。

### 1. 为什么“端到端 MVP/可视化界面”能极大加速迭代？

在产品早期，拥有一个能让人（或 AI）完整走通主流程的东西，会产生强大的“飞轮效应”：

- 暴露“全局系统性”缺陷，而非“局部逻辑”错误：
        - 开发单个 Python 函数（例如爬取论文）很容易完美，但这只是局部最优。
        - 当把“Gap检测 -> 检索 -> 写回”串联成端到端 MVP 时，你才会发现真正的痛点：比如检索返回的 JSON 太大导致大模型 Token 爆掉，或者写回时破坏了 Markdown 的原有排版。只有端到端，才能暴露出接口衔接处的摩擦力。

- 极速缩短反馈飞轮 (Feedback Loop)：
        - 如果没有界面或自动化流程，测试一次功能需要手动拼凑 JSON、用 Postman 发请求、看终端日志。这会让开发者产生畏难情绪。
        - 如果有一个可视化界面（或一行简单的终端命令能跑通全流程），开发者每天可以高频测试 50 次，迭代速度自然起飞。

- “体感（Empathy）”与“顿悟时刻（Aha Moment）”：
        - 可视化界面能让人直观看到产品的价值。当你在界面上点一个按钮，看到结果瞬间生成，这种“体感”会极大地激励开发者，并能迅速向利益相关者证明产品可行性。

### 2. 核心拷问：SROS 还需要传统的“可视化界面 (GUI)”吗？

结论：坚决不需要传统的 Web GUI（如 GraphMRI 那样的网页表单），但极度需要一个“面向 AI 与开发者的端到端可视化工作流”。

在《SROS V3.0 战略规划》中，我们已经将 SROS 定义为 “Headless Lab（无头实验室）”。如果我们花一个月去写一个 React 或 Vue 的前端面板，那就是战略上的倒退，原因如下：

- 目标用户变了：SROS 的主要使用者不再是“只会点鼠标的人类”，而是 Claude Code、OpenClaw 等 AI Agent。AI 不需要好看的 CSS 按钮，AI 需要的是标准化的 CLI 输入输出、无损的机器可读日志。
- GUI 是束缚：GUI 意味着你要预设所有的交互路径。这与 AI Agent “自由组合技能、动态规划”的理念背道而驰。

### 3. 那么，SROS 的“可视化与端到端 MVP”到底长什么样？

既然不写传统的 Web 界面，SROS 如何获得“加速迭代”的红利？答案是：将现成的顶级工具（IDE + 通用 Agent）作为 SROS 的“可视化界面和交互外壳”。

SROS V3 的端到端 MVP 应该是由以下三个组件拼合而成的“新型界面”：

#### 视角一：人类研究员的“可视化界面” (VS Code + 物理文件)

SROS 不需要自己画 UI，用户的编辑器（VS Code / Cursor）就是最完美的 UI。

- 界面体验：左边分屏是项目目录（看到 data/, figures/ 自动生成），中间分屏是实时预览的 draft.md，右边分屏是终端（运行 Claude Code）。
- 体感：当人类在终端输入一句话，中间的 draft.md 就像有幽灵打字机一样自动长出新的章节和图片。这就是极致的可视化反馈。

#### 视角二：AI Agent 的“UI 界面” (CLI Skills + 标准输出)

对于 Claude Code 来说，`sros-skill` 命令行就是它的 UI 按钮。

SROS 的 MVP 必须保证 `sros-skill` 足够“好按”（参数极简，支持 `--raw`，报错信息是自然语言建议而不是 Python 堆栈崩溃，引导 AI 自我纠正）。

### 4. 落地建议：构建基于 Claude Code 的“黄金主线 (Golden Thread)”

为了达到“通过端到端使用起来快速迭代”的效果，SROS V3 的开发不应该按照模块（先写完所有爬虫，再写所有数据库）来开发，而必须垂直切片，贯穿一条“黄金主线”。

建议的 MVP 研发与迭代路径：

#### 第一周：不写任何复杂计算，只求“走通”

- 构建一个极其简陋的 `sros-skill search`（哪怕后端写死只返回 3 篇固定的 mock 论文）。
- 构建一个简陋的 `sros-skill insert-markdown`。
- 关键动作：立刻使用 Claude Code，给它一句 Prompt：“帮我查 3 篇论文，插入到 draft.md 的前言中。”
- 迭代红利：在这一步，你立刻就会发现 Claude Code 是否能正确组合这两个命令，是否会搞错文件路径。你所有的优化精力都会集中在“如何让 Claude Code 用得更爽”上。

#### 第二周：引入数据生成闭环

- 开发 `sros-skill run-script` 和 SROS 目录下的 `figures/` 监听机制。
- 放入一个极其简单的 Python 画图脚本（比如画一个 2D 散点图，假装是复杂的脑影像处理）。
- 关键动作：让 Claude Code 运行该脚本，并将生成的 `plot.png` 用 Markdown 语法写入 draft.md。
- 迭代红利：你会发现相对路径在 Markdown 里怎么写才不会裂图，从而倒逼你去完善 SROS 的 Workspace 路径管理规范。

#### 第三周：真实能力替换 (Make it Real)

当上述的 Claude Code 端到端交互（找 gap -> 跑命令 -> 看到草稿更新）完全顺滑后，再把 mock 的搜索换成真正的 OpenAlex，把简陋的画图脚本换成真实的 GraphMRI / 脑网络提取逻辑。

### 5. 总结

“跑通端到端 MVP”是让项目活下来的唯一法则。

但请务必克制住“写一个前端网页”的冲动。在 AI4S 时代，Claude Code 的终端窗口就是你的超级对话框，VS Code 的 Markdown 预览就是你的前端画布。把 SROS 打造成能在这些现成工具里丝滑流转的 CLI 组件库，才能以最少的代码量获得最快的产品迭代速度。

