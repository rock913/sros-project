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

后端的核心是在 `backend/src/agent/graph.py` 中定义的 LangGraph 代理。它遵循以下步骤：

<img src="./agent.png" title="代理流程" alt="代理流程" width="50%">

1.  **生成初始查询:** 根据您的输入，它使用 Gemini 模型生成一组初始搜索查询。
2.  **网络研究:** 对于每个查询，它使用带有 Google Search API 的 Gemini 模型来查找相关的网页。
3.  **反思和知识差距分析:** 代理分析搜索结果以确定信息是否足够或是否存在知识差距。它使用 Gemini 模型进行此反思过程。
4.  **迭代优化:** 如果发现差距或信息不足，它会生成后续查询并重复网络研究和反思步骤 (最多可配置的最大循环次数)。
5.  **最终确定答案:** 一旦研究被认为是充分的，代理就会使用 Gemini 模型将收集到的信息合成为一个连贯的答案，包括来自网络来源的引文。

## CLI 示例

对于快速的一次性问题，您可以从命令行执行代理。脚本 `backend/examples/cli_research.py` 运行 LangGraph 代理并打印最终答案：

```bash
cd backend
python examples/cli_research.py "可再生能源的最新趋势是什么？"
```

## 部署

在生产环境中，后端服务器为优化的静态前端构建提供服务。LangGraph 需要一个 Redis 实例和一个 Postgres 数据库。Redis 用作发布/订阅代理，以实现从后台运行中流式传输实时输出。Postgres 用于存储助手、线程、运行、持久化线程状态和长期内存，并以“完全一次”的语义管理后台任务队列的状态。有关如何部署后端服务器的更多详细信息，请参阅 [LangGraph 文档](https://langchain-ai.github.io/langgraph/concepts/deployment_options/)。以下是如何构建一个包含优化的前端构建和后端服务器的 Docker 镜像，并通过 `docker-compose` 运行它的示例。

_注意：对于 docker-compose.yml 示例，您需要一个 LangSmith API 密钥，您可以从 [LangSmith](https://smith.langchain.com/settings) 获取。_

_注意：如果您没有运行 docker-compose.yml 示例或将后端服务器暴露给公共互联网，您应该将 `frontend/src/App.tsx` 文件中的 `apiUrl` 更新为您的主机。目前，`apiUrl` 设置为 `http://localhost:8123` (用于 docker-compose) 或 `http://localhost:2024` (用于开发)。_

**1. 构建 Docker 镜像:**

   从 **项目根目录** 运行以下命令：
   ```bash
   docker build -t gemini-fullstack-langgraph -f Dockerfile .
   ```
**2. 运行生产服务器:**

   ```bash
   GEMINI_API_KEY=<your_gemini_api_key> LANGSMITH_API_KEY=<your_langsmith_api_key> docker-compose up
   ```

打开浏览器并导航到 `http://localhost:8123/app/` 以查看应用程序。API 将在 `http://localhost:8123` 上可用。

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
