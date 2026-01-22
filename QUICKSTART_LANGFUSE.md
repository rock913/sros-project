# Phase 4.1 LangFuse 集成 - 快速启动指南

**更新时间**: 2025-10-16 12:30  
**适用场景**: 首次部署 Phase 4.1 LangFuse 可观测性功能  
**预计时间**: 15-30 分钟

---

## 🚀 快速启动 (3 步完成)

### 步骤 1: 配置 LangFuse 连接 (5 分钟)

#### 选项 A: 使用已有的 LangFuse 服务

```bash
# 1. 复制环境变量模板
cp .env.langfuse.example .env

# 2. 编辑 .env 文件，填入你的 LangFuse 配置
nano .env
```

修改以下内容：
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-your-actual-public-key
LANGFUSE_SECRET_KEY=sk-lf-your-actual-secret-key
LANGFUSE_HOST=http://your-langfuse-host:3000
```

#### 选项 B: 快速启动本地 LangFuse (首次使用)

```bash
# 1. 创建 LangFuse 目录
mkdir -p langfuse && cd langfuse

# 2. 下载 docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/langfuse/langfuse/main/docker-compose.yml

# 3. 启动 LangFuse
docker-compose up -d

# 4. 访问 http://localhost:3000
#    - 注册账号
#    - 登录后进入 Settings → API Keys
#    - 创建新的 API Key
#    - 复制 Public Key 和 Secret Key

# 5. 返回项目根目录并配置
cd ..
cp .env.langfuse.example .env
nano .env  # 填入刚才复制的 keys

# 设置如下:
# LANGFUSE_PUBLIC_KEY=pk-lf-xxx  (从 LangFuse 复制)
# LANGFUSE_SECRET_KEY=sk-lf-xxx  (从 LangFuse 复制)
# LANGFUSE_HOST=http://localhost:3000
```

---

### 步骤 2: 重启后端服务 (3 分钟)

```bash
# 1. 重新构建容器 (包含 langfuse 依赖)
docker-compose -f docker-compose-dev.yml build langgraph-api

# 2. 启动所有服务
docker-compose -f docker-compose-dev.yml up -d

# 3. 查看日志 (确认没有错误)
docker-compose -f docker-compose-dev.yml logs -f langgraph-api | head -50

# 按 Ctrl+C 停止查看日志
```

**预期输出**:
```
--- Initializing database ---
--- Database initialized ---
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ 如果看到 "Application startup complete"，说明服务启动成功！

---

### 步骤 3: 验证 LangFuse 集成 (5 分钟)

LangFuse Connection Test

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

✅ LangFuse Connection Test PASSED!

📊 Next Steps:
   1. Visit your LangFuse Dashboard: http://localhost:3000
   2. Go to the 'Traces' page
   3. Look for a trace named 'Connection Test'
   ...
```

✅ 如果看到 "LangFuse Connection Test PASSED!"，说明集成成功！
#### 3.1 运行连接测试脚本

```bash
# 在容器内运行测试脚本
docker exec -it langgraph-api python -m pytest /deps/backend/tests/infrastructure/langfuse/test_langfuse_connection.py -v
```

**预期输出**:
```
===================================== test session starts ======================================
platform linux -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /deps/backend
configfile: pytest.ini
plugins: anyio-4.10.0, bdd-8.1.0, mock-3.15.1, asyncio-1.3.0, langsmith-0.6.3
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/infrastructure/langfuse/test_langfuse_connection.py::test_langfuse_connection PASSED [100%]

====================================== 1 passed in 1.79s =======================================

📊 Next Steps:
   1. Visit your LangFuse Dashboard: http://localhost:3000
   2. Go to the 'Traces' page
   3. Look for a trace named 'Connection Test'
   ...
```

✅ 如果看到 "1 passed"，说明集成成功！
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

📊 Next Steps:
   1. Visit your LangFuse Dashboard: http://localhost:3000
   2. Go to the 'Traces' page
   3. Look for a trace named 'Connection Test'
   ...
```

✅ 如果看到 "LangFuse Connection Test PASSED!"，说明集成成功！

---

#### 3.2 在 LangFuse Dashboard 验证

1. **打开 LangFuse Dashboard**:
   - 访问 `http://localhost:3000` (或你的 LangFuse 地址)
   - 登录账号

2. **查看测试 Trace**:
   - 点击左侧菜单 **Traces**
   - 找到名为 **"Connection Test"** 的 trace
   - 点击查看详情

3. **验证 Trace 内容**:
   - ✅ Input 包含: message, timestamp, test_type
   - ✅ Output 包含: status="success", test_results
   - ✅ Tags 包含: test, connection, automated
   - ✅ 包含 1 个 Span: "Test Span"

✅ 如果所有内容正确，说明 LangFuse 可以正常接收 trace 数据！

---

## 🧪 运行端到端测试 (10 分钟)

### 方式 1: 通过前端界面

```bash
# 1. 启动前端 (新终端窗口)
cd frontend
npm run dev

# 2. 访问 http://localhost:5173

# 3. 创建新研究会话
#    - 点击 "New Research Session"
#    - 输入研究主题: "AI in Healthcare"
#    - 点击 "Start Research"

# 4. 等待流程完成 (约 2-3 分钟)
#    - 观察实时日志输出
#    - 查看报告逐步生成
#    - 如果触发 HITL，进行人工决策

# 5. 研究完成后，打开 LangFuse Dashboard
```

---

### 方式 2: 通过 WebSocket 测试脚本

创建测试脚本 `test_websocket.py`:

```python
import asyncio
import websockets
import json

async def test_research_session():
    uri = "ws://localhost:8121/agent/stream"
    
    async with websockets.connect(uri) as websocket:
        # 发送研究请求
        await websocket.send(json.dumps({
            "messages": [
                {"role": "user", "content": "AI in Healthcare"}
            ]
        }))
        
        # 接收消息
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data.get('type')} - {data.get('message', '')}")
            
            if data.get('type') == 'complete':
                print("Research completed!")
                break

asyncio.run(test_research_session())
```

运行测试:
```bash
python test_websocket.py
```

---

### 在 LangFuse Dashboard 查看完整 Trace

1. **打开 Traces 页面**: `http://localhost:3000/traces`

2. **应该看到以下 Traces**:

   | Trace 名称 | 说明 | 预期数量 |
   |-----------|------|---------|
   | **WebSocket Research Session** | 整个研究会话 | 1 |
   | **HITL Query Approval** | 查询审批决策 | 0-1 (取决于是否触发) |
   | **HITL Paper Selection** | 论文选择决策 | 0-1 |
   | **Report Synthesis** | 报告生成 | 1 |
   | **Document Diff Generation** | 文档差异检测 | 多个 |
   | **Document Conflict Detection** | 冲突检测 | 0-多个 |
   | **HITL Report Revision** | 报告修改决策 | 0-1 |

3. **点击 "WebSocket Research Session" trace**:
   - 查看完整的会话生命周期
   - 查看 Timeline (各节点耗时)
   - 查看 Spans (文档更新、HITL 请求)
   - 查看 Input/Output (session_id, research_topic, 最终结果)

---

## 📊 LangFuse Dashboard 功能导览

### 1. Traces 页面 (主要页面)

**功能**: 查看所有 trace 列表

**筛选技巧**:
- 按时间范围筛选: `Last 24 hours` / `Last 7 days`
- 按 Tags 筛选: `hitl`, `websocket`, `report`
- 按 Status 筛选: `completed`, `error`, `interrupted`
- 搜索: 输入 `session_id` 或 `research_topic`

---

### 2. Sessions 页面

**功能**: 按 session_id 分组查看 trace

**用途**:
- 跟踪单个用户的完整研究流程
- 分析用户行为路径
- 识别异常会话

---

### 3. Metrics 页面 (高级功能)

**功能**: 聚合统计数据

**关键指标**:
- Total Traces: 总 trace 数量
- Average Duration: 平均耗时
- Error Rate: 错误率
- P95 Latency: 95% 分位延迟

---

### 4. Users 页面 (如配置 user_id)

**功能**: 按用户分析行为

**配置方法**:
```python
trace = langfuse.trace(
    name="...",
    user_id=state.get("user_id"),  # 添加 user_id
    session_id=state.get("session_id")
)
```

---

## � 常见问题排查

### 问题 1: 环境变量未生效

**症状**: `LANGFUSE_PUBLIC_KEY is not set`

**解决方法**:
```bash
# 检查环境变量是否正确加载
docker exec -it langgraph-api env | grep LANGFUSE

# 如果为空，检查 .env 文件位置
ls -la .env

# 确保 docker-compose-dev.yml 引用了 .env
# 重启服务
docker-compose -f docker-compose-dev.yml restart langgraph-api
```

---

### 问题 2: LangFuse SDK 未安装

**症状**: `ModuleNotFoundError: No module named 'langfuse'`

**解决方法**:
```bash
# 重新构建容器 (langfuse 已添加到 Dockerfile.dev)
docker-compose -f docker-compose-dev.yml build langgraph-api

# 或临时手动安装
docker exec -it langgraph-api pip install langfuse
```

---

### 问题 3: 连接 LangFuse 失败

**症状**: `Connection refused` 或 `Authentication failed`

**解决方法**:
```bash
# 1. 检查 LangFuse 服务是否运行
curl -I http://localhost:3000
# 应返回 HTTP/1.1 200 OK

# 2. 检查密钥是否正确
#    - 重新登录 LangFuse Dashboard
#    - 进入 Settings → API Keys
#    - 验证 Public Key 和 Secret Key

# 3. 重新生成密钥并更新 .env
```

---

### 问题 4: Trace 未出现在 Dashboard

**可能原因**:
1. 数据尚未上传 (异步上传，可能延迟几秒)
2. LangFuse 服务问题
3. 网络连接问题

**解决方法**:
```bash
# 1. 等待 10-30 秒后刷新 Dashboard

# 2. 检查后端日志
docker-compose -f docker-compose-dev.yml logs -f langgraph-api | grep -i langfuse

# 3. 手动刷新 (在代码中)
langfuse.flush()  # 立即上传数据

# 4. 检查 LangFuse 服务日志
cd langfuse
docker-compose logs -f
```

---

## 📈 性能优化建议

### 1. 配置采样率 (生产环境)

```python
# 仅采集 10% 的 trace (减少存储成本)
langfuse = Langfuse(sample_rate=0.1)
```

---

### 2. 减少 Payload 大小

```python
# ❌ 不推荐: 发送完整 prompt (可能几十 KB)
trace = langfuse.trace(input={"prompt": full_prompt})

# ✅ 推荐: 发送截断的 prompt
trace = langfuse.trace(input={
    "prompt_preview": full_prompt[:500] + "...",
    "prompt_length": len(full_prompt)
})
```

---

### 3. 批量上传配置

```python
langfuse = Langfuse(
    flush_at=10,        # 每 10 个 trace 批量上传
    flush_interval=1.0  # 或每 1 秒上传一次
)
```

---

## 🎯 下一步建议

### 立即可做 (可选)

1. ✅ **创建自定义仪表板**
   - LangFuse Dashboard → Dashboards → Create New
   - 添加常用指标图表 (成功率、P95 延迟)

2. ✅ **配置告警规则**
   - Settings → Alerts
   - 配置错误率 > 5% 时邮件通知

3. ✅ **数据保留策略**
   - Settings → Data Retention
   - 配置自动清理 (保留 30 天)

---

### 下一阶段 (Phase 4.2)

1. **压力测试**
   - 模拟 100 并发用户
   - 基于 LangFuse trace 分析性能瓶颈

2. **多模型对比**
   - 添加 GPT-4、Claude 的 trace
   - 对比性能和成本

3. **A/B 测试框架**
   - 使用 LangFuse 的 experiment 功能
   - 测试不同 prompt 策略

---

## ✅ 完成检查清单

- [ ] 配置 LangFuse 环境变量 (.env)
- [ ] 重新构建并启动后端服务
- [ ] 运行连接测试脚本 (test_langfuse_connection.py)
- [ ] 验证测试 trace 出现在 Dashboard
- [ ] 运行端到端研究测试
- [ ] 验证完整研究流程的 trace
- [ ] 熟悉 LangFuse Dashboard 基本功能
- [ ] (可选) 配置自定义仪表板和告警

---

## 🆘 需要帮助?

**参考文档**:
- `.ai-sessions/development/2025-10-16-1000-phase-4.1-guide-langfuse-configuration.md`
- `.ai-sessions/development/2025-10-15-1700-phase-4.1-implementation-langfuse-integration.md`

**LangFuse 官方文档**:
- https://langfuse.com/docs

**问题反馈**:
- 在项目 GitHub 创建 Issue
- 或联系开发团队

---

**文档创建时间**: 2025-10-16 12:30  
**文档版本**: v1.0  
**适用版本**: Phase 4.1+

祝你部署顺利！🚀
