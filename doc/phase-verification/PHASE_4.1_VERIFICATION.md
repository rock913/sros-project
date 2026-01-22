# Phase 4.1 部署验证清单

**创建时间**: 2025-10-16  
**状态**: 准备验证

---

## ✅ 验证步骤

### 1. 配置 LangFuse API 密钥 ⏳

**选择一种方式：**

#### 方式 A: 使用配置向导（推荐）
```bash
./scripts/setup_langfuse.sh
```

#### 方式 B: 手动配置
```bash
# 1. 访问 http://localhost:3000
# 2. 登录并获取 API 密钥
# 3. 编辑 .env 文件
nano .env
# 4. 替换占位符为实际密钥
```

**验证结果：**
- [ ] Public Key 已设置 (pk-lf-...)
- [ ] Secret Key 已设置 (sk-lf-...)
- [ ] Host 已设置 (http://localhost:3000)

---

### 2. 重新构建后端容器 ⏳

```bash
# 重新构建容器（包含 langfuse 依赖）
docker-compose -f docker-compose-dev.yml build langgraph-api

# 预计时间: 2-3 分钟
```

**验证结果：**
- [ ] 构建成功，无错误
- [ ] langfuse 包已安装

---

### 3. 启动服务 ⏳

```bash
# 启动所有服务
docker-compose -f docker-compose-dev.yml up -d

# 查看日志
docker-compose -f docker-compose-dev.yml logs -f langgraph-api
```

**预期日志输出：**
```
--- Initializing database ---
--- Database initialized ---
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**验证结果：**
- [ ] 服务启动成功
- [ ] 无 LangFuse 相关错误

---

### 4. 运行 LangFuse 连接测试 ⏳

```bash
# 在容器内运行测试脚本
docker exec -it langgraph-api python /deps/backend/test_langfuse_connection.py
```

**预期输出：**
```
======================================================================
LangFuse Connection Test
======================================================================

📋 Step 1: Checking environment variables...
✅ LANGFUSE_PUBLIC_KEY: pk-lf-xxxxxxx...
✅ LANGFUSE_SECRET_KEY: sk-lf-xxxxxxx...
✅ LANGFUSE_HOST: http://localhost:3000

📦 Step 2: Importing LangFuse SDK...
✅ LangFuse SDK imported successfully

🔌 Step 3: Initializing LangFuse client...
✅ LangFuse client initialized

📊 Step 4: Creating test trace...
✅ Test trace created
   Trace ID: xxx-xxx-xxx

🔍 Step 5: Creating test span...
✅ Test span created and completed

📝 Step 6: Updating trace output...
✅ Trace output updated

🚀 Step 7: Flushing data to LangFuse...
✅ Data flushed to LangFuse

======================================================================
✅ LangFuse Connection Test PASSED!
======================================================================
```

**验证结果：**
- [ ] 所有 7 个步骤通过
- [ ] 测试 trace 创建成功

---

### 5. 在 LangFuse Dashboard 验证 ⏳

```bash
# 打开浏览器
xdg-open http://localhost:3000  # Linux
# 或直接访问 http://localhost:3000
```

**验证步骤：**
1. 登录 LangFuse Dashboard
2. 进入 **Traces** 页面
3. 查找名为 **"Connection Test"** 的 trace
4. 点击查看详情

**验证 Trace 内容：**
- [ ] Input 包含: message, timestamp, test_type
- [ ] Output 包含: status="success", test_results
- [ ] Tags 包含: test, connection, automated
- [ ] 包含 1 个 Span: "Test Span"

---

### 6. 运行端到端研究测试 ⏳

```bash
# 启动前端（新终端窗口）
cd frontend
npm run dev

# 访问 http://localhost:5173
```

**测试流程：**
1. 创建新研究会话
2. 输入研究主题: "AI in Healthcare"
3. 等待流程完成（约 2-3 分钟）
4. 观察实时日志输出

**验证结果：**
- [ ] 研究流程成功完成
- [ ] 报告生成成功
- [ ] 无错误发生

---

### 7. 在 LangFuse 验证完整 Trace ⏳

打开 LangFuse Dashboard (http://localhost:3000)，验证以下 Traces：

| Trace 名称 | 说明 | 状态 |
|-----------|------|------|
| **WebSocket Research Session** | 整个研究会话 | [ ] |
| **HITL Query Approval** | 查询审批决策 | [ ] (如触发) |
| **HITL Paper Selection** | 论文选择决策 | [ ] (如触发) |
| **Report Synthesis** | 报告生成 | [ ] |
| **Document Diff Generation** | 文档差异检测 | [ ] |
| **HITL Report Revision** | 报告修改决策 | [ ] (如触发) |

**点击 "WebSocket Research Session" trace，验证：**
- [ ] Timeline 显示完整流程
- [ ] Spans 包含文档更新和 HITL 请求
- [ ] Input/Output 数据完整
- [ ] 无错误状态

---

## 🎯 验证结果统计

### 核心功能验证

- [ ] **环境配置**: LangFuse API 密钥已配置
- [ ] **服务启动**: 后端服务正常运行
- [ ] **连接测试**: LangFuse 连接测试通过
- [ ] **Dashboard**: 测试 trace 在 Dashboard 中可见
- [ ] **端到端**: 完整研究流程成功完成
- [ ] **Trace 完整性**: 所有关键 trace 都已记录

### 覆盖率检查

- [ ] **HITL 节点**: 3/3 个节点 trace 可见
- [ ] **报告生成**: 1/1 个节点 trace 可见
- [ ] **文档协作**: 2/2 个函数 trace 可见
- [ ] **WebSocket**: 1/1 个端点 trace 可见

---

## ❌ 故障排查

### 问题 1: 环境变量未生效

**症状**: `LANGFUSE_PUBLIC_KEY is not set`

**解决方法**:
```bash
# 检查环境变量
docker exec -it langgraph-api env | grep LANGFUSE

# 如果为空，重启服务
docker-compose -f docker-compose-dev.yml restart langgraph-api
```

---

### 问题 2: LangFuse SDK 未安装

**症状**: `ModuleNotFoundError: No module named 'langfuse'`

**解决方法**:
```bash
# 重新构建容器
docker-compose -f docker-compose-dev.yml build langgraph-api

# 或临时手动安装
docker exec -it langgraph-api pip install langfuse
```

---

### 问题 3: 连接 LangFuse 失败

**症状**: `Connection refused` 或 `Authentication failed`

**解决方法**:
```bash
# 1. 检查 LangFuse 服务
curl -I http://localhost:3000

# 2. 验证密钥格式
# Public Key 应以 pk-lf- 开头
# Secret Key 应以 sk-lf- 开头

# 3. 重新生成密钥
# 访问 http://localhost:3000 → Settings → API Keys
```

---

### 问题 4: Trace 未出现在 Dashboard

**可能原因**:
1. 数据尚未上传（异步，延迟几秒）
2. LangFuse 服务问题
3. 网络连接问题

**解决方法**:
```bash
# 1. 等待 10-30 秒后刷新 Dashboard

# 2. 检查后端日志
docker-compose -f docker-compose-dev.yml logs -f langgraph-api | grep -i langfuse

# 3. 检查 LangFuse 服务日志
# (如果使用 Docker 部署 LangFuse)
cd langfuse
docker-compose logs -f
```

---

## 🎉 验证完成标准

所有以下项目都应打勾 ✅：

- [ ] 环境配置完成
- [ ] 服务成功启动
- [ ] 连接测试通过
- [ ] Dashboard 可访问
- [ ] 测试 trace 可见
- [ ] 端到端测试通过
- [ ] 所有关键 trace 完整

**当所有项目都打勾后，Phase 4.1 部署验证完成！** 🎉

---

## 📚 参考文档

- **快速部署**: `QUICKSTART_LANGFUSE.md`
- **配置指南**: `.ai-sessions/development/2025-10-16-1000-phase-4.1-guide-langfuse-configuration.md`
- **实施报告**: `.ai-sessions/development/2025-10-15-1700-phase-4.1-implementation-langfuse-integration.md`

---

**验证清单创建时间**: 2025-10-16  
**下一步**: 验证通过后开始 Phase 4.2 (性能测试与优化)
