# SROS V4.0 战略规划：泛科研通用操作系统与生态矩阵

> **文档角色**：SROS 主 PRD — 定义 WHY（战略愿景）和 WHAT（架构设计、领域规范、验收标准）。
> 实现级规格（HOW：CLI 契约、MCP tool schema、实现 checklist）→ `doc/PRD_SXMU_Data_Ingestion_HPC.md`。
> 进度追踪（WHEN + STATUS）→ `ROADMAP.md`。

## 0. 核心定位 (The Paradigm Shift)

SROS V3.0 是"让大模型可以在本地跑 Python 脚本的无头实验室"。V4.0 的目标是成为 AI4S (AI for Science) 领域的 "Linux/Docker"。

三个战略跃迁：

1. **底层重构 — 全面 MCP 化**：剥离 LangChain/AutoGen 框架控制流，全面拥抱 Claude Code + Model Context Protocol (MCP)。SROS 退化为提供高质量"系统调用"的 MCP Servers 集合。

2. **生态兼容 — 向下纳管**：统一纳管本地机器、HPC（Slurm 集群）、分布式数据库。将 graphmri、fMRIPrep 等垂直工具转化为标准化的 Apptainer 计算组件。

3. **数据血缘 — DuckDB 引擎**：彻底告别文件系统暴力扫描。所有被试信息、量表数据、文献图谱统一收敛至超高速内嵌数据库 DuckDB。

---

## 1. 架构设计：MCP 控制层与执行层分离

### 1.1 认知主控层 (The Brain)

Claude Code（或兼容 MCP 协议的 Agent 端）理解用户高层意图，自主制定计划，调用底层 SROS MCP Servers。

### 1.2 SROS 物理执行层 (MCP Servers 矩阵)

| Server | 封装对象 | MCP Tools |
|--------|---------|-----------|
| `sros-db-server` | DuckDB 数据摄入 + SQL 查询 | `db.ingest` / `db.query` |
| `sros-hpc-server` | Slurm 调度器 + OOM 自愈 + Apptainer | `hpc.submit` / `hpc.status` / `hpc.cancel` / `hpc.list` / `hpc.logs` |
| `sros-lit-server` | 文献 RAG、Zotero 同步、手稿生成 | 传承自 V3.0 MVP |
| `sros-neuro-server` | BIDS 验证、graphmri 脚本生成、fMRIPrep 管线编排 | `neuro.validate` / `neuro.generate_graphmri` / `neuro.generate_fmriprep` |

### 1.3 ARC Code-Wiki 架构图谱

SROS 与 ARC Engine 通过契约文件集成，使 LLM Agent 在修改代码前自动读取架构图谱：

- **契约文件**：`arc_wiki.json`（项目配置）+ `docs/code_schema.md`（SROS 特化提取规则）
- **编译器**：ARC `claw-code-ingest`，将 `src/sros/` 源码分析为 `docs/code_wiki/` 结构化 Markdown
- **激活机制**：CLAUDE.md 硬性规定 + Makefile `update-wiki` 目标 + CI Sidecar 双边检测

---

## 2. 核心生态包 (Skill Packs)

### 2.1 HPC-Pack — 破局物理执行力

**痛点**：超算中心禁止 sudo、禁止 Docker、限制 Wall-time、Lustre I/O 瓶颈。

**方案**：
- **沙盒化执行**：所有计算环境打包为 Apptainer (.sif) 镜像，SROS 负责挂载目录
- **智能 Job Array**：根据 DuckDB 中被试数量自动切分最优宽度的 Slurm Job Array
- **OOM 自愈**：自动监控 .err 日志，检测内存溢出 → 自动提升 `--mem` 重试（最多 3 次）

### 2.2 Neuro-Pack — 多模态队列分析

- **整合而非重写**：将 graphmri / fMRIPrep 视为"黑盒函数"，SROS 准备完美数据输入
- **DuckDB 表型对齐**：SQL JOIN 关联临床量表与 BIDS 目录树，避免 HPC I/O 风暴
- **端到端闭环**：fMRIPrep 预处理 → graphmri 图论提取 → Scikit-learn 统计 → Markdown 报告

### 2.3 Lit-Pack — 文献与知识合成闭环

- **泛在知识摄入**：自动读取非结构化材料（Deep Research 报告、网页剪报），提取核心观点
- **Zotero 同步**：通过 citekey 和 DOI 确保系统内知识与外部文献库的硬关联
- **RAG 草稿重构**：生成 Markdown 手稿时强制校验引用合法性，防止幻觉

### 2.4 SDK-Pack — AI4S DSL 科学编译器

在 SROS/GraphMRI 底盘之上构建声明式 DSL 抽象层，让科学家用 Fluent API 表达科学意图：

```python
from sros.brain import BrainGraphDataset
from sros.ml import GNNTrainer

result = (
    GNNTrainer(
        BrainGraphDataset
        .from_duckdb("SELECT * FROM mdd_cohort WHERE intervention_type='dTMS'")
        .apply_pipeline("fmriprep", resolution="2mm")
        .extract_connectome(atlas="aal", kind="correlation")
        .compute()
    )
    .train(model="GraphSAGE", target="HAMD_improvement_pct", infra_strategy="auto")
)
```

**核心组件**：
- `BrainGraphDataset` — 链式调用：from_duckdb → apply_pipeline → extract_connectome → compute → to_dataloader
- `GNNTrainer` — GNN 训练器，`infra_strategy="auto"` 自动侦测 Slurm / GPU / CPU
- DuckDB 连接器 — SQL → 被试列表，自动列映射推断（中英文双语）
- DSPy 断言 — 对称正定矩阵硬断言 + gradient checkpointing 软建议

**首期范围**：SXMU_MDD 项目，封装 GraphMRI-Lite 已验证的核心算法。

---

## 3. 验收标准

### 3.1 基础设施 ✅

- [x] 至少两个 MCP Server 可独立运行：`sros-db-server` + `sros-hpc-server`
- [x] Claude Code 可通过自然语言提交 Slurm Job Array 并轮询 COMPLETED 状态

### 3.2 领域能力 ✅

- [x] 数千例被试 participants.tsv + BIDS 路径树成功 ingest 进入 DuckDB
- [x] 自然语言筛选队列 → 生成 fMRIPrep Slurm 批处理脚本（不引起 I/O 阻塞）
- [x] S1–S7 + DSL-1–DSL-6 + FS-1 全部交付（详见 ROADMAP.md）

### 3.3 文献合成 ✅

- [x] MVP 全链路技能面（ext / zotero-sync / rag / manuscript.refactor）
- [x] draft.md Related Work 包含 [@citekey]，所有引用在 DuckDB 中存在合法 CITES 关系边

### 3.4 待完成

- [ ] ARC CI 契约测试（ARC-Engine 侧执行提案）
- [ ] Hermes H1H2 框架验证（Hermes-Workflows 侧执行提案）
- [ ] AgenticOps 遥测集成（AgenticOps 仓库就绪后集成）
- [ ] TypeScript SDK / 分布式 DuckDB（P3，远期规划）

---

## 4. CLI 结构化终端输出

SROS CLI 采用 Python Rich 库实现结构化视觉反馈：

| 命令 | 输出形式 |
|------|---------|
| `sros start` | 启动自检 Panel：工作区路径、端口绑定、MCP 配置更新、Scholar 后端模式 |
| `sros db ingest` | 长时间 spinner + 完成摘要 Panel（成功/跳过/失败计数，各表写入行数） |
| `sros doctor` | 按子系统分组 Panel + 嵌套 Table + 色彩编码（绿/黄/红） |

**输出契约**：
- `--raw` 模式：stdout=JSON，不受视觉增强影响
- 默认（TTY）：Rich 渲染，stderr 保留原始日志流
- 非 TTY（管道/重定向）：自动降级为纯文本

---

## 5. DevX 混合架构基础设施

### 5.1 SLAIB Git 流

`main` 分支写保护，所有修改通过 `feat/` / `fix/` / `refactor/` 分支 → PR → Squash & Merge。规则已落地至 `CLAUDE.md`。

### 5.2 跨项目契约验证

- **ARC CI 契约测试**：ARC-Engine 侧 CI 拉取 SROS 契约文件快照验证编译（提案已交付）
- **Hermes MCP 挂载**：Hermes-Workflows 通过 SSE 挂载 SROS MCP Gateway（提案已交付）

### 5.3 双通道运行环境

- 交互式终端 (Tmux)：完整 Claude Code 对话界面，别名 `cauto` / `cdo`
- 非交互式飞书桥接：systemd 守护的 `lark-channel-bridge`

详细部署指南：`docs/DevX-GitHub-Branch-Protection.md` / `docs/DevX-Systemd-Bridge-Setup.md`

### 5.4 飞书多维表格控制平面

飞书多维表格作为 GraphMRI-Lite 任务提交与监控界面：

```
SXMU 团队 → 飞书多维表格填一行 → 状态改为"请求执行"
  → 飞书自动化 Webhook → SROS POST /webhook/execute
  → 字段翻译（中英双语） → BackgroundTasks → GraphMRI-Lite /api/jobs/submit
  → 任务完成后 GraphMRI-Lite FeishuClient 回写结果到同一行
```

**SROS 侧交付**：`src/sros/gateway/webhook.py` — `POST /webhook/execute` 端点，202 即时响应，超时/连接错误安全处理。20 个单元测试全部通过。

**飞书《SXMU 组学分析工作台》表格结构**：项目 / 分析类型 / 被试筛选SQL / 图谱 / 模型 / 预测目标 / 状态 / 结果链接（自动回写）

### 5.5 AgenticOps 遥测集成（前瞻）

SROS MCP Gateway 后续迭代中将增加遥测中间件，向 AgenticOps Dashboard 上报 MCP tool 调用次数/成功率/延迟。非侵入式 FastAPI middleware，不修改业务逻辑。

---

## 6. sros-sdk 验收标准

### 6.1 骨架与导入 ✅
- [x] `sros-sdk/` 目录骨架就绪，`pyproject.toml` 可解析
- [x] `from sros.brain import BrainGraphDataset` / `from sros.ml import GNNTrainer` 导入成功

### 6.2 BrainGraphDataset ✅
- [x] `from_duckdb(query)` 执行 SQL 返回被试列表
- [x] `from_bids(bids_dir)` 扫描 BIDS 目录
- [x] `.apply_pipeline()` / `.extract_connectome()` / `.to_dataloader()` 链式调用
- [x] DSL 链式调用可脱离 Jupyter 在纯 Python 脚本中运行

### 6.3 GNNTrainer ✅
- [x] `train(model, target, infra_strategy="auto")` 成功启动训练
- [x] `infra_strategy="auto"` 正确侦测 Slurm / GPU / Docker / CPU
- [x] 回归/分类自动检测分发（continuous labels → RandomForestRegressor）

### 6.4 DSPy 断言 ✅
- [x] 对称正定矩阵硬断言（demo compute 模式生成合法 SPD 矩阵）
- [x] `suggest_gradient_checkpointing()` 软建议（>1GB 模型触发）

### 6.5 测试 ✅
- [x] `test_brain_dataset.py` (14) / `test_trainer.py` (12) / `test_duckdb_connector.py` (8)
- [x] `test_dsl6_e2e.py` (23) — SXMU_MDD dTMS 106 例全链路回归
- [x] `examples/sxmu_mdd_dtms_e2e.ipynb` — 10-cell Jupyter notebook
- [x] `test_webhook.py` (20) — 飞书 Webhook 端点

---

## 7. MCP-to-OpenAI Adapter — 模型无关的协议翻译层 (V4.2)

> 交付日期：2026-06-16 | 任务：MCP-Adapter ✅ | 测试：10 tests green

SROS MCP Gateway 原生输出 JSON-RPC 格式。为使 DeepSeek v4 Pro 等 OpenAI 兼容 API 的模型也能调用 SROS 工具，新增协议翻译层：

- `mcp_tools_to_openai()`: MCP tools/list → OpenAI Function Calling `[{type: "function", function: {name, description, parameters}}]`
- `openai_tool_call_to_mcp()`: OpenAI tool_call 响应 → MCP tools/call 参数
- `build_deepseek_request()`: 构建完整 DeepSeek API 请求体

**Gateway 端点**:
- `GET /api/v1/mcp/openai-tools` — 返回 OpenAI Function Calling 兼容格式的工具列表
- `POST /api/v1/mcp/call-openai` — 接收 OpenAI tool_call，内部转换为 JSON-RPC 并分发

**位置**: `src/sros/gateway/mcp_openai_adapter.py` | `tests/unit/test_mcp_openai_adapter.py` (10 tests)

## 8. 总结：系统哲学的升维

放弃开发内置 LangChain 路由的 Python 巨石应用。

拥抱 **"Claude Code (主观能动性) + SROS MCP Servers (客观物理规律)"**。

SROS 将成为连接大模型顶级认知能力与真实世界复杂算力（HPC、海量临床数据）之间的最强操作系统基座。
