# **基于模型上下文协议 (MCP) 的下一代科研与创作平台架构演进深度研究报告：全流程数据智能与跨学科巨著管理系统的构建指南**

## **1\. 战略背景与架构重构综述**

当前，自动化科研平台正处于从单一工具集成向智能生态系统转型的关键十字路口。根据对现有技术文档《MCP 技术升级与改进建议》的深度审计，以及对全流程科研支持（含数据处理）、书籍辅助撰写与跨学科巨著管理等新增需求的综合分析，现有的基于 API 适配器的架构已难以满足日益复杂的科研场景 1。传统的“VS Code 即平台”模式虽然利用了 IDE 的上下文优势，但在处理异构数据源集成、上下文动态感知以及系统扩展性方面，受限于传统的硬编码适配器模式，导致了严重的“集成疲劳”和“上下文瓶颈” 1。

本报告旨在制定一套详尽的架构升级指南，核心战略是引入**模型上下文协议 (Model Context Protocol, MCP)** 作为系统的神经中枢，将平台从封闭的工具集合重构为开放、分布式的**智能科研操作系统**。这一转型不仅仅是接口标准的统一，更是对人、AI 智能体（Agent）与数据之间交互关系的根本性重构。通过 MCP 的标准化协议层，我们将解耦核心智能编排（LangGraph）与底层能力供给（Tools/Resources），实现从“单体智能”向“分布式生态”的跨越 1。

升级后的架构体系（Architecture V2.0）将围绕三个核心平面展开：**用户交互平面（VS Code Host）**、**智能编排平面（LangGraph Client）** 以及 **能力供给平面（MCP Servers）**。这种分层设计旨在解决跨学科巨著管理中涉及的超长上下文一致性问题，以及科研数据处理中对持久化执行环境的依赖 1。通过引入双重传输机制（Stdio 与 SSE）和分层智能体架构，新系统将能够支持从文献发现、数据清洗、知识图谱构建到长篇巨著撰写的全链路自动化。

## **2\. MCP 核心技术生态与传输架构的深度选型**

在构建支持多场景的科研平台时，正确选择和配置 MCP 的传输层协议是确保系统性能、安全性和扩展性的基石。基于对技术文档的分析，我们建议采用一种**混合传输策略（Hybrid Transport Strategy）**，以平衡本地交互的低延迟需求与远程计算的隔离性需求 1。

### **2.1 Stdio 与 SSE 的战略性权衡与部署**

MCP 协议定义了两种主要的传输方式：基于标准输入输出的 Stdio 和基于 HTTP 流式传输的 SSE (Server-Sent Events)。在 Architecture V2.0 中，这两种协议并非互斥，而是各司其职，共同构成了平台的通信骨架。

**表 1：Stdio 与 SSE 在科研平台中的差异化应用分析**

| 特性维度 | Stdio (标准输入输出) | SSE (Server-Sent Events) | 架构决策建议 |
| :---- | :---- | :---- | :---- |
| **通信机制** | 通过进程管道 (Pipe) 直接通信，父子进程强绑定 | 基于 HTTP 协议的单向流式传输 \+ POST 回调 | **混合部署**：前端用 Stdio，后端用 SSE |
| **安全性** | **极高**。仅限本地进程间通信，无网络端口暴露，天然隔离外部攻击 | **中等**。依赖网络边界防护和鉴权机制，需配置网关 | 本地敏感操作（如密钥管理）必须走 Stdio |
| **延迟性能** | **毫秒级**。零网络开销，适合高频交互 | 毫秒至秒级。受网络环境影响，适合长耗时任务 | UI 交互操作选 Stdio，重计算任务选 SSE |
| **部署形态** | 本地插件、CLI 工具 | Docker 容器、微服务集群、云端 API | 核心计算与数据服务容器化，通过 SSE 暴露 |
| **多路复用** | 不支持。通常是一对一连接 | **支持**。一个 Server 可服务多个 Client | 知识库、数据库等共享资源必须使用 SSE |
| **典型场景** | 本地文件读写、Git 操作、本地 Zotero 连接 | Jupyter 代码执行、Postgres 数据库查询、Arxiv 检索 | 遵循“数据在哪里，计算就在哪里”原则 |

在升级方案中，**VS Code 插件端**将作为 MCP Host，通过 Stdio 直接挂载本地的 Filesystem Server 和 Git Server。这种设计确保了用户在编辑器中对笔记、代码的修改能够被实时捕获，且没有任何数据离开本地机器，最大程度保障了科研数据的隐私与安全 1。

相对地，**核心智能层（LangGraph Backend）** 将部署在 Docker 容器中。为了访问外部服务（如 Arxiv 搜索、Jupyter 执行环境），它将作为 MCP Client，通过 Docker 内部网络以 SSE 方式连接到独立的 MCP Server 容器。这种设计不仅实现了微服务架构的解耦，还提供了天然的沙箱隔离——即使 Jupyter Server 在执行用户代码时崩溃，也不会影响到核心编排逻辑的稳定性 5。

### **2.2 动态工具加载与适配器模式的革新**

传统的架构中，开发者需要为每一个外部工具（如 Zotero、PubMed）编写 Python 适配器类（Adapter Classes），这种硬编码方式导致了严重的维护负担 1。在 MCP 架构下，我们引入 langchain-mcp-adapters 库来实现工具的动态加载与注入。

通过 MCP 的 list\_tools 协议，LangGraph Agent 可以在启动时自动扫描所有连接的 MCP Servers，并将发现的功能动态注册为 LangChain 的 BaseTool 对象 1。这意味着，当科研人员需要新增一个数据源（例如 Google Drive）时，运维人员只需部署对应的 MCP Server 容器并在配置文件中添加一行 SSE URL，后端核心代码无需任何修改即可获得新能力。这种“配置即集成”的模式极大地降低了系统演进的边际成本。

此外，MCP 的 **Prompt 资源（Prompts）** 特性允许 Server 端直接提供预设的提示词模板。例如，Zotero Server 可以内置一个 summarize-citation 的 Prompt，包含如何正确格式化 BibTeX 的指令。这意味着关于“如何使用工具”的领域知识被下沉到了工具本身，从而使通用的 Agent 变得更加轻量和专注 1。

## **3\. 全流程科研数据处理：构建自主数据智能体**

针对“全流程科研支持含数据处理”的新增需求，平台必须具备执行代码、分析数据并生成可视化结果的能力。这要求系统从单纯的文本生成转向具备**代码执行环境（Code Execution Environment）** 的架构。我们将通过集成 Jupyter MCP Server 和 Pandas MCP Server 来实现这一目标。

### **3.1 基于 Jupyter MCP 的持久化分析环境**

数据科学任务具有高度的迭代性：加载数据、探索特征、清洗数据、训练模型、评估结果。这一过程依赖于内存中的变量状态（State）。传统的 API 调用方式是无状态的，无法支持这种连续的分析流。

**Jupyter MCP Server** 的引入解决了这一痛点。作为一个运行在 Docker 容器中的 MCP Server，它允许 LangGraph Agent 通过标准协议操作 Jupyter Notebook 3。

* **持久化状态管理：** Agent 可以在一个 Session 中执行多段代码，后续的代码可以直接引用前序步骤加载的数据框（DataFrame）或训练好的模型对象。这使得 Agent 能够像人类数据科学家一样，分步骤地进行探索性数据分析（EDA）3。  
* **多模态输出处理：** Jupyter MCP 支持返回图像数据（如 Matplotlib 生成的图表）。升级后的 VS Code 前端需适配处理 Base64 编码的图像流，将其直接渲染在聊天窗口或专门的“数据面板”中，实现图文并茂的分析报告 9。  
* **沙箱安全机制：** 由于允许执行任意 Python 代码，Jupyter MCP 必须部署在受限的 Docker 容器中，配置 CPU/内存限额，并切断非必要的公网访问，仅允许通过 SSE 与 LangGraph Backend 通信。这种设计确保了数据处理的安全性 6。

### **3.2 自动化数据清洗与验证流水线**

结合 LangGraph 的编排能力，我们设计了一个专门的 **"Data Engineer" 子图（Subgraph）**，用于自动化处理科研数据的清洗任务 12。

该流水线包含以下关键节点：

1. **数据画像（Profiling Node）：** 调用 Pandas MCP 读取上传的 CSV/Excel 文件，生成统计摘要（缺失值比例、数据类型分布、异常值检测）14。  
2. **策略规划（Planning Node）：** 基于画像结果，LLM 推理出清洗策略（例如：“列 A 缺失率 \< 5%，建议用中位数填充；列 B 为非结构化文本，建议提取关键词”）。  
3. **人机交互（HITL Node）：** 利用 MCP 的 **Sampling（采样）** 机制，将清洗计划发送给用户确认。用户可以在 VS Code 中批准或修改策略 1。  
4. **代码执行（Execution Node）：** 获得批准后，Agent 生成相应的 Python 代码并通过 Jupyter MCP 执行。  
5. **质量验证（Validation Node）：** 执行断言检查（如 assert df.isnull().sum().sum() \== 0），确保清洗后的数据符合预期，并自动保存为新版本 15。

这一流程将繁琐的数据预处理工作转化为“对话-确认”的简洁交互，极大提升了科研效率。

## **4\. 跨学科巨著管理：知识图谱与分层智能体架构**

针对“书籍辅助撰写与跨学科巨著管理”的需求，系统面临的最大挑战是长篇内容的**叙事一致性（Narrative Consistency）** 和跨学科知识的**语义关联**。传统的向量检索（Vector RAG）在处理长文本时存在“中间丢失”现象，且难以捕捉复杂的实体关系。因此，我们需要引入 **GraphRAG（基于图谱的检索增强生成）** 和 **分层智能体（Hierarchical Agent）** 架构。

### **4.1 基于 Obsidian 与 Neo4j 的双层知识库架构**

为了管理跨学科的复杂知识，我们构建了一个双层知识库体系：

1. 交互层：Obsidian MCP Server  
   Obsidian 作为用户的一级知识库和写作界面，通过 obsidian-mcp-server 暴露给 Agent 16。  
   * **能力：** 提供了 read\_note、search\_vault（全文搜索）以及 get\_backlinks（获取反向链接）等工具。  
   * **场景：** 当 Agent 撰写新章节时，它可以实时读取用户在 Obsidian 中维护的“设定集”或“灵感笔记”。反向链接功能允许 Agent 查找某个概念在哪些文档中被提及，从而在写作时建立跨文档的引用 18。  
2. 逻辑层：Neo4j Knowledge Graph  
   对于长篇巨著，单纯的 Markdown 文件难以维护复杂的人物关系、时间线和因果逻辑。我们引入 Neo4j MCP Server 构建深层知识图谱 20。  
   * **实体同步：** 开发一个后台 Agent，定期解析 Obsidian 笔记，提取实体（人物、地点、理论、事件）及其关系，通过 text2cypher 写入 Neo4j 数据库 22。  
   * **一致性检查：** 在写作过程中，Agent 可以执行 Cypher 查询（例如：“查找所有在 1990 年之前发生的涉及人物 A 的事件”），以确保新生成的文本与既定事实不冲突。这种基于图谱的逻辑校验是实现“巨著管理”的核心技术 24。

### **4.2 分层写作智能体系统（The "Writer's Room" Pattern）**

为了应对长篇写作的复杂性，我们在 LangGraph 中实现了一个**分层监督（Hierarchical Supervisor）** 架构，模拟人类的编辑部工作流 26。

* **架构师（The Architect \- Supervisor）：**  
  * **职责：** 维护全书的大纲、核心主题和章节进度。它不直接写作，而是负责拆解任务和调度子智能体。  
  * **状态管理：** 持有全局状态（Global State），包括已完成章节的摘要、未解决的伏笔列表。  
* **档案员（The Archivist \- Consistency Worker）：**  
  * **职责：** 负责“世界观一致性”。在写作开始前，它会调用 Neo4j MCP 和 Obsidian MCP，检索当前章节涉及的人物小传、地理环境设定和前文提及的细节。  
  * **输出：** 生成一份“上下文简报（Context Brief）”，注入到写作 Agent 的上下文中。  
* **起草者（The Drafter \- Prose Worker）：**  
  * **职责：** 专注于特定章节或场景的文本生成。它接收架构师的任务和档案员的简报，生成高质量的草稿。  
* **评论家（The Critic \- Review Worker）：**  
  * **职责：** 根据预设的风格指南（Style Guide）和学术规范，对草稿进行评审。它可以指出逻辑漏洞、风格不统一或引用缺失，并将修改意见反馈给起草者进行迭代 28。

这种分层架构有效地突破了 LLM 的上下文窗口限制，通过将长任务分解为独立的子任务，并利用知识图谱维持全局一致性，从而实现了对跨学科巨著的有效管理。

## **5\. 自动化文献综述：Elicit 与 Zotero 的深度集成**

“全流程科研支持”要求平台能够自动化地进行文献发现、筛选、阅读和管理。我们将通过集成 Elicit（智能检索）和 Zotero（文献管理）来实现这一闭环。

### **5.1 Elicit 的 API 封装与集成策略**

虽然目前 Elicit 尚未发布官方的 MCP Server，但我们可以通过封装其 API（或使用 Selenium/Puppeteer 进行无头浏览器操作，作为临时方案）来构建一个 **Custom Elicit MCP Server** 30。

* **功能封装：** 该 Server 应暴露 find\_papers（基于语义问题的检索）、extract\_claims（提取论文核心观点）和 screen\_papers（基于标准的筛选）等工具。  
* **工作流集成：** 在 LangGraph 中，当用户提出一个模糊的研究问题时，Agent 首先调用 Elicit 进行发散性搜索，获取候选论文列表。然后，利用 LLM 对 Elicit 返回的摘要进行二次筛选，识别出高价值文献 32。

### **5.2 Zotero 的双向同步与全文解析**

**Zotero MCP Server** 是连接外部文献与本地知识库的桥梁 8。

* **写入与归档：** 经过 Elicit 筛选出的论文，Agent 可以调用 zotero\_create\_item 将其元数据自动存入用户的 Zotero 库中，并自动下载 PDF 附件 35。  
* **深度阅读与提取：** 利用 Zotero 的本地 PDF 解析能力，Agent 可以调用 zotero\_item\_fulltext 读取全文，或者调用 zotero\_get\_annotations 获取用户在阅读时的高亮和批注 35。  
* **引用注入：** 在写作阶段，Agent 可以通过 zotero\_search\_items 查找参考文献，并以正确的 Citation Key 格式（如 \[@author2023\]）插入到 Markdown 草稿中，确保学术写作的规范性。

## **6\. 实施指南与系统迁移路线图**

为了平稳地将现有系统升级到 V2.0 架构，建议遵循“绞杀者模式（Strangler Fig Pattern）”，分四个阶段逐步实施。

### **第一阶段：基础连接与协议升级（Weeks 1-4）**

* **目标：** 建立 Docker 化环境，验证 SSE 通信，替换基础文件操作。  
* **行动：**  
  1. 部署 **MCP Gateway**（Nginx/Traefik），配置 Docker 内部网络的 SSE 路由。  
  2. 在 FastAPI 后端引入 langchain-mcp-adapters，移除原有的 PaperFetcher 等硬编码类。  
  3. 部署 **Filesystem MCP**（Stdio 模式连接 VS Code）和 **Zotero MCP**（SSE 模式连接 Backend），验证双端连接通畅。  
* **交付物：** 一个能够通过 MCP 协议读取本地文件并查询 Zotero 库的最小可行性产品（MVP）。

### **第二阶段：数据智能层建设（Weeks 5-8）**

* **目标：** 实现 Python 代码执行与数据清洗流水线。  
* **行动：**  
  1. 构建并部署加固的 **Jupyter MCP Server** 容器（限制 CPU/RAM，网络隔离）。  
  2. 在 LangGraph 中开发 **Data Engineer Subgraph**，实现从 Profiling 到 Validation 的全自动流程。  
  3. 升级 VS Code 插件 UI，支持渲染来自 Jupyter 的 Base64 图像数据。  
* **交付物：** 具备上传 CSV、自动清洗数据并生成可视化报表能力的科研 Agent。

### **第三阶段：写作引擎与知识图谱（Weeks 9-12）**

* **目标：** 支持长篇写作与一致性管理。  
* **行动：**  
  1. 部署 **Obsidian MCP Server** 和 **Neo4j MCP Server**。  
  2. 开发 **Sync Agent**，实现 Obsidian 笔记到 Neo4j 图谱的单向同步与实体提取。  
  3. 实现 **Hierarchical Writer Agent**（架构师-档案员-起草者-评论家）的多智能体编排逻辑。  
* **交付物：** 一个能够生成长篇章节并自动进行事实一致性检查的写作辅助系统。

### **第四阶段：全链路集成与跨学科协同（Weeks 13+）**

* **目标：** 打通文献-数据-写作的完整闭环。  
* **行动：**  
  1. 封装并部署 **Elicit MCP Server**（API Wrapper）。  
  2. 构建“引用注入”工作流：写作 Agent 提出论点 \-\> 研究 Agent 检索 Elicit \-\> 档案员存入 Zotero \-\> 写作 Agent 插入引用。  
  3. 进行跨学科压力测试，验证系统在处理大规模异构数据时的稳定性。  
* **交付物：** 完整的 V2.0 智能科研操作系统，支持从选题发现到论文初稿生成的端到端自动化。

## **7\. 结论**

本次架构升级并非简单的功能堆砌，而是对科研工作流及其底层支撑系统的深度重构。通过采用 **MCP 混合传输架构**，我们解决了工具集成的标准化与安全性问题；通过 **LangGraph 分层编排**，我们赋予了系统处理长篇复杂任务的认知能力；通过集成 **Jupyter 与 Knowledge Graph**，我们将单纯的文本生成提升为具备数据执行力与逻辑一致性的科研生产力。

Architecture V2.0 将使平台从一个被动的辅助工具进化为主动的科研合作伙伴。它不仅能够“回答问题”，更能“执行研究”、“管理知识”和“协助创作”。这一转型将极大地释放科研人员的创造力，使他们能够从繁琐的数据清洗和格式调整中解脱出来，专注于跨学科的创新与深度的思想构建。随着这一架构的落地，平台将成为 Agentic Science（智能体科学）时代的标杆性基础设施。

---

参考文献索引：  
1 现有架构评估与 MCP 升级建议  
3 Jupyter MCP Server 功能与架构  
14 Pandas MCP Server 数据分析能力  
26 LangGraph 分层智能体与监督者模式  
16 Obsidian MCP Server 集成方案  
20 Neo4j 知识图谱与 GraphRAG 技术  
8 Zotero MCP 文献管理集成  
30 Semantic Scholar 与 Elicit 科研搜索集成  
2 MCP Sampling (HITL) 机制  
4 Stdio 与 SSE 传输协议对比与应用

#### **Works cited**

1. MCP 技术升级与改进建议  
2. MCP elicitation: Request user input at runtime \- WorkOS, accessed January 20, 2026, [https://workos.com/blog/mcp-elicitation](https://workos.com/blog/mcp-elicitation)  
3. MCP Jupyter: AI-Powered Machine Learning and Data Science | goose, accessed January 20, 2026, [https://block.github.io/goose/blog/2025/08/04/mcp-jupyter-server/](https://block.github.io/goose/blog/2025/08/04/mcp-jupyter-server/)  
4. Build Your First MCP Server in 15 Minutes (Complete Code), accessed January 20, 2026, [https://medium.com/data-science-collective/build-your-first-mcp-server-in-15-minutes-complete-code-d63f85c0ce79](https://medium.com/data-science-collective/build-your-first-mcp-server-in-15-minutes-complete-code-d63f85c0ce79)  
5. Discovering MCP Servers in Python | CodeSignal Learn, accessed January 20, 2026, [https://codesignal.com/learn/courses/developing-and-integrating-a-mcp-server-in-python/lessons/getting-started-with-fastmcp-running-your-first-mcp-server-with-stdio-and-sse](https://codesignal.com/learn/courses/developing-and-integrating-a-mcp-server-in-python/lessons/getting-started-with-fastmcp-running-your-first-mcp-server-with-stdio-and-sse)  
6. Introducing The pgEdge Postgres MCP Server \- And How to Connect it to Claude Code and Cursor, accessed January 20, 2026, [https://www.pgedge.com/blog/introducing-the-pgedge-postgres-mcp-server](https://www.pgedge.com/blog/introducing-the-pgedge-postgres-mcp-server)  
7. Postgres MCP Pro provides configurable read/write access and performance analysis for you and your AI agents. \- GitHub, accessed January 20, 2026, [https://github.com/crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp)  
8. Jupyter MCP \- Jan.ai, accessed January 20, 2026, [https://www.jan.ai/docs/desktop/mcp-examples/data-analysis/jupyter](https://www.jan.ai/docs/desktop/mcp-examples/data-analysis/jupyter)  
9. Jupyter MCP Server by datalayer \- Glama.ai, accessed January 20, 2026, [https://glama.ai/mcp/servers/@datalayer/jupyter-mcp-server](https://glama.ai/mcp/servers/@datalayer/jupyter-mcp-server)  
10. How to Use Jupyter MCP Server? \- Analytics Vidhya, accessed January 20, 2026, [https://www.analyticsvidhya.com/blog/2025/05/jupyter-mcp-server/](https://www.analyticsvidhya.com/blog/2025/05/jupyter-mcp-server/)  
11. marlonluo2018/pandas-mcp-server \- GitHub, accessed January 20, 2026, [https://github.com/marlonluo2018/pandas-mcp-server](https://github.com/marlonluo2018/pandas-mcp-server)  
12. Multi-Agentic AI Data Cleaning Solution — Part 1 | by Suijth Somanunnithan | Medium, accessed January 20, 2026, [https://medium.com/@sujith.adr/multi-agentic-ai-data-cleaning-solution-d3636663bc43](https://medium.com/@sujith.adr/multi-agentic-ai-data-cleaning-solution-d3636663bc43)  
13. Build a Data Cleaning & Validation Pipeline in Under 50 Lines of Python \- Analytics Vidhya, accessed January 20, 2026, [https://www.analyticsvidhya.com/blog/2025/07/data-cleaning-pipeline/](https://www.analyticsvidhya.com/blog/2025/07/data-cleaning-pipeline/)  
14. Mastering AI-Driven Data Analysis: A Deep Dive into the pandas-mcp-server \- Skywork.ai, accessed January 20, 2026, [https://skywork.ai/skypage/en/Mastering%20AI-Driven%20Data%20Analysis%3A%20A%20Deep%20Dive%20into%20the%20pandas-mcp-server/1972822954112380928](https://skywork.ai/skypage/en/Mastering%20AI-Driven%20Data%20Analysis%3A%20A%20Deep%20Dive%20into%20the%20pandas-mcp-server/1972822954112380928)  
15. Revolutionizing Data Science with AI: Gemini CLI \+ Jupyter MCP Server Workflow \- Titanic \- Machine Learning from Disaster | Kaggle, accessed January 20, 2026, [https://www.kaggle.com/competitions/titanic/discussion/607974](https://www.kaggle.com/competitions/titanic/discussion/607974)  
16. Getting Started with Obsidian MCP Server: A Comprehensive Guide | by Asaki Sakamoto | Towards AGI | Medium, accessed January 20, 2026, [https://medium.com/towards-agi/getting-started-with-obsidian-mcp-server-a-comprehensive-guide-6f44ba3fb279](https://medium.com/towards-agi/getting-started-with-obsidian-mcp-server-a-comprehensive-guide-6f44ba3fb279)  
17. cyanheads/obsidian-mcp-server: Obsidian Knowledge-Management MCP (Model Context Protocol) server that enables AI agents and development tools to interact with an Obsidian vault. It provides a comprehensive suite of tools for reading, writing, searching, and managing notes, tags, and frontmatter, acting as a bridge to \- GitHub, accessed January 20, 2026, [https://github.com/cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server)  
18. New MCP for Obsidian: richer tools for tags, links, frontmatter, and search, accessed January 20, 2026, [https://forum.obsidian.md/t/new-mcp-for-obsidian-richer-tools-for-tags-links-frontmatter-and-search/108798](https://forum.obsidian.md/t/new-mcp-for-obsidian-richer-tools-for-tags-links-frontmatter-and-search/108798)  
19. Let AI auto backlink for you | Obsidian MCP Update : r/ObsidianMD \- Reddit, accessed January 20, 2026, [https://www.reddit.com/r/ObsidianMD/comments/1lul7xp/let\_ai\_auto\_backlink\_for\_you\_obsidian\_mcp\_update/](https://www.reddit.com/r/ObsidianMD/comments/1lul7xp/let_ai_auto_backlink_for_you_obsidian_mcp_update/)  
20. Implementing Neo4j GraphRAG Retrievers as MCP Server \- Graph Database & Analytics, accessed January 20, 2026, [https://neo4j.com/blog/developer/neo4j-graphrag-retrievers-as-mcp-server/](https://neo4j.com/blog/developer/neo4j-graphrag-retrievers-as-mcp-server/)  
21. The Fastest Path To Building An Agent For Your Knowledge Graph Is By Using MCP, accessed January 20, 2026, [https://www.youtube.com/watch?v=sBf8TJgqdwY](https://www.youtube.com/watch?v=sBf8TJgqdwY)  
22. How to Convert Unstructured Text to Knowledge Graphs Using LLMs \- Neo4j, accessed January 20, 2026, [https://neo4j.com/blog/developer/unstructured-text-to-knowledge-graph/](https://neo4j.com/blog/developer/unstructured-text-to-knowledge-graph/)  
23. Effortless RAG With Text2CypherRetriever \- Neo4j, accessed January 20, 2026, [https://neo4j.com/blog/developer/effortless-rag-text2cypherretriever/](https://neo4j.com/blog/developer/effortless-rag-text2cypherretriever/)  
24. AI-Driven Storytelling with Multi-Agent LLMs \- Part III \- The Computist Journal, accessed January 20, 2026, [https://blog.apiad.net/p/ai-driven-storytelling-with-multi-3ed](https://blog.apiad.net/p/ai-driven-storytelling-with-multi-3ed)  
25. Using AI to Generate Your Stories is NOT THE BEST WAY TO USE AI. The Best Way is Using Knowledge Graphs Combined With AI \- Reddit, accessed January 20, 2026, [https://www.reddit.com/r/AIAssisted/comments/1q0i9qc/using\_ai\_to\_generate\_your\_stories\_is\_not\_the\_best/](https://www.reddit.com/r/AIAssisted/comments/1q0i9qc/using_ai_to_generate_your_stories_is_not_the_best/)  
26. What are Hierarchical AI Agents? \- IBM, accessed January 20, 2026, [https://www.ibm.com/think/topics/hierarchical-ai-agents](https://www.ibm.com/think/topics/hierarchical-ai-agents)  
27. Hierarchical Agent Teams \- GitHub Pages, accessed January 20, 2026, [https://langchain-ai.github.io/langgraph/tutorials/multi\_agent/hierarchical\_agent\_teams/](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)  
28. How to Build an AI Content Workflow: 5-Tool Step-by-Step Guide, accessed January 20, 2026, [https://www.ai.cc/blogs/ai-content-workflow-step-by-step-guide/](https://www.ai.cc/blogs/ai-content-workflow-step-by-step-guide/)  
29. LangGraph: Building Self-Correcting RAG Agent for Code Generation, accessed January 20, 2026, [https://learnopencv.com/langgraph-self-correcting-agent-code-generation/](https://learnopencv.com/langgraph-self-correcting-agent-code-generation/)  
30. Introducing Elicit Systematic Review, accessed January 20, 2026, [https://elicit.com/blog/systematic-review/](https://elicit.com/blog/systematic-review/)  
31. Elicit AI Research Assistant Tutorial (2026) \- YouTube, accessed January 20, 2026, [https://www.youtube.com/watch?v=Xj3RtBADb60](https://www.youtube.com/watch?v=Xj3RtBADb60)  
32. \[2403.08399\] System for systematic literature review using multiple AI agents: Concept and an empirical evaluation \- arXiv, accessed January 20, 2026, [https://arxiv.org/abs/2403.08399](https://arxiv.org/abs/2403.08399)  
33. Systematic Literature Reviews | Elicit: Al for scientific research, accessed January 20, 2026, [https://elicit.com/solutions/literature-review](https://elicit.com/solutions/literature-review)  
34. Zotero MCP: AI Integration for Smart Reference Management, accessed January 20, 2026, [https://mcpmarket.com/server/zotero-4](https://mcpmarket.com/server/zotero-4)  
35. Zotero MCP: Connects your Zotero research library with Claude and other AI assistants via the Model Context Protocol to discuss papers, get summaries, analyze citations, and more. \- GitHub, accessed January 20, 2026, [https://github.com/54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)  
36. Zotero MCP | Your Research Library in Claude \- Yiyang (Steven) Yu, accessed January 20, 2026, [https://stevenyuyy.us/zotero-mcp/](https://stevenyuyy.us/zotero-mcp/)  
37. Building Multi-Agent Systems with LangGraph — A Comprehensive Guide | by S Sankar, accessed January 20, 2026, [https://levelup.gitconnected.com/building-multi-agent-systems-with-langgraph-a-comprehensive-guide-c20ba96ab3ba](https://levelup.gitconnected.com/building-multi-agent-systems-with-langgraph-a-comprehensive-guide-c20ba96ab3ba)  
38. jianruidutong/obsidian-mcp \- NPM, accessed January 20, 2026, [https://www.npmjs.com/package/%40jianruidutong%2Fobsidian-mcp](https://www.npmjs.com/package/%40jianruidutong%2Fobsidian-mcp)  
39. Unleash Your Second Brain: A Deep Dive into the Obsidian MCP Server by newtype-01, accessed January 20, 2026, [https://skywork.ai/skypage/en/obsidian-mcp-server/1978708761422450688](https://skywork.ai/skypage/en/obsidian-mcp-server/1978708761422450688)  
40. A2A, MCP, Knowledge Graphs, and GraphRAG for Next-Generation Intelligent Systems | by Vishal Mysore | Nov, 2025, accessed January 20, 2026, [https://medium.com/@visrow/a2a-mcp-knowledge-graphs-and-graphrag-for-next-generation-intelligent-systems-9954d9ded8ee](https://medium.com/@visrow/a2a-mcp-knowledge-graphs-and-graphrag-for-next-generation-intelligent-systems-9954d9ded8ee)  
41. Zotero MCP Server by kujenga \- Glama, accessed January 20, 2026, [https://glama.ai/mcp/servers/@kujenga/zotero-mcp](https://glama.ai/mcp/servers/@kujenga/zotero-mcp)  
42. Semantic Scholar \- Awesome MCP Servers, accessed January 20, 2026, [https://mcpservers.org/servers/FujishigeTemma/semantic-scholar-mcp](https://mcpservers.org/servers/FujishigeTemma/semantic-scholar-mcp)  
43. Elevate Your Research: Top Elicit Alternatives You Should Know | by ByteBridge \- Medium, accessed January 20, 2026, [https://bytebridge.medium.com/elevate-your-research-top-elicit-alternatives-you-should-know-015575b17bb8](https://bytebridge.medium.com/elevate-your-research-top-elicit-alternatives-you-should-know-015575b17bb8)  
44. Elicitation \- Model Context Protocol, accessed January 20, 2026, [https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)  
45. Build Voice Agents With MCP: The Top 4 Frameworks and APIs, accessed January 20, 2026, [https://medium.com/@amosgyamfi/build-voice-agents-with-mcp-the-top-4-frameworks-and-apis-1d86f1bb1381](https://medium.com/@amosgyamfi/build-voice-agents-with-mcp-the-top-4-frameworks-and-apis-1d86f1bb1381)