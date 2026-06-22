> 本文档从 Meta 层 proposal 下沉而来。原文件：meta-docs/proposals/delivered/SROS-SXMU-Update.md。下沉日期：2026-06-21。

# SROS PRD 更新提案：SXMU_MDD 驱动的数据摄入与 HPC 调度能力

> 目标主 PRD：`01-Core_Infra/SROS/doc/SROS_V4.0.md`
> 提案日期：2026-05-12
> 驱动来源：SXMU_MDD 数字孪生协同作战规划 + 总 PRD 附录 A
> 状态：已交付 (2026-05-12 整合至 SROS_V4.0.md + ROADMAP.md)

## 动机 (Why)

SROS V4.0 已规划 `sros-db-server` 和 `sros-hpc-server` 两个 MCP Server 的战略方向，但停留在概念层。SXMU_MDD 项目提供了首个具体使用场景：

1. **数据摄入**：5.3TB 多模态数据（MRI BIDS + DICOM + EEG + 临床量表）需结构化导入 DuckDB
2. **HPC 调度**：106 例 dTMS 的 fMRIPrep/QSIPrep/GraphMRI 需要批量 Slurm 提交
3. **SQL 查询**：研究者需通过 MCP 协议对 DuckDB 执行跨表 JOIN 查询

这三个需求恰好对应 V4.0 战略中的三个 MCP Server，是 V4.0 从概念到投产的最佳 MVP。

## 提议新增/修改的章节

### 建议在 SROS_V4.0.md 第 1.2 节（SROS 物理执行层）中扩写

当前描述：
```
sros-db-server：封装 DuckDB，提供大模型友好的 SQL 交互...
sros-hpc-server：封装 Slurm 调度器...
```

建议替换为以下具象规格（保持原战略方向，增加实现细节）：

---

#### sros-db-server — 数据摄入 + SQL 查询

**数据摄入 CLI**：
```bash
sros db ingest --source /lustre/.../SXMU_Data \
  --bids-dir MRI/Bids_data \
  --participants participants.tsv \
  --clinical clinical_scales.xlsx \
  --db sxmu.duckdb
```

**摄入流程**：
1. 解析 `participants.tsv` → DuckDB `subjects` 表
2. 遍历 BIDS 目录树 `sub-*/ses-*/` → `mri_scans` 表
3. 读取临床 Excel（HAMD/CTQ/RBANS 等）→ `clinical_scales` 表
4. 使用 `config/duckdb/schema.sql`（8 表 DDL，已在 SXMU 项目中定义）初始化 schema

**SQL 查询 MCP Tool**：
```json
{
  "tool": "sros-db-query",
  "input": {"sql": "SELECT s.*, m.bids_path FROM subjects s JOIN mri_scans m ON s.subject_id = m.subject_id WHERE s.group_status = 'dTMS'"},
  "output": {"ok": true, "rows": [...], "count": 106}
}
```

---

#### sros-hpc-server — Slurm 作业管理

**MCP Tools**：

| Tool | Slurm 命令 | 输入 | 输出 |
|------|-----------|------|------|
| `sros-hpc-submit` | `sbatch` | script_path, array_size | `{job_id, estimated_completion}` |
| `sros-hpc-status` | `squeue -j <id>` | job_id | `{state: PENDING\|RUNNING\|COMPLETED\|FAILED, elapsed, ...}` |
| `sros-hpc-cancel` | `scancel` | job_id | `{cancelled: true}` |
| `sros-hpc-list` | `squeue -u <user>` | — | `[{job_id, name, state, ...}]` |

**OOM 自愈策略**（来自 V4.0 第 2.1 节已有描述，建议增加实现细节）：
- 监控 `.err` 日志检测 `oom-kill` / `OutOfMemoryError`
- 自动以 2x `--mem` 重试（最多 3 次）
- 首次 16G → 32G → 48G → 标记 `FAILED_OOM` 并通知

**Apptainer 集成**（来自 V4.0 第 2.1 节，建议增加模板路径引用）：
- 使用 SXMU 项目中的 `config/slurm/fmriprep_template.slurm`、`qsiprep_template.slurm`、`graphmri_template.slurm`
- Slurm 模板变量 `{SUBJECT}` 由 HPC Server 自动替换

---

### 建议在 V4.0 第 3 节（验收标准）中新增 Phase 1 子项

```markdown
[ ] sros db ingest 可解析 SXMU BIDS 目录 + participants.tsv + 临床 Excel → 填充 8 张 DuckDB 表
[ ] sros-hpc-submit 可向交我算 Pi 2.0 提交 Slurm 作业并返回 job_id
[ ] sros-hpc-status 可查询作业状态并返回标准化 JSON
[ ] OOM 自愈：Slurm 作业因 OOM 失败时自动以 2x 内存重试
[ ] sros-db-query 可通过 MCP 执行任意 SELECT 查询并返回 JSON 结果集
```

## 验收标准

- [x] SROS_V4.0.md 第 1.2 节中 `sros-db-server` 和 `sros-hpc-server` 的描述已扩写为具象规格
- [x] SROS_V4.0.md 第 3 节验收标准中新增了上述 5 个 checklist 项
- [x] SROS ROADMAP.md 中新增了 S1/S2/S3 任务（如尚未创建 ROADMAP.md，需一并创建）

## 参考实现 (Don't Guess, Copy)

| 模式 | 路径 | 可复用点 |
|------|------|---------|
| MCP Server 架构 | `01-Core_Infra/SROS/src/sros/gateway/main.py` | FastAPI + SSE transport + tool registration 模式 |
| DuckDB 集成 | `01-Core_Infra/SROS/src/sros/servers/memory/handler.py` | DuckDB 连接、建表、JSON 序列化 |
| CLI 入口模式 | `01-Core_Infra/SROS/src/sros/skills/cli.py` | typer + sub-command groups |
| Plugin 动态发现 | `01-Core_Infra/SROS/src/sros/plugins/` | `.sros/plugins/*.py` 动态加载 |
| Subprocess 包装 | `01-Core_Infra/SROS/src/sros/skills/data/handler.py` 中的 `run-script` | subprocess.run + 输出捕获 |
