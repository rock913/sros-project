SROS CLI 架构与交互规范：面向 HPC 与大模型的双向桥梁

一、 核心反思：为什么 SROS 必须是 CLI？

在 SROS V4.0 全面转向 MCP (Model Context Protocol) 和大模型（如 Claude Code）主导的背景下，为什么我们还需要一个底层的 sros 命令？

1. HPC (交我算) 生态的原生限制

正如我们在实际部署中遇到的，HPC 集群的登录节点（如 pilogin.hpc.sjtu.edu.cn）只有终端 (Terminal)。没有图形界面，不允许运行常驻 Web 服务，甚至对后台守护进程都有严格限制。
在这样的物理限制下，一个强大的 CLI 是部署 SROS 系统的唯一合法且稳健的载体。

2. CLI 是大模型最好的“物理抓手”

Claude Code 这类顶尖 Agent 本质上是极度擅长生成和执行 Shell 命令的。
虽然我们有 MCP 协议，但 MCP Server 本身也需要被启动和管理。提供一个标准化的 CLI（如 sros hpc submit），不仅让人类可以使用，大模型在排障时也可以通过阅读 CLI 的 --help 提示，自主纠正参数错误（这在 SROS V4.0 规划中被称为“减少 Agent 摩擦”）。

3. 人机协作的“降级通道 (Human-Fallback)”

当大模型产生幻觉，或者您需要快速在 SSH 终端里查一下 SXMU_MDD 队列的预处理进度时，您不可能每次都去唤醒大模型。此时，敲入一行 sros hpc status 获取直观的结果，是不可或缺的兜底能力。

二、 SROS CLI vs ARC CLI 的边界划定

遵循“解耦与协同”战略，我们在终端里的命令前缀必须泾渭分明：

arc ...：面向知识与文档。负责解析代码（Code-Wiki）、将 DuckDB 数据编译为 Markdown（Data-Wiki）。

sros ...：面向算力与数据执行。负责与 Slurm 对接、拉取 Apptainer、管理底层 DuckDB 的摄入。

三、 SROS CLI 核心命令树设计 (Command Tree)

SROS 的 CLI 应该采用类似 git 或 kubectl 的主子命令结构，直接映射我们在 PRD 中定义的几个核心 Skill Packs。

1. 守护进程与 MCP 服务管理 (sros mcp)

这是 SROS 与 Claude Code 对接的桥梁。

sros mcp start：在当前 HPC 登录节点前台拉起 MCP Server（允许 Claude Code 通过 stdio 接入）。

sros mcp list：查看当前注册了哪些 MCP 工具（如 hpc-submit, db-query）。

2. 底层数据基座层 (sros db)

接管之前依赖 HPC 文件系统扫描的灾难操作。

sros db ingest --source /lustre/.../SXMU_Data --db sxmu.duckdb：将 BIDS 目录树和临床量表结构化压入 DuckDB。

sros db query "SELECT count(*) FROM subjects WHERE age > 60"：允许人类或 Agent 直接快速执行 SQL，返回格式化表格。

3. HPC 调度与算力层 (sros hpc)

将繁琐的 Slurm 脚本生成和 OOM 报错进行封装。

sros hpc submit --array 1-1427 --mem 48G --script run_fmriprep.sh：自动封装 sbatch 并提交作业。

sros hpc status --job <job_id>：不仅返回 Slurm 的状态，还能自动分析 .err 日志，用自然语言输出“节点 vol01 发生 OOM，建议提升内存”。

4. 垂类工具纳管层 (sros neuro)

完美向下兼容 NeuroClaw、graphmri 等特定领域的镜像应用。

sros neuro run --skill adni-skill --data /lustre/... --container neuroclaw.sif：通过 Apptainer 隔离运行 NeuroClaw 的封装命令。

四、 "Agent-First" 的 CLI 开发规范

为了让 Claude Code 能够丝滑地使用 sros CLI，在开发时必须遵循以下“机器友好”原则：

全局 --json 输出：任何命令只要加上 --json，必须返回严格格式化的 JSON 字符串，彻底摒弃人类友好的 ASCII 表格，方便大模型直接解析 AST 或提取 ID。

幂等性 (Idempotency)：执行两次 sros db ingest 不应导致数据重复；执行多次提交，如果发现参数一致且已有排队任务，应自动跳过。这能防止 Agent 陷入死循环。

极度详细的 Error Codes：报错信息不能只写 "Failed"。必须写明：Error: [E-OOM] Memory limit exceeded. Recommendation: Re-run with --mem > 32G。大模型看到 Recommendation 后，就能自动修正并重试。