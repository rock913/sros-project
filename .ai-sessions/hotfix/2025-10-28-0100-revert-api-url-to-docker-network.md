# Hotfix: 恢复 API URL 为 Docker 内部网络地址

**日期**: 2025-10-28 01:00 UTC  
**严重性**: P0 - 关键修复  
**影响**: VS Code 扩展 API 连接  
**耗时**: 10 分钟

---

## 问题描述

昨天的修复（commit 1741826）错误地将 API Base URL 从 `http://langgraph-api:8000` 改为 `http://localhost:8121`。

### 错误分析

**之前的假设（错误）**:
- 认为 VS Code 扩展运行在主机上
- 认为无法访问 Docker 内部网络
- 因此使用 localhost:8121（主机端口映射）

**实际情况（正确）**:
- VS Code 扩展运行在 `vscode-dev` Docker 容器中
- 该容器与 `langgraph-api` 在同一个 Docker 网络中
- 可以直接使用 Docker 内部主机名通信
- `localhost:8121` 在容器内部无法访问（没有端口转发到容器内）

### 环境架构

```
┌─────────────────────────────────────────────┐
│         Docker Network (bridge)             │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ vscode-dev   │      │ langgraph-api   │ │
│  │              │─────>│                 │ │
│  │ Port: N/A    │  ✅  │ Port: 8000      │ │
│  │              │      │                 │ │
│  └──────────────┘      └─────────────────┘ │
│                              │              │
└──────────────────────────────┼──────────────┘
                               │
                          Port 8121
                               │
                               ▼
                      ┌─────────────────┐
                      │  Host Machine   │
                      │  localhost:8121 │
                      └─────────────────┘
```

### 影响范围

**受影响功能**:
- ❌ Analytics Dashboard (无法加载会话数据)
- ❌ Start New Research (无法连接后端)
- ❌ Session Details (无法获取详情)
- ❌ Control Panel (无法获取状态)
- ❌ 所有 API 调用

**症状**:
```
Network Error: connect ECONNREFUSED 127.0.0.1:8121
```

---

## 修复方案

### 代码更改

**文件**: `vscode-extension/src/api.ts`

```typescript
// ❌ 错误的配置（昨天的修复）
const API_BASE_URL = process.env.VSCODE_RESEARCH_AGENT_URL || 'http://localhost:8121';

// ✅ 正确的配置（恢复原始版本）
const API_BASE_URL = process.env.VSCODE_RESEARCH_AGENT_URL || 'http://langgraph-api:8000';
```

### 验证步骤

1. **从 vscode-dev 容器测试连接**:
```bash
docker exec vscode-dev wget -qO- http://langgraph-api:8000/health
```
结果: ✅ 成功返回健康检查数据

2. **编译扩展**:
```bash
cd vscode-extension && npm run compile
```
结果: ✅ 编译成功，无错误

3. **测试扩展功能** (在 vscode-dev 容器内按 F5):
   - Analytics Dashboard 应显示会话数据
   - Start New Research 应能连接后端
   - 所有 API 调用应正常工作

---

## 部署清单

- [x] 恢复 API URL 配置
- [x] 重新编译扩展
- [x] 验证 Docker 网络连通性
- [x] 创建修复文档
- [ ] 提交修复 (待测试确认)

---

## 根本原因分析

### 为什么会出现这个错误？

1. **缺乏架构理解**: 昨天的修复没有查看 `docker-compose-dev.yml`
2. **错误假设**: 假设扩展运行在主机上，而不是 Docker 容器中
3. **测试不充分**: 没有在实际环境中测试 API 连接

### 预防措施

1. **架构文档**: 在 README 中明确说明扩展的运行环境
2. **环境配置**: 使用环境变量支持不同部署场景
3. **测试流程**: 修复后必须在实际环境中测试

---

## 环境变量说明

为了支持不同的部署场景，API URL 支持环境变量配置：

### 场景 1: vscode-dev 容器（推荐）
```bash
# 默认值，无需设置
# API_BASE_URL = 'http://langgraph-api:8000'
```

### 场景 2: 主机开发（备选）
```bash
# 设置环境变量
export VSCODE_RESEARCH_AGENT_URL='http://localhost:8121'
```

### 场景 3: 自定义部署
```bash
# 设置为自定义地址
export VSCODE_RESEARCH_AGENT_URL='http://your-custom-api:port'
```

---

## 性能影响

### 网络延迟对比

**Docker 内部网络** (langgraph-api:8000):
- 延迟: ~0.1-0.5ms
- 带宽: 无限制
- 路由: 直接容器间通信

**主机端口映射** (localhost:8121):
- 延迟: ~1-5ms
- 带宽: 受主机网络栈限制
- 路由: 容器 → Docker 桥接 → 主机 → Docker 桥接 → 容器

**结论**: Docker 内部网络性能更优 ✅

---

## 相关提交

- **错误引入**: commit 1741826 (2025-10-27)
  - 标题: "feat: fix VS Code extension frontend issues"
  - 错误: 将 API URL 改为 localhost:8121

- **本次修复**: (待提交)
  - 标题: "fix: revert API URL to Docker internal network address"
  - 修复: 恢复为 langgraph-api:8000

---

## 测试建议

### 手动测试（推荐）

1. 在 vscode-dev 容器中打开 VS Code:
   ```bash
   # 确保 vscode-dev 容器运行
   docker ps | grep vscode-dev
   
   # 在容器内 VS Code 按 F5 启动扩展
   ```

2. 测试所有功能:
   - [ ] Analytics Dashboard 加载数据
   - [ ] Start New Research 可以输入主题
   - [ ] Session Details 显示详情
   - [ ] Control Panel 显示状态

### 自动化测试（TODO）

创建集成测试验证 API 连接:
```typescript
// tests/integration/api-connectivity.test.ts
describe('API Connectivity', () => {
  it('should connect to langgraph-api from vscode-dev container', async () => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    expect(response.status).toBe(200);
    expect(response.data.status).toMatch(/healthy|degraded/);
  });
});
```

---

## 总结

✅ **修复完成**: API URL 已恢复为 Docker 内部网络地址  
✅ **编译成功**: 扩展代码无错误  
⏳ **待测试**: 需要在 vscode-dev 容器中验证功能  
📝 **经验教训**: 修复前必须理解系统架构  

---

**下一步**: 请在 vscode-dev 容器中测试扩展，确认所有功能正常后提交修复。
