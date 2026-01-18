# Phase 3.6 准备工作清单
**开始日期**: 2025年10月15日 (计划)  
**预计时长**: 3周  
**核心目标**: Human-in-the-Loop (HITL) + 实时文档协作

---

## 📋 Phase 3.6 总览

### Week 1-2: HITL 决策系统
- **Day 1-2**: LangGraph interrupt 节点实现
- **Day 3-4**: WebSocket HITL 协议 + 后端 API
- **Day 5-6**: 前端 HITL 决策卡片 UI
- **Day 7-8**: 集成测试 + 性能优化
- **Day 9-10**: E2E 测试 + 文档编写

### Week 3: 实时文档协作
- **Day 11-12**: 流式文档更新后端
- **Day 13**: VS Code 文档编辑集成
- **Day 14**: 变更高亮 + Accept/Reject UI
- **Day 15**: 冲突检测 + 最终测试

---

## 🎯 立即行动项 (本周)

### 1. 环境准备 ✅

```bash
# 创建 Phase 3.6 分支
git checkout -b phase-3.6-hitl-collaboration

# 确保依赖最新
cd backend
pip install langgraph>=0.2.0
```

**状态**: 待执行

---

### 2. 技术调研 (Day 1)

#### 2.1 LangGraph Interrupt 机制

**文档阅读**:
- [ ] LangGraph 官方文档：`interrupt()` API
- [ ] LangGraph 示例：Human-in-the-Loop patterns
- [ ] StateGraph 中断与恢复流程

**关键问题**:
1. ❓ 如何在节点中触发 interrupt？
2. ❓ 中断状态如何序列化存储？
3. ❓ 用户响应后如何恢复执行？
4. ❓ 多个 interrupt 节点如何管理？

**参考代码**:
```python
# 预研：LangGraph interrupt 示例
from langgraph.graph import StateGraph, interrupt

def approval_node(state):
    # 触发人工审批
    user_input = interrupt({
        "type": "approval_request",
        "message": "是否继续执行查询？",
        "options": ["approve", "reject", "modify"]
    })
    
    if user_input == "reject":
        return {"status": "rejected"}
    
    return {"status": "approved", "user_input": user_input}
```

**调研输出**: `docs/LANGGRAPH_INTERRUPT_RESEARCH.md`

---

#### 2.2 WebSocket HITL 协议设计

**协议规范草稿**:
```typescript
// HITL Request (Backend → Frontend)
interface HITLRequest {
    type: 'hitl_request';
    request_id: string;
    decision_type: 'query_approval' | 'paper_selection' | 'report_revision';
    prompt: string;
    options: HITLOption[];
    context: {
        current_query?: string;
        papers?: Paper[];
        report_draft?: string;
    };
    timeout_seconds?: number;
}

// HITL Response (Frontend → Backend)
interface HITLResponse {
    type: 'hitl_response';
    request_id: string;
    decision: string;
    modified_data?: any;
    timestamp: string;
}
```

**待定义**:
- [ ] Timeout 机制（用户不响应怎么办？）
- [ ] 取消研究时的清理逻辑
- [ ] 多个 HITL 请求队列管理

**设计输出**: `docs/WEBSOCKET_HITL_PROTOCOL.md`

---

#### 2.3 VS Code 文档编辑 API

**需要掌握**:
```typescript
import * as vscode from 'vscode';

// 1. 打开文档
const doc = await vscode.workspace.openTextDocument(uri);

// 2. 应用编辑
const edit = new vscode.WorkspaceEdit();
edit.insert(uri, new vscode.Position(0, 0), "# 研究报告\n");
await vscode.workspace.applyEdit(edit);

// 3. 变更装饰器（高亮）
const decorationType = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(0, 255, 0, 0.3)'
});
editor.setDecorations(decorationType, [range]);
```

**实验项目**: 创建 `vscode-extension/src/experiments/document-edit-test.ts`

---

### 3. 架构设计 (Day 1-2)

#### 3.1 后端架构变更

**当前架构**:
```
graph.py
  ├─ query_generation_node()
  ├─ paper_search_node()
  ├─ paper_analysis_node()
  └─ report_generation_node()
```

**目标架构**:
```
graph.py
  ├─ query_generation_node()
  ├─ query_approval_node() ⭐ NEW (HITL)
  ├─ paper_search_node()
  ├─ paper_selection_node() ⭐ NEW (HITL)
  ├─ paper_analysis_node()
  ├─ report_generation_node_streaming() ⭐ MODIFIED
  └─ report_revision_node() ⭐ NEW (HITL)
```

**数据流**:
```
1. query_generation → query_approval (HITL) → paper_search
2. paper_search → paper_selection (HITL) → paper_analysis
3. paper_analysis → report_generation (streaming) → report_revision (HITL)
```

**新增状态字段**:
```python
class ResearchState(TypedDict):
    # 现有字段...
    
    # 新增 HITL 字段
    hitl_requests: List[HITLRequest]
    hitl_responses: Dict[str, HITLResponse]
    pending_approval: Optional[str]
```

**设计文档**: `backend/docs/HITL_ARCHITECTURE.md`

---

#### 3.2 前端架构变更

**新增组件**:
```
vscode-extension/src/
  ├─ hitlWebview.ts ⭐ NEW
  │   └─ generateHITLDecisionCardHTML()
  │
  ├─ documentCollaborationManager.ts ⭐ NEW
  │   ├─ applyStreamingEdit()
  │   ├─ highlightChanges()
  │   └─ showAcceptRejectUI()
  │
  └─ extension.ts (MODIFIED)
      ├─ handleHITLRequest()
      ├─ sendHITLResponse()
      └─ onDocumentUpdate()
```

**WebSocket 消息处理增强**:
```typescript
// 在 extension.ts 中
ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    switch (message.type) {
        case 'hitl_request':
            handleHITLRequest(message);
            break;
        
        case 'document_update':
            documentCollaborationManager.applyEdit(message);
            break;
        
        // 现有消息类型...
    }
});
```

---

### 4. 技术栈确认

#### 4.1 后端依赖

```toml
[tool.poetry.dependencies]
langgraph = "^0.2.0"  # 确保支持 interrupt()
langchain-core = "^0.3.0"
```

**验证命令**:
```bash
docker exec langgraph-api bash -c "python -c 'from langgraph.graph import interrupt; print(interrupt.__doc__)'"
```

**状态**: 待验证

---

#### 4.2 前端依赖

**当前已有**:
- VS Code Extension API (v1.x)
- WebSocket client (内置)
- TypeScript 4.x

**无需新增依赖** ✅

---

### 5. 数据库 Schema 更新 (Day 2)

#### 5.1 新增 HITL 记录表

```sql
-- backend/src/db/migrations/add_hitl_table.sql
CREATE TABLE hitl_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    request_id VARCHAR(255) NOT NULL,
    decision_type VARCHAR(50) NOT NULL,
    prompt TEXT NOT NULL,
    options JSONB NOT NULL,
    user_decision VARCHAR(255),
    modified_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    responded_at TIMESTAMP,
    timeout_seconds INTEGER,
    
    INDEX idx_session_hitl (session_id),
    INDEX idx_request_id (request_id)
);
```

**SQLAlchemy 模型**:
```python
# backend/src/db/models.py
class HITLDecision(Base):
    __tablename__ = "hitl_decisions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    request_id = Column(String(255), nullable=False, index=True)
    decision_type = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    options = Column(JSONB, nullable=False)
    user_decision = Column(String(255))
    modified_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)
    timeout_seconds = Column(Integer)
    
    # Relationship
    session = relationship("Session", back_populates="hitl_decisions")
```

**迁移命令**:
```bash
docker exec langgraph-api bash -c "cd /deps/backend && alembic revision --autogenerate -m 'Add HITL decisions table'"
docker exec langgraph-api bash -c "cd /deps/backend && alembic upgrade head"
```

**状态**: 待执行

---

### 6. API 端点设计 (Day 2)

#### 6.1 HITL 响应端点

```python
# backend/src/agent/app.py

@app.post("/agent/hitl/respond")
async def respond_to_hitl(
    request_id: str,
    decision: str,
    modified_data: Optional[Dict] = None
):
    """
    用户响应 HITL 请求
    
    1. 验证 request_id 有效性
    2. 恢复 LangGraph 执行
    3. 传递用户决策到节点
    4. 记录到数据库
    """
    # TODO: 实现逻辑
    pass

@app.get("/agent/hitl/pending")
async def get_pending_hitl(session_id: str):
    """
    获取待处理的 HITL 请求
    
    用于断线重连场景
    """
    # TODO: 实现逻辑
    pass
```

**OpenAPI 规范更新**: `openapi.yaml` 添加 `/agent/hitl/*` 端点

---

### 7. 测试策略 (Day 8-10)

#### 7.1 单元测试

**后端**:
```python
# backend/tests/test_hitl_nodes.py

def test_query_approval_node():
    """测试查询审批节点"""
    state = {"query": "test query"}
    result = query_approval_node(state)
    assert "pending_approval" in result

def test_hitl_timeout():
    """测试 HITL 超时处理"""
    # TODO
```

**前端**:
```typescript
// vscode-extension/src/test/suite/hitl.test.ts

suite('HITL Decision Cards', () => {
    test('should render approval card', () => {
        // TODO
    });
});
```

---

#### 7.2 集成测试

```python
# backend/tests/integration/test_hitl_workflow.py

async def test_full_hitl_workflow():
    """
    端到端 HITL 流程测试
    
    1. 启动研究会话
    2. 触发 query_approval HITL
    3. 模拟用户响应
    4. 验证继续执行
    5. 检查数据库记录
    """
    # TODO
```

---

#### 7.3 E2E 测试

**场景覆盖**:
- [ ] 用户批准查询 → 研究继续
- [ ] 用户拒绝查询 → 研究终止
- [ ] 用户修改查询 → 使用新查询
- [ ] HITL 超时 → 使用默认决策
- [ ] 断线重连 → 恢复 HITL 状态

**测试工具**: Playwright (可选) 或手动测试清单

---

## 📚 参考资料准备

### 必读文档

1. **LangGraph 官方文档**
   - [ ] [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
   - [ ] [Interrupt and Resume](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/interrupt/)
   - [ ] [Checkpointing](https://langchain-ai.github.io/langgraph/concepts/persistence/)

2. **VS Code API 文档**
   - [ ] [Workspace API](https://code.visualstudio.com/api/references/vscode-api#workspace)
   - [ ] [TextEditor API](https://code.visualstudio.com/api/references/vscode-api#TextEditor)
   - [ ] [Webview API](https://code.visualstudio.com/api/extension-guides/webview)

3. **WebSocket 协议**
   - [ ] [WebSocket RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
   - [ ] FastAPI WebSocket 文档

---

### 示例代码库

- [ ] LangGraph 示例仓库：`langgraph/examples/human-in-the-loop/`
- [ ] VS Code 示例扩展：`vscode-extension-samples/webview-sample/`

---

## 🎯 成功标准 (Week 3 结束)

### 功能完整性

- [ ] 3个 HITL 决策点正常工作（query, paper selection, report revision）
- [ ] WebSocket 实时推送 HITL 请求
- [ ] 前端决策卡片正确渲染
- [ ] 用户响应正确传回后端
- [ ] LangGraph 正确恢复执行
- [ ] 实时文档编辑流畅
- [ ] 变更高亮清晰可见
- [ ] Accept/Reject 按钮功能正常

### 测试覆盖

- [ ] 单元测试覆盖率 >80%
- [ ] 集成测试通过 (后端 + 前端)
- [ ] E2E 测试 5 个核心场景通过
- [ ] 性能测试：HITL 响应时间 <2秒

### 文档完整性

- [ ] HITL 用户使用指南
- [ ] HITL 开发者文档
- [ ] WebSocket 协议规范
- [ ] API 文档更新（OpenAPI）
- [ ] 架构图更新

---

## 🚧 风险识别

### 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| LangGraph interrupt 不稳定 | 中 | 高 | 提前验证，准备降级方案 |
| WebSocket 断线重连复杂 | 高 | 中 | 实现状态持久化 |
| VS Code 文档编辑冲突 | 中 | 中 | 文档锁机制 |
| HITL 超时处理不当 | 低 | 低 | 默认决策 fallback |

### 时间风险

| 任务 | 预估 | 缓冲 | 总计 |
|------|------|------|------|
| HITL 后端 | 5天 | +1天 | 6天 |
| HITL 前端 | 3天 | +1天 | 4天 |
| 文档协作 | 3天 | +0.5天 | 3.5天 |
| 测试 + 文档 | 2天 | +0.5天 | 2.5天 |
| **总计** | 13天 | +3天 | **16天** |

**建议**: 如果进度紧张，可将 `report_revision` HITL 推迟到 Phase 3.7

---

## ✅ 本周任务清单 (Week of Oct 15)

### Day 1 (周二)
- [ ] 创建 `phase-3.6-hitl-collaboration` 分支
- [ ] 阅读 LangGraph interrupt 文档（2小时）
- [ ] 验证 LangGraph 版本（30分钟）
- [ ] 编写 HITL 架构设计文档草稿（2小时）
- [ ] 设计 WebSocket HITL 协议（2小时）

### Day 2 (周三)
- [ ] 完成 HITL 架构设计文档
- [ ] 设计数据库 Schema（1小时）
- [ ] 编写 Alembic 迁移脚本（1小时）
- [ ] 执行数据库迁移（30分钟）
- [ ] 设计 API 端点（1小时）
- [ ] 更新 OpenAPI 规范（1小时）

### Day 3 (周四)
- [ ] 实现 `query_approval_node` (3小时)
- [ ] 实现 `paper_selection_node` (3小时)
- [ ] 单元测试 HITL 节点 (2小时)

### Day 4 (周五)
- [ ] 实现 `/agent/hitl/respond` API (2小时)
- [ ] 实现 `/agent/hitl/pending` API (1小时)
- [ ] WebSocket 消息处理增强 (2小时)
- [ ] 集成测试后端 HITL 流程 (2小时)

### Day 5 (周六) - 可选加班
- [ ] Code Review
- [ ] 调整架构（如有必要）
- [ ] 准备前端开发环境

---

## 📞 协作与支持

### 技术讨论

**问题收集**:
1. LangGraph interrupt 的最佳实践？
2. WebSocket 断线重连的状态同步策略？
3. VS Code 文档编辑冲突如何优雅处理？

**讨论渠道**:
- GitHub Discussions (推荐)
- 项目 Wiki
- 开发者会议 (每周一)

### 外部支持

- **LangChain 社区**: Discord, GitHub Issues
- **VS Code 社区**: Stack Overflow, GitHub Discussions

---

## 🎉 期望成果

### Week 3 结束时

**用户体验**:
```
用户启动研究会话
    → AI 生成初步查询
    → 🔔 弹出审批卡片："是否使用此查询？"
    → 用户点击"批准"
    → AI 继续搜索论文
    → 🔔 弹出选择卡片："从100篇中选择关注哪些？"
    → 用户勾选 10 篇
    → AI 分析并生成报告
    → 📝 实时编辑 Markdown 文件
    → 用户看到变更高亮
    → 点击"接受所有修改"
    → ✅ 研究完成
```

**技术成就**:
- ✅ LangGraph interrupt 机制成功应用
- ✅ WebSocket 双向 HITL 通信稳定
- ✅ VS Code 文档编辑流畅无冲突
- ✅ 测试覆盖率 >80%
- ✅ 文档完整清晰

---

**作者**: 开发团队  
**创建日期**: 2025年10月14日  
**状态**: 📋 待开始  
**预计开始**: 2025年10月15日

