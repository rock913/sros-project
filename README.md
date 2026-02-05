# Scientific Research Operating System (SROS) V2.2 / 科研操作系统 (SROS) V2.2

[English Version](#english-version) | [中文版本](#中文版本)

---

## English Version

### Overview
The Scientific Research Operating System (SROS) is a revolutionary platform that transforms the research workflow by combining the power of Model Context Protocol (MCP) servers with intelligent AI agents.

🎉 **RELEASE V2.2 (Gateway Edition)**: Major architectural upgrade implementing the "Hub-and-Spoke" model with a unified Gateway, solving connection limits and introducing Context-Aware Research.

### Core Philosophy
- **Draft-centered**: Writing drives research rather than separate search phases
- **Gateway-unified**: Single access point for all tools, enabling infinite scalability
- **Context-aware**: "paid-onboarding" for agents via pre-ingested materials
- **Local-first**: All data stored locally with Git compatibility

### Architecture
SROS V2.2 implements a **Hub-and-Spoke Model**:
- **Gateway (Hub)**: A single SSE server (Port 8000) managing all sub-services via stdio.
- **Sub-servers (Spokes)**: Specialized MCP servers running as managed subprocesses.
- **Client**: Roo Code connects only to the Gateway.

### Key Components

#### MCP Servers - ✅ ALL OPERATIONAL
All MCP servers are located in the [`mcp_servers/`](mcp_servers/) directory:

1. **sros_gateway/** (NEW) - United Gateway managing routing and sub-processes (Port 8000).
2. **context_ingester/** (NEW) - Ingests soft knowledge from `materials/` into the graph.
3. **federal_academic_search/** - Next-generation academic search federal architecture.
4. **manuscript_manager/** - Core manuscript operations.
5. **duckdb_memory/** - Local knowledge graph storage.
6. **zotero_expert/** - Local citation management.

#### Workspace Structure
Each research project uses a local-first approach with all data stored in the project directory:
SROS V2.2 adopts a multi-project workspace structure. All research work should happen inside the `workspace/` directory to keep the root clean.

```
/gemini-fullstack-langgraph-quickstart/  <-- Root (Open in VS Code)
├── .roo/                  # Global Configuration
│   ├── mcp.json           # Gateway definition
│   └── .roomodes          # Agent Personas (Researcher/Writer)
├── mcp_servers/           # Tool Implementations
└── workspace/             # Your Work Area
    ├── sros-paper-v1/     # Project A
    │   ├── .sros/         # [Auto] Local Graph & Logs
    │   ├── draft.md       # Manuscript
    │   └── materials/     # Context
    └── research-playground/ # Project B
        └── ...
```

#### How to Use
1. **Open the Root Folder** in VS Code to load the MCP servers and Modes.
2. **Navigate to `workspace/`** and create a new folder for your paper/project.
3. **Select a Mode** (SROS Researcher or Writer) and begin working on `draft.md` in your sub-folder.


### Core Workflows: Context-Enhanced Research - ✅ FUNCTIONAL
The system operates on a "write-while-researching" model with Context Enhancement:

1. **Warm-up / Ingest** (New): `context_ingester` scans `ideas.md` and `materials/` to inject "Soft Knowledge" into the graph.
2. **Observe**: Roo Code calls `manuscript_manager` to get current Markdown structure.
3. **Detect**: Identify gaps. *Optimization*: Checks "Soft Knowledge" in graph first; if answer exists in `materials/`, uses it instead of external search.
4. **Retrieve**: Call `federal_academic_search` via Gateway to find evidence for specific gaps.
5. **Build**: Store literature relationships (CiTO ontology) in local `.sros/graph.db`.
6. **Expand**: Use `manuscript_manager` atomic editing tools to insert cited content.
7. **Iterate**: Rescan manuscript to check if gaps are eliminated.

### Development Status - ✅ RELEASED
🚀 **V2.2 Gateway Implementation COMPLETE**

The SROS V2.2 system architecture has been successfully established with the Gateway + 5 core sub-servers.

#### Key Achievements:
- ✅ **Single Port Architecture**: Only port 8000 needed.
- ✅ **Unlimited Tools**: Gateway multiplexes requests, bypassing VS Code connection limits.
- ✅ **Context Awareness**: New Ingester service enables "warm start" for research.
- ✅ **Simplified Operation**: One command to start everything.

### Getting Started - ✅ READY FOR USE

#### Prerequisites
- Python 3.7+
- VS Code with Roo Code/Cline extension
- Git (for version control)

#### MCP Server Configuration - Gateway Mode (V2.2)

The SROS system now operates in Gateway mode.

##### Gateway Configuration
The `.roo/mcp.json` should be configured to connect to the Gateway:

```json
{
  "mcpServers": {
    "sros-gateway": {
      "name": "SROS Gateway",
      "url": "http://localhost:8000/sse",
      "type": "sse",
      "description": "Unified Gateway for all SROS services (Search, Manuscript, Memory, etc.)",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

##### Starting the Gateway
Use `run_servers.py` to start the Gateway (which automatically manages all sub-servers):

```bash
# Start Gateway (Port 8000) - Manages all sub-servers internally
python run_servers.py gateway
```

##### Testing
Verify the Gateway and sub-servers are working:

```bash
# Run Gateway end-to-end tests
python test_gateway.py
```


3. **Set Up Environment Variables**
The system now supports `.env` file configuration. Copy the `.env.example` file to `.env` and fill in your actual values:

```bash
cp .env.example .env
# Edit .env file with your actual configuration
```

Alternatively, you can set environment variables directly:
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
# 复制环境配置
cp /path/to/sros/.env.example .env
# 创建初始稿件
touch draft.md
# [可选] 创建材料目录
mkdir materials
# 创建初始想法文件
touch ideas.md
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
# Run all servers (now supports SSE mode)
python run_servers.py all

# Run with automatic port assignment to prevent conflicts
python run_servers.py all --auto-port

# Or run individual servers
python run_servers.py federal-academic-search --port 8001
python run_servers.py manuscript-manager --port 8004
python run_servers.py duckdb-memory --port 8005
python run_servers.py sros-logic --port 8006
python run_servers.py zotero-expert --port 8003
```

**Note**: With SSE mode, servers will be accessible via HTTP endpoints at the configured ports. The `.roo/mcp.json` file should be updated to use the SSE configuration with URLs pointing to these endpoints.

6. **Start Research Workflow**
- Open VS Code in your research project directory
- Install and activate Roo Code/Cline extension
- Begin writing in `draft.md` - the system will automatically detect gaps and suggest research

#### Usage Tutorial

**Step 0: Project Initialization**
1. Create a dedicated project folder for your research
2. Copy the `.env.example` file to `.env` and configure your API keys
3. Create your initial `draft.md` with basic structure
4. Add any preliminary ideas in `ideas.md` and supporting materials in `materials/`

**Step 1: Writing and Gap Detection**
1. **(Auto-Warmup)**: The system first digests your `ideas.md` and `materials/` into the graph
2. Start writing in your `draft.md` file
3. Add `[TODO:]` markers for sections you want to research
4. Roo Code will automatically detect gaps and trigger research workflows

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

**Best Practices:**
- Always work in a dedicated project folder (never in the SROS root directory)
- Use the `materials/` directory to store pre-existing research, notes, and AI-generated reports
- Regularly check the `.sros/graph.db` for knowledge graph updates
- Monitor `.sros/research_log.jsonl` for research activity tracking

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
- [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md) - Current status and history.
- [doc/SROS_V2.2_DEPLOYMENT_GUIDE.md](doc/SROS_V2.2_DEPLOYMENT_GUIDE.md) - Comprehensive deployment guide.
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md) - Contributing guidelines.
- [doc/SROS V2.2 架构实施总蓝图.md](doc/SROS%20V2.2%20架构实施总蓝图.md) - Architecture blueprint.

### Troubleshooting

**Common Issues:**
1. **Gateway not starting**: Check if port 8000 is occupied.
2. **Missing Dependencies**: `pip install duckdb` is required for Memory.
3. **Sub-process fails**: Run `python run_servers.py gateway` in a terminal to see stderr output from sub-servers.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## Key Updates in V2.2

### MCP Server Status
- **sros_gateway/**: ✅ New Hub.
- **context_ingester/**: ✅ New Service.
- **federal_academic_search/**: ✅ Integrated.
- **manuscript_manager/**: ✅ Integrated.

### 项目结构要求
- **根目录配置**: `.roomodes` 已迁移至 `.roo/.roomodes` 以保持根目录整洁。
- **工作区 (Workspace)**: 建议在 `workspace/` 目录下创建子文件夹来管理不同的研究项目。
- **MCP配置**: `.roo/mcp.json` 仅指向端口 8000 的网关。


## 中文版本

### 概述
科研操作系统 (SROS) 是一个革命性的平台，通过结合模型上下文协议 (MCP) 服务器和智能 AI 代理的力量来改变研究工作流程。

🎉 **V2.2 版本 (网关版)**：重大架构升级，实现了“Hub-and-Spoke”模型与统一网关，解决了连接数限制并引入了上下文感知研究。

### 核心理念
- **以草稿为中心**：写作驱动研究
- **统一网关**：单点接入，无限扩展
- **上下文感知**：预读材料，带薪进组
- **本地优先**：数据本地存储

### 架构
SROS V2.2 实现 **Hub-and-Spoke 模型**：
- **网关 (Hub)**：单一 SSE 服务器 (端口 8000)，管理所有子服务。
- **子服务 (Spokes)**：作为子进程运行，通过 stdio 通信。

### 关键组件

#### MCP 服务器 - ✅ 全部运行中
所有 MCP 服务器位于 [`mcp_servers/`](mcp_servers/) 目录中：

1. **sros_gateway/** (新增) - 统一网关 (Port 8000)。
2. **context_ingester/** (新增) - 上下文摄取服务。
3. **federal_academic_search/** - 联邦学术搜索。
4. **manuscript_manager/** - 核心手稿操作。
5. **duckdb_memory/** - 本地知识图谱存储。
6. **zotero_expert/** - 本地引用管理。


#### 工作区结构
每个研究项目都采用本地优先的方法，所有数据都存储在项目目录中：
```
/My_Research_Project/
├── .sros/                 # [自动生成] 隐藏状态目录
│   ├── graph.db           # 本地知识图谱 (DuckDB)
│   └── research_log.jsonl # 检索足迹
├── .roomodes              # [复制] 项目特定的行为定义
├── draft.md               # [核心] 单一事实来源
├── materials/             # [新增] Context Ingester 扫描区
│   ├── deep_research.md   
│   └── web_clips.txt      
└── references/            # PDF 附件
```

### 核心工作流：上下文增强 - ✅ 功能正常
1. **预热**: `context_ingester` 扫描 `materials/` 注入软知识。
2. **观察**: 获取 `draft.md` 结构。
3. **检测**: 识别 Gap (优先查本地软知识)。
4. **检索**: 通过网关调用 `federal_academic_search`。
5. **构建**: 知识图谱存入 `.sros/graph.db`。
6. **扩展**: 写入手稿。

### 开发状态 - ✅ 发布
🚀 **V2.2 网关版实现完成**

SROS V2.2 系统架构已确立，网关与所有子服务运行正常。

### 快速开始 - ✅ 就绪

#### 前提条件
- Python 3.7+
- VS Code + Roo Code
- Git

#### MCP 服务器配置 - 网关模式 (V2.2)

必须将 `.roo/mcp.json` 配置为指向网关：

```json
{
  "mcpServers": {
    "sros-gateway": {
      "name": "SROS Gateway",
      "url": "http://localhost:8000/sse",
      "type": "sse",
      "description": "SROS 统一网关",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

#### 启动网关
```bash
# 启动网关 (Port 8000) - 自动管理所有子服务
python run_servers.py gateway
```

#### 测试
```bash
python test_gateway.py
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