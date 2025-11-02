# Phase 2 后端集成 - 快速参考卡

## 🎯 一句话总结
将 VS Code 扩展从 Mock 模式升级到真实后端 API 集成，实现完整的 AI 研究助手功能。

---

## 📋 当前问题

```typescript
// 当前代码（Mock）：vscode-extension/src/extension.ts:961-1004
vscode.window.showInformationMessage(
    '⚠️ WebSocket streaming not yet implemented. Using mock progress for now.'
);

// 模拟进度...
setTimeout(() => { 
    panel.webview.postMessage({ progress: 20 }); 
}, 1000);

// ❌ 问题：
// - 不调用后端 API
// - 进度是假的
// - 无法获取真实论文和报告
```

---

## ✅ 解决方案（3周）

### Week 1: API 基础集成
```typescript
// 1. 添加 API 函数（api.ts）
export async function createThread(request: CreateThreadRequest): Promise<ThreadResponse>
export async function startResearch(threadId: string, topic: string): Promise<string>
export async function getThreadState(threadId: string): Promise<ThreadState>

// 2. 重构启动命令
const thread = await createThread({ metadata: { research_topic: topic } });
const runId = await startResearch(thread.thread_id, topic);

// 3. 轮询状态（临时）
setInterval(async () => {
  const state = await getThreadState(thread.thread_id);
  updateProgress(state);
}, 2000);
```

**验收：** ✅ 能启动真实研究，看到真实结果

---

### Week 2: WebSocket 实时通信
```typescript
// 1. 创建 WebSocket 客户端（websocket.ts）
export class ResearchWebSocketClient {
  connect(url: string): void
  on(event: string, handler: Function): void
  send(message: any): void
  close(): void
}

// 2. 替换轮询
const ws = new ResearchWebSocketClient(thread.thread_id);
ws.on('state_update', (state) => updateProgress(state));
ws.on('complete', () => showResults());

// 3. 更新 TreeView 数据源
async getChildren(): Promise<AssetItem[]> {
  const result = await getAllPapers({ limit: 20 });
  return result.papers.map(p => new AssetItem(p.title, ...));
}
```

**验收：** ✅ 实时进度更新，显示历史数据

---

### Week 3: HITL 与文档协作
```typescript
// 1. HITL 集成
ws.on('hitl_request', async (request) => {
  const decision = await showDecisionUI(request);
  await axios.post('/agent/hitl/respond', { decision });
});

// 2. 文档协作
ws.on('document_update', async (update) => {
  const edit = new vscode.WorkspaceEdit();
  edit.replace(docUri, range, update.content);
  await vscode.workspace.applyEdit(edit);
});
```

**验收：** ✅ 完整交互功能

---

## 🔑 关键 API 端点

| 端点 | 方法 | 用途 | Week |
|------|------|------|------|
| `/threads` | POST | 创建会话 | 1 |
| `/threads/{id}/runs/stream` | POST | 启动研究 | 1 |
| `/threads/{id}/state` | GET | 获取状态 | 1 |
| `/agent/stream` | WS | 实时更新 | 2 |
| `/papers` | GET | 获取论文 | 2 |
| `/reports` | GET | 获取报告 | 2 |
| `/agent/hitl/respond` | POST | HITL 决策 | 3 |

---

## 📝 代码修改清单

### 必改文件（高优先级）

- [ ] `vscode-extension/src/api.ts`
  - 添加 `createThread()`, `startResearch()`, `getThreadState()`
  
- [ ] `vscode-extension/src/extension.ts` (920-1007行)
  - 删除 Mock 代码
  - 调用真实 API
  
- [ ] `vscode-extension/src/websocket.ts` (新建)
  - 实现 WebSocket 客户端

### 次要文件（中优先级）

- [ ] `vscode-extension/src/extension.ts` (AssetLibraryProvider)
  - 从 `getAllPapers()` 获取数据
  
- [ ] `vscode-extension/src/extension.ts` (ManuscriptProvider)
  - 从 `getAllReports()` 获取数据

### 可选文件（低优先级）

- [ ] `vscode-extension/src/extension.ts` (1385-1472行)
  - HITL 集成
  
- [ ] `vscode-extension/src/documentCollaboration.ts`
  - 文档协作

---

## 🧪 测试命令

### 测试后端
```bash
# 健康检查
curl http://localhost:8121/ok

# 创建线程
curl -X POST http://localhost:8121/threads \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"test": true}}'

# 启动研究
curl -X POST http://localhost:8121/threads/{THREAD_ID}/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {"messages": [{"role": "user", "content": "Research LangGraph"}]},
    "stream_mode": ["values"]
  }'
```

### 测试前端
```bash
cd vscode-extension
npm test
```

---

## ⚡ 快速开始

```bash
# 1. 启动后端
docker compose -f docker-compose-dev.yml up -d

# 2. 验证服务
curl http://localhost:8121/ok

# 3. 开发扩展
cd vscode-extension
npm install
code .
# 按 F5 启动调试

# 4. 测试 Mock 功能
# Ctrl+Shift+P → "Auto-Researcher: Start New Research"
# 输入主题 → 看到 Mock 进度

# 5. 开始集成（Week 1）
# 编辑 src/api.ts，添加 createThread()
# 编辑 src/extension.ts，替换 Mock 代码
```

---

## 📊 进度跟踪

### Week 1: API 集成
- [ ] Day 1-2: 扩展 `api.ts`
- [ ] Day 3-5: 重构启动命令
- [ ] Day 6-7: 更新控制面板

### Week 2: WebSocket
- [ ] Day 1-3: 实现 WebSocket 客户端
- [ ] Day 4-5: 集成到启动流程
- [ ] Day 6-7: 更新 TreeView

### Week 3: 完整功能
- [ ] Day 1-3: HITL 集成
- [ ] Day 4-6: 文档协作
- [ ] Day 7: 测试优化

---

## 🎯 成功标准

### 功能
- [x] Mock 模式运行 ✅（当前）
- [ ] 真实研究启动 📋（Week 1）
- [ ] 实时进度更新 📋（Week 2）
- [ ] 历史数据显示 📋（Week 2）
- [ ] HITL 决策 📋（Week 3）
- [ ] 文档协作 📋（Week 3）

### 性能
- [ ] API 响应 < 1秒
- [ ] WebSocket 延迟 < 100ms
- [ ] UI 流畅（60fps）

### 测试
- [ ] 单元测试 > 80%
- [ ] 集成测试 100%
- [ ] 端到端测试 100%

---

## 📚 详细文档

- **完整计划：** [PHASE2_BACKEND_INTEGRATION_PLAN.md](./PHASE2_BACKEND_INTEGRATION_PLAN.md) (4000+ 行)
- **执行摘要：** [PHASE2_INTEGRATION_SUMMARY.md](./PHASE2_INTEGRATION_SUMMARY.md) (500 行)
- **调试指南：** [PHASE2_DEBUG_GUIDE.md](./PHASE2_DEBUG_GUIDE.md) (300 行)

---

## 💡 贴士

### 调试技巧
1. 使用 `console.log()` 跟踪 API 调用
2. 检查浏览器开发者工具（Webview）
3. 查看 Docker 日志：`docker compose logs -f langgraph-api`

### 常见错误
- **CORS 错误：** 后端已配置 CORS，应该不会出现
- **连接拒绝：** 检查容器是否运行：`docker compose ps`
- **超时：** 增加 API 超时时间（默认 30 秒）

### 最佳实践
- 先测试 API（curl），再写前端代码
- 使用 TypeScript 类型检查（`npm run compile`）
- 频繁提交代码（每个任务完成后）

---

**准备好了？开始 Week 1！** 🚀

修改 `vscode-extension/src/api.ts`，添加第一个函数：`createThread()`
