# SROS V3.0-Beta 进展分析与端到端测试指南

> 最后更新：2026-03-17
>
> 本文目标：给你一条“从 0 到可回归”的最短路径。
> - Beta 核心：数据闭环 + 最小溯源链（DuckDB 图谱）
> - 可选：Slice 3 插件生态 + 长任务完成通知（用于唤醒 Agent 继续写作）

## 0. 安装与升级（是否需要重新安装 SROS？）

### 0.1 是否需要重新安装？（结论先说）

- 如果你在本仓库用了 **editable 安装**（推荐）：`python -m pip install -e .`（或 `-e ".[test]"`）
  - 一般 **不需要重新安装**：拉取/修改代码后，CLI 会直接运行最新源码。
  - 但如果你改了依赖或入口（`pyproject.toml` 的 dependencies / scripts），建议重新跑一次安装命令以刷新依赖/entry_points。
- 如果你是 **非 editable 安装**（例如 `pip install sros` 或安装了 wheel）：更新仓库源码不会生效，需要重新安装（`pip install -U sros` 或切换到本仓库 `pip install -e .`）。

### 0.2 推荐安装方式（开发/跑测试）

在本仓库根目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install -U pip

# 需要跑 pytest / 集成测试推荐装 test extra
python -m pip install -e ".[test]"
```

### 0.3 快速自检（确认 CLI 可用）

```bash
sros --help
sros-skill --help
python -c "import sros; print('sros version:', sros.__version__)"
python -m pip show sros | sed -n '1,12p'
```

常见问题：

- 找不到命令：确认激活了虚拟环境（`which python` / `which sros` 指向 `.venv/`）
- 依赖缺失：重新运行 `python -m pip install -e ".[test]"`
- 端口 8000 被占用：
  - 先运行 `sros status` 查看占用者
  - 若你确认占用者是残留的 SROS 进程但当前工作区没有 `.sros/gateway.pid`，可使用：`sros stop --kill-port-owner -p 8000`

版本说明：

- 你看到的 `sros.__version__` / `pip show sros` 是 **Python 包版本**。
- V3.0-Beta 阶段建议使用 `3.0.0b*`（beta 预发布）语义；仓库内历史文档可能仍沿用 2.x 版本号，这不影响使用，但以本指南与 `pyproject.toml` 为准。

### 0.4 升级 / 重装速查

```bash
# 你在本仓库开发（editable 安装）时：拉代码后通常无需重装；
# 但如果依赖/入口脚本变了，建议刷新一次安装（会同步依赖）。
python -m pip install -e ".[test]" -U

# 你之前是 pip 安装的已发布包（非 editable）时：升级需要重新安装
python -m pip install -U sros
```

依赖说明：本项目以 `pyproject.toml` 为依赖单一事实来源；`requirements.txt` 仅用于极简场景，不保证覆盖全部运行依赖。

现在起：仓库根目录的 `requirements.txt` 由 `pyproject.toml` 自动导出生成。

```bash
python scripts/export_requirements.py --output requirements.txt
```

## 1. 当前进展深度分析：真正的“无头实验室 (Headless Lab)”已上线

根据 MVP 测试结果，SROS 已经实现《V3.0 战略规划》中定义的 Phase 2（突破纯文本 —— 数据、计算与全息图谱）。这具有以下几个架构意义：

### 1.1 “黄金主线”的维度扩张 (From Text to Modality)

之前的 SROS 只能处理文本（Gap → 找论文 → 插入文字）。现在的 SROS 具备处理“物质/数据”的能力（CSV 数据 → 运算 → 图表 → 插入稿件）。这条扩展后的黄金主线，让 SROS 覆盖了科研的核心中段——“实验与分析”。

### 1.2 异构图谱的觉醒 (Heterogeneous Provenance Graph)

测试日志中提到 Script 节点、Figure 节点和 `GENERATES` 边已成功写入 DuckDB。这是复现性痛点的关键解法：数据血缘追踪（Data Provenance）。

SROS 会在底层账本清晰记录：

- 这篇文章里的图 B，由脚本 A 基于数据集 C 生成

### 1.3 `sros-skill` 确立了最佳的 Agent UI 形态

- `data.preview`：返回行列信息/样本/空值统计等
- `data.run-script`：自动拦截产物并落盘 + 写入图谱

证明了“把复杂环境操作封装成原子化 CLI Skill”是正确路线：Agent 只需要调用这些稳定命令，就能无痛完成复杂科研任务。

## 2. 基于 Claude Code 的端到端（E2E）测试指南

为了验证数据闭环，我们让 Claude Code 扮演“双手”，SROS 扮演“实验室”。

### 2.1 准备工作区

> 提示：本指南默认使用 `sros-skill` 作为 CLI 技能入口（来自 `pyproject.toml` 的 `project.scripts`）。

```bash
# 1) 创建并初始化 V3.0 工作区（推荐同时生成 Roo/Claude 配置）
sros init e2e-data-test --target both
cd e2e-data-test

# 2) 强绑定当前工作区（推荐）
export SROS_WORKSPACE_DIR="$PWD"
```

### 2.2 准备 mock 数据（模拟真实 raw 数据）

```bash
mkdir -p data/raw

cat > data/raw/experiment_scores.csv <<'EOF'
subject_id,group,score
sub-01,control,85
sub-02,control,88
sub-03,treatment,95
sub-04,treatment,92
sub-05,control,82
sub-06,treatment,98
EOF
```

### 2.3 唤醒 Claude Code 并注入系统提示

在 `e2e-data-test` 目录下启动 Claude Code（如果 `sros init` 生成了 `.clauderc`，Claude Code 启动会自动加载 SROS 的技能说明）：

```bash
claude
```

### 2.4 输入“魔法指令（Golden Prompt）”

把下面整段粘贴到 Claude Code：

```text
你是一个数据分析师。请按照以下步骤操作：

1) 使用 sros-skill 预览 data/raw/experiment_scores.csv 的数据结构。
命令：sros-skill --raw data preview --file data/raw/experiment_scores.csv

2) 编写一个 Python 脚本（保存到 scripts/plot_scores.py），使用 matplotlib 绘制 control 和 treatment 两组的 score 箱线图（boxplot），并将图片保存到 figures/ 目录（例如 figures/scores_boxplot.png）。

3) 使用 sros-skill 执行这个脚本。
命令：sros-skill --raw data run-script --script scripts/plot_scores.py --dataset data/raw/experiment_scores.csv

4) 最后使用 sros-skill manuscript insert，把实验结论和生成的图表路径写入到 draft.md 末尾（比如新建一个 Results 章节）。

5)（可选但推荐）运行 figure 引用索引，把“图表出现在稿件哪里”写回图谱。
命令：sros-skill --raw manuscript index-figures --file draft.md
```

### 2.5 观察 Agent 的“自动驾驶”过程（你应该看到什么）

- `sros-skill --raw data preview ...` 返回列名、样本、空值等
- Claude 自动写入 `scripts/plot_scores.py`
- `sros-skill --raw data run-script ...` 执行脚本，检测 `figures/` 新增图片并写入图谱
- `sros-skill manuscript insert ...` 把结论与图片引用写入 `draft.md`

### 2.6 验证闭环产物（Verification Checklist）

✅ 1) 检查文件树（Workspace）

你应该看到：

```text
e2e-data-test/
├── scripts/plot_scores.py
└── figures/<some_figure>.png
```

✅ 2) 检查稿件（draft.md）

打开 `draft.md`，应包含类似：

```markdown
## Results
实验数据分析表明，Treatment 组的得分显著高于 Control 组。详情如下图所示：
![Scores Boxplot](figures/<some_figure>.png)
```

✅ 3) 检查全息图谱（DuckDB）

用 Python here-doc 验证血缘关系（避免 shell 转义痛苦）：

```bash
python - <<'PY'
import duckdb

con = duckdb.connect('.sros/graph.db')

print('GENERATES edges:')
print(con.execute("SELECT * FROM edges WHERE relationship = 'GENERATES'").df())

print('ANALYZES edges:')
print(con.execute("SELECT * FROM edges WHERE relationship = 'ANALYZES'").df())
PY
```

预期：

- `GENERATES`：看到从 `scripts/plot_scores.py` 指向 `figures/...png` 的记录
- `ANALYZES`：看到从 `scripts/plot_scores.py` 指向 `data/raw/experiment_scores.csv` 的记录

（可选）如果执行了 `manuscript index-figures`，还应能查到 `REFERENCED_IN`：

```bash
python - <<'PY'
import duckdb

con = duckdb.connect('.sros/graph.db')
print(con.execute("SELECT * FROM edges WHERE relationship = 'REFERENCED_IN'").df())
PY
```

## 3.（可选）Slice 3：插件生态与长任务事件钩子验证

目标：验证 Phase 3 的两件事：

- 插件能被 Gateway 动态暴露为第一类 MCP 工具（`plugin.<id>`）
- 长耗时任务完成后，通过 Gateway SSE 发出 `sros.task.completed` 通知，用于“唤醒 Agent 继续写作”

### 3.1 准备一个最小插件

```bash
mkdir -p .sros/plugins

cat > .sros/plugins/hello.py <<'EOF'
SKILL_NAME = "Hello"
SKILL_DESCRIPTION = "A minimal demo plugin"
SKILL_INPUT_SCHEMA = {
  "type": "object",
  "properties": {"name": {"type": "string"}},
  "additionalProperties": False
}

# 单行函数：避免文档复制时缩进/Tab 混入导致 IndentationError
def run(args: dict): return {"greeting": f"hello {args.get('name', 'world')}"}
EOF
```

### 3.2 本地直连验证（不经过 Gateway）

```bash
export SROS_WORKSPACE_DIR="$PWD"

sros-skill --raw plugins list
sros-skill --raw plugins run --name hello --args-json '{"name":"sros"}'
```

### 3.3 Gateway / MCP 验证：`tools/list` 出现 `plugin.hello`

启动 Gateway：

```bash
sros start -w . -p 8000
```

然后用 HTTP JSON-RPC 检查 `tools/list`（说明：本实现同时支持对 `/sse` 进行 POST 的同步请求，便于 curl 快速验证）：

```bash
curl -s -X POST http://localhost:8000/sse \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
| python - <<'PY'
import sys, json
d = json.load(sys.stdin)
tools = d["result"]["tools"]
print([t["name"] for t in tools if t["name"].startswith("plugin.")])
PY
```

也可以直接 `tools/call` 调用插件（无需 `plugins.run`）：

```bash
curl -s -X POST http://localhost:8000/sse \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"plugin.hello","arguments":{"name":"sros"}}}' \
| python -m json.tool
```

补充说明（如果你在对接标准 MCP SSE transport）：

- `GET /sse` 会返回一个 `endpoint` event，其中包含 `/messages?session_id=...`
- MCP client（例如 `mcp.client.sse.sse_client`）会把后续 JSON-RPC POST 到该 `/messages` 地址

### 3.4 长任务通知（最稳妥的自动化验证）

长任务通知牵涉 SSE 会话/流式消费，最推荐用回归测试一键验证：

```bash
pytest -q tests/integration/test_v3_slice3_plugins_and_tasks_gateway.py
```

## 4. 下一步迭代建议（Towards V3.0-GA）

当上述 E2E 流程能够 100% 稳定跑通后，SROS 的骨架就已经大成。下一步建议切入 Phase 3（插件系统与垂直领域扩展），并把“可验收的最小生态”作为 GA 目标：

- 固化自动化集成测试：把关键流程都落到 pytest（不需要外接真实 Claude API）
- 研发 Pack MVP：把常用分析脚本封装为 `.sros/plugins/*.py`，提供 `SKILL_INPUT_SCHEMA` 让 Gateway 暴露 `plugin.<id>`，再用 `tasks.run_plugin_async` 升级为可通知的长任务（完成后触发 `sros.task.completed`）