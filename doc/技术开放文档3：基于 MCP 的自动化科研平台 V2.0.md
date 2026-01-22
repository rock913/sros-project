# **技术开放文档：基于 MCP 的自动化科研平台 V2.0**

## **第 1 章：愿景与核心理念**

本规划旨在将科研平台从单一的“VS Code 插件”进化为**基于模型上下文协议 (MCP) 的分布式智能科研操作系统**。

通过引入 MCP 协议，我们实现了核心智能（LangGraph）与工具能力（Tools）的解耦。同时，平台采用 **MPA (MetaGPT \+ PydanticAI \+ Aider)** 架构进行自主演进，利用 GitHub Copilot 作为架构师，Aider (Qwen Max) 作为构建者，实现 AI 驱动的自我开发与优化。首要任务是打通\*\*“文献调研 \-\> 知识内化 \-\> 自动化写作”\*\*的科研闭环，将平台从“聊天机器人”升格为“上下文感知的科研 IDE”。

## **第 2 章：系统架构 V2.0 (三平面模型)**

平台采用 MCP 推荐的三平面架构，确保极高的扩展性与上下文感知能力。

### **2.1 用户交互平面 (VS Code Host)**

* **角色**: 作为 MCP Host，管理本地上下文。  
* **连接方式**: 通过 Stdio 传输协议挂载本地服务。  
* **核心组件**:  
  * **Filesystem Server**: 实时读取项目 Markdown 笔记与代码。  
  * **Zotero Bridge**: 本地文献库的实时感知与引用注入。  
  * **Collaboration UI**: 基于 React 的 Webview，提供任务控制台与 AI “思考链”展示。

### **2.2 智能编排平面 (LangGraph Client)**

* **角色**: 平台大脑，负责任务拆解、状态流转与 HITL（人在环路）干预。  
* **连接方式**: 通过 SSE 连接后端能力池。  
* **核心引擎**: LangGraph，支持复杂迭代循环与持久化检查点（PostgresSaver）。

### **2.3 能力供给平面 (MCP Servers)**

* **角色**: 提供异构数据访问与特定科研功能。  
* **核心服务**:  
  * **Research Server**: 封装 Arxiv, Semantic Scholar, PubMed, CrossRef。  
  * **Observability Server**: 集成 LangSmith (追踪) 与 LangFuse (成本分析)。  
  * **Writing Server**: 基于 diff-match-patch 实现非破坏性的实时文档编辑。

## **第 3 章：核心技术栈与通信策略**

| 组件 | 技术选型 | 说明 / MCP 作用 |
| :---- | :---- | :---- |
| **开发架构** | **MPA (MetaGPT \+ PydanticAI \+ Aider)** | 实现 AI-Native 的自主开发与工具重构 (如 Unpaywall 重构) |
| **智能框架** | Python \+ LangGraph \+ PydanticAI | 利用 langchain-mcp-adapters 动态加载 Server 端工具 |
| **通信协议** | **Hybrid Strategy** | 本地隐私走 **Stdio**；重计算/外部检索走 **SSE** |
| **可观测性** | LangSmith \+ LangFuse | 专注于科研流程追踪，无需重复构建可视化链 |
| **数据库** | PostgreSQL \+ pgvector | 存储 ResearchSession、Paper、Report 等核心实体 |
| **文档编辑器** | VS Code Workspace API | AI 通过 applyEdit 实现与用户的实时协作编辑 |

## **第 4 章：核心闭环：从调研到协作写作**

我们专注于实现“文献到稿件”的无缝闭环，强调用户在关键节点的控制权。

### **4.1 智能文献发现与筛选 (Discovery & Screening)**

* **流程**: 用户提出主题 \-\> Agent 调用多源 Research MCP \-\> 生成搜索建议 \-\> **HITL 节点：用户批准/编辑检索词** \-\> 获取文献。  
* **关键特性**: 集成 PubMed 与 Semantic Scholar，支持跨学科语义搜索。

### **4.2 资源管理与历史追踪 (Management & History) ✅ 已完成**

* **状态**: 已实现 Session 管理与历史数据分析。  
* **功能**: 自动在 Zotero 中创建条目并附加 PDF；在 PostgreSQL 中持久化所有研究事件。  
* **可视化**: 实时渲染数据面板（Chart.js），展示文献分布与任务成功率。

### **4.3 人在环路 (HITL) 决策系统 (Interaction)**

* **决策点**:  
  1. **查询审批**: 在执行大规模搜索前确认检索策略。  
  2. **文献初筛**: 用户在 Webview 卡片中勾选需要深入解读的论文。  
  3. **大纲确认**: 在起草长篇报告前，由用户调整章节逻辑。

### **4.4 实时文档协作与引文归一化 (Collaborative Writing)**

* **流程**: Agent 产生 document\_update 消息 \-\> VS Code 插件接收并执行局部 WorkspaceEdit。  
* **关键技术**:  
  * 使用 diff-match-patch 进行增量更新，避免覆盖用户正在编辑的内容。  
  * **Inline Review**: 在编辑器中通过 CodeLens 提供“接受/拒绝”AI 修改的选择。  
  * **引文注入**: 自动从 Zotero MCP 获取 Citation Key 并插入标准引用格式。

## **第 5 章：开发路线图 (基于最新进展)**

### **第一阶段：后端基础与 MCP 协议升级 (已完成 ✅)**

* 搭建 FastAPI 后端与 PostgreSQL 持久化层。  
* 实现核心四阶段线性 LangGraph 代理。  
* 实现基础 Research MCP (Arxiv)。

### **第二阶段：历史管理与高级分析 (已完成 ✅)**

* 实现 ResearchSession 与 Paper 的持久化管理。  
* **数据面板**: 交付可视化 Analytics Dashboard。  
* **通信**: 打通 WebSocket 实时状态流式传输。

### **第三阶段：深度交互与写作闭环 (当前重点 🚀)**

* **目标**: 实现真正的 AI-Human 协同工作流。  
* **核心任务**:  
  1. 实现 **HITL 决策卡片** (查询审批、文献选择)。  
  2. 开发 **实时文档协同引擎** (基于 Workspace API 的非破坏性编辑)。  
  3. 集成 **LangSmith/LangFuse** 进行生产级监控。

### **第四阶段：多场景增强与数据智能 (未来阶段)**

* **目标**: 补全数据处理与跨学科管理能力。  
* **核心任务**:  
  1. **Jupyter MCP Server**: 提供沙箱环境执行代码。  
  2. **Obsidian & Neo4j**: 构建基于图谱的长篇叙事一致性校验。  
  3. **多模型适配**: 通过 LiteLLM 支持 GPT-4/Claude 3/Qwen Max 的动态切换。

## **第 6 章：工程规范与安全**

* **MPA 流程**: 遵循 Architect (Copilot) \-\> Blueprint \-\> Builder (Aider) \-\> Inspector 的闭环开发流程。  
* **沙箱隔离**: Jupyter 与外部执行环境强制运行在受限容器中。  
* **密钥管理**: 所有 API Key (如 QWEN\_API\_KEY) 严格通过 .env 注入，禁止硬编码。  
* **版本追溯**: 利用 Git Server MCP 记录 AI 代理对项目进行的每一次代码或文档修改。