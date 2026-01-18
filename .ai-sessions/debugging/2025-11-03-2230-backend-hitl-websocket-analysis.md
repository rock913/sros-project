# Backend HITL WebSocket 流程分析报告

**日期**: 2025-11-03 22:30  
**文件**: `backend/src/agent/app.py`  
**端点**: `/agent/stream` (WebSocket)  
**问题**: WebSocket 在发送 HITL 请求后立即关闭

---

## 问题根源分析

### 当前实现流程

**文件**: `backend/src/agent/app.py` Lines 1450-1640

```python
# 1. WebSocket 端点开始流式传输
async for chunk in async_graph.astream(input_data, config=config):
    for node_name, state_update in chunk.items():
        # 发送进度更新
        await websocket.send_json({
            "type": "progress",
            "node": node_name,
            "message": f"Processing {node_name}..."
        })
        
        # Lines 1530-1575: HITL 检测与请求发送
        if state_update.get("hitl_pending"):
            hitl_request = state_update.get("hitl_request", {})
            
            # 发送 HITL 请求到前端
            await websocket.send_json({
                "type": "hitl_request",
                "request_id": hitl_request.get("request_id"),
                "decision_type": hitl_request.get("decision_type"),
                "prompt": hitl_request.get("prompt"),
                "options": hitl_request.get("options", []),
                "context": hitl_request.get("context", {}),
                "timeout_seconds": hitl_request.get("timeout_seconds", 300),
                "session_id": session_id,
                "thread_id": thread_id
            })
            
            print(f"[HITL] Sent request {hitl_request.get('request_id')} to frontend")
            
            # ❌ 问题：没有等待前端响应！
            # 代码继续执行，循环结束，WebSocket 关闭

# 2. 循环结束后立即发送完成信号并关闭
await websocket.send_json({
    "type": "complete",  # ❌ 错误：研究还没真正完成
    "session_id": session_id,
    "thread_id": thread_id
})

# 3. finally 块中关闭连接
finally:
    if websocket.client_state == WebSocketState.CONNECTED:
        await websocket.close()  # ❌ 立即关闭，前端无法发送响应
```

### 问题说明

**核心问题**: `async_graph.astream()` 在遇到 HITL 节点时**不会暂停流式传输**。

**当前行为**:
1. Agent 图执行到 `query_generation_node`
2. 节点设置 `state["hitl_pending"] = True` 和 `state["hitl_request"] = {...}`
3. 条件边返回空列表 `[]`（表示暂停）
4. **但 `astream()` 并不知道要等待外部输入**
5. 流式循环立即结束
6. 发送 `{"type": "complete"}` 并关闭 WebSocket

**预期行为**:
1. 发送 HITL 请求后，WebSocket 应保持连接
2. 等待前端发送 `{"type": "hitl_response", ...}`
3. 收到响应后，更新 graph 状态
4. 使用 `graph.invoke()` 继续执行（或重新启动流）
5. 完成后再关闭 WebSocket

---

## 设计缺陷

### 1. LangGraph 检查点机制误解

**误解**: 认为 `checkpointer` 会自动暂停并恢复流式传输

**实际**: 
- `checkpointer` 只负责**持久化状态**到数据库
- 不会自动暂停 `astream()` 的执行
- 条件边返回 `[]` 只是让图**不继续往下走**，但不会暂停流

### 2. 双向通信设计缺失

**当前实现**: 单向流（后端 → 前端）
```python
# 只有发送，没有接收
async for chunk in async_graph.astream(...):
    await websocket.send_json(...)
```

**需要**: 双向通信（后端 ⇄ 前端）
```python
# 需要同时监听 WebSocket 消息
async def handle_messages():
    while True:
        message = await websocket.receive_json()
        if message['type'] == 'hitl_response':
            # 处理响应并继续图执行

asyncio.create_task(handle_messages())
```

### 3. HITL 流程设计问题

**当前架构**:
```
Graph 执行 → 设置 hitl_pending 标志 → 条件边返回 [] → 流结束
```

**正确架构应该是**:
```
Graph 执行 → 遇到 HITL 节点 → 暂停图 → 发送请求 → 等待响应 → 更新状态 → 继续图
```

---

## 解决方案

### 方案 A: 重构为真正的双向 WebSocket（推荐）

**改动**: 大幅重构 `/agent/stream` 端点

**实现步骤**:

1. **创建消息监听任务**
```python
async def listen_for_client_messages(websocket, message_queue):
    """监听前端消息（如 hitl_response）"""
    try:
        while True:
            message = await websocket.receive_json()
            await message_queue.put(message)
    except WebSocketDisconnect:
        await message_queue.put({"type": "disconnect"})
```

2. **修改流式执行逻辑**
```python
@app.websocket("/agent/stream")
async def stream_agent_progress(websocket: WebSocket):
    message_queue = asyncio.Queue()
    
    # 启动消息监听任务
    listen_task = asyncio.create_task(
        listen_for_client_messages(websocket, message_queue)
    )
    
    try:
        # 开始流式执行
        async for chunk in async_graph.astream(input_data, config=config):
            for node_name, state_update in chunk.items():
                # 发送进度
                await websocket.send_json(...)
                
                # 检测 HITL 请求
                if state_update.get("hitl_pending"):
                    hitl_request = state_update.get("hitl_request", {})
                    request_id = hitl_request.get("request_id")
                    
                    # 发送 HITL 请求
                    await websocket.send_json({
                        "type": "hitl_request",
                        ...
                    })
                    
                    # ✅ 等待前端响应
                    hitl_response = await wait_for_hitl_response(
                        message_queue, 
                        request_id,
                        timeout=300
                    )
                    
                    # ✅ 更新数据库中的 HITL 记录
                    update_hitl_decision(
                        request_id,
                        hitl_response["approved"],
                        hitl_response.get("modified_data")
                    )
                    
                    # ✅ 使用 graph.invoke() 继续执行
                    # 注意：需要从暂停点恢复
                    config["configurable"]["checkpoint_id"] = get_latest_checkpoint(thread_id)
                    
                    # 继续流式传输
                    async for chunk2 in async_graph.astream(None, config=config):
                        ...
        
        # 发送完成信号
        await websocket.send_json({"type": "complete", ...})
        
    finally:
        listen_task.cancel()
        await websocket.close()
```

3. **辅助函数**
```python
async def wait_for_hitl_response(message_queue, request_id, timeout=300):
    """等待特定 request_id 的 HITL 响应"""
    try:
        while True:
            message = await asyncio.wait_for(
                message_queue.get(), 
                timeout=timeout
            )
            
            if message.get("type") == "hitl_response" and \
               message.get("request_id") == request_id:
                return message
            
            # 忽略其他消息或放回队列
    
    except asyncio.TimeoutError:
        # 超时，使用默认决策
        return {"request_id": request_id, "approved": False, "timeout": True}
```

**优点**:
- ✅ 真正的双向通信
- ✅ 支持多次 HITL 交互
- ✅ 符合 WebSocket 设计原则

**缺点**:
- ❌ 需要大量重构
- ❌ 复杂度较高
- ❌ 需要处理并发消息

---

### 方案 B: 混合模式（WebSocket + HTTP 回调）

**改动**: 中等规模重构

**实现思路**:

1. **WebSocket 流只负责发送**（保持当前逻辑）
2. **前端通过 HTTP POST 发送 HITL 响应**（已存在的 `/agent/hitl/respond`）
3. **后端使用事件循环等待数据库更新**

```python
async for chunk in async_graph.astream(input_data, config=config):
    if state_update.get("hitl_pending"):
        # 发送 HITL 请求
        await websocket.send_json({"type": "hitl_request", ...})
        
        # ✅ 等待数据库中的 HITL 记录被更新
        hitl_response = await poll_hitl_decision(request_id, timeout=300)
        
        if not hitl_response:
            # 超时，使用默认决策
            ...
        
        # ✅ 从检查点恢复并继续
        config["configurable"]["checkpoint_id"] = get_latest_checkpoint(thread_id)
        async for chunk2 in async_graph.astream(None, config=config):
            ...
```

**辅助函数**:
```python
async def poll_hitl_decision(request_id, timeout=300):
    """轮询数据库直到 HITL 决策完成"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # 查询数据库
        hitl_record = db.query(HITLDecision).filter_by(
            request_id=request_id
        ).first()
        
        if hitl_record and not hitl_record.is_pending:
            return {
                "approved": hitl_record.user_decision == "approved",
                "modified_data": hitl_record.modified_data
            }
        
        # 等待 1 秒后重试
        await asyncio.sleep(1)
    
    return None  # 超时
```

**优点**:
- ✅ 重构量适中
- ✅ 利用现有的 HTTP 端点
- ✅ 数据库作为通信中间层

**缺点**:
- ⚠️  需要轮询数据库（性能开销）
- ⚠️  WebSocket 仍然是单向流（不够优雅）

---

### 方案 C: 最小改动（临时方案，已实施）

**改动**: 前端自动批准

**实现**: ✅ 已完成（参见 Debugging Snapshot #1）

**优点**:
- ✅ 无需后端改动
- ✅ 研究流程立即恢复

**缺点**:
- ❌ 失去人工审核能力
- ❌ 不符合 HITL 设计初衷
- ❌ 只是权宜之计

---

## 推荐方案

**短期（本周）**: 方案 C（已实施） + 方案 B
- 保持前端自动批准，确保功能可用
- 逐步实现方案 B，通过数据库轮询恢复 HITL

**中期（下周）**: 完整实现方案 A
- 重构 WebSocket 为真正的双向通信
- 支持完整的 HITL 审批流程
- 添加超时处理和默认决策

**长期（下月）**: 优化与增强
- WebSocket 消息队列优化
- 支持多个 HITL 请求并发
- 添加 HITL 决策审计日志
- 实现前端超时倒计时 UI

---

## 实施计划

### Phase 1: 数据库轮询方案（2-3 天）

**任务清单**:
- [ ] 创建 `poll_hitl_decision()` 辅助函数
- [ ] 修改 `/agent/stream` 在 HITL 请求后等待决策
- [ ] 实现从检查点恢复流式传输
- [ ] 测试完整流程（发送请求 → HTTP 响应 → 继续执行）
- [ ] 前端移除自动批准，启用 HITL UI

**验证标准**:
- ✅ 研究暂停在 HITL 请求
- ✅ 前端显示审批 UI
- ✅ 用户批准后研究继续
- ✅ WebSocket 保持连接直到真正完成

### Phase 2: 双向 WebSocket（1 周）

**任务清单**:
- [ ] 创建消息监听任务 `listen_for_client_messages()`
- [ ] 重构流式执行逻辑支持消息队列
- [ ] 实现 `wait_for_hitl_response()` 函数
- [ ] 处理超时和错误情况
- [ ] 前端改为通过 WebSocket 发送 HITL 响应
- [ ] 完整端到端测试

**验证标准**:
- ✅ WebSocket 双向通信正常
- ✅ 支持多次 HITL 交互
- ✅ 超时自动使用默认决策
- ✅ 错误恢复机制健壮

---

## 相关文件

### 后端
- `backend/src/agent/app.py` - WebSocket 端点（需要重构）
- `backend/src/agent/graph.py` - Graph 定义（检查点配置）
- `backend/src/agent/models.py` - HITLDecision 数据模型

### 前端
- `vscode-extension/src/api.ts` - WebSocket 客户端
- `vscode-extension/src/extension.ts` - HITL UI 和处理逻辑

### 调试日志
- `.ai-sessions/debugging/2025-11-03-0040-phase-4.1-debug-hitl-ui-optimization.md`
- `.ai-sessions/debugging/2025-11-03-2230-backend-hitl-websocket-analysis.md` (本文件)

---

**分析完成时间**: 2025-11-03 22:30  
**下一步**: 等待用户确认修复方案选择
