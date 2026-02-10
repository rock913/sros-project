# Scientific Research Operating System (SROS) V2.2 / 科研操作系统 (SROS) V2.2

[English Version](#english-version) | [中文版本](#中文版本)

---

## English Version

### Overview
SROS V2.2 is a gateway-based MCP system for draft-driven research workflows. The Gateway exposes a single SSE endpoint and manages all sub-servers via stdio.

### Repository Structure (Concise)
```
/gemini-fullstack-langgraph-quickstart/
├── .roo/                  # Global MCP config and modes
├── mcp_servers/           # MCP server implementations
├── tests/                 # Unit / integration / performance tests
├── scripts/               # Diagnostics and utilities
├── workspace/             # User projects (drafts, materials, graphs)
├── doc/                   # Documentation
├── run_servers.py         # Gateway + server runner
├── run_all_tests.py       # Test entrypoint
└── requirements.txt       # Base dependencies
```

### MCP Servers (Current Reality)
- [mcp_servers/sros_gateway](mcp_servers/sros_gateway): Gateway SSE server (Port 8000).
- [mcp_servers/context_ingester](mcp_servers/context_ingester): MVP ingester; parsing works, graph storage/search is a stub.
- [mcp_servers/federal_academic_search](mcp_servers/federal_academic_search): OpenAlex + Unpaywall + S2 integration.
- [mcp_servers/manuscript_manager](mcp_servers/manuscript_manager): Manuscript editing tools.
- [mcp_servers/duckdb_memory](mcp_servers/duckdb_memory): Local graph store (DuckDB).
- [mcp_servers/zotero_expert](mcp_servers/zotero_expert): Local citation management.

### Workflow (High Level)
1. Ingest materials and ideas into soft knowledge.
2. Read manuscript structure.
3. Detect gaps and retrieve evidence.
4. Store relationships in the graph.
5. Expand manuscript with citations.

### Getting Started (Minimal)
- Configure the gateway in [README.md](README.md) and [run_servers.py](run_servers.py).
- Use [run_servers.py](run_servers.py) to start the Gateway.
- Validate with [test_gateway.py](test_gateway.py).
- Work inside [workspace](workspace) projects.

### Documentation Map
- [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md): Current status and cleanup plan.
- [doc/SROS_V2.2_DEPLOYMENT_GUIDE.md](doc/SROS_V2.2_DEPLOYMENT_GUIDE.md): Deployment and ops.
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md): Contribution rules.
- [doc/SROS V2.2 架构实施总蓝图.md](doc/SROS%20V2.2%20%E6%9E%B6%E6%9E%84%E5%AE%9E%E6%96%BD%E6%80%BB%E8%93%9D%E5%9B%BE.md): Architecture blueprint.
- [doc/SROS_V2.2_STABILITY_FIX.md](doc/SROS_V2.2_STABILITY_FIX.md): Stability fixes (candidate for merge).

### Cleanup Direction (Summary)
- Consolidate root test scripts into a [tests](tests) folder with unit, integration, and performance subfolders.
- Merge overlapping docs into a smaller set (see [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md)).

---

## 中文版本

### 概述
SROS V2.2 是基于网关的 MCP 系统，通过单一 SSE 入口协调所有子服务，实现“以草稿驱动研究”的工作流。

### 代码与目录结构（精简）
```
/gemini-fullstack-langgraph-quickstart/
├── .roo/                  # 全局 MCP 配置与模式
├── mcp_servers/           # MCP 服务器实现
├── tests/                 # 单元 / 集成 / 性能测试
├── scripts/               # 诊断与工具脚本
├── workspace/             # 用户项目目录
├── doc/                   # 文档
├── run_servers.py         # 网关与服务器启动
├── run_all_tests.py       # 测试入口
└── requirements.txt       # 依赖
```

### MCP 服务器现状
- [mcp_servers/sros_gateway](mcp_servers/sros_gateway)：网关 SSE 服务（端口 8000）。
- [mcp_servers/context_ingester](mcp_servers/context_ingester)：MVP 可用，解析存在，图存储与检索为占位实现。
- [mcp_servers/federal_academic_search](mcp_servers/federal_academic_search)：OpenAlex + Unpaywall + S2。
- [mcp_servers/manuscript_manager](mcp_servers/manuscript_manager)：手稿编辑工具。
- [mcp_servers/duckdb_memory](mcp_servers/duckdb_memory)：本地图存储（DuckDB）。
- [mcp_servers/zotero_expert](mcp_servers/zotero_expert)：本地引用管理。

### 工作流（高层）
1. 摄取材料与想法形成软知识。
2. 读取手稿结构。
3. 发现空白并检索证据。
4. 写入图谱。
5. 写回手稿并带引用。

### 快速开始（最小路径）
- 配置 [README.md](README.md) 与 [run_servers.py](run_servers.py) 中的网关使用方式。
- 使用 [run_servers.py](run_servers.py) 启动网关。
- 使用 [test_gateway.py](test_gateway.py) 验证。
- 在 [workspace](workspace) 中进行研究项目。

### 文档索引
- [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md)：状态与清理计划。
- [doc/SROS_V2.2_DEPLOYMENT_GUIDE.md](doc/SROS_V2.2_DEPLOYMENT_GUIDE.md)：部署与运行。
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md)：贡献规范。
- [doc/SROS V2.2 架构实施总蓝图.md](doc/SROS%20V2.2%20%E6%9E%B6%E6%9E%84%E5%AE%9E%E6%96%BD%E6%80%BB%E8%93%9D%E5%9B%BE.md)：架构蓝图。
- [doc/SROS_V2.2_STABILITY_FIX.md](doc/SROS_V2.2_STABILITY_FIX.md)：稳定性修复（建议合并）。

### 精简方向（摘要）
- 将根目录的测试脚本收敛到 [tests](tests) 下，按单元/集成/性能拆分。
- 文档去重合并（详见 [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md)）。
- 安装并激活 Roo Code/Cline 扩展
- 在 `draft.md` 中开始写作 - 系统将自动检测空白并建议研究

#### 使用教程

**第 1 步：写作和空白检测**
1. **(自动预热)**：系统首先消化您的 `ideas.md` 和 `materials/` 到图谱中
2. 在 `draft.md` 文件中开始写作
3. 添加 `[TODO:]` 标记来标识想要研究的部分
4. Roo Code 将自动检测空白并触发研究工作流

**第 2 步：研究自动化**
1. 系统自动调用 `federal_academic_search` 服务器 查找相关论文
2. 文献关系存储在本地知识图谱中（`.sros/graph.db`）
3. 相关发现被建议插入到您的手稿中

**第 3 步：内容扩展**
1. 接受或拒绝研究建议
2. 使用 `manuscript_manager` 原子编辑工具插入内容
3. 引用自动格式化和管理

**第 4 步：迭代改进**
1. 继续写作和完善草稿
2. 系统持续监控新的空白
3. 构建全面、经过充分研究的文档

#### 高级使用

**自定义研究模式**
- 在研究员模式（广泛搜索）和作家模式（专注写作）之间切换
- 通过 `.roomodes` 文件配置行为

**本地知识图谱**
- 使用 DuckDB SQL 查询关系
- 可视化研究连接
- 导出引用网络

**协作功能**
- 通过 Git 共享工作区
- 在 `.sros/research_log.jsonl` 中维护研究历史
- 在团队成员间同步发现

### 文档
- [SROS_ARCHITECTURE_REFACTORING_COMPLETED.md](doc/SROS_ARCHITECTURE_REFACTORING_COMPLETED.md) - 完整重构实现
- [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md) - 当前进度和时间线
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md) - 开发指南和标准
- [doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md](doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md) - 原始架构计划
- [doc/SROS_FEDERAL_ACADEMIC_SEARCH_UPGRADE_PLAN.md](doc/SROS_FEDERAL_ACADEMIC_SEARCH_UPGRADE_PLAN.md) - 联邦学术搜索完整开发计划

### 故障排除

**常见问题：**
1. **导入错误**：确保所有目录名称使用 snake_case 格式
2. **缺少依赖**：根据需要安装可选包（`pip install duckdb`）
3. **服务器连接问题**：检查 MCP 服务器是否在正确端口运行
4. **权限错误**：确保项目目录有写权限

**调试技巧：**
- 检查 `.sros/logs/` 中的服务器日志
- 使用 `run_servers.py --debug` 获取详细输出
- 验证环境变量是否正确设置

### 贡献
1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 如适用，添加测试
5. 提交拉取请求

### 许可证
该项目采用 MIT 许可证 - 详情请见 LICENSE 文件。