# Phase 2 调试指南

## 📋 问题修复总结

### 问题描述
后端启动时报错：`ModuleNotFoundError: No module named 'langfuse'`

### 根本原因
Docker 镜像使用了缓存，没有安装最新的依赖包 `langfuse`。

### 解决方案
```bash
# 1. 停止容器
docker compose down langgraph-api

# 2. 重新构建镜像（不使用缓存）
docker compose build --no-cache langgraph-api

# 3. 启动容器
docker compose up -d langgraph-api

# 4. 验证服务
curl http://localhost:8121/ok
```

### 修复结果 ✅
- ✅ `langfuse` 模块已成功加载
- ✅ 服务器已成功启动在 `http://0.0.0.0:8000`
- ✅ 数据库已初始化
- ⚠️ Langfuse 配置警告（需配置环境变量，但不影响运行）

---

## 🎯 Phase 2 功能概述

根据 `GEMINI.md` 和 `README.md`，Phase 2 的目标是：

### 核心目标
1. **容器化开发环境** ✅
2. **三面板布局** ✅
3. **API 集成（只读）** ✅
4. **静态可视化** ✅

### 三面板布局
- **左侧面板（Asset Library）**：显示研究资源（论文）
- **中间面板（Manuscript）**：显示最终报告
- **右侧面板（AI Control Panel）**：Webview 显示 agent 状态

---

## 🔧 手工调试步骤

### 步骤 1: 验证后端服务

#### 1.1 检查容器状态
```bash
docker compose ps
```

**预期输出：**
```
NAME                 STATUS
langgraph-api        Up (healthy)
langgraph-postgres   Up
langgraph-redis      Up (healthy)
```

#### 1.2 检查后端日志
```bash
docker compose logs langgraph-api --tail=50
```

**关键日志：**
- ✅ `Uvicorn running on http://0.0.0.0:8000`
- ✅ `Database initialized`
- ✅ `Registering graph with id 'agent'`

#### 1.3 测试 API 端点
```bash
# 健康检查
curl http://localhost:8121/ok

# 获取 agent 信息
curl http://localhost:8121/info

# 列出所有线程
curl http://localhost:8121/threads
```

---

### 步骤 2: 验证前端服务

#### 2.1 检查前端是否在后端容器中
```bash
docker compose exec langgraph-api ls -la /deps/frontend/dist
```

**预期输出：**
```
index.html
assets/
```

#### 2.2 访问前端
在浏览器中打开：
```
http://localhost:8121/
```

**预期：**
- 看到 React 应用界面
- 三面板布局显示正常

---

### 步骤 3: 测试 VS Code 扩展（如果已开发）

#### 3.1 检查扩展源码
```bash
ls -la vscode-extension/src/
```

#### 3.2 在 VS Code 中调试扩展
1. 打开 `vscode-extension` 文件夹
2. 按 `F5` 启动调试
3. 在新窗口中按 `Ctrl+Shift+P`
4. 输入 "Research Agent" 查看可用命令

#### 3.3 验证扩展功能
- [ ] 左侧面板：Asset Library 显示论文列表
- [ ] 中间面板：Manuscript 显示报告
- [ ] 右侧面板：AI Control Panel 显示 agent 状态
- [ ] API 连接：能够从后端获取数据

---

### 步骤 4: 端到端测试

#### 4.1 创建测试线程
```bash
curl -X POST http://localhost:8121/threads \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "test": "phase2_debug"
    }
  }'
```

**保存返回的 thread_id**

#### 4.2 发送测试查询
```bash
THREAD_ID="<your_thread_id>"

curl -X POST "http://localhost:8121/threads/${THREAD_ID}/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": "What is LangGraph?"
        }
      ]
    },
    "stream_mode": ["values"]
  }'
```

#### 4.3 验证前端显示
1. 刷新前端页面
2. 检查是否显示新的线程
3. 检查 agent 状态是否更新

---

## 🐛 常见问题排查

### 问题 1: 容器无法启动

**症状：**
```
langgraph-api exited with code 1
```

**排查步骤：**
```bash
# 查看详细日志
docker compose logs langgraph-api

# 检查依赖是否安装
docker compose exec langgraph-api pip list | grep langfuse

# 重新构建镜像
docker compose build --no-cache langgraph-api
```

---

### 问题 2: API 连接失败

**症状：**
```
curl: (7) Failed to connect to localhost:8121
```

**排查步骤：**
```bash
# 检查端口映射
docker compose ps
netstat -tlnp | grep 8121

# 检查防火墙
sudo ufw status

# 测试容器内部端口
docker compose exec langgraph-api curl http://localhost:8000/ok
```

---

### 问题 3: 前端无法显示

**症状：**
浏览器显示 404 或空白页面

**排查步骤：**
```bash
# 检查前端文件是否存在
docker compose exec langgraph-api ls -la /deps/frontend/dist

# 检查 app.py 静态文件配置
docker compose exec langgraph-api cat /deps/backend/src/agent/app.py | grep -A 5 "StaticFiles"

# 重新构建前端
docker compose build --no-cache langgraph-api
```

---

### 问题 4: Langfuse 警告

**症状：**
```
Authentication error: Langfuse client initialized without public_key
```

**解决方案：**
这是配置警告，不影响基本功能运行。如需启用 Langfuse，请配置环境变量：

```bash
# 在 .env 文件中添加
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

参考：`QUICKSTART_LANGFUSE.md`

---

## 📊 调试检查清单

### 后端服务 ✅
- [ ] 容器状态正常（Up）
- [ ] 日志无报错
- [ ] API 端点响应正常
- [ ] 数据库连接成功
- [ ] Redis 连接成功

### 前端服务 ✅
- [ ] 静态文件存在于 `/deps/frontend/dist`
- [ ] 浏览器能访问 `http://localhost:8121`
- [ ] 三面板布局显示正常
- [ ] 控制台无 JavaScript 错误

### VS Code 扩展 ✅
- [ ] 扩展能在调试模式启动
- [ ] 命令面板显示扩展命令
- [ ] 三个面板能正常显示
- [ ] 能从 API 获取数据

### 端到端流程 ✅
- [ ] 能创建新线程
- [ ] 能发送查询
- [ ] Agent 能响应
- [ ] 前端能显示结果

---

## 🚀 下一步

Phase 2 完成后，可以开始 Phase 3 的开发：

1. **实时通信**：WebSocket 集成
2. **交互控制**：中断、审批流程
3. **动态更新**：实时状态同步

参考：
- `ROADMAP.md` - Phase 3 规划
- `doc/PHASE3_WEBSOCKET_SUMMARY.md` - WebSocket 实现指南
- `GEMINI.md` - 完整开发框架

---

## 📝 调试记录模板

记录你的调试过程：

```markdown
## 调试日期：2025-11-02

### 发现的问题
- [ ] 问题描述
- [ ] 错误信息
- [ ] 复现步骤

### 排查过程
1. 检查了...
2. 测试了...
3. 发现...

### 解决方案
- 修改了...
- 验证了...

### 验证结果
- [ ] 功能正常
- [ ] 测试通过
- [ ] 文档更新
```

---

## 🔗 相关文档

- `GEMINI.md` - AI 辅助开发框架
- `README.md` - 项目概述
- `ROADMAP.md` - 开发路线图
- `QUICKSTART_LANGFUSE.md` - Langfuse 配置指南
- `backend/API_DOCUMENTATION.md` - API 文档
- `doc/PHASE3_WEBSOCKET_SUMMARY.md` - WebSocket 指南

---

**祝调试顺利！** 🎉
