# 研究循环测试指南

**Date**: 2025-11-06  
**Purpose**: 验证研究工作流的循环逻辑是否正常工作

---

## 测试配置

- **MAX_RESEARCH_LOOPS**: 2
- **循环触发条件**: `is_sufficient=False` 且 `loop_count < MAX_RESEARCH_LOOPS`
- **循环退出条件**: `is_sufficient=True` 或 `loop_count >= MAX_RESEARCH_LOOPS`

---

## 测试场景

### 场景 1: 研究充分（无需循环）

**测试主题**: "transformer architecture"

**预期流程**:
```
Loop 1:
  generate_initial_queries → execute_searches
  → reflection (is_sufficient=True, loop_count=1)
  → ✅ "Research is sufficient"
  → automated_resource_management → ... → report
```

**关键日志**:
```
[Research Loop] is_sufficient=True, loop_count=1/2
[Research Loop] ✅ Research is sufficient, proceeding to resource management
```

---

### 场景 2: 需要改进循环

**测试主题**: "recent advance on neuro ai9"

**预期流程**:
```
Loop 1:
  generate_initial_queries → execute_searches
  → reflection (is_sufficient=False, loop_count=1)
  → 🔄 "Insufficient research, looping back"
  
Loop 2:
  execute_searches (new queries)
  → reflection (is_sufficient=True/False, loop_count=2)
  → If True: ✅ → resource management
  → If False: ⚠️ "Max loops reached" → resource management
```

**关键日志**:
```
# First reflection
[Research Loop] is_sufficient=False, loop_count=1/2
[Research Loop] 🔄 Insufficient research, looping back with X new queries

# Second reflection
[Research Loop] is_sufficient=True/False, loop_count=2/2
[Research Loop] ✅/⚠️ Research is sufficient / Max loops reached
```

---

### 场景 3: 达到最大循环次数

**测试主题**: "未来的量子计算在人工智能中的应用前景" (复杂且模糊的主题)

**预期流程**:
```
Loop 1:
  → reflection (is_sufficient=False, loop_count=1)
  → 🔄 Loop back
  
Loop 2:
  → reflection (is_sufficient=False, loop_count=2)
  → ⚠️ "Max loops (2) reached"
  → automated_resource_management (使用已收集的论文)
  → ... → report (基于有限的数据生成报告)
```

**关键日志**:
```
[Research Loop] is_sufficient=False, loop_count=2/2
[Research Loop] ⚠️ Max loops (2) reached, proceeding to resource management
```

---

## 验证步骤

### 1. 启动监控

```bash
# 实时查看循环相关日志
docker compose logs -f langgraph-api | grep -E "(Research Loop|reflection_and_refinement|execute_searches)"
```

### 2. 运行测试

使用 VS Code 扩展创建研究任务，或使用 API：

```bash
# 示例: WebSocket 测试
# (通过 VS Code 扩展更方便)
```

### 3. 检查数据库

```bash
# 查看最新会话的循环次数
docker compose exec -T langgraph-postgres psql -U postgres -d postgres -c \
  "SELECT event_type, created_at FROM session_events WHERE session_id = (SELECT id FROM sessions ORDER BY created_at DESC LIMIT 1) ORDER BY created_at;"

# 检查是否生成了报告和论文
docker compose exec -T langgraph-postgres psql -U postgres -d postgres -c \
  "SELECT 
     (SELECT COUNT(*) FROM reports WHERE session_id = s.id) as report_count,
     (SELECT COUNT(*) FROM papers WHERE session_id = s.id) as paper_count
   FROM sessions s ORDER BY s.created_at DESC LIMIT 1;"
```

---

## 预期结果

### ✅ 成功标准

1. **循环触发正确**: 当 `is_sufficient=False` 时，能看到 `execute_searches` 被执行第二次
2. **循环次数限制**: 不会超过 `MAX_RESEARCH_LOOPS=2` 次
3. **最终生成报告**: 无论循环多少次，最终都能生成 manuscript 和 papers
4. **日志清晰**: 每次循环决策都有对应的 `[Research Loop]` 日志

### ❌ 失败标准

1. **无限循环**: 循环次数超过 MAX_RESEARCH_LOOPS
2. **过早退出**: 在 `is_sufficient=False` 且 `loop_count < MAX_RESEARCH_LOOPS` 时退出
3. **缺少报告**: 循环结束后没有生成 reports 或 papers
4. **日志缺失**: 看不到 `[Research Loop]` 日志输出

---

## 调试技巧

### 查看完整的节点执行序列

```bash
docker compose logs langgraph-api --since 5m | grep "NODE:"
```

预期输出示例（有循环）:
```
---NODE: generate_initial_queries---
---NODE: execute_searches (Loop 1)---
---NODE: execute_searches (Loop 1)---
---NODE: execute_searches (Loop 1)---
---NODE: reflection_and_refinement---
---NODE: execute_searches (Loop 2)---  ← 第二轮搜索
---NODE: execute_searches (Loop 2)---
---NODE: reflection_and_refinement---
---NODE: automated_resource_management---
---NODE: ingest_and_embed_documents---
---NODE: retrieve_and_synthesize_report---
```

### 查看 reflection 结果

```bash
docker compose logs langgraph-api --since 5m | grep "Reflection:"
```

预期输出:
```
Reflection: Sufficient? False. Gap: Need more information about X...
Reflection: Sufficient? True. Gap: ...
```

---

## 已知问题和注意事项

1. **Arxiv API 限制**: 如果触发了 API 速率限制，可能导致第二轮搜索返回空结果
2. **LLM 判断不稳定**: `is_sufficient` 的判断依赖于 LLM，可能对相同主题给出不同结果
3. **测试环境**: 在 `TEST_MODE=1` 下，某些外部 API 调用会被跳过

---

**测试负责人**: AI Assistant  
**最后更新**: 2025-11-06 14:00 UTC
