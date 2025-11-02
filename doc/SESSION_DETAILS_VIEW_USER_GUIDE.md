# Session Details View 用户指南

**版本**: Phase 3.5.4  
**最后更新**: 2025-10-14

---

## 📖 概述

Session Details View 是 VS Code Auto-Researcher 扩展中的新功能，允许您查看研究会话的完整详细信息，包括事件时间线、收集的论文、生成的报告以及统计数据。

---

## 🚀 快速开始

### 方式一：通过命令面板

1. 打开命令面板：
   - Windows/Linux: `Ctrl+Shift+P`
   - macOS: `Cmd+Shift+P`

2. 输入并选择：
   ```
   Auto-Researcher: View Session Details
   ```

3. 在弹出的输入框中粘贴 Session ID（UUID格式）：
   ```
   例如: 4565e1f6-1c57-4658-a603-0ea242ffb241
   ```

4. 按 `Enter` - 系统将加载并显示会话详情

### 方式二：从代码直接调用（未来支持）

```typescript
// 未来版本将支持从 Sessions TreeView 直接点击
vscode.commands.executeCommand(
    'auto-researcher.viewSessionDetails',
    sessionId
);
```

---

## 🎨 界面组成

### 1. Header（顶部栏）

显示会话标题和状态徽章：

```
┌──────────────────────────────────────────────────┐
│  Research: AI in Healthcare          [COMPLETED] │
└──────────────────────────────────────────────────┘
```

**状态颜色编码**:
- 🟢 `completed` - 绿色（成功完成）
- 🔵 `running` - 蓝色（正在运行）
- 🔴 `failed` - 红色（执行失败）
- 🟠 `pending` - 橙色（等待中）
- ⚫ `archived` - 灰色（已归档）

---

### 2. Statistics Grid（统计卡片）

4个关键指标卡片：

```
┌────────────┬────────────┬────────────┬────────────┐
│ Papers     │ Reports    │ Duration   │ Cost       │
│ Collected  │ Versions   │            │            │
│    25      │     3      │  12m 45s   │  $0.0045   │
└────────────┴────────────┴────────────┴────────────┘
```

**指标说明**:
- **Papers Collected**: 会话期间收集的论文总数
- **Report Versions**: 生成的报告版本数
- **Duration**: 从第一个事件到最后一个事件的总时长
- **Cost**: 基于LLM token使用的估算成本（$0.01/1000 tokens）

---

### 3. Session Information（会话信息）

详细的会话元数据表格：

| 字段 | 说明 | 示例 |
|------|------|------|
| Session ID | 唯一标识符（UUID） | `4565e1f6-1c57-...` |
| Thread ID | LangGraph线程ID | `b42e9b70-6679-...` |
| Research Topic | 研究主题 | "AI applications in healthcare" |
| Created At | 创建时间 | 2025-10-14 09:00:59 |
| Last Updated | 最后更新时间 | 2025-10-14 09:15:23 |
| Total Events | 事件总数 | 45 |
| Tags | 标签（如果有） | websocket, streaming |
| Notes | 备注（如果有） | Started via WebSocket... |

---

### 4. Event Timeline（事件时间线）

可滚动的垂直时间线，显示会话的关键事件：

```
  09:00:59  RESEARCH STARTED
            │ Query: "AI applications in healthcare"
            │
  09:01:15  QUERIES GENERATED
            │ Generated 5 search queries
            │
  09:02:30  PAPERS COLLECTED
            │ Retrieved 25 papers from arXiv
            │
  09:05:45  REPORT GENERATED
            │ Created report version 1 (2,500 words)
            │
  09:10:00  ERROR OCCURRED  ⚠️
            │ Error: API rate limit exceeded
```

**特性**:
- ✅ 垂直时间线设计，清晰展示事件顺序
- ✅ 错误事件以红色高亮显示
- ✅ 长文本自动截断到200字符
- ✅ 最多显示50个最近事件
- ✅ 可滚动（最大高度500px）

**事件类型**:
- `research_started` - 研究开始
- `queries_generated` - 查询生成
- `papers_collected` - 论文收集
- `report_generated` - 报告生成
- `report_revised` - 报告修订
- `error_occurred` - 错误发生

---

### 5. Papers List（论文列表）

会话中收集的所有论文：

```
📚 Papers (25)

• Transformers for Medical Image Analysis
  Authors: Smith, J., Doe, A., Lee, K. • 2024

• Deep Learning in Healthcare: A Survey
  Authors: Wang, L., Chen, M. • 2023

• AI-Powered Diagnostics
  Authors: Brown, R. • 2025

... and 22 more papers
```

**显示规则**:
- 默认显示前10篇论文
- 如果超过10篇，显示 "... and N more papers"
- 每篇论文显示：标题、作者、年份

---

### 6. Reports List（报告列表）

会话生成的所有报告版本：

```
📝 Reports (3 versions)

• Version 3
  Created 2025-10-14 09:15:23 • 3,200 words • 25 papers

• Version 2
  Created 2025-10-14 09:10:15 • 2,800 words • 20 papers

• Version 1
  Created 2025-10-14 09:05:45 • 2,500 words • 15 papers
```

**元数据包括**:
- 版本号（递增）
- 创建时间戳
- 字数统计
- 使用的论文数量

---

### 7. Action Buttons（操作按钮）

底部的4个操作按钮：

```
┌─────────────────┬───────────────────┬──────────┬──────────┐
│ 📥 Export       │ 🔍 View in        │ 🔄       │ 🗑️      │
│    Session Data │    LangSmith      │ Refresh  │ Delete   │
└─────────────────┴───────────────────┴──────────┴──────────┘
```

#### 📥 Export Session Data
**状态**: 🚧 即将推出（Phase 4）

**功能**:
- 导出完整的会话数据为JSON文件
- 包括所有论文、报告、事件
- 可用于备份或数据分析

**计划格式**:
```json
{
  "session": {...},
  "events": [...],
  "papers": [...],
  "reports": [...]
}
```

---

#### 🔍 View in LangSmith
**状态**: 🚧 即将推出（Phase 4.1）

**功能**:
- 在LangSmith平台中打开当前会话
- 查看详细的trace和调试信息
- 分析LLM调用性能

**链接格式**:
```
https://smith.langchain.com/public/{project_id}/r/{thread_id}
```

---

#### 🔄 Refresh
**状态**: ✅ 可用

**功能**:
- 重新加载会话数据
- 更新统计信息
- 刷新事件时间线

**使用场景**:
- 会话正在运行，需要查看最新进展
- 怀疑数据不同步时

**操作**:
1. 点击 "Refresh" 按钮
2. 系统显示 "Loading..."
3. 数据更新后显示成功提示

---

#### 🗑️ Delete Session
**状态**: ⚠️ 需谨慎使用

**功能**:
- 永久删除会话及所有关联数据
- 包括论文、报告、事件记录
- **此操作不可撤销**

**操作流程**:
1. 点击红色 "Delete Session" 按钮
2. 弹出确认对话框：
   ```
   Are you sure you want to delete this session?
   This action cannot be undone.
   
   [Cancel]  [Delete]
   ```
3. 点击 "Delete" 确认删除
4. 会话被删除，视图关闭

**影响**:
- ✅ 释放数据库空间
- ✅ 清理不需要的会话
- ⚠️ 丢失所有研究数据（不可恢复）

---

## 💡 使用技巧

### 技巧1: 快速定位Session ID

**从Analytics Dashboard获取**:
1. 打开 Analytics Dashboard (`Ctrl+Shift+P` → "Show Analytics Dashboard")
2. 查看 "Recent Sessions" 表格
3. 复制Session ID
4. 打开Session Details View并粘贴

**从后端日志获取**:
```bash
docker logs langgraph-api | grep "session_id"
```

---

### 技巧2: 监控长时间运行的研究

对于耗时较长的研究任务：

1. 记录初始Session ID
2. 定期（每5-10分钟）打开Session Details
3. 点击 "Refresh" 查看最新进展
4. 查看Event Timeline了解当前阶段

---

### 技巧3: 分析失败的会话

当研究失败时：

1. 打开Session Details View
2. 找到红色高亮的 `ERROR OCCURRED` 事件
3. 展开事件详情查看错误消息
4. 根据错误类型采取措施：
   - API rate limit → 等待后重试
   - Network timeout → 检查网络连接
   - Invalid API key → 更新环境变量

---

### 技巧4: 比较不同版本的报告

1. 查看Reports List中的所有版本
2. 注意字数和论文数的变化
3. 识别HITL修订（通常版本号递增且字数变化）

---

## 🔍 故障排查

### 问题1: "Invalid UUID format" 错误

**原因**: 输入的Session ID格式不正确

**解决方案**:
- 确保ID是标准UUID格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- 字母必须是小写
- 包含4个连字符

**正确示例**:
```
✅ 4565e1f6-1c57-4658-a603-0ea242ffb241
❌ 4565E1F6-1C57-4658-A603-0EA242FFB241  (大写)
❌ 4565e1f61c5746580ea242ffb241        (缺少连字符)
```

---

### 问题2: "Session not found" 错误

**原因**: Session ID不存在或已被删除

**解决方案**:
1. 检查ID是否完整复制
2. 确认会话未被删除
3. 从Analytics Dashboard重新获取最新的Session ID

---

### 问题3: 视图加载缓慢

**原因**: 会话包含大量数据（如100+篇论文）

**优化建议**:
- 系统已限制事件显示为50条最近事件
- 论文列表限制为前10篇
- 如果仍然很慢，考虑优化数据库索引

---

### 问题4: Refresh按钮无响应

**解决方案**:
1. 检查后端服务是否运行：
   ```bash
   curl http://localhost:8121/health
   ```
2. 查看VS Code Output面板（Ctrl+Shift+U）
3. 查找错误日志

---

## 📊 最佳实践

### 1. 定期清理旧会话

建议每月删除不需要的会话：
- 测试会话
- 失败的会话（已修复问题后）
- 重复的会话

**保留**:
- 重要研究结果
- 需要引用的会话
- 正在进行的项目

---

### 2. 使用Tags组织会话

在创建会话时添加有意义的tags：
```python
tags=["quantum-computing", "review-paper", "2025-q1"]
```

便于在Session Details中快速识别会话类型。

---

### 3. 监控成本

定期检查会话的 `cost_estimate`：
- 单个会话 > $1.00 → 可能存在无限循环
- 每月总成本 → 评估预算使用情况

---

### 4. 保存关键会话的截图

对于重要的研究结果：
1. 打开Session Details View
2. 截图整个视图（包括所有组件）
3. 保存为PNG文件
4. 作为研究记录的一部分

---

## 🎯 快捷键（计划中）

| 快捷键 | 功能 | 状态 |
|--------|------|------|
| `Ctrl+R` | 刷新当前视图 | 📋 计划中 |
| `Ctrl+E` | 导出会话数据 | 📋 计划中 |
| `Ctrl+L` | 在LangSmith中打开 | 📋 计划中 |

---

## 🔗 相关功能

### Analytics Dashboard
查看所有会话的聚合统计：
- 总会话数
- 成功率
- 论文收集趋势
- 热门研究主题

**打开方式**: `Ctrl+Shift+P` → "Show Analytics Dashboard"

### Papers Library
浏览所有收集的论文：
- 按来源筛选（arXiv, Unpaywall）
- 关键词搜索
- 导出论文列表

### Reports Library
管理所有生成的报告：
- 查看报告版本历史
- 比较报告差异
- 导出为Markdown/PDF

---

## ❓ 常见问题

**Q: 为什么cost_estimate可能不准确？**

A: 成本估算基于以下假设：
- Gemini API定价：$0.01/1000 tokens
- 仅统计LLM调用事件
- 不包括API调用、存储等其他成本
- 实际成本可能有10-20%浮动

---

**Q: 可以同时查看多个会话吗？**

A: 目前不支持。但可以：
1. 打开多个Session Details View（不同的Webview）
2. 使用 `Ctrl+Tab` 在视图间切换

---

**Q: 事件时间线为什么只显示50条？**

A: 出于性能考虑：
- 避免大量数据导致UI卡顿
- 50条事件通常涵盖关键里程碑
- 如需完整事件，可通过API导出

---

**Q: 删除会话后能恢复吗？**

A: **不能**。删除是永久性的，包括：
- Session记录
- 关联的Papers
- 关联的Reports
- 所有Events

建议删除前先导出数据（Phase 4功能）。

---

## 📞 支持

遇到问题？

1. **查看日志**:
   ```bash
   # 后端日志
   docker logs langgraph-api --tail=100
   
   # VS Code输出面板
   Ctrl+Shift+U → "Auto-Researcher"
   ```

2. **检查健康状态**:
   ```bash
   curl http://localhost:8121/health
   ```

3. **提交Issue**:
   - GitHub: `AutoBrainLab/gemini-fullstack-langgraph-quickstart`
   - 包括：错误信息、Session ID、截图

---

## 🔄 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2025-10-14 | 初始发布（Phase 3.5.4） |

---

**最后更新**: 2025-10-14  
**贡献者**: Development Team  
**许可证**: MIT
