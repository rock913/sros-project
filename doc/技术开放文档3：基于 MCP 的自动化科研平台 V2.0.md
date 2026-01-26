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

### **3.1 智能文献调研 (The Discovery Loop)**
1.  **Intent Recognition**: Supervisor 解析用户模糊指令。
2.  **Parallel Search**: Librarian 调用 Academic Server 并行检索。
3.  **HITL Filter**: 推送 **Refinement Card** 至前端，用户勾选 ROI (Interest) 文献。
4.  **Ingestion**: 自动下载 PDF 并通过 Unpaywall 校验版权，存入 Zotero。

### **3.2 知识图谱构建 (The Knowledge Graph)**
*   **技术栈**: Neo4j + GraphRAG。
*   **逻辑**: Analyst 读取 PDF，提取 (Entity) -> [Relation] -> (Entity) 三元组。
*   **引用本体**: 遵循 **CiTO (Citation Typing Ontology)**，区分 `citesAsEvidence` (作为证据) 与 `citesAsAuthority` (作为权威)。

### **3.3 写作与自我反思 (The Reflexion Loop)**
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

### **5.2 阶段 2: 学术调研闭环 (Alpha - Discovery Loop)**
**目标**: 完成“用户提问 -> 搜索 Arxiv -> 生成简报”的单线程闭环。
*   [ ] **MCP Tool 挂载**: 将 `ArxivRetriever` 封装为标准 MCP Tool 供 Agent 调用。
*   [ ] **Zotero 基础集成**: 实现 `check_zotero_items` 工具，确保能读取本地条目。
*   [ ] **UI 组件**: 开发基础的 "Reference List" Webview，展示检索到的论文列表。

### **5.3 阶段 3: 高级编排与深度写作 (Beta - Writer's Room)**
**目标**: 启用多智能体协作与长文本生成。
*   [ ] **Writer's Room 迁移**: 将单体 Agent 拆分为 Librarian/Analyst/Scribe。
*   [ ] **决策卡片 (Decision Cards)**: 实现前端交互组件，允许用户干预 Agent 路径（如选择具体论文）。
*   [ ] **PDF 解析**: 集成非结构化 PDF 解析能力，构建向量索引。

## **第 6 章：安全与隐私**
*   **Local First**: 默认通过 Stdio 运行本地 MCP Server，敏感数据不出域。
*   **Token Management**: 所有 API Key 仅存储于 `.env`，禁止硬编码。
*   **Container Sandboxing**: 复杂推理与 Python 代码执行强制在 Docker 容器中运行。