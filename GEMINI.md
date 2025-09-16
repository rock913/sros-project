# Gemini 项目上下文指南

## 1. 项目架构总览

- **架构模式**: 本项目是一个全栈应用，采用前后端分离的架构。
    - **后端**: 基于 Python 和 LangGraph 构建的 AI 代理服务。它将代理逻辑封装在一个 FastAPI 应用中，并通过 WebSocket 进行实时通信。
    - **前端**: 基于 React (TypeScript) 和 Vite 构建的单页面应用 (SPA)，提供一个与后端代理交互的聊天界面。
- **核心目录**:
    - `backend/src/agent`: 包含后端代理的核心逻辑，包括状态、图、工具和 API 端点。
    - `frontend/src`: 包含前端 React 应用的所有组件、页面和业务逻辑。
    - `docker-compose.yml`: 定义和编排前端、后端以及任何依赖服务（如数据库）的容器化环境。
- **设计原则**:
    - **后端**: 模块化和可组合性。LangGraph 的使用强制采用基于图的状态机方法来设计代理流程。关注点分离（State, Graph, Tools, API）。
    - **前端**: 组件化架构。通过可复用的 React 组件构建用户界面，状态管理集中在顶层组件中。

## 2. 模块地图

### 后端

- **`app.py`**:
    - **职责**: 创建 FastAPI 应用，设置 WebSocket 端点 (`/ws`) 用于与前端进行双向通信。管理代理的并发执行。
    - **依赖**: `graph.py` (获取可执行的 LangGraph 实例)。

- **`graph.py`**:
    - **职责**: 定义和构建 LangGraph。它将 `AgentState`、工具和代理节点（`agent.py`）连接在一起，形成一个完整的执行图。
    - **依赖**: `agent.py`, `state.py`, `tools_and_schemas.py`。

- **`agent.py`**:
    - **职责**: 定义代理的核心逻辑节点。决定在每一步是调用工具还是响应用户。
    - **依赖**: `tools_and_schemas.py` (访问可用工具)。

- **`state.py`**:
    - **职责**: 定义 `AgentState` TypedDict，这是 LangGraph 中用于在节点间传递数据的核心数据结构。
    - **被依赖**: `graph.py` 和图中的所有节点。

- **`tools_and_schemas.py`**:
    - **职责**: 定义代理可以使用的工具（例如，文件系统工具、shell 命令）以及它们的 Pydantic 输入模式。
    - **被依赖**: `agent.py`, `graph.py`。

- **`database.py`**:
    - **职责**: 提供与 SQLite 数据库的连接，用于持久化存储会话历史记录。
    - **依赖**: `aifos`, `sqlalchemy`。

### 前端

- **`App.tsx`**:
    - **职责**: 应用程序的主入口点。管理 WebSocket 连接，维护全局状态（如消息历史），并组合主要的 UI 组件。
    - **依赖**: `ChatMessagesView.tsx`, `InputForm.tsx`, `WelcomeScreen.tsx`。

- **`ChatMessagesView.tsx`**:
    - **职责**: 渲染代理和用户的消息列表。
    - **依赖**: `lib/utils.ts` (用于 UI 逻辑)。

- **`InputForm.tsx`**:
    - **职责**: 提供用户输入框和提交按钮，处理用户消息的发送。
    - **依赖**: `ui/button.tsx`, `ui/textarea.tsx`。

- **`WelcomeScreen.tsx`**:
    - **职责**: 在聊天开始前显示的欢迎界面。
    - **依赖**: `ui/card.tsx`。
