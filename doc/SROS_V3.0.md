# SROS V3.0 战略规划（AI4S 全链路科研操作系统）

> 本文是“战略 + 可执行研发节奏”的单页版单一事实来源。
> 最后更新：2026-03-17（分支：v3.0-main）。

## 0. TL;DR

SROS V3.0 的定位是 **Headless Lab（无头实验室）**：

- Agent（Claude Code / OpenClaw / Roo）负责“思考与编排”。
- SROS 负责“提供规范化实验室（Workspace）+ 封装可调用仪器（Skills）+ 维护不可见账本（DuckDB 图谱）”。

研发方法：坚持 **Golden Thread + TDD**，每个 Slice 都要端到端可跑、可验收、可回归。

本文阅读方式：

- 先看「第 4 节：当前进度」确认现状
- 再看「第 5 节：Slice 3 → GA 路径」按迭代推进
- 最后用「第 6 节：验收清单」把关键链路跑一遍

## 1. 系统契约：Agent vs SROS

Agent 负责：

- 理解意图、拆解任务、组织技能调用
- 生成临时代码/脚本、撰写草稿、修订排版

SROS 负责：

- **Workspace 规范**：数据/脚本/图表/草稿的物理位置固定且可预测
- **Skills 封装**：把复杂能力变成一条稳定命令（人类可读 + 机器可读）
- **溯源图谱**：在生成数据/图表/文本时，自动写入“数据-代码-产物-文本”的可追溯链

## 2. 架构（1 页）

```text
┌───────────────────────────────────────────────────────────────┐
│ AI Agents: Claude Code / OpenClaw / Roo                        │
└───────┬───────────────────────────────┬───────────────────────┘
        │ CLI                            │ MCP / JSON-RPC
        ▼                                ▼
┌───────────────────────────────────────────────────────────────┐
│                SROS CLI Router & Thin Gateway                  │
└───────┬───────────────────────────────┬───────────────────────┘
        ▼                               ▼
┌─────────────────┐             ┌───────────────────────────────┐
│ sros-skill CLI   │             │ Domain/Core Skills (Python)    │
│ (human + --raw)  │             │ - manuscript / scholar / data  │
└───────┬─────────┘             └───────────────┬───────────────┘
        ▼                                       ▼
┌───────────────────────────────────────────────────────────────┐
│ SROS Workspace (Single Source of Truth)                        │
│ - draft.md / data/ / scripts/ / figures/ / .sros/graph.db      │
└───────────────────────────────────────────────────────────────┘
```

设计约束：**IDE-as-UI**（VS Code 的文件树 + Markdown 预览 + 终端即“可视化界面”），不投入传统 Web GUI。

## 3. 里程碑（Milestones）

| 版本 | 核心目标 | 最小验收标准（必须自动化/可复现） |
|---|---|---|
| V3.0-Alpha（Skill-Driven） | 写作闭环 & CLI/Gateway 基础设施 | 通过 `sros-skill` 走通“gap → search → insert → draft.md 更新”，并有集成回归测试 |
| V3.0-Beta（Data-Aware OS） | 数据/图表闭环 & 最小溯源链 | 读 CSV → 跑脚本出图 → draft 引用 → DuckDB 里可查到 `Script -GENERATES-> Figure` |
| V3.0-GA（Ecosystem） | 插件生态与长任务能力 | 插件可动态加载为新 skill；长耗时任务具备事件回调/通知机制 |

## 4. 研发切片（Slices）与当前进度（2026-03-17）

为避免“规划很宏大但无法落地”，V3.0 用切片管理交付：每个 Slice 都有 CLI 接口、工作区产物、图谱写入、测试回归。

### Slice 0：Workspace Bootstrapping ✅

- `sros init <proj> --target both` 初始化 V3 工作区结构（`data/raw`、`data/processed`、`figures`、`scripts`），并生成 Agent 配置（如 `openclaw.yaml`）。

### Slice 1：Writing Loop（Golden Thread）✅

- 已具备写作闭环的端到端回归：gap → search(mock) → insert → `draft.md` 更新。

### Slice 2：Data Loop（数据闭环）✅

- `sros-skill --raw data preview --file <csv>`：返回 CSV 摘要（行列数/列名/类型/样本/空值统计）。
- `SROS_WORKSPACE_DIR=<proj> sros-skill --raw data run-script --script <py> --dataset <csv> [--dataset <csv> ...]`：执行脚本，检测 `figures/` 新增文件并写入 DuckDB 图谱（并记录最小数据溯源）。
- 已落地最小溯源链：`[Script] -GENERATES-> [Figure]`（节点类型 Script/Figure）。

### Slice 2+：Provenance Enrichment（溯源增强）✅

目标：把“能跑”升级为“可解释、可追问、可复用”。

- Dataset 节点与 `ANALYZES` 边：`[Script] -ANALYZES-> [Dataset]`（通过 `--dataset` 显式声明）。
- Figure -> Draft/Section 引用关系：`[Figure] -REFERENCED_IN-> [draft_section:*]`（通过 `sros-skill --raw manuscript index-figures --file draft.md` 写回图谱）。

### Slice 2++：Data Loop Hardening（防逃逸 + Headless 默认值）✅

动机：真实 Agent 流水线里，“图画出来了但图谱是空的”通常不是能力缺失，而是 Agent 在报错后绕过 `sros-skill` 直接跑 `python scripts/*.py` 导致拦截器失效。

交付物：

- `data run-script` 环境硬化：默认注入 `MPLBACKEND=Agg`（无头环境画图不再因 `plt.show()` 等行为崩溃）
- Workspace 契约强化：`sros init` 生成的 `CLAUDE.md` 明确“禁止原生 python 运行数据脚本，必须用 `sros-skill data run-script`”

验收标准（TDD）：

- `data run-script` 子进程环境包含 `MPLBACKEND=Agg`（允许用户显式覆盖）
- `CLAUDE.md` 包含“不可触碰红线规则”与数据闭环的 Golden commands

### Slice 3：Plugins / Packs / Event Hooks ✅（MVP）

- 插件（First-class MCP Tools）
  - 工作区 `.sros/plugins/*.py` 自动发现
  - 在 Gateway `tools/list` 中动态暴露为 MCP tools：`plugin.<plugin_id>`
  - 也提供通用工具：`plugins.list` / `plugins.run`
  - 插件可选声明 `SKILL_INPUT_SCHEMA`（JSON Schema）以获得精确入参约束
- 长耗时任务（最小事件钩子）
  - `tasks.run_plugin_async` 启动后台任务并返回 `task_id`
  - `tasks.get/list/wait` 查询/等待任务状态
  - 任务完成后通过 Gateway SSE 广播 JSON-RPC notification：`method = sros.task.completed`

说明：这里的 Slice 3 标记为「MVP」——已经能被 Agent 调用、能回归测试，但还未做持久化/隔离/订阅等 GA 级硬化。

## 5. Slice 3 → GA 的最快研发路径（聚焦 2-3 个迭代，TDD 优先）

目标：把 Slice 3 从“能演示（MVP）”推进到“能长期维护 & 可放心扩展（GA）”。优先顺序遵循：可回归 > 可观测 > 可扩展。

现状（已具备）：

- 插件可在 Gateway 动态暴露为 `plugin.<id>`，并可通过 `plugins.list` / `plugins.run` 调用。
- 长任务可通过 `tasks.run_plugin_async` 启动，并在完成时通过 SSE 广播 `sros.task.completed` 通知。

一键回归入口（建议把它当成 Slice 3 的“金线”）：

```bash
pytest -q tests/integration/test_v3_slice3_plugins_and_tasks_gateway.py
```

### Iteration D：Plugin 工具化（让生态可“被调用”）

交付物（面向 Agent / MCP）：

- Gateway `tools/list` 能动态发现 `.sros/plugins/*.py` 并暴露为 `plugin.<id>`。
- `tools/call` 可直接调用 `plugin.<id>`，返回 JSON 可序列化结果。
- 插件可选提供 `SKILL_INPUT_SCHEMA`（JSON Schema），在 `tools/list` 中体现（便于 Agent 生成正确入参）。

验收标准（自动化）：

- `tools/list` 动态包含 `plugin.<id>`
- `tools/call` 可直接调用 `plugin.<id>` 并返回结构化结果
- 插件可选提供 `SKILL_INPUT_SCHEMA`，在 `tools/list` 中体现

最小约定（当前已支持）：

- 插件路径：`.sros/plugins/<id>.py`
- 元数据：`SKILL_NAME` / `SKILL_DESCRIPTION` / `SKILL_INPUT_SCHEMA`
- 入口：`def run(args: dict) -> Any`

GA 补强建议（下一步优先）：

- 插件命名约束：限定 `<id>` 只允许 `[a-z0-9_\-]`（避免奇怪路径/显示问题）
- 插件失败语义：统一错误 envelope（例如 `{ok:false,error:{code,message,details}}`），CLI/Gateway 一致
- 插件导入/执行隔离（最小可用）：异常不污染核心模块，错误信息可定位（含 `plugin_id`、`trace_id`/`task_id`）

### Iteration E：Long Task + Event Hook（让 Agent 可“被唤醒”）

交付物（面向 Agent / 编排）：

- `tasks.run_plugin_async` 可启动后台执行并返回 `task_id`
- `tasks.get/list/wait` 可查询并等待最终状态
- 完成时在 SSE 流中广播 `sros.task.completed` 通知（JSON-RPC notification）

验收标准（自动化）：

- `tasks.run_plugin_async` 返回 `task_id`
- 任务完成后在 SSE 流中收到 `sros.task.completed` 通知（JSON-RPC notification）
- `tasks.get/wait` 可稳定拿到最终状态（succeeded/failed）

GA 补强建议（下一步优先）：

- 事件订阅/路由：避免“全量广播”，至少支持按 session 订阅（或按 workspace 隔离）
- 资源治理：超时/取消/并发上限（避免任务堆积拖垮进程）
- 任务状态持久化（可选但推荐）：写入 `.sros/tasks.jsonl` 或 DuckDB 表（进程崩溃后可追溯）

### Iteration F：硬化与可维护性（GA 必备）

最小必做（推荐都落到自动化测试里）：

- 稳定错误语义：插件异常/任务失败在 CLI 与 Gateway 都有一致结构与错误码
- 可观测性：日志包含 `plugin_id` / `task_id` / `session_id`（至少能把一次失败串起来）
- 边界与回退：插件目录缺失/为空/包含坏文件时不影响核心工具可用性

可选（准备对外发布时再做）：

- 任务状态持久化：把任务结果写入 `.sros/`（例如 jsonl/duckdb 表）用于崩溃后排查
- 事件路由：支持按 session_id/订阅过滤，而不是全量广播

### Iteration G：Gateway 进程与端口治理（PID / status / stop / restart）

目标：解决“8000 端口占用但不知道是谁占的 / 同一工作区重复启动 / Zombie 进程残留”等日常痛点，让 SROS Gateway 具备类似 `docker` / `systemctl` 的自诊断与自启停能力。

交付物（面向用户 / Agent 的工程化能力）：

- 状态落盘：工作区写入 `.sros/gateway.pid`（JSON），包含 `pid` / `port` / `started_at`
- `sros status`：能判断端口占用者归属
  - 若 PID 文件存在且进程仍存活：显示 `RUNNING (Owned by this workspace)`
  - 若 PID 文件存在但进程已不存在：自动清理 PID 文件（Zombie 修复）
  - 若 PID 文件不存在但端口被占用：显示占用进程信息（尽力而为：name/pid）
- `sros start`：防呆 + 自适应
  - 同一工作区已运行：直接提示并退出（不再二次启动）
  - 端口被外部进程占用：提示占用者 + 给出 `--auto-port` / `-p` 建议
- 新命令：`sros stop` / `sros restart`
  - `stop`：按 PID 文件优雅退出（SIGTERM）→ 超时后强杀（SIGKILL），并清理 PID 文件
  - `restart`：组合 stop + start，便于 Agent 重置环境

验收标准（自动化 / 可回归）：

- 在临时工作区写入“存活 PID”的 `.sros/gateway.pid` 后，`sros start -w <ws>` 不会再次启动，并明确提示“已在本工作区运行”
- `.sros/gateway.pid` 指向不存在的 PID 时，`sros status`/`sros stop` 会清理 PID 文件
- `sros stop` 能终止一个由测试进程启动的“可控子进程”（用于验证 kill 逻辑）
- `sros status` 在端口被占用时能尽力输出占用者信息（至少区分：本工作区 / 外部进程 / 未知）

实现策略（保持最小入侵）：

- 依赖：引入 `psutil`（端口占用者识别 & 更稳的进程管理）
- Gateway：在 FastAPI `startup` 时写 PID 文件，在 `shutdown` 时清理（best-effort，不影响启动/关闭）
- CLI：把“端口占用诊断 + PID 文件归属判断 + stop/restart”封装到可测试的 utils

TDD 建议（先写测试再补实现）：

- 新增：`tests/unit/test_v3_gateway_process_governance.py`
  - `test_start_refuses_when_workspace_pid_alive`
  - `test_stop_cleans_zombie_pid_file`
  - `test_stop_terminates_spawned_process`
  - `test_status_cleans_zombie_pid_file`

开发者模式（可选，后置）：

- `sros start --reload`：开发时监听 `.sros/plugins/` 变更并热重启（需要 Uvicorn reload/watchfiles 支持；建议作为 `dev`/`extra` 能力单独开关）

实现入口（读代码从这里开始）：

- `src/sros/gateway/main.py`：SSE Hub、动态 `tools/list` 聚合、通知广播
- `src/sros/skills/rpc.py`：`tools/call` 分发（静态工具 + 动态插件 + tasks）
- `src/sros/utils/plugin_loader.py`：插件发现、元数据/Schema 解析
- `src/sros/utils/task_manager.py`：后台任务生命周期（start/get/list + 完成回调）
- `src/sros/servers/tasks/handler.py`：`tasks.*` RPC handler
- `src/sros/cli.py`：`sros start/status/stop/restart` CLI 入口

### Iteration H：CLI Compatibility / Agent UX Hardening（降低“报错即逃逸”概率）

动机：真实 Agent 执行里，最常见的失败不是能力缺失，而是 **命令/参数/target 名称不匹配**（例如把 `outline` 误写成 `get-outline-tree`、把 `sha256` 误写成 `get-file-sha256`、使用不存在的 `--position`、使用 `section:end` 作为插入目标）。这些“小摩擦”会显著提高 Agent 绕过 `sros-skill` 直接跑原生命令的概率，从而让图谱/溯源链路断裂。

交付物（最小兼容层，保持主语义不变）：

- 命令别名：
  - `sros-skill manuscript get-outline-tree` → 等价于 `outline`
  - `sros-skill manuscript get-file-sha256` → 等价于 `sha256`
- 插入兼容：
  - `--target section:end` / `section:append` 被识别为 `end`
  - `manuscript insert --position ...` 被接受但忽略（避免 hard fail）

验收标准（自动化 / 可回归）：

- 兼容别名命令在 `--raw` 模式下输出结构化 JSON 并 exit code = 0
- `manuscript insert --target section:end` 能成功追加写入
- `manuscript insert --position after ...` 不会因参数解析失败而退出

测试入口：

```bash
pytest -q tests/unit/test_v3_skills_cli_compatibility.py
```

## 6. MVP 端到端验收清单（本地可直接照做）

> 说明：`--raw` 是 `sros-skill` 的根选项，必须放在子命令前。

1) 初始化工作区

```bash
sros init <proj> --target both
```

2) 准备数据（放入任意 CSV）

```bash
cd <proj>
cp <your.csv> data/raw/sample_data.csv
```

3) 预览数据（机器可读 JSON）

```bash
sros-skill --raw data preview --file data/raw/sample_data.csv
```

4) 运行脚本（脚本需把图输出到 `figures/`）

```bash
SROS_WORKSPACE_DIR="$PWD" sros-skill --raw data run-script --script scripts/plot.py --dataset data/raw/sample_data.csv
```

5) 校验产物

- `figures/` 下出现新图表文件
- `.sros/graph.db` 的 `nodes/edges` 有增量写入（至少包含 Script/Figure 与 GENERATES）

6) 写回草稿（IDE 预览应可见）

```markdown
![my figure](figures/<file>)
```

7) 可选：把“图表在草稿中的位置”写回图谱（支持追问）

```bash
SROS_WORKSPACE_DIR="$PWD" sros-skill --raw manuscript index-figures --file draft.md
```

8) 可选：Slice 3（插件 + 长任务通知）

```bash
# 先放一个插件到工作区
mkdir -p .sros/plugins
cat > .sros/plugins/hello.py << 'EOF'
SKILL_NAME = "Hello"
SKILL_DESCRIPTION = "Return a greeting"

def run(args: dict): return {"greeting": f"hello {args.get('name', 'world')}"}
EOF

# 启动 Gateway（MCP SSE Hub）
sros start -w . -p 8000

# （本地直连 CLI）调用插件
SROS_WORKSPACE_DIR="$PWD" sros-skill --raw plugins run --name hello --args-json '{"name":"sros"}'

# （推荐）一键回归：验证 gateway tools/list 动态包含 plugin.<id>，并验证任务完成通知
pytest -q tests/integration/test_v3_slice3_plugins_and_tasks_gateway.py
```

9) 可选：全量回归（准备提测/发版前）

```bash
pytest -q
```

---

## 6.1 Slice 3（MVP）验收：回归入口（已覆盖）

目标：确保“插件动态工具 + 长任务 + 完成通知”在 Gateway 形态下可稳定回归。

```bash
pytest -q tests/integration/test_v3_slice3_plugins_and_tasks_gateway.py
```

## 6.2 Slice 3（GA）验收：必须补强的发布门槛（建议逐条落测试）

说明：以下是 **GA 发布门槛**。其中部分能力当前仍处于“建议/待实现”，这里先把验收标准固化，避免后续口径漂移。

1) 稳定错误语义（CLI 与 Gateway 一致）

- 插件异常 / 参数不合法 / 插件缺失等错误，返回统一 envelope：`{ok:false,error:{code,message,details}}`
- `tools/call` 与 `sros-skill --raw` 的错误字段一致（至少 code/message 可对齐）

建议测试：新增 `tests/integration/test_v3_slice3_error_envelope.py`

2) 插件命名与发现边界

- 插件 id 只允许 `[a-z0-9_\-]`；不合法文件名不会被暴露为 tool
- 插件目录缺失/为空/包含坏文件时：Gateway 仍可启动，核心工具仍可用

建议测试：新增 `tests/integration/test_v3_slice3_plugin_discovery_edge_cases.py`

3) 事件路由（避免全量广播）

- `sros.task.completed` 至少支持按 `session_id` 隔离（同一进程多会话互不干扰）

建议测试：扩展现有用例，覆盖“双 session 并发 + 只收自己的通知”

4) 资源治理（避免拖垮进程）

- 支持超时/取消（最小可用：取消后状态可见且不会继续执行）
- 并发上限可配置（默认值要安全）

建议测试：新增 `tests/integration/test_v3_slice3_task_limits.py`

5) 任务状态持久化（推荐，允许延后但需明确策略）

- 进程崩溃后仍可追溯：至少能查到 `task_id` 的最终状态/错误摘要（jsonl 或 DuckDB 表）

建议测试：新增 `tests/integration/test_v3_slice3_task_persistence.py`

## 7. 参考文档（把“长文分析”留在外部，保持本文可读）

- V3.0-Beta 端到端测试与操作指南：
  - [SROS V3.0-Beta 进展分析与端到端测试指南.md](SROS%20V3.0-Beta%20进展分析与端到端测试指南.md)
- 更细的架构/目录/迁移计划见 `plans/` 与 `doc/` 下对应文档（本文只保留可执行路线图）。

