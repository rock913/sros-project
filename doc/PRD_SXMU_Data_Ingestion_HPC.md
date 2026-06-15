# SROS SXMU 数据摄入与 HPC 调度 PRD v1.0

> 主 PRD：`doc/SROS_V4.0.md` — SROS V4.0 战略规划
> 上游：`meta-docs/SROS-ARC 协同开发 PRD v1.0.md` 附录 A
> 定位：SROS V4.0 的 SXMU 驱动特性 PRD — 将 V4.0 战略中的 `sros-db-server` + `sros-hpc-server` 具象化为 SXMU 项目可执行的开发任务
> 依赖：总 PRD Phase 1–5 基础设施就位后，本 PRD 方可全面执行

## 1. 背景

SXMU_MDD 数字孪生项目的 5 阶段工作流中，SROS 负责 L1 原子工具层：

| 阶段 | SROS 职责 | 当前状态 |
|------|----------|---------|
| 1. 数据底座 | BIDS + 临床数据 → DuckDB 摄入 | **不存在** |
| 4. 算力执行 | HPC Slurm 作业提交/监控/取消 | **不存在** |
| 5. 增量更新 | 特征元数据写回 DuckDB | **不存在** |

SROS V3.0.0b1 当前是"写作 OS"（文稿闭环 + 文献搜索 + 知识图谱 + RAG），不具备数据摄入和 HPC 调度能力。V4.0 战略已规划 `sros-db-server` 和 `sros-hpc-server`，但未实施。

## 2. 交付物

### Task S1: `sros db ingest` — 结构化数据摄入

**目标**：一键将 BIDS 目录 + participants.tsv + 临床 Excel 压入 DuckDB。

```bash
sros db ingest --source /lustre/.../SXMU_Data \
  --bids-dir MRI/Bids_data \
  --participants participants.tsv \
  --clinical clinical_scales.xlsx \
  --db sxmu.duckdb
```

**子任务**：
- S1.1: BIDS 目录解析器 — 遍历 `sub-*/ses-*/` 结构，提取文件路径和元数据
- S1.2: participants.tsv 读取器 — 被试人口学信息 → `subjects` 表
- S1.3: 临床量表 Excel 读取器 — HAMD/CTQ/RBANS 等 → `clinical_scales` 表
- S1.4: DuckDB schema 初始化 — 使用 `config/duckdb/schema.sql`（8 表 DDL）
- S1.5: CLI 入口 `sros db ingest` + MCP tool 注册

**DuckDB 目标表**（来自 SXMU 项目的 `config/duckdb/schema.sql`）：
`subjects`, `mri_scans`, `clinical_scales`, `eeg_records`, `interventions`, `omics_data`, `exposome`, `brain_features`

### Task S2: `sros-hpc-server` MCP — Slurm 作业管理

**目标**：通过 MCP 协议向交我算 Pi 2.0 提交和监控 Slurm 作业。

**暴露的 MCP Tools**：

| Tool | 功能 | Slurm 命令 |
|------|------|-----------|
| `sros-hpc-submit` | 提交作业 | `sbatch` |
| `sros-hpc-status` | 查询作业状态 | `squeue -j <id>` |
| `sros-hpc-cancel` | 取消作业 | `scancel <id>` |
| `sros-hpc-list` | 列出用户所有作业 | `squeue -u <user>` |
| `sros-hpc-logs` | 获取作业输出/错误 | 读取 `.out`/`.err` 文件 |

**子任务**：
- S2.1: Slurm 命令包装器 — Python subprocess 调用 sbatch/squeue/scancel
- S2.2: 作业数组生成 — 从被试列表批量生成 Slurm 作业
- S2.3: Apptainer 集成 — 自动 `module load apptainer` + bind mount
- S2.4: OOM 自愈重试 — 检测 OOM 错误，自动以更高 `--mem` 重试（最多 3 次）
- S2.5: MCP Server 实现 + MCP Gateway 注册

### Task S3: `sros db query` — DuckDB SQL 查询 MCP 工具

**目标**：通过 MCP 暴露 DuckDB 结构化查询能力。

```bash
sros db query "SELECT s.*, m.bids_path FROM subjects s JOIN mri_scans m ON s.subject_id = m.subject_id WHERE s.group_status = 'dTMS'"
```

**子任务**：
- S3.1: SQL 查询 CLI 入口
- S3.2: 结果集 JSON 序列化（支持分页）
- S3.3: MCP tool 注册为 `sros-db-query`

## 3. 接口契约

### 与 ARC 的契约
- SROS 写入 DuckDB 的表 schema 必须与 ARC Data-Wiki 编译器期望的 schema 一致
- Schema 版本化在 `config/duckdb/schema.sql`，变更通过 PR 通知 ARC 侧

### 与 Hermes 的契约
- `sros-hpc-submit` 返回 JSON 格式的 job_id 和预估完成时间
- `sros-hpc-status` 返回标准化的作业状态枚举（PENDING/RUNNING/COMPLETED/FAILED/CANCELLED）

## 4. 验收标准

- [ ] `sros db ingest` 可解析 SXMU BIDS 目录并填充 8 张 DuckDB 表
- [ ] `sros-hpc-submit` 可向交我算提交作业并返回 job_id
- [ ] `sros-hpc-status` 可查询作业状态并返回标准化 JSON
- [ ] `sros db query` 可通过 MCP 执行任意 SELECT 查询
- [ ] OOM 自愈重试：Slurm 作业因 OOM 失败时自动以 2x 内存重试
