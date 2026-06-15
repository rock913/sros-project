# CLAUDE.md — SROS (Scientific Research Operating System)

> SROS V3.1-dev：AI4S 科研操作系统 — 文稿写作 + 文献合成 + 知识图谱 + 数据摄入 + HPC 调度。
> 战略方向 V4.0：全面 MCP 化 + 生态纳管 + 数据 OS。

## Code-Wiki 架构图谱读取要求（硬性规定）

当你在修改本仓库的代码前：

1. **必须**先读取 `docs/code_wiki/index.md` 获取全局架构概览（~1500 tokens）
2. 读取 `docs/code_wiki/` 下与你要修改的模块相关的图谱页面，了解架构连线关系
3. 如果不确定影响范围，使用 `claw-graph-query --action search --keyword <module_name>` 查询依赖关系
4. 修改完代码后，提醒用户运行 `make update-wiki` 刷新图谱

违反此规定的代码修改属于无效交付。

## 项目架构速览

```
src/sros/
  cli.py               — sros CLI: init/start/stop/status/doctor
  gateway/             — MCP SSE Hub (FastAPI + JSON-RPC)
  skills/
    cli.py             — sros-skill CLI: manuscript/scholar/memory/data/db/hpc/rag/ext/plugins/tasks
    rpc.py             — 单一 dispatch_tool() 分发器 (~50 tool names → handlers)
  servers/
    manuscript/        — 文稿 gap/outline/insert/patch/refactor
    scholar/           — 联邦搜索 + OpenAlex + Zotero 同步
    memory/            — DuckDB 知识图谱 (nodes/edges)
    data/              — CSV preview + Python 脚本执行 + 溯源
    db/                — V4: BIDS/TSV/Excel 摄入 + SQL 查询
    hpc/               — V4: Slurm 作业管理 + OOM 自愈
    rag/               — 词法分块 + DuckDB RAG
    ext/               — 网页抓取
    tasks/             — 异步任务管理
    zotero/            — Zotero 引用管理
  domain/
    ports/             — Protocol 接口定义
    schemas/           — Pydantic 数据模型
  utils/               — 进程管理、健康检查、插件加载
config/
  duckdb/schema.sql    — 8 表 DDL
  slurm/*.slurm        — Slurm 作业模板
docs/
  code_wiki/           — ARC 编译器生成的架构图谱（make update-wiki）
tests/
  unit/                — 80+ 单元测试
  integration/         — Gateway + SSE 集成测试
```

## 关键约定

- **IDE-as-UI**：Claude Code / Roo Code 通过 MCP 协议调用 SROS tools
- **Thin Gateway**：Gateway 不含业务逻辑，所有实现通过 `rpc.dispatch_tool()` 分发到 handler
- **Skill-First**：所有能力通过 `sros-skill` CLI 暴露，`--raw` 输出纯 JSON
- **Workspace-Relative Paths**：所有路径 workspace-relative，禁止 `../` 遍历
- **TDD**：先写 failing test → 实现 → pytest 绿条
- **Don't Guess, Copy**：新功能从现有 handler 模式复制骨架

## ARC Code-Wiki 集成

```
arc_wiki.json          → ARC 编译器配置文件
docs/code_schema.md    → SROS 特有的实体/概念/关系提取规则
docs/code_wiki/        → ARC 编译器输出（版本化，随代码提交）
make update-wiki       → 一键刷新图谱
```

## ⚠️ DevX 全局行为准则与 Git 规范

> 来源：Meta Phase 7 DevX 混合架构基础设施升级
> 本规范适用于交互式终端 (Tmux) 和非交互式飞书桥接两种运行环境。

1. **环境认知**：你可能运行在交互式终端 (Tmux) 或非交互式的飞书桥接中。严禁使用阻塞性交互命令 (`vim`, `nano`, `less`)。读取文件请用 `cat` 或 `head`。

2. **静默优先**：当前环境已开启 Auto Mode。对于确定性的依赖安装、Linter 执行、文件覆盖，请直接执行，遇到询问默认加 `-y`，尽量减少向用户索要权限。

3. **隔离红线**：当前所有项目运行在同一 Linux 账户下。**绝对禁止**通过 `cd ../` 访问或修改当前项目根目录以外的任何文件。所有操作必须在当前仓库目录内完成。

4. **Git 短期分支流 (SLAIB)**：
   - `main` 分支已被写保护，无法直接 push。
   - 任何修改前，必须执行 `git checkout -b <type>/<desc>`（例如 `feat/add-login`, `fix/oom-error`, `refactor/scheduler`）。
   - 修改完成后推送分支到远程。

5. **PR 门禁**：
   - 推送分支后，使用 GitHub CLI (`gh pr create --fill`) 发起 Pull Request。
   - 等待人类主理人在 GitHub 上审批并 Squash and Merge。
   - **严禁**尝试绕过 PR 机制直接 push main。

6. **自动清理**：
   - PR 被 Squash and Merge 后，远程分支会自动删除。
   - 本地执行 `git fetch --prune` 清理已删除的远程分支引用。
   - 本地分支可手动删除：`git branch -d <type>/<desc>`。
