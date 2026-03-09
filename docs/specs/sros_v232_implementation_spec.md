# SROS V2.3.2 实现规范

> 本文档是 Builder 的实现依据：优先保证“可落地、可验收、低歧义”。

## 1. 目录结构规范

### 1.1 包结构 (安装后位于 site-packages/sros/)
```
/System_Python_Path/site-packages/sros/
├── cli.py                    # 命令行入口（Typer/Click）
├── domain/                    # 领域层（纯契约/纯数据结构，不依赖基础设施）
│   ├── ports/                 # Protocols（接口契约）
│   └── schemas/               # Pydantic Models（数据结构）
├── gateway/                  # MCP Hub（Starlette + FastMCP）
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── sse_handler.py
├── servers/                  # 内置 MCP 服务能力
│   ├── __init__.py
│   ├── manuscript/           # [核心] 稿件解析与 Gap 检测
│   │   ├── __init__.py
│   │   ├── handler.py
│   ├── scholar/              # [核心] 联邦搜索 + Co-STORM 视角生成
│   │   ├── __init__.py
│   │   ├── handler.py
│   ├── memory/               # DuckDB 知识图谱
│   │   ├── __init__.py
│   │   ├── handler.py
│   └── zotero/               # 引用管理
│       ├── __init__.py
│       ├── handler.py
└── utils/                    # 进程管理、健康检查、端口检测等
    ├── __init__.py
    ├── process_manager.py
    ├── health_checker.py
    └── port_detector.py
```

### 1.2 用户工作区结构 (sros init 生成)
```
/User/Documents/my_paper/
├── .roo/
│   └── mcp.json              # [自动生成] 指向 http://localhost:8000/sse
├── .roomodes                 # [可选/自动生成] Roo Code 自定义模式定义（YAML）
├── .sros/
│   ├── graph.db              # DuckDB（私有知识图谱）
│   └── gap_log.json          # Gap 检测记录（可选）
├── materials/                # 原始素材（Deep Research Reports）
├── references/               # 可选：导出引用/缓存 BibTeX 等
├── draft.md                  # [单一真理来源] 正在撰写的稿件
└── ideas.md                  # 核心论点备忘录
```

### 1.3 源码仓库结构 (面向打包的标准形态)
```
/sros-repo/
├── pyproject.toml            # [核心] 包定义与 CLI 入口点
├── src/
│   └── sros/
│       ├── __init__.py
│       ├── cli.py            # CLI 入口（init/start/doctor）
│       ├── domain/            # 领域层（ports/schemas，禁止依赖 servers/gateway/utils）
│       │   ├── ports/
│       │   └── schemas/
│       ├── gateway/          # 原 mcp_servers/sros_gateway
│       ├── servers/          # 原 mcp_servers/*（子服务聚合）
│       └── utils/            # 原 scripts/ 与 run_servers.py 的可复用逻辑
└── README.md
```

### 1.4 分层与依赖方向（强约束）

- domain/ 是“纯净层”：只包含 Protocol（ports）与数据模型（schemas），不得 import gateway/servers/utils，也不得做 IO。
- servers/ 与 gateway/ 是“适配层”：实现 domain/ports 并将其暴露为 MCP tools；可以依赖 domain/。
- utils/ 是“通用基础设施”：可被 gateway/servers 调用；不得反向依赖 domain/。

依赖方向：

domain → (无)

servers/gateway/utils → domain

## 2. 协议接口规范

说明：以下代码块用于定义“契约形态”，实际实现时建议拆分为：

- src/sros/domain/schemas/*.py
- src/sros/domain/ports/*.py

### 2.1 Manuscript Protocol
```python
from __future__ import annotations

from typing import Protocol, List, Dict, Any
from pydantic import BaseModel

class GapAnalysisResult(BaseModel):
    section: str
    type: str  # "Evidence Needed", "Elaboration Needed", "Citation Needed"
    confidence: float
    suggestions: List[str]

class OutlineNode(BaseModel):
    id: str
    title: str
    level: int
    content: str
    children: List['OutlineNode']

# Pydantic v2 注意：递归模型需要在模块加载后执行 `OutlineNode.model_rebuild()`
# 或使用 `from __future__ import annotations`（本示例已包含）。

class ManuscriptProtocol(Protocol):
    def find_gaps(self, file_path: str) -> List[GapAnalysisResult]:
        """基于规则识别待办项"""
        ...
    
    def get_outline_tree(self, file_path: str) -> OutlineNode:
        """返回 Markdown/AST 的树状结构"""
        ...
    
    def insert_section(self, target: str, content: str, citations: List[str]) -> bool:
        """带引用的增量写入"""
        ...
    
    def patch_draft(self, patches: List[Dict[str, Any]]) -> bool:
        """批量更新稿件内容"""
        ...
```

### 2.2 Scholar Protocol
```python
class ResearchPerspective(BaseModel):
    id: str
    title: str
    description: str
    relevance_score: float
    supporting_evidence: List[str]

class SearchQuery(BaseModel):
    query: str
    max_results: int = 10
    filters: Dict[str, Any] = {}

class ScholarProtocol(Protocol):
    def brainstorm_perspectives(self, query: str) -> List[ResearchPerspective]:
        """Co-STORM 核心，生成多维研究视角"""
        ...
    
    def find_critiques(self, paper_id: str) -> List[Dict[str, Any]]:
        """CiTO 逻辑，寻找反驳/质疑类文献"""
        ...
    
    def federated_search(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """联邦搜索多个学术数据库"""
        ...
```

### 2.3 Memory Protocol
```python
class KnowledgeEdge(BaseModel):
    source: str
    target: str
    relationship: str  # "CITES", "REFERENCES", "RELATED_TO", "CONTRADICTS"
    confidence: float

class MemoryProtocol(Protocol):
    def store_knowledge(self, nodes: List[Dict[str, Any]], edges: List[KnowledgeEdge]) -> bool:
        """存储知识节点和关系"""
        ...
    
    def query_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """查询知识图谱"""
        ...
    
    def get_citation_map(self, section_id: str) -> List[KnowledgeEdge]:
        """获取特定章节的引用关系图"""
        ...
```

### 2.4 Zotero Protocol
```python
class Citation(BaseModel):
    citekey: str
    title: str
    authors: List[str]
    year: int
    journal: str
    url: str
    bibtex: str

class ZoteroProtocol(Protocol):
    def add_citation(self, citation: Citation) -> bool:
        """添加引用到数据库"""
        ...
    
    def get_citation(self, citekey: str) -> Citation:
        """根据 citekey 获取引用信息"""
        ...
    
    def search_citations(self, query: str) -> List[Citation]:
        """搜索引用"""
        ...
```

## 3. CLI 命令行为规范

### 3.1 sros init
```bash
sros init <project_name>
```
**行为**：
- 在当前目录创建 `<project_name>` 文件夹
- 生成完整的用户工作区结构
- 自动生成 `.roo/mcp.json` 指向 `http://localhost:8000/sse`
- 初始化 `.sros/` 目录和可用的 DuckDB `graph.db`（必须是可连接的 DB 文件，不能是空文本）
- 可选生成项目级 `.roomodes` 配置

**验证**：
- 检查目标目录是否已存在
- 验证磁盘空间足够
- 确认 Python 环境兼容性

### 3.2 sros start
```bash
sros start
```
**行为**：
- 启动 MCP Gateway 服务
- 启动所有内置 MCP 服务器
- 监听端口 8000 提供 SSE 连接
- MVP 阶段默认以前台方式运行（便于跨平台与可调试），输出服务状态与连接信息，并打印 "SYSTEM READY"

**验证**：
- 检查端口 8000 是否被占用
- 验证所有 MCP 服务启动成功
- 确认 SSE 连接可用

## 4. MVP 定义（Done Definition）

本仓库的 MVP 目标是“Roo 可以连上 Gateway 并成功调用至少 1 个工具”，同时 CLI 能初始化/启动最小工作流。

MVP 必须满足（可自动化验证）：
- 安装后可用：`pip install -e .` 后 `sros --help` 正常
- `sros init <workspace>` 生成：`.roo/mcp.json`、`.sros/graph.db`（DuckDB 可连接）、`draft.md`、`ideas.md`
- `sros start -w <workspace> -p <port>` 启动后：
    - `GET /health` 返回 200
    - `GET /sse` 返回 `text/event-stream`
    - `POST /sse` 支持 JSON-RPC：`initialize`、`tools/list`、`tools/call`
    - `tools/list` 至少包含 `manuscript.find_gaps`
    - `tools/call` 能成功调用 `manuscript.find_gaps` 并返回结构化结果

显式非目标（不阻塞 MVP）：
- `tools/list` 的 `inputSchema` 精确到每个参数（本仓库已作为可用性增强实现，不再是待办）
- draft IO 严格绑定 `SROS_WORKSPACE_DIR` + 路径安全（本仓库已实现，不再是待办）
- 完整 scholar 联邦搜索、zotero 全功能、复杂 patch/insertion 语义（仍属于 Future Work，不阻塞 MVP）

### 当前仓库状态（基于自动化测试）

- MVP 链路已可自动化验证通过：`GET /health` / `GET /sse` / `POST /sse`（initialize/tools/list/tools/call）
- Playbook B（DuckDB 可连接）与 Playbook C（workspace 绑定 + 路径安全）已落地并有测试覆盖
- 当前测试套件全绿：`python -m pytest -q`

结论：与 [docs/specs/sros_roo_playbooks.md](docs/specs/sros_roo_playbooks.md) 对齐的 Playbook A/B/C 以及文内列出的 Post-MVP 增强在本仓库均已实现；当前无阻塞性待完成项。

## 5. Post-MVP（为什么还要做“下一步计划”）

即便 MVP 已通过，仍建议继续做下一步计划的原因是：
- Roo 可用性：`inputSchema` 不精确会导致 Roo 自动构造参数失败、反复试错；这会显著降低“看起来能用”的真实体验。
- 稳定性：workspace 语义不严格（draft IO 不绑定 `SROS_WORKSPACE_DIR`）会造成“在错目录写文件”的数据事故。
- 可维护性：将契约（schemas/ports）与适配层（gateway/servers）的边界再固化，有利于后续升级而不破坏 Roo。

### 3.3 sros doctor
```bash
sros doctor
```
**行为**：
- 检查 Python 环境和依赖
- 验证端口占用情况
- 检查 DuckDB 文件完整性
- 测试 MCP 服务连通性
- 输出详细的健康报告

### 3.4 sros status（别名/可选）

建议将 `sros status` 作为 `sros doctor --short` 的别名（或子命令），避免命令心智负担。

**行为（若保留）**：

- 显示当前工作区状态（是否存在 draft.md/.roo/mcp.json/.sros/graph.db）
- 报告 Gateway 服务运行状态（端口占用/健康检查）
- 输出最近的 Gap 检测结果摘要（若存在 gap_log.json）

## 6. 扩展验收清单（Future Work，不阻塞 MVP）

> 说明：下列条目是“扩展验收/未来增强”的候选清单。
> 本仓库的 MVP Done Definition 以第 4 节为准；本节条目即使未全部完成，也不应被视为 MVP 未达成。

建议用法：把本节当作 Roadmap/Backlog；只有当你决定推进某条能力时，才需要把对应条目补齐实现与自动化测试。

### 4.1 功能验收
- [ ] **CLI 安装验证**：`pip install sros` 成功安装，`sros --help` 显示帮助信息
- [ ] **项目初始化**：`sros init test_paper` 正确生成完整的工作区结构
- [ ] **服务启动**：`sros start` 成功启动所有 MCP 服务，端口 8000 可访问
- [ ] **Gap 检测**：在 `draft.md` 中插入 `[TODO: test]` 后能正确识别并返回 Gap 分析结果
- [ ] **视角生成**：调用 `brainstorm_perspectives` 能生成至少 3 个有效的研究视角
- [ ] **增量写入**：`insert_section` 能正确向 `draft.md` 添加内容并保持格式
- [ ] **引用映射**：在 `.sros/graph.db` 中正确建立 `DraftSection → CITES → Paper` 关系

### 4.2 性能验收
- [ ] **启动时间**：`sros start` 在 10 秒内完成所有服务启动
- [ ] **Gap 检测响应**：`find_gaps` 在 2 秒内返回结果
- [ ] **内存使用**：Gateway 服务内存占用不超过 200MB
- [ ] **并发支持**：支持至少 5 个并发 MCP 连接

### 4.3 稳定性验收
- [ ] **异常处理**：所有 MCP 服务能优雅处理异常请求
- [ ] **数据持久化**：重启后 `.sros/graph.db` 数据不丢失
- [ ] **服务恢复**：单个 MCP 服务故障不影响其他服务
- [ ] **日志记录**：关键操作都有详细日志输出

### 4.4 用户体验验收
- [ ] **文档完整性**：所有 CLI 命令都有清晰的帮助信息
- [ ] **错误提示**：用户操作错误时提供明确的解决建议
- **工作流顺畅**：从 `sros init` 到开始写作的完整流程不超过 5 分钟
- [ ] **Roo Code 集成**：`.roo/mcp.json` 能被 Roo Code 自动识别并连接

## 5. 迁移兼容性要求

### 5.1 向后兼容
- 现有的 `draft.md` 格式完全兼容
- 新版工具命名以 `find_gaps` 为准；如需兼容旧客户端，可在服务端保留 `scan_gaps` 作为 deprecated alias（文档/新客户端不再使用）
- 现有的搜索和引用功能正常工作

### 5.2 数据迁移
- `sros migrate` 作为后续增强（Future Work）。在 MVP 阶段优先保证：用户可手动将旧 `draft.md` 复制到新 workspace 并继续工作。

（可选的最小迁移定义，若实现 migrate）：

- 输入：`sros migrate <old_project_path> [--name <new_project_name>]`
- 输出：在当前目录生成新 workspace；复制/链接 draft.md；生成 .roo/mcp.json；初始化 .sros/graph.db；可选生成 .roomodes(YAML)
- 验收：迁移后可直接执行 `sros start` 并在 VS Code 打开新目录写作
