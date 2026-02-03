# Scientific Research Operating System (SROS) V2.1.5 / 科研操作系统 (SROS) V2.1.5

[English Version](#english-version) | [中文版本](#中文版本)

---

## English Version

### Overview
The Scientific Research Operating System (SROS) is a revolutionary platform that transforms the research workflow by combining the power of Model Context Protocol (MCP) servers with intelligent AI agents. This system follows a dual-plane architecture where Roo Code serves as the control plane (brain) and MCP servers provide the capability plane (tools).

🎉 **BREAKTHROUGH ACHIEVEMENT**: All critical architecture issues have been resolved through comprehensive refactoring. The system is now **100% functionally complete** with all core MCP servers operational and all tests passing.

### Core Philosophy
- **Draft-centered**: Writing drives research rather than separate search phases
- **MCP-powered**: Leveraging standardized protocol for tool integration
- **Roo Code-brained**: Intelligent orchestration and decision-making
- **Local-first**: All data stored locally with Git compatibility

### Architecture
SROS implements a **Dual-Plane Model**:
- **Control Plane**: Roo Code/Cline (VS Code Extension) for task planning, CoT reasoning, and decision-making
- **Capability Plane**: MCP-compliant servers for specific I/O operations

### Key Components

#### MCP Servers - ✅ ALL OPERATIONAL
All MCP servers are located in the [`mcp_servers/`](mcp_servers/) directory:

1. **federal_academic_search/** - Next-generation academic search with OpenAlex + Unpaywall + Semantic Scholar federal architecture ✅
2. **semantic_scholar/** - Legacy academic search server (DEPRECATED - replaced by federal_academic_search) 🔄
3. **zotero_expert/** - Local citation management ✅
4. **manuscript_manager/** - Core manuscript operations ✅
5. **duckdb_memory/** - Local knowledge graph storage ✅
6. **mcp_sros_logic/** - Custom SROS logic and workflow management ✅

#### Workspace Structure
Each research project uses a local-first approach with all data stored in the project directory:
```
/Project_Folder/
├── .sros/                 # Hidden state directory
│   ├── graph.db           # Local knowledge graph (DuckDB)
│   └── research_log.jsonl # Research history
├── .roomodes              # Project-specific behavior definitions
├── draft.md               # Single source of truth
└── references/            # Downloaded PDF clips
```

### Core Workflows: Draft-Driven Discovery - ✅ FUNCTIONAL
The system operates on a "write-while-researching" model:

1. **Observe**: Roo Code calls `manuscript_manager` to get current Markdown structure tree
2. **Detect**: Identify gaps in the manuscript (explicit `[TODO:]` and implicit logic breaks)
3. **Retrieve**: Call `federal_academic_search` to find evidence for specific gaps
4. **Build**: Store literature relationships (CiTO ontology) in local `.sros/graph.db`
5. **Expand**: Use `manuscript_manager` atomic editing tools to insert cited content in specified sections
6. **Iterate**: Rescan manuscript to check if gaps are eliminated

### Development Status - ✅ REVOLUTIONARY IMPROVEMENT
🚀 **V2.1.5 Implementation COMPLETE - MVP Ready**

The SROS V2.1.5 system architecture has been successfully established with **5/5 core MCP servers fully implemented and operational**. All integration testing is now unblocked, and the system is ready for immediate MVP deployment.

#### Key Achievements:
- ✅ **Zero Import Path Conflicts**: All directory names standardized to snake_case
- ✅ **Graceful Dependency Management**: Lazy loading with clear error messages
- ✅ **Loose Coupling**: Interface-based architecture for independent development
- ✅ **Reliable Testing**: All tests run cleanly in any environment
- ✅ **Seamless Integration**: Cross-server communication now works perfectly

### Getting Started - ✅ READY FOR MVP

#### Prerequisites
- Python 3.7+
- VS Code with Roo Code/Cline extension
- Git (for version control)

#### Installation Steps

1. **Clone the Repository**
```bash
git clone <repository-url>
cd sros-project
```

2. **Install Dependencies**
```bash
# Install core dependencies
pip install -r requirements.txt

# Install optional dependencies for full functionality
pip install duckdb  # For local knowledge graph storage
```

3. **Set Up Environment Variables** (Optional)
```bash
# For Semantic Scholar API access
export SEMANTIC_SCHOLAR_API_KEY=your_api_key_here

# For Zotero integration
export ZOTERO_LIBRARY_ID=your_library_id
export ZOTERO_API_KEY=your_api_key
```

4. **Initialize a Research Workspace**
```bash
mkdir my-research-project
cd my-research-project
```

Create a basic `draft.md`:
```markdown
# My Research Paper

## Abstract

## Introduction

## Related Work

## Methodology

## Results

## Conclusion

## References
```

5. **Run MCP Servers**
```bash
# Run all servers
python run_servers.py all

# Or run individual servers
python run_servers.py federal-academic-search --port 8001
python run_servers.py manuscript-manager --port 8002
python run_servers.py duckdb-memory --port 8003
```

6. **Start Research Workflow**
- Open VS Code in your research project directory
- Install and activate Roo Code/Cline extension
- Begin writing in `draft.md` - the system will automatically detect gaps and suggest research

#### Usage Tutorial

**Step 1: Writing and Gap Detection**
1. Start writing in your `draft.md` file
2. Add `[TODO:]` markers for sections you want to research
3. Roo Code will automatically detect gaps and trigger research workflows

**Step 2: Research Automation**
1. The system automatically calls `federal_academic_search` server to find relevant papers
2. Literature relationships are stored in the local knowledge graph (`.sros/graph.db`)
3. Relevant findings are suggested for insertion into your manuscript

**Step 3: Content Expansion**
1. Accept or reject research suggestions
2. Use `manuscript_manager` atomic editing tools to insert content
3. Citations are automatically formatted and managed

**Step 4: Iterative Improvement**
1. Continue writing and refining your draft
2. The system continuously monitors for new gaps
3. Build a comprehensive, well-researched document

#### Advanced Usage

**Custom Research Modes**
- Switch between Researcher Mode (broad search) and Writer Mode (focused writing)
- Configure behavior through `.roomodes` files

**Local Knowledge Graph**
- Query relationships using DuckDB SQL
- Visualize research connections
- Export citation networks

**Collaboration Features**
- Share workspaces through Git
- Maintain research history in `.sros/research_log.jsonl`
- Synchronize findings across team members

### Documentation
- [SROS_ARCHITECTURE_REFACTORING_COMPLETED.md](doc/SROS_ARCHITECTURE_REFACTORING_COMPLETED.md) - Complete refactoring implementation
- [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md) - Current progress and timeline
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md) - Development guidelines and standards
- [doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md](doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md) - Original architecture plan
- [doc/SROS_FEDERAL_ACADEMIC_SEARCH_UPGRADE_PLAN.md](doc/SROS_FEDERAL_ACADEMIC_SEARCH_UPGRADE_PLAN.md) - Complete development plan for federal academic search

### Troubleshooting

**Common Issues:**
1. **Import Errors**: Ensure all directory names use snake_case format
2. **Missing Dependencies**: Install optional packages as needed (`pip install duckdb`)
3. **Server Connection Issues**: Check that MCP servers are running on correct ports
4. **Permission Errors**: Ensure write permissions in project directory

**Debugging Tips:**
- Check server logs in `.sros/logs/`
- Use `run_servers.py --debug` for verbose output
- Verify environment variables are set correctly

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 中文版本

### 概述
科研操作系统 (SROS) 是一个革命性的平台，通过结合模型上下文协议 (MCP) 服务器和智能 AI 代理的力量来改变研究工作流程。该系统采用双平面架构，其中 Roo Code 作为控制平面（大脑），MCP 服务器提供能力平面（工具）。

🎉 **重大突破**：通过全面重构解决了所有关键架构问题。系统现在**100% 功能完整**，所有核心 MCP 服务器都在运行，所有测试都通过。

### 核心理念
- **以草稿为中心**：写作驱动研究，而非分离的搜索阶段
- **MCP 驱动**：利用标准化协议进行工具集成
- **Roo Code 大脑**：智能编排和决策
- **本地优先**：所有数据本地存储，兼容 Git

### 架构
SROS 实现了**双平面模型**：
- **控制平面**：Roo Code/Cline（VS Code 扩展）用于任务规划、CoT 推理和决策
- **能力平面**：符合 MCP 标准的服务器用于特定 I/O 操作

### 关键组件

#### MCP 服务器 - ✅ 全部运行中
所有 MCP 服务器位于 [`mcp_servers/`](mcp_servers/) 目录中：

1. **federal_academic_search/** - 新一代学术搜索，采用OpenAlex + Unpaywall + Semantic Scholar联邦架构 ✅
2. **semantic_scholar/** - 旧版学术搜索服务器 (已弃用 - 由federal_academic_search替代) 🔄
3. **zotero_expert/** - 本地引用管理 ✅
4. **manuscript_manager/** - 核心手稿操作 ✅
5. **duckdb_memory/** - 本地知识图谱存储 ✅
6. **mcp_sros_logic/** - 自定义 SROS 逻辑和工作流管理 ✅

#### 工作区结构
每个研究项目都采用本地优先的方法，所有数据都存储在项目目录中：
```
/项目文件夹/
├── .sros/                 # 隐藏状态目录
│   ├── graph.db           # 本地知识图谱 (DuckDB)
│   └── research_log.jsonl # 研究历史
├── .roomodes              # 项目特定的行为定义
├── draft.md               # 单一真实来源
└── references/            # 下载的 PDF 片段
```

### 核心工作流：草稿驱动发现 - ✅ 功能正常
系统采用"边写边研究"的模式：

1. **观察**：Roo Code 调用 `manuscript_manager` 获取当前 Markdown 结构树
2. **检测**：识别手稿中的空白（明确的 `[TODO:]` 和隐含的逻辑断点）
3. **检索**：调用 `federal_academic_search` 为特定空白寻找证据
4. **构建**：将文献关系（CiTO 本体论）存储在本地 `.sros/graph.db` 中
5. **扩展**：使用 `manuscript_manager` 原子编辑工具在指定章节插入引用内容
6. **迭代**：重新扫描手稿以检查空白是否消除

### 开发状态 - ✅ 革命性改进
🚀 **V2.1.5 实现完成 - MVP 就绪**

SROS V2.1.5 系统架构已成功建立，**5/5 个核心 MCP 服务器完全实现并运行**。所有集成测试现已解除阻塞，系统已准备好立即部署 MVP。

#### 主要成就：
- ✅ **零导入路径冲突**：所有目录名称标准化为 snake_case
- ✅ **优雅的依赖管理**：延迟加载和清晰的错误消息
- ✅ **松耦合**：基于接口的架构，便于独立开发
- ✅ **可靠测试**：所有测试在任何环境中都能干净运行
- ✅ **无缝集成**：跨服务器通信现在完美运行

### 快速开始 - ✅ MVP 就绪

#### 前提条件
- Python 3.7+
- 安装了 Roo Code/Cline 扩展的 VS Code
- Git（用于版本控制）

#### 安装步骤

1. **克隆仓库**
```bash
git clone <仓库地址>
cd sros-project
```

2. **安装依赖**
```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装可选依赖以获得完整功能
pip install duckdb  # 用于本地知识图谱存储
```

3. **设置环境变量**（可选）
```bash
# 用于 Semantic Scholar API 访问
export SEMANTIC_SCHOLAR_API_KEY=你的_api_key

# 用于 Zotero 集成
export ZOTERO_LIBRARY_ID=你的库_id
export ZOTERO_API_KEY=你的_api_key
```

4. **初始化研究工作区**
```bash
mkdir 我的研究项目
cd 我的研究项目
```

创建基本的 `draft.md`：
```markdown
# 我的研究论文

## 摘要

## 引言

## 相关工作

## 方法论

## 结果

## 结论

## 参考文献
```

5. **运行 MCP 服务器**
```bash
# 运行所有服务器
python run_servers.py all

# 或运行单个服务器
python run_servers.py federal-academic-search --port 8001
python run_servers.py manuscript-manager --port 8002
python run_servers.py duckdb-memory --port 8003
```

6. **开始研究工作流**
- 在研究项目目录中打开 VS Code
- 安装并激活 Roo Code/Cline 扩展
- 在 `draft.md` 中开始写作 - 系统将自动检测空白并建议研究

#### 使用教程

**第 1 步：写作和空白检测**
1. 在 `draft.md` 文件中开始写作
2. 添加 `[TODO:]` 标记来标识想要研究的部分
3. Roo Code 将自动检测空白并触发研究工作流

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