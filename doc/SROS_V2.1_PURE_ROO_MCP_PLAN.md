SROS V2.1.5 开发全手册：科研自动化操作系统

版本: V2.1.5 (MVP Ready + Context Enhanced)
状态: ✅ 100% 功能完整 / 核心 Server 全部上线


核心哲学: 以稿件为中心，以 MCP 为触手，以环境隔离确保逻辑纯净。

1. 架构总览 (System Architecture)

SROS 采用 双平面模型 (Two-Plane Model)，严格区分“制造工具的人（Dev）”和“使用工具的人（User）”。

1.1 控制平面 (Control Plane)

载体: Roo Code / Cline (VS Code Extension)。

职责: 任务规划、CoT 推理、决策（决定何时检索、何时扩写）、人机交互。

逻辑存储:

.roomodes: 定义 SROS 的行为模式（如 Researcher vs Writer）。

mcp_sros_logic: 承载自定义的业务流逻辑。

1.2 能力平面 (Capability Plane)

载体: 驻留在 mcp_servers/ 目录下的 Python 脚本。

核心组件 (已落地):

federal_academic_search: 联邦学术搜索 (OpenAlex + Semantic Scholar)。

manuscript_manager: 稿件原子化操作与结构分析。

duckdb_memory: 本地知识图谱存储。

zotero_expert: 本地文献库管理。

context_ingester (新特性): 非结构化材料（笔记、AI 报告）解析与图谱注入。

2. 项目拓扑与环境策略 (Topology & Environment)

（核心更新：针对生产态目录的决策）

为了解决 Agent 上下文污染问题，我们定义两种截然不同的环境：

2.1 开发环境 (Maintenance Mode)

打开目录: SROS_ROOT/ (即 Git 仓库根目录)

目标: 维护 MCP Server 代码、运行测试、更新架构。

Agent 行为: 允许修改 python 脚本，运行 pytest。

2.2 生产环境 (Production/Research Mode)

打开目录: SROS_ROOT/workspace/My_Project_A/ (或磁盘上任何其他文件夹)

建议: 强烈建议直接打开具体的子项目文件夹，而不是父级 workspace。

理由:

上下文防火墙: Agent 只能看到当前论文的 draft.md，不会混淆项目 A 和 B 的引文。

路径相对性: 所有工具默认寻找 ./draft.md 和 ./.sros/，单一入口保证工具稳定性。

Git 独立性: 每个科研项目可以是一个独立的 Git Repo，方便投稿和协作。

推荐的文件结构：

/My_Research_Project/  <-- VS Code 打开此目录
├── .sros/                 # [自动生成] 隐藏状态目录
│   ├── graph.db           # 本地知识图谱 (DuckDB)
│   └── research_log.jsonl # 检索足迹
├── .roomodes              # [复制/软链] 项目特定的行为定义
├── .env                   # [复制] 环境变量配置
├── draft.md               # [核心] 单一事实来源
├── ideas.md               # [可选] 初始想法与头脑风暴记录（Agent 会优先读取此文件理解意图）
├── materials/             # [新增] 辅助参考材料
│   ├── deep_research.md   # Gemini/Perplexity 生成的调研报告
│   ├── web_clips.txt      # 网页剪藏
│   └── notes.md           # 随手笔记
└── references/            # [正式] 仅存放 Zotero 链接的正式 PDF 附件


3. 核心工作流：稿件驱动型调研 (Draft-Driven Discovery)

系统运作在 "Write-while-researching" 模式下，形成闭环：

预热 (Warm-up / Ingest): (新特性)

在开始工作前，Agent 自动扫描 ideas.md 和 materials/ 目录。

提取其中的关键概念、假设和初步数据，注入 .sros/graph.db，标记为“软知识 (Soft Knowledge)”。

目的：让 Agent “带薪进组”，不需要从零开始检索，而是先消化用户已有的思考。

观察 (Observe):

Agent 调用 manuscript_manager.get_structure() 获取当前 Markdown 结构树。

检测 (Detect):

Agent 识别稿件中的 Gap（显式的 [TODO:] 或隐式的逻辑断层）。

优化: Agent 会先比对 Gap 与“软知识”库，如果 materials/ 中已有答案，直接引用并提示用户“根据您的调研报告...”，而不是盲目去外部搜索。

检索 (Retrieve):

针对特定 Gap，如果本地材料不足，则调用 federal_academic_search。

V2.1.5 特性: 联邦搜索会自动聚合多源结果。

构建 (Build):

将文献关系（基于 CiTO 本体论）存入本地 .sros/graph.db。

扩展 (Expand):

使用 manuscript_manager.insert_section() 或 update_section() 进行原子化写入。

安全约束: 严禁使用 writeFile 覆盖整个文档。

迭代 (Iterate):

重新扫描稿件，确认 Gap 是否消除。

4. 启动与初始化 (Bootstrapping)

V2.1.5 引入了统一的启动脚本，简化了配置流程。

4.1 启动 MCP 服务器群

在任何终端（不需要在 VS Code 的内置终端）运行：

# 在 SROS 根目录下运行
python run_servers.py all



这将在后台启动所有 Server，并监听特定端口（如 8001, 8002 等）。

VS Code 中的 Roo Code 通过 SSE 或 Stdio 连接这些服务（具体取决于 .roo/mcp.json 的配置方式，推荐使用 SSE 以便跨目录调用）。

4.2 初始化新项目

mkdir my-new-paper
cd my-new-paper
# 复制环境配置
cp /path/to/sros/.env.example .env
# 创建初始稿件
touch draft.md
# [可选] 创建材料目录
mkdir materials
touch ideas.md



5. 开发重心：模式定义 (.roomodes)

由于架构已稳定，目前的开发重心转移到 Prompt Engineering。

5.1 SROS-Writer (写作模式)

System Prompt 关键指令:

"你的核心目标是消除 draft.md 中的 [TODO]。在写入任何内容前，必须先查询 .sros/graph.db（包含用户的 ideas.md 和 materials/ 上下文）。如果用户的笔记中已有相关论述，优先基于该内容扩写，并标记需要补充正式引用的地方。引用格式必须严格遵循 Zotero Key。"

5.2 SROS-Researcher (调研模式)

System Prompt 关键指令:

"你是一个严肃的分析员。你的任务不是写作，而是构建图谱。首先阅读 materials/ 下的所有文件，理解用户的初始假设。然后使用 federal_academic_search 寻找最新的综述，验证这些假设，并将其中的正反观点录入 duckdb_memory。"

6. 避坑指南 (V2.1.5 Updated)

Snake_case 强制: 在引用 Python 模块或目录时，务必检查是否符合 snake_case（如 manuscript_manager），V2.1.5 已全面标准化，旧的 kebab-case (如 manuscript-mcp) 已被废弃。

依赖懒加载: 如果发现某个 Server 启动慢，是因为 V2.1.5 采用了懒加载。不要因为没有立即响应就认为 Server 挂了，等待首次调用的 "Ready" 信号。

端口冲突: run_servers.py 默认使用 8000+ 端口。确保这些端口未被占用。

不要在 workspace 根目录写作: 再次强调，请为每篇论文建立单独文件夹。如果在 workspace/ 根目录下同时写三篇论文，Agent 会因为检索到错误的上下文而产生严重的幻觉。

7. 贡献与测试

运行全量测试:

pytest tests/



添加新工具:
在 mcp_servers/ 下创建新目录，并确保在 run_servers.py 中注册该服务。