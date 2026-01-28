# **技术开放文档：科研自动化操作系统 V2.1 (SROS)**

## **第 1 章：愿景与核心定义**

本规划旨在将平台从“VS Code 插件”正式升级为 **科研自动化操作系统 (Scientific Research Operating System, SROS)**。

V2.1 版本遵循 **"Native Integration" (原生集成)** 哲学，利用 MCP 协议打破工具孤岛。核心目标是构建一个 **MPA (MetaGPT + PydanticAI + Aider)** 驱动的自进化系统，打通 **“文献发现 (Discovery) -> 知识图谱 (Graph) -> 沉浸式写作 (Immersive Writing)”** 的完整闭环。

## **第 2 章：系统架构 V2.1 (六边形多平面)**

我们摒弃传统的单体分层，采用 **六边形架构 (Hexagonal Architecture)** 结合 **三平面模型**，确保业务逻辑（Domain）的纯净性与外部能力的可插拔性。

### **2.1 核心领域层 (Domain Layer - The Architect's Zone)**
*   **定位**: 纯 Python 逻辑，无 I/O 副作用。
*   **核心组件**:
    *   **Schemas**: 定义 `Paper`, `ResearchSession`, `Report` 等核心实体。
    *   **Ports (Protocols)**: 定义 `McpServer`, `LlmProvider`, `Database` 的抽象接口。
    *   **TestScenarios**: 契约驱动开发的测试用例集。

### **2.2 基础设施层 (Infrastructure Layer - The Builder's Zone)**
*   **LlmAdapter**: 基于 `litellm` 的多模型统一调用及成本监控。
*   **McpAdapters**: `langchain-mcp-adapters` 实现的动态工具挂载。
*   **Persistence**: PostgreSQL (pgvector) 存储实体，Neo4j 存储知识图谱。

### **2.3 三平面交互模型**

#### **A. 用户交互平面 (VS Code Host)**
*   **灵动大纲 (Smart Outline)**: 基于 TreeView API 的动态任务导航，显示“调研中”、“待扩写”等节点状态。
*   **沉浸式编辑器 (Main Editor)**:
    *   **Ghost Text**: 行间 AI 补全与提示。
    *   **CodeLens**: 实时引文验证与来源跳转。
*   **科研控制台 (Webview)**: 承载“决策卡片 (Decision Cards)”与多轮对话。

#### **B. 智能编排平面 (LangGraph "Writer's Room")**
采用分层多智能体架构 (**Hierarchical Multi-Agent**):
*   **Supervisor (PI)**: 任务拆解与路由 (State Machine)。
*   **Librarian**: 广度优先搜索 (arXiv, Google Scholar)。
*   **Analyst**: 深度阅读与图谱构建 (CiTO Ontology)。
*   **Scribe**: 基于 Reflexion 机制的写作与自我纠错。

#### **C. 能力供给平面 (MCP Servers)**
*   **Zotero Enhanced Server**: 双向同步，支持 PDF 高亮提取与语义搜索注入。
*   **Academic Server**: 聚合 Arxiv, Semantic Scholar, CrossRef, PubMed。
*   **FileSystem Server**: 受限的本地 Markdown/LaTeX 读写与 Git 自动版本控制。

## **第 3 章：核心业务流与技术实现**

### **3.1 智能文献调研 (The Discovery Loop - Co-STORM Enhanced)**
**核心理念**: 引入 Collaborative STORM 机制，用户作为"PI (Principal Investigator)"，观察并引导 Agent 团队的讨论。

1.  **Perspective Generation (视角发散)**: 
    *   用户输入模糊意图，Manager Agent (PI) 并不直接搜索，而是召集 Analyst 提出 3-5 个 **"Research Perspectives" (研究视角)**。
    *   *Output*: 生成初始的 **Dynamic Mind Map (动态思维导图)** 节点。
2.  **Round-Table Discussion (圆桌研讨)**:
    *   Librarian (检索员) 与 Analyst (分析员) 针对每个节点进行多轮对话。
    *   *Serendipity*: Analyst 会主动提出“反直觉问题”以挖掘 Unknown Unknowns。
    *   **UI 呈现**: 对话过程实时流式传输至 "Ghost Console"，用户可随时插入评论进行 **Steering (方向干预)**。
3.  **Mind Map Expansion (图谱生长)**:
    *   随着检索深入，新发现的 Entity/Concept 会自动从 Mind Map 节点上长出。
    *   用户可点击节点执行 **"Deep Dive" (深挖)** 或 **"Prune" (剪枝)**。
4.  **Ingestion & Evidence**: 
    *   确认有价值的节点会自动触发 PDF 下载与 Zotero 存证。

### **3.2 稿件驱动型调研 (Draft-Driven Discovery) - New
**核心理念**: 提前“写作”动作，让调研服务于“填补稿件空白”。从“文献循环”升级为**“稿件循环”**。

1.  **Dynamic Outline (动态大纲)**:
    *   根据用户意图或 Mind Map 自动生成 Markdown 大纲 (Scope)。
    *   Agent 实时监控大纲结构，如果用户手动删节，自动调整调研队列。
2.  **Gap Analysis (空白检测)**: 
    *   系统比对 [当前稿件内容] vs [写作目标]，识别出**"Evidence Gap" (证据缺失)**。
    *   *Example*: "第 2 章关于 Transformer 内存优化的论点缺乏近三年实验数据支持"。
3.  **Targeted Retrieval (定向狙击)**:
    *   触发 Discovery Loop，但不仅是搜关键词，而是带着**"Proof Goal" (论证目标)** 去搜。
4.  **Incremental Writing (增量写入)**:
    *   检索到的内容并非只存入数据库，而是直接生成一段带引用的内容插入到 Draft 的对应章节中。
    *   **Live Citation**: 自动更新 Zotero 并通过 Ghost Text 插入 `[@citekey]`。

### **3.3 知识图谱构建 (The Knowledge Graph)**
*   **技术栈**: Neo4j + GraphRAG。
*   **逻辑**: Analyst 读取 PDF，提取 (Entity) -> [Relation] -> (Entity) 三元组。
*   **引用本体**: 遵循 **CiTO (Citation Typing Ontology)**，区分 `citesAsEvidence` (作为证据) 与 `citesAsAuthority` (作为权威)。

### **3.4 写作与自我反思 (The Reflexion Loop)**
解决 AI 写作“幻觉引用”的核心机制：
1.  **Draft**: Scribe 生成包含 `[@citekey]` 的草稿。
2.  **Validate**: 系统拦截输出，调用 Zotero Server 校验 `citekey` 是否存在。
3.  **Grounding**: 检查引文内容是否支持论点 (Claim verification)。
4.  **Reflect**: 若校验失败，生成错误日志并回滚重写，直到通过验证。

## **第 4 章：工程规范与 MPA 开发流**

本项目遵循 **AI-Native** 开发模式：

### **4.1 角色定义**
*   **Architect (Copilot)**: 负责 `agent.domain` 设计，编写 Protocol 和 `@TestScenarios`。
*   **Builder (Aider)**: 负责 `agent.infrastructure` 实现，执行 TDD 循环。

### **4.2 自动化 TDD 流程**
1.  **Define**: Architect 生成 Interface 定义 (`ports/paper_repo.py`)。
2.  **Command**: 生成 `execute_tdd_loop` 指令。
3.  **Build**: Aider 读取接口，编写 `tests/test_paper_repo_impl.py` (Mock external APIs)。
4.  **Implement**: Aider 实现 `infrastructure/db/paper_repo_impl.py`。
5.  **Verify**: 自动运行 `pytest` 直至全绿。

### **4.3 MCP 架构分层设计 (MCP Layering Strategy)**

针对 **"Metatooling (Cline/Aider)"** 与 **"App Runtime (LangGraph)"** 混合使用 MCP 时可能出现的依赖冲突（如 `aider-agent` 缺少业务库报错），我们提出 **双平面隔离架构**：

#### **A. 控制平面 (Control Plane - The Builder)**
*   **主体**: `aider-agent` 容器 (VS Code 的手脚架)。
*   **职责**: 提供 **"Meta-Tools"** (构建工具)，如 `execute_tdd_loop`、`run_tests`、`git_commit`。
*   **环境原则 (Environment Parity)**: 
    *   **必须镜像 Runtime 依赖**: 虽然它是构建工具，但为了运行 `pytest`，必须安装 `pure-backend` 的所有依赖。
    *   **最佳实践**: `Dockerfile.aider` 应 COPY `pyproject.toml` 并运行 `pip install .[dev]`。
*   **反模式**: 禁止 Builder 尝试加载 App 的业务工具（如 `arxiv`）。Builder 应该调用 App 暴露的 API，而不是 import App 的代码。

#### **B. 应用平面 (Application Plane - The Runtime)**
*   **主体**: `backend` 容器 (LangGraph 运行时)。
*   **职责**: 提供 **"Domain-Tools"** (业务工具)，如 `search_arxiv`、`query_knowledge_graph`。
*   **连接方式**: VS Code 插件通过 MCP 直接连接 `backend` 获取业务能力，而不是通过 `aider-agent` 中转。

## **第 5 章：执行路线图 (Execution Roadmap)**

### **5.0 当前开发现状 (Current Status)**
*   **架构状态**: 正在进行 **Hexagonal Migration (六边形迁移)**。核心 Agent 逻辑正从散乱的脚本（`backend/src/legacy`）迁移至 `backend/src/agent/domain`（纯逻辑）与 `backend/src/agent/infrastructure`（实现层）。
*   **痛点**: 前后端通信尚未标准化，MCP Server 尚未完全接管客户端请求。
*   **当务之急**: 建立前端（VS Code Extension）与后端（LangGraph）之间稳定的 **MCP JSON-RPC 通道**。

### **5.1 阶段 1: 最小可行链路 (MVP - Connectivity)**
**目标**: 实现 VS Code "Hello World" -> LangGraph Agent -> VS Code Response 的全双工通信。
*   [ ] **协议定义**: 这里定义 `ChatRequest` 与 `ChatResponse` 的 Pydantic Schema。
*   [ ] **后端改造**: 使用 `mcp-server-py` 包装 LangGraph Entrypoint，暴露为 MCP Tool (`run_research_workflow`)。
*   [ ] **前端对接**: VS Code 插件侧实现 MCP Client，通过 Stdio 连接后端容器。
*   [ ] **验证**: 在 VS Code 侧边栏输入问题，后端日志显示接收，前端流式显示 "Thinking..." 状态。

### **5.2 阶段 2: 稿件调研闭环 (Alpha - Draft-Driven Discovery)
**目标**: 完成“用户提问 -> 动态大纲生成 -> 协作式检索 -> 局部稿件扩展”的闭环。
*   [x] **MCP Tool 挂载**: 将 `ArxivRetriever` 封装为标准 MCP Tool。
*   [x] **Discovery Graph**: 基础的检索工作流。
*   [ ] **Co-STORM Engine**:
    *   实现 `PerspectiveGenerator` 节点。
    *   实现 `DiscourseStream` (圆桌讨论流)。
*   [ ] **Gap Finder Node**: 
    *   实现“稿件空白检测”逻辑，输出具体的 `EvidenceGoal`。
*   [ ] **Incremental Writer**:
    *   实现“局部段落生成器”，支持 Markdown 注入。
*   [ ] **UI 组件升级**: 
    *   升级 Webview 为“三栏式”布局：[Outline | Editor | Agent Console]。
    *   实现 **"Steering Controls"**: 允许用户对 Agent 的 Plan 进行 Accept/Reject。

### **5.3 阶段 3: 高级编排与深度写作 (Beta - Writer's Room)**
**目标**: 启用多智能体协作与长文本生成。
*   [ ] **Writer's Room 迁移**: 将单体 Agent 拆分为 Librarian/Analyst/Scribe。
*   [ ] **决策卡片 (Decision Cards)**: 实现前端交互组件，允许用户干预 Agent 路径（如选择具体论文）。
*   [ ] **PDF 解析**: 集成非结构化 PDF 解析能力，构建向量索引。

## **第 6 章：安全与隐私**
*   **Local First**: 默认通过 Stdio 运行本地 MCP Server，敏感数据不出域。
*   **Token Management**: 所有 API Key 仅存储于 `.env`，禁止硬编码。
*   **Container Sandboxing**: 复杂推理与 Python 代码执行强制在 Docker 容器中运行。