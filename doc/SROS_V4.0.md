SROS V4.0 战略规划：泛科研通用操作系统与生态矩阵

0. 核心定位跃迁 (The Paradigm Shift)

如果说 SROS V3.0 是“让大模型可以在本地跑 Python 脚本画图的无头实验室”，那么 SROS V4.0 的目标是成为 AI4S 领域的 "Linux/Docker"。

生态兼容性（向下）：统一纳管本地机器、HPC（高性能计算）集群、分布式数据库。

领域可扩展（横向）：通过统一的“Skill Pack（技能包）”标准，无缝接入文献检索、天文星表、脑科学计算等垂直领域。

交互大一统（向上）：深度融合“VS Code 即平台”理念，结合 LangGraph/OpenClaw 等多智能体流，打造人机协同的终极科研 IDE。

1. 基础底座重塑：端到端文献与知识合成闭环

科研工作流往往不是从一张白纸开始的，而是充斥着前期的散乱调研材料（如其他大模型生成的 Deep Research 报告、零散的灵感笔记、下载的杂乱网页）。我们将整合 V2 的 OpenAlex/Zotero 积累，引入 RAG（检索增强生成） 与 泛在知识摄入（Omni-Ingestion） 理念，将其升级为标准化的 SROS-Lit-Pack。

1.1 工作流设计 (Omni-Ingestion -> Zotero -> RAG -> Draft)

泛在知识摄入 (knowledge.ingest_raw)：

核心痛点：处理 materials/ 目录下散乱的 Deep Research Markdown 报告、TXT 笔记或网页剪报。

能力：Agent 能够自动读取这些非结构化材料，提取核心观点（Claims）、遗漏的线索和待验证的假设，作为后续检索的“种子”。

联邦检索技能 (scholar.search)：Agent 根据前期摄入的“种子线索”，调用 OpenAlex/arXiv 接口，进行定向的高质量学术文献搜索，以验证或反驳那些散乱的灵感。

资产归档技能 (scholar.zotero_sync)：自动获取检索到的 PDF 全文，利用 Zotero API 建立本地/云端同步文献库，将非正式线索转化为正式的学术资产。

异构向量化合成 (rag.build & rag.query)：

技术升级：利用 DuckDB 的 vss 扩展（或外接 pgvector），不仅对 Zotero 中的 PDF 论文 进行切块向量化，同时也对 materials/ 中的 Deep Research 报告与零散笔记 进行索引。

能力：大模型能基于“正式文献 + 本地灵感”的混合知识库进行精确 RAG 问答（如：“结合我昨天写的脑暴笔记和这五篇最新论文，提炼出 fMRI 预处理的参数差异”）。

大纲重构与引用 (manuscript.refactor & manuscript.cite)：支持跨章节的 Markdown AST 重构，并自动生成标准化引用格式，将合成后的知识稳固地写入 draft.md。

1.2 引入 CLI-Anything 赋能极速生态构建

为了支撑上述复杂的文档摄入与处理，SROS 不应重新造轮子，而应引入类似 CLI-Anything 的设计哲学：万物皆可为 Skill。

什么是 CLI-Anything 赋能？ 允许将系统内现成的、任意语言编写的命令行工具，通过简单的 Schema 定义或自动解析 --help，瞬间转化为 SROS 的标准化 Skill。

在文献闭环中的应用场景：

文档转换：直接将现成的 pandoc 命令包装为 sros-skill ext.pandoc，让 Agent 能瞬间把散乱的 Word/PDF 调研材料转化为清晰的 Markdown 供 RAG 摄入。

网页抓取：将开源的 curl 或 trafilatura (网页正文提取工具) 直接包装为 sros-skill ext.web_scrape，当 Agent 在散乱笔记中发现一个网页 URL 时，能自主调用它抓取内容并入库。

架构收益：通过这种方式，SROS 的开发者无需为每一种文档格式手写 Python 包装器，极大地降低了生态扩展成本。

1.3 Agent 执行剧本示例

"我的 materials/ 目录下有一份我用其他大模型生成的关于 'Transformer 在天文测光中的应用' 的长篇调研草稿（Markdown），以及几个零散的网页链接。请你：\n1. 用工具读取并提取其中的核心观点。\n2. 去 OpenAlex 检索真实文献验证这些观点，下载前 5 篇核心论文。\n3. 将真实论文和我的草稿一起进行向量化比对，重构我 draft.md 的 Related Work 章节，剔除幻觉，加上真实的学术引用。"

2. 垂直领域攻坚：替代专业 GUI 与打通大型工程

SROS V4 必须证明其“泛化能力”，我们将针对您的三个核心诉求定义专属的 Domain Packs（领域扩展包）。

2.1 SROS-Neuro-Pack：彻底降维替代 GraphMRI

战略逻辑：如前所述，GraphMRI 是“人点鼠标的僵化流水线”。SROS 将其解构为可组合的 CLI 技能。

核心技能集：

neuro.bids_validate：规范化导入 DICOM 数据。

neuro.fmriprep_run：后台调用 fMRIPrep Docker 容器执行预处理。

neuro.connectome：基于 Nilearn/Brainnetome 提取网络矩阵。

图谱映射：将大脑网络特征直接写入 .sros/graph.db，实现表型数据与影像数据的异构关联。

2.2 SROS-Astro-Pack：与 Zero2x / OneAstronomy 的协同

战略逻辑：SROS 是“数据与计算后端”，Zero2x 是“三维可视化前端”。SROS 不负责渲染，它负责为 Zero2x 准备“子弹”。

核心技能集：

astro.fetch_catalog：对接 SDSS/DESI 数据库，下载/过滤 PB 级星表数据到本地工作区 (data/raw/)。

astro.process_fits：处理 FITS 图像或光谱数据。

astro.run_simulation：调用底层物理信息神经网络 (PINN) 生成推导数据。

与 Zero2x 的联动桥梁：

SROS Gateway 提供静态文件服务或 WebSocket 接口。

Zero2x (Three.js 引擎) 通过 API 读取 SROS 处理好的极简坐标与分类数据，触发 macro -> micro 的时空跃迁与聚类高亮渲染。

2.3 SROS-HPC-Pack：异构集群管理

战略逻辑：脑科学（DTB 动力学仿真）和天文学（星系宇宙学模拟）都需要庞大的算力。SROS 不能只在笔记本上跑，必须能作为**“集群调度中枢”**。

核心技能集：

hpc.submit_slurm / hpc.submit_k8s：Agent 生成 PBS/Slurm 脚本，自动提交到远端超算节点。

hpc.status：轮询任务状态。

图谱映射的史诗级增强：

DuckDB 图谱加入硬件维度：[Agent Prompt] -TRIGGERS-> [Script] -RUNS_ON-> [Slurm_Node_01] -GENERATES-> [Result.csv]。

实现真正意义上的科研计算全链路透明化。

3. 生态兼容性与可扩展性架构设计

为了支撑上述所有 Domain Packs，SROS 必须在底层进行“拔高”。

3.1 “插件即代码” (Plug-and-Play Architecture)

抛弃复杂的配置，采用类似 Python entry_points 或约定目录的插件分发机制：

任何人（包括生态开发者）只需编写一个符合 SROS 契约的 Python 文件（包含 run() 函数和 INPUT_SCHEMA），放入 ~/.sros/plugins/ 或通过 pip install sros-neuro 安装。

SROS Gateway 会动态反射，将这些函数自动暴露为供 Claude Code / OpenClaw 调用的 MCP Tools（如 plugin.neuro.fmriprep）。

3.2 拥抱“VS Code 科研 IDE”体验 (Frontend Shell)

结合您的《VS Code 自动化科研平台》规划，终端 CLI 对研究员来说依然有门槛。SROS 必须提供一个可视化的“壳”：

左侧（数据资产）：显示 SROS Workspace (data/, figures/) 和 Zotero 库的实时视图。

中间（工作区）：编辑器不仅能写 Markdown，还能直接内嵌打开 Zero2x 的 WebGL 渲染画布。

右侧（Agent 领航员）：内置类似 Roo Code/Claude 的 Webview，底座接驳 LangGraph 的多智能体编排（一个负责查文献、一个负责写代码、一个负责集群调度），提供“人在环路 (HITL)”的权限审批。

4. 实施路线图与升级计划 (The Roadmap)

我们将分三个阶段稳步推进 V4.0 的落地：

Phase 1：基建夯实与文献闭环 (1.5 个月)

目标（以测试指南为唯一验收口径）：满足《SROS V4.0 Phase 1: 文献与知识合成闭环 MVP 测试指南》中的全链路 Omni-Prompt，确保 Agent 能在 **不逃逸** 的前提下稳定跑通：

materials/（散乱笔记） → 网页正文抓取 → Scholar 检索 → 文献资产落盘（references/） → 本地 RAG 检索 → draft.md 重构写回（含引用） → DuckDB 图谱可验证。

交付物（Phase 1 MVP 必须具备的 Skill 面）：

1) Omni-Ingestion（最小闭环）

- `sros-skill --raw ext web-scrape --url <URL>`
	- 用 `requests` 抓取网页并做最小正文提取（MVP 允许返回 raw text/html 的简化版）
	- 结构化返回：`{ok, url, title?, text, error?}`

2) Scholar 检索（与现有 V3 能力对齐 + 兼容别名）

- `sros-skill --raw scholar search --query <q> --max-results <n>`（Phase 1 兼容入口）
	- 内部可复用当前 `scholar federated-search`（mock-first，`SROS_SCHOLAR_BACKEND=openalex` 时才联网）
	- 结构化返回统一字段：`title/authors/year/url/source`（可选 `abstract/doi`）

3) Zotero / References 资产沉淀（本地可验证）

- `sros-skill --raw scholar zotero-sync --citekeys <k1> --citekeys <k2> ...`
	- MVP 不强依赖真实 Zotero API：允许“mock 下载/落盘”，但必须满足可验证的物理资产结果
	- 产物：
		- `references/zotero_library.bib`（至少包含 citekey/title/year/author 的 BibTeX）
		- `references/pdfs/`（可选：占位 PDF / 元数据 JSON）
	- 同时写入 `.sros/graph.db`：`citations` 表（已存在）或等价的 paper 节点

4) 本地 RAG（MVP：先保证可用，再谈 vss）

- `sros-skill --raw rag build --source <path> --source <path> ...`
	- 构建 `document_chunks` 表：`{id, source_path, chunk_text, metadata_json, created_at}`
	- Phase 1 MVP 允许使用“轻量 lexical scoring”替代 embedding/vss（避免新增重依赖）
- `sros-skill --raw rag query --query <q> --top-k <n>`
	- 返回 `chunks:[{source_path, text, score, chunk_id}]`

5) Draft AST 重构写回（从插入进化到“可控重写”）

- `sros-skill --raw manuscript refactor --file draft.md --target heading:Related Work --content <md> --cite <citekey>...`
	- MVP 允许策略：若目标 heading 不存在则创建；存在则替换该 section 内容（或明确“先删后插”）
	- 必须写入图谱：
		- `draft_section -> paper` 的 `CITES` 边（复用现有写入机制，但要对 citekey 做存在性校验，防止幻觉引用）

验收标准（必须自动化/可复现）：

- 运行 Omni-Prompt 后：`references/zotero_library.bib` 存在且包含目标 citekeys
- DuckDB：
	- `edges` 表存在 `relationship='CITES'` 的边，且目标 citekey 可在 `citations` 或 paper 节点中解析
	- `document_chunks` 表存在（chunk_count > 0）
- `draft.md` 的 Related Work（或等价章节）包含 `[@citekey]` 且没有“引用不存在”的写入

说明（工程策略）：

- Phase 1 以“端到端可跑 + 可验收”为第一优先：embedding/vss 作为 Phase 1+ 或 Phase 2 的增强项。
- CLI 必须坚持 V3 的经验：对常见别名/参数误用做兼容层，减少 Agent 因摩擦而逃逸。

Phase 2：VS Code 融合与集群调度 (1.5 个月)

目标：解决“交互体验”与“算力边界”问题。

动作：

启动 VS Code 插件开发，实现左侧资源树与 SROS Workspace 状态同步。

开发 SROS-HPC-Pack：实现通过 SSH/API 向远程服务器分发脚本并监控结果的最小 MVP。DuckDB 图谱加入 Infrastructure 节点。

Phase 3：垂直领域大爆发 (长期演进)

目标：吃掉 GraphMRI 份额，赋能 Zero2x。

动作：

发布《SROS 插件开发标准白皮书》。

官方下场开发 SROS-Neuro-Pack，复现 GraphMRI 的核心图论与机器学习预测流水线。

联合开发 SROS-Astro-Pack，打通 SROS 数据预处理 -> Gateway 吐出 JSON -> Zero2x (Three.js) 渲染宇宙星表的全栈演示 Demo。

5. 结语

SROS V3 证明了它能**“握住鼠标和键盘”；
SROS V4 的使命，是为这双虚拟的手打造一个“从显微镜（脑科学）到望远镜（天文学），从本地笔记本到超级计算机”的全尺寸万能兵器库**。
通过严格的插件化（Skill Packs）、全息溯源（DuckDB）和极致的集成环境（VS Code），SROS 将不可阻挡地成为 AI4S 时代的绝对底座。