# Phase 2 后端集成 - TODO 清单

**开始日期：** 2025-11-02  
**预计完成：** 2025-11-23 (3周)  
**当前状态：** 📋 待开始

---

## ✅ 前置准备（已完成）

- [x] 后端服务运行正常
- [x] VS Code 扩展 Mock 模式可用
- [x] Docker Compose 配置正确
- [x] 开发环境设置完成
- [x] 详细计划文档编写

---

## 📅 Week 1: 基础 API 集成 (Day 1-7)

### Day 1-2: 扩展 API 客户端

**文件：** `vscode-extension/src/api.ts`

#### 任务 1.1.1: 添加线程管理接口
- [ ] 定义 `CreateThreadRequest` 接口
- [ ] 定义 `ThreadResponse` 接口
- [ ] 实现 `createThread()` 函数
- [ ] 测试：能成功创建线程

#### 任务 1.1.2: 添加研究启动接口
- [ ] 定义 `StartResearchRequest` 接口
- [ ] 实现 `startResearch()` 函数
- [ ] 测试：能启动研究任务

#### 任务 1.1.3: 添加状态查询接口
- [ ] 定义 `ThreadState` 接口
- [ ] 实现 `getThreadState()` 函数
- [ ] 测试：能获取线程状态

#### 验收标准 Day 1-2
- [ ] 3 个新函数编译无错误
- [ ] 手动测试所有函数（使用 curl 验证后端）
- [ ] TypeScript 类型检查通过
- [ ] 代码提交到 git

---

### Day 3-5: 重构研究启动命令

**文件：** `vscode-extension/src/extension.ts` (920-1007 行)

#### 任务 1.2.1: 删除 Mock 代码
- [ ] 删除模拟进度更新的 `setTimeout` 代码
- [ ] 删除 Mock 警告消息

#### 任务 1.2.2: 集成真实 API
- [ ] 添加后端健康检查
- [ ] 调用 `createThread()` 创建会话
- [ ] 调用 `startResearch()` 启动任务
- [ ] 实现轮询机制查询状态

#### 任务 1.2.3: 实现进度计算
- [ ] 添加 `calculateProgress()` 函数
- [ ] 添加 `getProgressMessage()` 函数
- [ ] 根据真实状态更新 Webview

#### 任务 1.2.4: 错误处理
- [ ] 添加网络错误处理
- [ ] 添加超时处理
- [ ] 添加用户友好的错误消息

#### 验收标准 Day 3-5
- [ ] 启动研究命令调用真实 API
- [ ] 能看到真实的进度更新
- [ ] 完成后显示真实的论文和报告
- [ ] 错误情况有友好提示
- [ ] 端到端测试通过

---

### Day 6-7: 更新控制面板

**文件：** `vscode-extension/src/extension.ts` (1009-1049 行)

#### 任务 1.3.1: 添加会话选择
- [ ] 调用 `getSessionsList()` 获取会话列表
- [ ] 实现 QuickPick 选择器
- [ ] 允许查看历史会话

#### 任务 1.3.2: 显示会话状态
- [ ] 根据选择的会话获取状态
- [ ] 更新控制面板 HTML
- [ ] 显示会话元数据

#### 验收标准 Day 6-7
- [ ] 控制面板能选择会话
- [ ] 显示真实的会话数据
- [ ] 未选择会话时显示全局状态
- [ ] 测试通过

---

### Week 1 里程碑
- [ ] **M1: 能启动真实研究任务** ✅
- [ ] 所有 Day 1-7 任务完成
- [ ] 功能验收通过
- [ ] 代码审查完成
- [ ] 文档更新

---

## 📅 Week 2: WebSocket 实时通信 (Day 8-14)

### Day 8-10: 实现 WebSocket 客户端

**新文件：** `vscode-extension/src/websocket.ts`

#### 任务 2.1.1: 创建基础类
- [ ] 定义 `ResearchWebSocketClient` 类
- [ ] 实现构造函数和连接逻辑
- [ ] 添加事件处理器映射

#### 任务 2.1.2: 实现消息处理
- [ ] 实现 `handleMessage()` 方法
- [ ] 添加消息类型分发
- [ ] 实现 `on()` 和 `emit()` 方法

#### 任务 2.1.3: 实现连接管理
- [ ] 实现 `connect()` 方法
- [ ] 实现 `send()` 方法
- [ ] 实现 `close()` 方法

#### 任务 2.1.4: 错误处理与重连
- [ ] 添加错误事件处理
- [ ] 实现自动重连逻辑
- [ ] 添加心跳检测

#### 验收标准 Day 8-10
- [ ] WebSocket 能成功连接
- [ ] 能接收后端消息
- [ ] 能发送消息到后端
- [ ] 断线能自动重连
- [ ] 单元测试通过

---

### Day 11-12: 集成 WebSocket

**文件：** `vscode-extension/src/extension.ts`

#### 任务 2.2.1: 替换轮询机制
- [ ] 删除 `setInterval` 轮询代码
- [ ] 创建 `ResearchWebSocketClient` 实例
- [ ] 监听 `state_update` 事件

#### 任务 2.2.2: 实现事件处理
- [ ] 处理 `connected` 事件
- [ ] 处理 `state_update` 事件
- [ ] 处理 `progress` 事件
- [ ] 处理 `complete` 事件
- [ ] 处理 `error` 事件

#### 任务 2.2.3: 清理资源
- [ ] 在面板关闭时断开 WebSocket
- [ ] 实现 dispose 模式

#### 验收标准 Day 11-12
- [ ] 实时进度更新流畅
- [ ] 状态变化即时反映
- [ ] 资源清理正确
- [ ] 集成测试通过

---

### Day 13-14: 更新 TreeView 数据源

**文件：** `vscode-extension/src/extension.ts`

#### 任务 2.3.1: 重构 AssetLibraryProvider
- [ ] 修改 `getChildren()` 调用 `getAllPapers()`
- [ ] 实现按会话分组
- [ ] 添加论文详情显示
- [ ] 添加图标和工具提示

#### 任务 2.3.2: 重构 ManuscriptProvider
- [ ] 修改 `getChildren()` 调用 `getAllReports()`
- [ ] 实现版本历史显示
- [ ] 添加点击打开功能
- [ ] 添加上下文菜单

#### 任务 2.3.3: 实现刷新机制
- [ ] WebSocket 更新时自动刷新
- [ ] 添加手动刷新命令
- [ ] 优化刷新性能

#### 验收标准 Day 13-14
- [ ] Asset Library 显示所有历史论文
- [ ] Manuscript 显示所有报告版本
- [ ] 刷新功能正常
- [ ] 点击操作正确
- [ ] UI 测试通过

---

### Week 2 里程碑
- [ ] **M2: 实时进度更新 + 历史数据显示** ✅
- [ ] 所有 Day 8-14 任务完成
- [ ] WebSocket 稳定运行
- [ ] TreeView 显示真实数据
- [ ] 性能测试通过

---

## 📅 Week 3: HITL 与文档协作 (Day 15-21)

### Day 15-17: HITL 决策集成

**文件：** `vscode-extension/src/extension.ts` (1385-1472 行)

#### 任务 3.1.1: 删除 Mock HITL
- [ ] 删除 `mockRequest` 变量
- [ ] 删除硬编码的决策数据

#### 任务 3.1.2: 集成真实 HITL
- [ ] WebSocket 监听 `hitl_request` 事件
- [ ] 调用 `handleHITLRequest()` 显示 UI
- [ ] 收集用户决策

#### 任务 3.1.3: 提交决策到后端
- [ ] 实现 API 调用 `POST /agent/hitl/respond`
- [ ] 处理提交成功/失败
- [ ] 更新 Agent 状态

#### 验收标准 Day 15-17
- [ ] HITL 请求能正确显示
- [ ] 用户决策能提交
- [ ] Agent 能根据决策继续
- [ ] 错误处理完善

---

### Day 18-20: 文档协作集成

**文件：** `vscode-extension/src/documentCollaboration.ts`

#### 任务 3.2.1: 删除 Mock 更新
- [ ] 删除 `mockUpdates` 数组
- [ ] 删除模拟的 `setTimeout`

#### 任务 3.2.2: 集成真实更新
- [ ] WebSocket 监听 `document_update` 事件
- [ ] 调用 `handleDocumentUpdate()` 应用编辑
- [ ] 实现 `getOrCreateReportDocument()`

#### 任务 3.2.3: 实现编辑应用
- [ ] 实现 `insert` 操作
- [ ] 实现 `delete` 操作
- [ ] 实现 `replace` 操作
- [ ] 显示变更理由

#### 任务 3.2.4: 冲突处理
- [ ] 检测编辑冲突
- [ ] 提供解决 UI
- [ ] 记录变更历史

#### 验收标准 Day 18-20
- [ ] 文档更新能实时应用
- [ ] 变更理由正确显示
- [ ] 冲突能检测和解决
- [ ] 多个更新顺序正确

---

### Day 21: 端到端测试与优化

#### 任务 3.3.1: 创建集成测试
- [ ] 创建 `realBackend.test.ts`
- [ ] 编写完整研究流程测试
- [ ] 编写 HITL 测试
- [ ] 编写文档协作测试

#### 任务 3.3.2: 性能优化
- [ ] 测量 API 响应时间
- [ ] 测量 WebSocket 延迟
- [ ] 优化 UI 刷新频率
- [ ] 检查内存泄漏

#### 任务 3.3.3: 用户体验优化
- [ ] 添加加载指示器
- [ ] 改进错误消息
- [ ] 添加取消操作
- [ ] 优化动画效果

#### 验收标准 Day 21
- [ ] 所有集成测试通过
- [ ] 性能指标达标
- [ ] 用户体验流畅
- [ ] 代码质量检查通过

---

### Week 3 里程碑
- [ ] **M3: 完整功能可用** ✅
- [ ] 所有 Day 15-21 任务完成
- [ ] HITL 和文档协作正常
- [ ] 测试覆盖率 > 80%
- [ ] 性能达标

---

## 🎯 最终验收（Day 22）

### 功能验收
- [ ] ✅ 用户能输入主题，启动真实研究
- [ ] ✅ 实时看到 Agent 进度
- [ ] ✅ Asset Library 显示所有历史论文
- [ ] ✅ Manuscript 显示所有报告版本
- [ ] ✅ HITL 决策能提交到后端
- [ ] ✅ 报告能实时编辑

### 性能验收
- [ ] ✅ API 响应 < 1秒
- [ ] ✅ WebSocket 延迟 < 100ms
- [ ] ✅ UI 流畅（60fps）
- [ ] ✅ 内存稳定（< 500MB）

### 测试验收
- [ ] ✅ 单元测试覆盖率 > 80%
- [ ] ✅ 集成测试 100% 通过
- [ ] ✅ 端到端测试 100% 通过

### 文档验收
- [ ] ✅ README 更新
- [ ] ✅ API 文档更新
- [ ] ✅ 用户指南完成
- [ ] ✅ 开发文档完成

---

## 📊 进度跟踪

### 整体进度
- [ ] Week 1: 基础 API 集成 (0/7 天)
- [ ] Week 2: WebSocket 实时通信 (0/7 天)
- [ ] Week 3: HITL 与文档协作 (0/7 天)

### 任务统计
- **总任务数：** 50+
- **已完成：** 0
- **进行中：** 0
- **待开始：** 50+

### 完成率
- **Week 1:** 0%
- **Week 2:** 0%
- **Week 3:** 0%
- **总体:** 0%

---

## 📝 笔记区域

### 遇到的问题


### 解决方案


### 待优化项


### 下次迭代改进


---

## 🔗 相关资源

- [详细计划](./PHASE2_BACKEND_INTEGRATION_PLAN.md)
- [执行摘要](./PHASE2_INTEGRATION_SUMMARY.md)
- [快速参考](./PHASE2_QUICK_REFERENCE.md)
- [调试指南](./PHASE2_DEBUG_GUIDE.md)

---

**开始日期：** 填写开始日期  
**预计完成：** 填写预计完成日期  
**实际完成：** 填写实际完成日期  

**当前状态：** 📋 待开始 / 🚧 进行中 / ✅ 已完成
