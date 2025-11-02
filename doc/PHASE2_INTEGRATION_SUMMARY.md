# Phase 2 后端集成 - 执行摘要

**日期：** 2025-11-02  
**状态：** ✅ 现状分析完成，📋 待开始实施

---

## 🎯 核心目标

将 VS Code 扩展从 **Mock 模式** 升级到 **后端真实数据交互**，实现完整的 AI 研究助手功能。

---

## 📊 当前状态总结

### ✅ 已完成（可用）

1. **后端服务运行正常**
   - ✅ FastAPI 在 `http://localhost:8121`
   - ✅ PostgreSQL + pgvector 数据库
   - ✅ LangGraph Agent 四阶段流程
   - ✅ 20+ API 端点可用
   - ✅ Langfuse 可观测性集成

2. **VS Code 扩展骨架完成**
   - ✅ 三面板布局（Library / Manuscript / Control）
   - ✅ 基础命令注册
   - ✅ API 客户端框架
   - ✅ Mock 模式运行正常

### ❌ 当前限制（需要修复）

1. **研究启动流程使用 Mock 数据**
   - ❌ 不调用后端 API
   - ❌ 进度更新是模拟的
   - ❌ 无法获取真实结果

2. **没有 WebSocket 集成**
   - ❌ 无实时进度更新
   - ❌ HITL 决策是 Mock
   - ❌ 文档协作是 Mock

3. **TreeView 不显示历史数据**
   - ❌ Asset Library 只显示示例
   - ❌ Manuscript 不显示报告历史

---

## 🚀 解决方案（3周计划）

### Week 1: 基础 API 集成
**目标：** 启动真实研究流程

**核心任务：**
1. 扩展 `api.ts`：添加 `createThread()`、`startResearch()`、`getThreadState()`
2. 重构 `auto-researcher.start` 命令：调用真实 API
3. 实现状态轮询（临时方案，Week 2 改为 WebSocket）
4. 更新控制面板：显示真实数据

**交付物：**
- [ ] 能创建研究线程
- [ ] 能启动真实 Agent
- [ ] 能看到真实论文和报告

---

### Week 2: WebSocket 实时通信
**目标：** 实时进度更新

**核心任务：**
1. 创建 `websocket.ts`：WebSocket 客户端封装
2. 替换轮询为 WebSocket：实时状态更新
3. 更新 TreeView：显示历史数据
4. 优化用户体验：加载指示器、错误处理

**交付物：**
- [ ] WebSocket 连接稳定
- [ ] 实时进度流畅
- [ ] Asset Library 显示历史论文
- [ ] Manuscript 显示报告历史

---

### Week 3: HITL 与文档协作
**目标：** 完整交互功能

**核心任务：**
1. HITL 决策集成：接收真实决策请求
2. 文档协作集成：实时文档编辑
3. 端到端测试：完整流程验证
4. 性能优化：响应速度、内存使用

**交付物：**
- [ ] HITL 决策正常工作
- [ ] 文档协作实时更新
- [ ] 所有测试通过
- [ ] 性能达标

---

## 📋 技术要点

### API 端点使用

| 端点 | 用途 | 状态 |
|------|------|------|
| `POST /threads` | 创建研究会话 | 📋 待集成 |
| `POST /threads/{id}/runs/stream` | 启动研究 | 📋 待集成 |
| `GET /threads/{id}/state` | 获取状态 | 📋 待集成 |
| `WS /agent/stream` | 实时更新 | 📋 待集成 |
| `GET /papers` | 获取论文 | ✅ 已实现 |
| `GET /reports` | 获取报告 | ✅ 已实现 |
| `POST /agent/hitl/respond` | HITL 决策 | 📋 待集成 |

### 代码修改位置

| 文件 | 修改内容 | 优先级 |
|------|---------|--------|
| `vscode-extension/src/api.ts` | 添加线程/研究 API | 🔴 高 |
| `vscode-extension/src/extension.ts` (920-1007行) | 重构启动命令 | 🔴 高 |
| `vscode-extension/src/websocket.ts` | 新建 WebSocket 客户端 | 🟡 中 |
| `vscode-extension/src/extension.ts` (AssetLibraryProvider) | 显示历史数据 | 🟡 中 |
| `vscode-extension/src/extension.ts` (ManuscriptProvider) | 显示报告历史 | 🟡 中 |
| `vscode-extension/src/extension.ts` (1385-1472行) | HITL 集成 | 🟢 低 |
| `vscode-extension/src/documentCollaboration.ts` | 文档协作 | 🟢 低 |

---

## ✅ 验收标准

### 功能验收
- [ ] 用户能输入主题，启动真实研究
- [ ] 实时看到 Agent 进度（查询生成 → 论文收集 → 报告生成）
- [ ] Asset Library 显示所有历史论文
- [ ] Manuscript 显示所有报告版本
- [ ] HITL 决策能提交到后端
- [ ] 报告能实时编辑

### 性能验收
- [ ] API 响应 < 1秒
- [ ] WebSocket 延迟 < 100ms
- [ ] UI 流畅（60fps）
- [ ] 内存稳定（< 500MB）

### 测试验收
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试 100% 通过
- [ ] 端到端测试 100% 通过

---

## 🎯 里程碑

| 里程碑 | 日期 | 标志 |
|--------|------|------|
| M1: API 集成完成 | Week 1 结束 | 能启动真实研究 |
| M2: WebSocket 完成 | Week 2 结束 | 实时进度更新 |
| M3: 完整功能 | Week 3 结束 | 所有功能可用 |

---

## 🚦 风险与缓解

### 风险 1: WebSocket 连接不稳定
**缓解：**
- 实现自动重连机制
- 添加心跳检测
- 降级到轮询作为备选

### 风险 2: API 响应慢
**缓解：**
- 添加超时处理
- 显示加载指示器
- 实现请求缓存

### 风险 3: 文档编辑冲突
**缓解：**
- 实现冲突检测
- 提供手动解决 UI
- 记录变更历史

---

## 📚 相关文档

- **详细计划：** [PHASE2_BACKEND_INTEGRATION_PLAN.md](./PHASE2_BACKEND_INTEGRATION_PLAN.md)
- **调试指南：** [PHASE2_DEBUG_GUIDE.md](./PHASE2_DEBUG_GUIDE.md)
- **API 文档：** [../backend/API_DOCUMENTATION.md](../backend/API_DOCUMENTATION.md)
- **路线图：** [../ROADMAP.md](../ROADMAP.md)

---

## 🏁 下一步行动

### 立即开始

1. **阅读详细计划**
   ```bash
   cat doc/PHASE2_BACKEND_INTEGRATION_PLAN.md
   ```

2. **启动后端服务**
   ```bash
   docker compose -f docker-compose-dev.yml up -d
   curl http://localhost:8121/ok
   ```

3. **启动扩展开发**
   ```bash
   cd vscode-extension
   npm install
   code .
   # 按 F5 调试
   ```

4. **开始 Week 1 任务**
   - 修改 `vscode-extension/src/api.ts`
   - 添加 `createThread()` 函数
   - 运行测试验证

---

**准备好开始了吗？** 🚀

参考详细计划文档，按照 Week 1 → Week 2 → Week 3 的顺序逐步实施。每完成一个任务，在验收清单中打勾 ✅。

祝开发顺利！💪
