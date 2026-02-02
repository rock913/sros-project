# API Documentation Guide

本文档说明如何查看和使用 Auto-Researcher 后端 API 文档，以便前后端开发者能够高效协作。

# API Documentation Guide

本文档说明如何查看和使用 Auto-Researcher 后端 API 文档，以便前后端开发者能够高效协作。

## 🔑 核心概念：State Persistence & Thread Management

### State Persistence（状态持久化）

**从 v0.0.2 开始**，后端使用 **LangGraph PostgresSaver Checkpointer** 实现状态持久化：

- **多会话支持**: 每个研究任务通过 `thread_id`（UUID）隔离
- **自动保存**: 所有状态自动保存到 PostgreSQL
- **断点续传**: 可随时暂停和恢复研究任务
- **并发安全**: 支持多个研究任务并行执行

### Thread ID（会话标识符）

**格式要求**: 必须是有效的 UUID v4 格式
```
✅ 正确: "550e8400-e29b-41d4-a716-446655440000"
❌ 错误: "my-research-001" (非 UUID 格式)
```

**生成方法**:
```python
# Python
import uuid
thread_id = str(uuid.uuid4())
```

```typescript
// TypeScript
import { v4 as uuidv4 } from 'uuid';
const threadId = uuidv4();
```

**使用场景**:
- **新研究**: 生成新的 UUID
- **继续研究**: 使用之前的 UUID
- **查看历史**: 用 UUID 检索过往研究

---

## 📖 API 文档来源

### 1. OpenAPI 契约文件（单一真相来源）

**位置**: `../openapi.yaml`（项目根目录）

这是项目的 **API 契约**，遵循 "Contract First" 原则：

- **用途**: 定义前后端交互的标准规范
- **优先级**: ⭐⭐⭐⭐⭐ 最高（这是前后端开发的基准）
- **何时使用**:
  - 开发新功能前，首先更新此契约
  - 前后端对接口有疑问时，以此为准
  - 前端可基于此生成 Mock Server

**如何查看**:
```bash
# 直接在编辑器中打开
code ../openapi.yaml

# 或使用在线 Swagger Editor 可视化查看
# 访问 https://editor.swagger.io/ 并导入此文件
```

---

### 2. FastAPI 自动生成的交互式文档

**前提**: 后端服务必须正在运行（默认端口 8121）

#### 📱 Swagger UI（推荐用于测试）

**URL**: http://localhost:8121/docs

**特点**:
- ✅ 交互式界面，可直接测试 API
- ✅ 自动与代码实时同步
- ✅ 显示请求/响应示例
- ✅ 可以在浏览器中执行 API 调用

**截图说明**:
```
┌─────────────────────────────────────────┐
│  Autonomous Research Agent API          │
│  Version 1.0.0                          │
├─────────────────────────────────────────┤
│  GET  /ok                               │ ← 健康检查
│  GET  /agent/state                      │ ← 获取最新状态
│  GET  /agent/state/{thread_id}          │ ← 获取特定会话状态
│  POST /agent/invoke                     │ ← 调用研究代理
│  ...                                     │
└─────────────────────────────────────────┘
```

#### 📘 ReDoc（推荐用于阅读）

**URL**: http://localhost:8121/redoc

**特点**:
- ✅ 更美观的阅读体验
- ✅ 更好的结构化展示
- ✅ 适合打印或分享

#### 🔧 OpenAPI JSON Schema

**URL**: http://localhost:8121/openapi.json

**特点**:
- 机器可读的 JSON 格式
- 可用于自动生成客户端代码
- 可导入到 Postman 等工具

---

## 🚀 快速开始指南

### 对于前端开发者

1. **开发前**：阅读 `../openapi.yaml` 了解 API 契约
2. **开发中**：
   - 基于 `openapi.yaml` 生成 TypeScript 类型定义
   - 或使用 Mock Server（如 `prism`）进行独立开发
3. **联调时**：访问 http://localhost:8121/docs 测试真实 API

### 对于后端开发者

1. **开发前**：更新 `../openapi.yaml` 定义新接口
2. **开发中**：实现 API 并添加详细的文档字符串
3. **开发后**：
   - 访问 http://localhost:8121/docs 验证文档自动生成正确
   - 确保生成的文档与 `openapi.yaml` 契约一致

## 📋 核心 API 端点总览

| 端点 | 方法 | 用途 | Thread ID | 契约定义 |
|------|------|------|-----------|----------|
| `/ok` | GET | 健康检查 | 不需要 | ✅ 已定义 |
| `/agent/state` | GET | 获取最新状态（便捷端点） | 不需要 | ✅ 已定义 |
| `/agent/state/{thread_id}` | GET | 获取特定会话状态 | **必需（UUID）** | ✅ 已定义 |
| `/agent/invoke` | POST | 启动或继续研究任务 | 推荐提供 | ✅ 已定义 |
| `/agent/stream` | POST | 流式调用研究代理 | 推荐提供 | ❌ 待实现 |

### 端点详解

#### 1. `GET /agent/state/{thread_id}` - 获取会话状态

**用途**: 检索特定研究会话的持久化状态

**Path 参数**:
- `thread_id` (string, UUID格式, 必需): 会话标识符

**示例请求**:
```bash
curl http://localhost:8121/agent/state/550e8400-e29b-41d4-a716-446655440000
```

**成功响应 (200)**:
```json
{
  "research_topic": "Quantum Computing Applications",
  "search_queries": ["quantum computing 2024", "quantum algorithms"],
  "literature_abstracts": [
    {
      "title": "Advances in Quantum Computing",
      "authors": ["Alice", "Bob"],
      "summary": "..."
    }
  ],
  "report": "# Research Report\n\n...",
  "is_sufficient": true
}
```

**错误响应 (404)**:
```json
{
  "detail": "No state found for thread 550e8400-e29b-41d4-a716-446655440000"
}
```

#### 2. `POST /agent/invoke` - 调用研究代理

**用途**: 启动新研究或继续现有研究

**请求体**:
```json
{
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "Research recent advances in quantum computing"
      }
    ]
  },
  "config": {
    "configurable": {
      "thread_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

**重要说明**:
- 如果 `thread_id` 已存在，agent 将从上次状态继续
- 如果 `thread_id` 是新的，将创建新的研究会话
- 省略 `thread_id` 会使用默认线程（不推荐）

**示例请求**:
```bash
curl -X POST http://localhost:8121/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [{"role": "user", "content": "Quantum computing"}]
    },
    "config": {
      "configurable": {
        "thread_id": "550e8400-e29b-41d4-a716-446655440000"
      }
    }
  }'
```

**典型工作流**:
```
1. 生成 UUID → thread_id = uuid.uuid4()
2. 调用 POST /agent/invoke (创建新研究)
3. 可选：中途调用 GET /agent/state/{thread_id} (检查进度)
4. 可选：再次调用 POST /agent/invoke (继续研究)
5. 最终：调用 GET /agent/state/{thread_id} (获取完整结果)
```

---

## 🔍 如何验证 API 实现与契约一致

### 方法 1: 手动对比

1. 打开 `../openapi.yaml`
2. 访问 http://localhost:8121/openapi.json
3. 对比两者的差异

### 方法 2: 使用自动化工具（推荐）

```bash
# 安装 OpenAPI 比对工具
npm install -g @openapitools/openapi-generator-cli

# 比对契约与实现
# TODO: 添加具体的比对脚本
```

---

## 🛠️ 常见问题

### Q1: 为什么需要两个文档来源？

**A**: 
- `openapi.yaml` 是**设计阶段**的契约，用于前后端并行开发
- FastAPI 文档是**实现阶段**的实时文档，反映代码的真实状态
- 理想情况下，两者应该保持一致

### Q2: 如果契约与实现不一致怎么办？

**A**: 优先级顺序：
1. 如果契约是正确的，修改代码实现
2. 如果契约需要更新，先更新契约，再修改代码
3. 永远不要让两者长期不一致

### Q3: 我不想启动完整服务，只想查看文档怎么办？

**A**: 
- 查看 `../openapi.yaml` 即可
- 或使用在线工具：https://editor.swagger.io/

### Q4: thread_id 是什么？为什么需要它？

**A**: 
- `thread_id` 是研究会话的唯一标识符（UUID 格式）
- **用途**: 
  - 支持多个独立的研究任务并行进行
  - 允许暂停和恢复研究（断点续传）
  - 隔离不同用户或不同研究主题的数据
- **格式**: 必须是有效的 UUID v4，如 `"550e8400-e29b-41d4-a716-446655440000"`

### Q5: 如果不提供 thread_id 会怎样？

**A**: 
- 系统会使用默认线程（不推荐生产环境使用）
- 所有请求会共享同一个状态，导致数据混乱
- **最佳实践**: 总是为每个独立的研究任务生成新的 UUID

### Q6: 如何在前端生成和管理 thread_id？

**A**: 
```typescript
// 1. 生成新的研究会话
import { v4 as uuidv4 } from 'uuid';
const threadId = uuidv4();

// 2. 存储到本地（可选）
localStorage.setItem('currentResearchThreadId', threadId);

// 3. 在 API 调用中使用
const response = await fetch('/agent/invoke', {
  method: 'POST',
  body: JSON.stringify({
    input: { messages: [{ role: 'user', content: topic }] },
    config: { configurable: { thread_id: threadId } }
  })
});

// 4. 稍后检索状态
const state = await fetch(`/agent/state/${threadId}`);
```

### Q7: thread_id 可以是任意字符串吗？

**A**: 
- **❌ 不可以**！必须是有效的 UUID v4 格式
- PostgreSQL 数据库的 `checkpoints` 表中 `thread_id` 列定义为 UUID 类型
- 如果使用非 UUID 字符串，会导致数据库错误：
  ```
  psycopg.errors.InvalidTextRepresentation: 
  invalid input syntax for type uuid: "my-research-001"
  ```

### Q8: 如何列出所有的研究会话？

**A**: 
- 当前 API 不支持列出所有 thread（这是 Phase 3.5 的规划功能）
- **临时方案**: 在数据库中直接查询
  ```sql
  SELECT DISTINCT thread_id FROM checkpoints ORDER BY created_at DESC;
  ```
- **未来功能**: `GET /sessions` 将提供完整的会话管理（计划在 Phase 3.5.1 实现）

### Q9: checkpointer 保存了什么数据？

**A**: 
Checkpointer 自动保存完整的 agent 状态，包括：
- **messages**: 完整的对话历史
- **research_topic**: 研究主题
- **search_queries**: 生成的所有搜索查询
- **literature_abstracts**: 收集的论文摘要
- **literature_full_text**: 下载的论文全文
- **knowledge_gap**: 识别的知识缺口
- **report**: 生成的研究报告
- **is_sufficient**: 是否有足够的信息

**数据库表**:
- `checkpoints`: 主检查点数据
- `checkpoint_writes`: 写入操作日志
- `checkpoint_blobs`: 大型二进制数据（如PDF内容）

---

## 📞 相关资源

- **OpenAPI 规范**: https://swagger.io/specification/
- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **Swagger Editor**: https://editor.swagger.io/
- **项目测试文档**: `../TESTING.md`
- **开发工作流**: `../doc/WORKFLOW_STRATEGY.md`

---

**最后更新**: 2025-10-12
**维护者**: Auto-Researcher Team
