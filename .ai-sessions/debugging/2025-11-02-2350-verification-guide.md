# 快速验证指南 - 研究进度修复

## 🎯 目标

验证研究进度不再卡在 20%，能够正常完成整个研究流程。

**最新修复** (2025-11-02 23:55 UTC):
- ✅ 修复 Langfuse 未定义错误 (`LangfuseManager.trace()`)
- ✅ 修复 NotImplementedError (`AsyncPostgresSaver` + `AsyncConnectionPool`)
- ✅ 创建独立的同步和异步 graph
  - `graph` → 用于 `/agent/invoke` (同步端点)
  - `async_graph` → 用于 `/agent/stream` (WebSocket 异步端点)

---

## 🚀 测试步骤

### 步骤 1: 启动 Extension Development Host

1. 打开 VS Code
2. 打开 `vscode-extension` 文件夹
3. 按 `F5` 启动调试
4. 等待新窗口打开

---

### 步骤 2: 打开 Analytics Dashboard

1. 在新窗口中，按 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. 输入: `Auto Researcher: Show Analytics Dashboard`
3. 回车执行

---

### 步骤 3: 启动研究任务

1. 在 Dashboard 顶部的输入框中输入:
   ```
   vision llm recent advance
   ```

2. 点击 "🚀 Start Research" 按钮
   - 或者按 `Enter` 键

3. **预期行为**:
   - Dashboard 自动关闭
   - 弹出新的 "Research Progress" 面板
   - 显示通知: "🚀 Starting research on: 'vision llm recent advance'"

---

### 步骤 4: 观察进度更新

**关键观察点**:

| 时间 | 进度 | 状态 | 说明 |
|------|------|------|------|
| 0s | 10% | 🚀 Starting... | 初始化 |
| 2-3s | 20% | ✅ Task created | 任务创建成功 |
| 5-10s | **30-50%** | ⏸️ Waiting for approval | **HITL 暂停** ← 这是关键！ |
| 手动批准后 | 60-80% | 📚 Collecting papers | 文献收集 |
| 30-60s | 100% | ✅ Completed | 报告生成完成 |

**🚨 关键验证点**:

✅ **如果看到这些 = 修复成功**:
- 进度从 20% 继续更新到 30% 以上
- 显示 "⏸️ Waiting for user approval" 或类似的 HITL 提示
- 进度条持续更新（不卡住）

❌ **如果看到这些 = 修复失败**:
- 进度卡在 20% 超过 30 秒
- 没有任何状态更新
- 出现错误提示

---

### 步骤 5: 处理 HITL 暂停（如果出现）

**什么是 HITL?**
Human-in-the-Loop，人工审批环节。Agent 会暂停并等待你批准生成的搜索查询。

**如何批准?**

**方式 1: 使用后端 API (当前可用)**
```bash
# 1. 从进度面板中复制 Thread ID
# 2. 在终端执行:
curl -X POST "http://localhost:8121/agent/hitl/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "YOUR_THREAD_ID",
    "request_id": "hitl_query_approval_...",
    "approved": true
  }'
```

**方式 2: 等待自动超时 (未来改进)**
- 如果 5 分钟内没有批准，Agent 会自动继续（使用默认选择）

---

## ✅ 成功标准

### 必须满足 (P0)

- [ ] 进度从 20% 继续更新（不卡住）
- [ ] 能看到 HITL 暂停提示或直接跳过到文献收集
- [ ] 最终进度达到 100%

### 应该满足 (P1)

- [ ] 每个阶段的状态消息清晰（如 "📚 Found 12 papers"）
- [ ] HITL 批准后进度继续
- [ ] 最终生成研究报告

### 可选满足 (P2)

- [ ] 进度更新流畅（无明显延迟）
- [ ] 错误提示友好（如有错误）

---

## 🐛 如果测试失败

### 收集诊断信息

1. **复制进度面板内容**:
   - 截图或复制所有文本
   - 记录卡住的时间点和进度

2. **查看后端日志**:
   ```bash
   docker compose logs --tail=100 langgraph-api
   ```

3. **检查 thread_id**:
   - 从进度面板或通知中复制
   - 尝试手动查询状态:
     ```bash
     curl "http://localhost:8121/agent/state/{thread_id}"
     ```

4. **检查服务健康**:
   ```bash
   curl http://localhost:8121/ok
   docker compose ps
   ```

### 报告问题

如果测试失败，请提供:
1. 进度卡住的截图
2. 后端日志（最后 50 行）
3. Thread ID
4. 输入的研究主题
5. 卡住前最后看到的状态消息

---

## 📊 测试结果记录

**测试时间**: ___________  
**研究主题**: "vision llm recent advance"  
**Thread ID**: ___________  

**进度记录**:
- [ ] 0-20%: 任务创建 - ⏱️ 耗时: ___ 秒
- [ ] 20-50%: HITL 或查询生成 - ⏱️ 耗时: ___ 秒
- [ ] 50-80%: 文献收集 - ⏱️ 耗时: ___ 秒
- [ ] 80-100%: 报告生成 - ⏱️ 耗时: ___ 秒

**总耗时**: ___ 秒  
**结果**: ✅ 成功 / ❌ 失败  

**备注**:
```
(记录任何异常、卡顿或错误)
```

---

## 🎉 测试通过后的下一步

1. **更新会话文件**:
   - 在 `.ai-sessions/debugging/2025-11-02-2330-debug-progress-stuck-at-20.md` 中
   - 添加 "用户验证通过" 标记

2. **提交修复代码** (如有代码修改):
   ```bash
   git add .
   git commit -m "fix: Resolve research progress stuck at 20% due to Langfuse integration"
   git push origin dev
   ```

3. **更新 ROADMAP.md**:
   - 标记 Phase 4.1 Langfuse 集成状态
   - 添加后续改进任务

4. **关闭相关 Issue**:
   - 如果有 GitHub Issue，添加测试结果并关闭

---

## 💡 常见问题

### Q1: 进度在 HITL 暂停了，怎么继续?

**A**: 这是正常行为！Agent 在等待你批准生成的搜索查询。使用上面的 API 命令批准即可继续。

### Q2: 进度更新很慢，正常吗?

**A**: 取决于阶段:
- 查询生成: 2-5 秒 ✅
- 文献收集: 10-30 秒 ✅ (取决于查询数量)
- 报告生成: 5-15 秒 ✅

如果某个阶段超过 60 秒无更新，可能有问题。

### Q3: 看到 404 错误怎么办?

**A**: 这可能意味着:
1. 后端服务未启动: 运行 `docker compose up -d langgraph-api`
2. Thread ID 不存在: 检查输入是否正确
3. Agent 执行失败: 查看后端日志

---

**快速验证指南版本**: v1.0  
**创建时间**: 2025-11-02 23:50 UTC  
**适用版本**: dev branch (after Langfuse NoOp fix)
