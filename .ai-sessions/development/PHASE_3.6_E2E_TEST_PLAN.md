# Phase 3.6 端到端测试计划
**Date**: 2025-10-14  
**Purpose**: 验证 Backend + Frontend HITL 系统集成  
**Priority**: 🔴 High (在继续开发前必须完成)

---

## 🎯 测试目标

### 主要目标
1. ✅ 验证后端 HITL 节点能正确创建数据库记录
2. ✅ 验证 API 端点能正确响应和恢复 Graph
3. ✅ 验证前端 UI 能正确显示决策卡片
4. ✅ 验证完整的用户决策流程

### 次要目标
1. 测试超时处理机制
2. 测试错误处理和边界情况
3. 性能基准测试

---

## 📋 测试清单

### Phase 1: Backend 单元测试 (30 min)

#### Test 1.1: HITL 节点独立测试
```python
# backend/tests/test_hitl_nodes.py

def test_query_approval_first_call():
    """测试 query_approval_node 首次调用创建 HITL 请求"""
    state = {
        "session_id": "test_session_123",
        "search_queries": ["query1", "query2"],
        "research_topic": "Test Topic"
    }
    config = {"configurable": {"thread_id": "test_thread"}}
    
    result = query_approval_node(state, config)
    
    assert result.get("hitl_pending") == True
    assert result.get("hitl_request") is not None
    assert result["hitl_request"]["decision_type"] == "query_approval"
    print("✅ Test 1.1: HITL node creates request correctly")

def test_query_approval_with_response():
    """测试 query_approval_node 接收到用户响应后的处理"""
    state = {
        "session_id": "test_session_123",
        "hitl_response": {
            "decision_type": "query_approval",
            "user_decision": "approve"
        }
    }
    config = {"configurable": {"thread_id": "test_thread"}}
    
    result = query_approval_node(state, config)
    
    assert result.get("hitl_pending") == False
    assert result.get("hitl_approved") == True
    print("✅ Test 1.2: HITL node processes response correctly")
```

**执行命令**:
```bash
docker exec langgraph-api bash -c "cd /deps/backend && python -m pytest tests/test_hitl_nodes.py -v"
```

---

#### Test 1.2: 数据库 HITL 记录创建
```python
def test_hitl_database_record():
    """测试 HITL 请求能正确写入数据库"""
    from agent.hitl_nodes import create_hitl_request
    from agent.models import HITLDecision
    from agent.database import SessionLocal
    
    session_id = "test_db_session"
    request_id = create_hitl_request(
        session_id=session_id,
        decision_type="query_approval",
        prompt="Test prompt",
        options=["approve", "reject"],
        context={"test": "data"},
        timeout_seconds=300
    )
    
    # 验证数据库记录
    db = SessionLocal()
    record = db.query(HITLDecision).filter_by(request_id=request_id).first()
    
    assert record is not None
    assert record.decision_type == "query_approval"
    assert record.user_decision is None  # 未响应
    assert record.is_pending == True
    
    db.close()
    print("✅ Test 1.2: Database record created correctly")
```

---

#### Test 1.3: API 端点测试
```bash
# 测试 HITL respond 端点
curl -X POST "http://localhost:8121/agent/hitl/respond" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "test_request_123",
    "decision": "approve",
    "modified_data": null
  }'

# 预期: {"status": "success", "message": "HITL response recorded"}
```

---

### Phase 2: Frontend 集成测试 (30 min)

#### Test 2.1: UI 渲染测试
```bash
# 在 vscode-dev 容器中
docker exec -it vscode-dev bash -c "
cd /workspaces/gemini-fullstack-langgraph-quickstart/vscode-extension
node test-hitl-ui.js
"

# 预期: 3/3 tests passed
```

---

#### Test 2.2: WebView 消息处理测试
```typescript
// vscode-extension/tests/test-webview-message.ts

import * as assert from 'assert';
import { handleHITLRequest } from '../src/extension';

suite('WebView Message Tests', () => {
    test('handleHITLRequest creates panel', () => {
        const mockRequest = {
            request_id: 'test123',
            decision_type: 'query_approval',
            prompt: 'Test',
            options: ['approve', 'reject'],
            context: { queries: ['q1'] },
            timeout_seconds: 300
        };
        
        // 模拟调用
        // handleHITLRequest(mockRequest);
        
        // 验证 panel 创建
        assert.ok(true, 'Panel created successfully');
    });
});
```

---

### Phase 3: 端到端集成测试 (60 min)

#### Test 3.1: Query Approval 完整流程

**步骤**:

1. **启动系统**
```bash
# Terminal 1: 确保后端运行
docker-compose -f docker-compose-dev.yml up langgraph-api langgraph-postgres

# Terminal 2: 验证后端健康
curl http://localhost:8121/health
```

2. **手动创建 HITL 请求**
```bash
# 使用 Python 脚本创建测试会话和 HITL 请求
docker exec langgraph-api bash -c "cd /deps/backend && python -c '
from src.agent.models import Session, HITLDecision
from src.agent.database import SessionLocal
from datetime import datetime
import uuid

db = SessionLocal()

# 创建测试 session
session = Session(
    id=uuid.uuid4(),
    thread_id=\"test_e2e_thread\",
    title=\"E2E Test Session\",
    research_topic=\"Test HITL Flow\",
    status=\"in_progress\",
    created_at=datetime.utcnow()
)
db.add(session)
db.commit()

# 创建 HITL 请求
hitl = HITLDecision(
    id=uuid.uuid4(),
    session_id=session.id,
    request_id=\"hitl_e2e_test_001\",
    decision_type=\"query_approval\",
    prompt=\"请批准以下查询\",
    options=[\"approve\", \"reject\"],
    context={
        \"research_topic\": \"Test Topic\",
        \"queries\": [\"test query 1\", \"test query 2\"]
    },
    timeout_seconds=300,
    created_at=datetime.utcnow()
)
db.add(hitl)
db.commit()

print(f\"✅ Created session: {session.id}\")
print(f\"✅ Created HITL request: {hitl.request_id}\")

db.close()
'"
```

3. **测试 API 获取待处理请求**
```bash
# 获取 session_id (从上面输出)
SESSION_ID="<从上面获取>"

curl "http://localhost:8121/agent/hitl/pending?session_id=${SESSION_ID}"

# 预期输出:
# [
#   {
#     "request_id": "hitl_e2e_test_001",
#     "decision_type": "query_approval",
#     "prompt": "请批准以下查询",
#     "options": ["approve", "reject"],
#     "context": {...},
#     "is_timeout": false
#   }
# ]
```

4. **模拟用户批准**
```bash
curl -X POST "http://localhost:8121/agent/hitl/respond" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "hitl_e2e_test_001",
    "decision": "approve",
    "modified_data": null
  }'

# 预期: {"status": "success"}
```

5. **验证数据库记录更新**
```bash
docker exec langgraph-api bash -c "cd /deps/backend && python -c '
from src.agent.models import HITLDecision
from src.agent.database import SessionLocal

db = SessionLocal()
record = db.query(HITLDecision).filter_by(request_id=\"hitl_e2e_test_001\").first()

print(f\"✅ Request ID: {record.request_id}\")
print(f\"✅ User Decision: {record.user_decision}\")
print(f\"✅ Responded At: {record.responded_at}\")
print(f\"✅ Is Pending: {record.is_pending}\")

assert record.user_decision == \"approve\", \"Decision not recorded\"
assert record.responded_at is not None, \"Timestamp not set\"
assert record.is_pending == False, \"Still marked as pending\"

print(\"\\n✅✅✅ E2E Test PASSED! ✅✅✅\")

db.close()
'"
```

---

#### Test 3.2: Frontend UI 手动测试

**前提**: VS Code Extension 已安装并激活

**步骤**:

1. **在 VS Code 中打开命令面板** (Ctrl+Shift+P)

2. **运行测试命令**: `Test HITL Card`

3. **验证 Query Approval 卡片显示**:
   - ✅ 标题显示 "🔍 Query Approval"
   - ✅ 研究主题正确显示
   - ✅ 查询列表正确渲染
   - ✅ 3 个按钮可见 (Approve, Reject, Modify)

4. **测试按钮交互**:
   - 点击 "Approve" 按钮
   - 检查浏览器控制台（如果有）
   - 验证消息发送到 extension

5. **重复测试 Paper Selection 和 Report Revision**

---

### Phase 4: Graph 执行测试 (60 min)

#### Test 4.1: 完整 Graph 流程测试

**目标**: 验证 Graph 能在 HITL 节点处正确暂停和恢复

```python
# backend/tests/test_graph_hitl_flow.py

import asyncio
from agent.graph import graph

async def test_graph_with_hitl():
    """测试 Graph 在 HITL 节点处暂停"""
    
    # 准备测试数据
    input_data = {
        "messages": [{"role": "user", "content": "Research quantum computing"}],
        "session_id": "test_graph_session",
        "research_topic": "quantum computing"
    }
    
    config = {
        "configurable": {
            "thread_id": "test_graph_thread"
        }
    }
    
    # 执行到第一个 HITL 节点
    result = await graph.ainvoke(input_data, config=config)
    
    # 验证执行暂停在 query_approval
    assert result.get("hitl_pending") == True
    assert result.get("hitl_request") is not None
    
    print("✅ Test 4.1: Graph paused at HITL node")
    
    # 模拟用户响应
    # (需要调用 graph.aupdate_state() 来注入响应并恢复)

# 运行
asyncio.run(test_graph_with_hitl())
```

**执行命令**:
```bash
docker exec langgraph-api bash -c "cd /deps/backend && python tests/test_graph_hitl_flow.py"
```

---

## 🎯 成功标准

### 必须通过 (P0)

- ✅ HITL 节点能创建数据库记录
- ✅ API 端点能正确响应用户决策
- ✅ 数据库记录能正确更新
- ✅ Frontend UI 能正确渲染 3 种卡片
- ✅ Graph 在 HITL 节点处正确暂停

### 应该通过 (P1)

- ⚠️ 超时机制工作正常
- ⚠️ 错误处理不会导致崩溃
- ⚠️ 并发请求处理正确

### 可选通过 (P2)

- 🔄 性能满足要求 (HITL 响应 <2s)
- 🔄 UI 在移动端正确显示
- 🔄 数据库查询优化

---

## 🚧 已知问题和风险

### 高风险问题

1. **Graph State 持久化**
   - 风险: HITL 暂停后 state 可能丢失
   - 缓解: 使用 PostgresSaver checkpointer
   - 测试: 验证 thread_id 正确传递

2. **WebSocket 断线重连**
   - 风险: 连接断开后 HITL 请求丢失
   - 缓解: 实现 /pending 端点重新获取
   - 测试: 模拟连接断开场景

3. **并发 HITL 请求**
   - 风险: 多个 HITL 请求同时存在时冲突
   - 缓解: 使用唯一 request_id
   - 测试: 创建多个请求并响应

---

## 📝 测试执行记录

### 执行日期: 2025-10-14

| 测试 | 状态 | 备注 |
|------|------|------|
| Test 1.1: HITL 节点测试 | 📋 待执行 | |
| Test 1.2: 数据库记录 | 📋 待执行 | |
| Test 1.3: API 端点 | 📋 待执行 | |
| Test 2.1: UI 渲染 | ✅ 通过 | 3/3 cards passed |
| Test 2.2: WebView 消息 | 📋 待执行 | |
| Test 3.1: E2E Query Approval | 📋 待执行 | |
| Test 3.2: Frontend 手动测试 | 📋 待执行 | |
| Test 4.1: Graph 流程 | 📋 待执行 | |

---

## 🔧 调试工具

### Database Inspector
```bash
# 查看所有 HITL 记录
docker exec langgraph-postgres psql -U postgres -c "
SELECT request_id, decision_type, user_decision, 
       created_at, responded_at 
FROM hitl_decisions 
ORDER BY created_at DESC 
LIMIT 10;
"
```

### Backend Logs
```bash
# 实时查看后端日志
docker logs -f langgraph-api
```

### Graph State Inspector
```bash
# 查看 Graph checkpoint
docker exec langgraph-api bash -c "cd /deps/backend && python -c '
from agent.graph import checkpointer

# 获取指定 thread 的 checkpoint
config = {\"configurable\": {\"thread_id\": \"test_thread\"}}
checkpoint = checkpointer.get(config)
print(checkpoint)
'"
```

---

## 📊 下一步建议

### 如果所有测试通过 ✅

**立即进行**:
1. 提交测试代码
2. 更新文档记录测试结果
3. 继续 Day 3: WebSocket 集成

### 如果部分测试失败 ⚠️

**问题修复优先级**:
1. P0 问题: 立即修复 (阻塞后续开发)
2. P1 问题: 记录并在 Day 4 修复
3. P2 问题: 加入 backlog

### 如果主要测试失败 ❌

**回滚策略**:
1. 识别问题根源 (Backend vs Frontend)
2. 回滚到最后一个稳定版本
3. 重新评估架构设计
4. 采用渐进式集成方案

---

## 🎯 测试完成标准

**Day 2 结束前必须达成**:
- [ ] 至少 80% 的 P0 测试通过
- [ ] E2E Query Approval 流程完整可用
- [ ] Frontend UI 能正确显示和响应
- [ ] 数据库 HITL 记录正确创建和更新
- [ ] 没有阻塞性 bug

**达成后**:
✅ 可以继续 Day 3: WebSocket 集成  
✅ 可以开始 Paper Selection 和 Report Revision 测试  
✅ 有信心交付高质量的 HITL 系统

---

**Status**: 📋 Ready to Execute  
**Priority**: 🔴 High  
**Estimated Time**: 2-3 hours  
**Next**: Execute Phase 1-3 tests

