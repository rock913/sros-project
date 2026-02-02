# SROS V2.1.5 开发全手册：科研自动化操作系统

**版本**: V2.1.5 (Agentic & Serverless)
**核心哲学**: 以稿件为中心，以 MCP 为触手，以 Roo Code 为大脑。
**代号**: "Growing Doc"

## 0. 瘦身重构计划 (The Great Purge)

鉴于项目架构已从“重后端应用”转向“Serverless Agent配置”，当前代码库存在大量冗余。

### 0.1 归档策略
我们将创建一个 `legacy_v1_archive/` 目录，将以下不再直接维护的模块移入，作为参考库：

*   ❌ **`backend/`**: 原 LangGraph Python 后端（包含 StateGraph, FastAPI, Dockerfile）。
    *   *迁移价值*: 保留 `src/agent/domain/schemas` 中的 Pydantic 模型作为 MCP 开发参考。
*   ❌ **`frontend/`**: 原 React 前端。
*   ❌ **`vscode-extension/`**: 原独立插件源码（现有架构直接复用 Roo Code，无需自研插件 Host）。
*   ❌ **`docker-compose*.yml`**: 不再需要编排容器服务。

### 0.2 保留与新生
项目根目录将只保留以下轻量级结构：

```
.
├── .roomodes                  # Roo Code 角色定义 (Brain)
├── .clinerules                # 全局行为准则
├── mcp_servers/               # 能力平面 (Tools)
│   ├── zotero-expert/
│   ├── semantic-scholar/
│   └── manuscript-manager/    # 核心自研
├── doc/                       # 核心文档
└── workspace/                 # 用户科研工作区示例
```

---

## 1. 架构总览 (System Architecture)

SROS 摒弃了复杂的后端服务器（LangGraph），采用 **双平面模型 (Two-Plane Model)**。

### 1.1 控制平面 (Control Plane - The Brain)
*   **载体**: Roo Code / Cline (VS Code Extension).
*   **职责**: 任务规划、CoT 推理、决策（决定何时检索、何时扩写）、人机交互。
*   **逻辑存储**: 所有的编排逻辑存储在 `.roomodes` 和 `.clinerules` 中。

### 1.2 能力平面 (Capability Plane - The Tools)
*   **载体**: 遵循 Model Context Protocol (MCP) 的标准服务器。
*   **职责**: 执行具体的 I/O 操作（学术检索、文件结构化读写、数据库存取）。
*   **原则**: 尽量使用成熟的社区服务器，仅自研核心科研逻辑。

## 2. 核心工作流：稿件驱动型调研 (Draft-Driven Discovery)

系统不再是“先检索再写作”，而是“边写边补”。

1.  **观察 (Observe)**: Roo Code 调用 `manuscript-mcp` 获取当前 Markdown 的结构树。
2.  **检测 (Detect)**: 识别稿件中的 Gap (空白)。
    *   *显式*：`[TODO: 补充实验数据]`。
    *   *隐式*：段落过短、逻辑跳跃、缺乏引文。
3.  **检索 (Retrieve)**: 针对特定 Gap，调用 `scholar-mcp` (Semantic Scholar) 寻找证据。
4.  **构建 (Build)**: 将文献关系（CiTO 本体论）存入本地 `.sros/graph.db`。
5.  **扩写 (Expand)**: 调用 `manuscript-mcp` 的原子编辑工具，在指定章节插入带有引文的内容。
6.  **迭代 (Loop)**: 重新扫描稿件，检查 Gap 是否消除。

## 3. 工具链集成方案 (MCP Ecosystem)

为了避免重复造轮子，SROS 集成以下成熟服务器：

### 3.1 学术检索与文献
*   **Server**: `@fegizii/mcp-server-semanticscholar`
    *   *用途*: 搜索论文、获取 Citation Context (引文语境)、下载 PDF。
*   **Server**: `zotero-mcp` (Enhanced)
    *   *用途*: 读取本地 Zotero 库，确保引文 key 一致；回写 AI 笔记。

### 3.2 稿件操作 (核心)
*   **Server**: `quantalogic-markdown-mcp` (或自研 `manuscript-manager`)
    *   *用途*: 这是最核心的工具。支持 `edit_section`（基于标题的章节编辑）和原子化修改，确保 Roo Code 不会破坏大文件。

### 3.3 局部知识图谱 (Local Memory)
*   **Server**: `mcp-duckdb-memory-server`
    *   *用途*: 在项目目录下 `.sros/` 中建立 DuckDB。用于存储文献间的三元组关系（如：Paper A -> critiques -> Paper B）。

### 3.4 自研逻辑扩展 (Custom SROS Server)
*   **Server**: `mcp-sros-logic` (Python 实现)
    *   *职责*:
        *   `init_workspace()`: 初始化 `.sros` 目录。
        *   `detect_academic_gaps()`: 基于学术规则检测稿件薄弱环节。

## 4. 存储与状态管理 (SROS Workspace)

系统采用 **Filesystem-as-Database**。每个科研项目是一个独立的隔离空间。

```
/Project_Folder/
├── .sros/                 # 隐藏状态目录
│   ├── graph.db           # 本地局部知识图谱 (DuckDB)
│   └── research_log.jsonl # 检索历史记录 (避免重复消耗 Token)
├── .roomodes              # 针对当前项目的 Roo Code 行为定义
├── draft.md               # 唯一的真理来源 (Single Source of Truth)
└── references/            # 调研下载的 PDF 剪辑
```

## 5. 开发重心：Prompt 工程 (.roomodes)

由于移除了 Python 后端编排，逻辑下沉到提示词中。

### 5.1 角色定义
*   **Researcher Mode**: 侧重于广度检索，更新 `.sros/graph.db`，不修改稿件。
*   **Writer Mode**: 侧重于根据图谱和检索结果，使用 `manuscript-mcp` 更新正文。

### 5.2 核心指令示例 (System Prompt)
> "你当前的模式是 SROS-Writer。在开始写作前，必须执行 `get_structure`。你必须在每个段落结尾检查是否引用了正确的 `[@citekey]`。如果发现逻辑断裂，必须自动激活 Researcher 模式进行深挖。"

## 6. 实施路线图 (Roadmap)

### 阶段 1: 基础设施连接 (Weeks 1-2)
- [ ] **执行大清理**: 建立 `legacy_archive`，移除过时代码。
- [ ] **集成 MCP**: 配置 `semantic-scholar` 和 `markdown-manager`。
- [ ] **自研核心**: 编写 `mcp-sros-logic`，实现项目初始化逻辑。

### 阶段 2: 知识闭环 (Weeks 3-4)
- [ ] **DuckDB 模型**: 在 DuckDB 中建立 CiTO (Citation Typing Ontology) 表结构。
- [ ] **Prompt 调优**: 编写 `.roomodes`，教会 Roo Code 从 DuckDB 读取关联关系来写综述。

### 阶段 3: 体验优化 (Weeks 5+)
- [ ] **决策卡片**: 利用 MCP `sampling` (input_request) 功能询问用户优先阅读哪篇论文。
- [ ] **内容解析**: 集成本地 PDF 解析，提取高亮部分存入图谱。

## 7. 避坑指南
1.  **不要在 Prompt 里存数据**: 大量的文献信息必须存入 `graph.db`，Agent 仅按需查询，否则会触发上下文爆炸。
2.  **原子化编辑**: 绝对禁止 Agent 使用 `writeFile` 覆盖全文，必须使用 `edit_section`。
3.  **Local-First**: 所有的 `graph.db` 必须放在项目内，支持 Git 版本控制，方便跨设备同步。
