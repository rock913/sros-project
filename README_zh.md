# Gemini Fullstack LangGraph 快速入门

本项目演示了一个全栈应用程序，它使用 React 前端和由 LangGraph 驱动的后端代理。该代理旨在通过动态生成搜索词条、使用 Google 搜索查询网络、反思结果以识别知识差距，并迭代优化其搜索，直到能够提供有引文支持的完善答案，从而对用户查询进行全面研究。此应用程序是使用 LangGraph 和 Google 的 Gemini 模型构建研究增强型对话式人工智能的一个示例。

<img src="./app.png" title="Gemini Fullstack LangGraph" alt="Gemini Fullstack LangGraph" width="90%">

## 功能

- 💬 带有 React 前端和 LangGraph 后端 的全栈应用程序。
- 🧠 由 LangGraph 代理提供支持，用于高级研究和对话式人工智能。
- 🔍 使用 Google Gemini 模型动态生成搜索查询。
- 🌐 通过 Google Search API 集成网络研究。
- 🤔 反思性推理以识别知识差距并优化搜索。
- 📄 生成带有从收集来源中引用的答案。
- 🔄 在开发过程中为前端和后端提供热重载。

## 项目结构

该项目分为两个主要目录：

- `frontend/`: 包含使用 Vite 构建的 React 应用程序。
- `backend/`: 包含 LangGraph/FastAPI 应用程序，包括研究代理逻辑。

## 入门：开发和本地测试

请按照以下步骤在本地运行应用程序以进行开发和测试。

**1. 先决条件:**

- Node.js 和 npm (或 yarn/pnpm)
- Python 3.11+
- **`GEMINI_API_KEY`**: 后端代理需要 Google Gemini API 密钥。
    1. 通过复制项目根目录中的 `.env.example` 文件来创建一个名为 `.env` 的文件。
    2. 打开 `.env` 文件并添加您的 Gemini API 密钥：`GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"`

**2. 安装依赖项:**

**后端:**

```bash
cd backend
pip install .
```

**前端:**

```bash
cd frontend
npm install
```

**3. 运行开发服务器:**

**后端和前端:**

```bash
make dev
```
这将运行后端和前端开发服务器。打开浏览器并导航到前端开发服务器 URL (例如, `http://localhost:5173/app`)。

_或者，您可以分别运行后端和前端开发服务器。对于后端，在 `backend/` 目录中打开一个终端并运行 `langgraph dev`。后端 API 将在 `http://127.0.0.1:2024` 上可用。它还将在浏览器中打开一个指向 LangGraph UI 的窗口。对于前端，在 `frontend/` 目录中打开一个终端并运行 `npm run dev`。前端将在 `http://localhost:5173` 上可用。_

## 后端代理工作原理 (高级)

后端的核心是 `backend/src/agent/graph.py` 中定义的 LangGraph 代理。它现在遵循一个为自动化研究设计的复杂的四阶段工作流：

```mermaid
graph TD
    A[开始] --> B{1. 生成初始查询};
    B --> C{2. 执行搜索 (Arxiv等)};
    C --> D{3. 反思和优化};
    D -- 信息不足 --> C;
    D -- 信息充足 --> E{4. 自动化资源管理};
    E --> F{5. 基于RAG的知识合成};
    F --> G{6. 自动化报告生成};
    G --> H[结束];
```

1.  **智能文献发现与反思:**
    -   代理接收一个研究主题，并生成一组初始搜索查询。
    -   它使用学术搜索API（如Arxiv）执行这些查询。
    -   关键的是，它随后进入一个 **反思循环**。代理分析搜索结果以判断其是否充分。
    -   如果存在知识差距，它会生成新的查询并重新运行搜索。此循环将持续进行，直到信息全面或达到最大迭代次数。

2.  **自动化资源管理:**
    -   文献搜索完成后，代理会在收集到的摘要中查找DOI（数字对象标识符）。
    -   它使用 Unpaywall API 查找论文的开放获取PDF版本。
    -   然后，它使用 Zotero API 为每篇论文自动创建一个文献库条目，并附上找到的PDF。

3.  **基于RAG的知识合成:**
    -   代理从发现的PDF URL下载全文。
    -   它提取文本，将其分割成易于管理的小块，并使用Gemini模型为每个块生成向量嵌入。
    -   这些文本块及其嵌入存储在带有 `pgvector` 扩展的PostgreSQL数据库中，从而创建了一个强大的检索增强生成（RAG）知识库。

4.  **自动化报告生成:**
    -   最后，代理使用RAG数据库中合成的知识生成一份全面的报告，以回答最初的研究主题，并附上引文。

## 项目升级计划：迈向自动化研究平台

该项目正在进行重大升级，旨在从一个演示项目转变为一个强大的、VS Code原生的自动化研究平台。开发分为三个阶段。

### 第一阶段：后端基础与核心代理 (已完成)

这个基础阶段已经完成。我们构建了一个健壮的、“无头”的AI代理，它可以通过API调用，并完全实现了上述的四阶段研究工作流。

**此阶段的主要交付成果:**
-   **功能性的FastAPI服务器:** 后端通过FastAPI提供服务。
-   **PostgreSQL + pgvector数据库:** 集成了带有`pgvector`扩展的PostgreSQL数据库用于RAG。
-   **四阶段LangGraph代理:** 核心代理逻辑在`backend/src/agent/graph.py`中实现。
-   **集成工具:** 代理使用`arxiv`、`unpaywall`、`pyzotero`和`litellm`来执行其任务。
-   **容器化环境:** 整个后端堆栈可以使用Docker Compose运行。

### 第二阶段：VS Code骨架与静态展示 (进行中)

下一个阶段专注于构建平台面向用户的组件：一个VS Code扩展。目标是创建一个研究过程的“只读”视图。

**详细计划:**
1.  **开发基础VS Code扩展:**
    -   为扩展设置一个新的TypeScript项目。
    -   按照技术文档中的描述实现三栏布局：
        -   **左侧面板 (研究资产库):** 一个TreeView，用于显示研究资源（论文、笔记）。
        -   **中间面板 (动态手稿):** 主编辑器，将显示最终报告。
        -   **右侧面板 (AI控制面板):** 一个Webview，用于显示代理的状态和思考过程。
2.  **API集成 (只读):**
    -   扩展将调用后端API以获取已完成研究任务的状态和结果。
    -   数据将用于填充三个面板（例如，资产库中的论文列表、编辑器中的最终报告、控制面板中的代理日志）。
3.  **静态可视化:**
    -   主要目标是证明前端可以成功连接并显示来自后端的数据。目前，所有触发新运行的交互都将通过API工具（如Insomnia或curl）处理。

### 第三阶段：实时交互与动态协作 (未来)

最后一个阶段将通过在用户和代理之间实现完全的、实时的、双向的通信，使平台焕发生机。

**详细计划:**
1.  **WebSocket集成:**
    -   在VS Code扩展和FastAPI后端之间实现WebSocket通信。
    -   这将允许代理将其“思考”和进度实时流式传输到AI控制面板。
2.  **交互式控件:**
    -   在AI控制面板中构建UI组件（使用React和VS Code Webview UI Toolkit），允许用户：
        -   用自然语言提示开始新的研究任务。
        -   观察代理的进度。
        -   实现“人在环路”（HITL）决策点，即代理暂停并请求用户输入后再继续。
3.  **动态文档编辑:**
    -   代理将能够使用VS Code Workspace API直接编辑中间面板中的Markdown文件。这将允许代理与用户协同撰写报告。


## 使用的技术

- [React](https://reactjs.org/) (与 [Vite](https://vitejs.dev/)) - 用于前端用户界面。
- [Tailwind CSS](https://tailwindcss.com/) - 用于样式设计。
- [Shadcn UI](https://ui.shadcn.com/) - 用于组件。
- [LangGraph](https://github.com/langchain-ai/langgraph) - 用于构建后端研究代理。
- [Google Gemini](https://ai.google.dev/models/gemini) - 用于查询生成、反思和答案合成的 LLM。

## 许可证

该项目根据 Apache License 2.0 获得许可。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 工具

该项目在 `scripts` 目录中包含一系列实用工具脚本。这些工具通过根 `Makefile` 进行管理和执行。

### 列出模型

该工具从 Google Generative AI API 获取可用模型列表，并将其保存到 `logs/models.log`。

**先决条件:**

- 确保已设置 `GEMINI_API_KEY` 环境变量。

**用法:**

在项目根目录中运行以下命令：
    ```bash
    make list-models
    ```
