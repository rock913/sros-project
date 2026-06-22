> 本文档从 Meta 层 proposal 下沉而来。原文件：meta-docs/proposals/delivered/SROS-DSL6-SXMU-E2E.md。下沉日期：2026-06-21。

# SROS PRD 更新提案：DSL-6 — SXMU_MDD dTMS 106 例 E2E 验证

> 目标主 PRD：`01-Core_Infra/SROS/doc/SROS_V4.0.md`
> 提案日期：2026-06-01
> 驱动来源：总 PRD Phase 9 — DSL-6 (SXMU_MDD E2E)，前置 DSL-3+DSL-4+DSL-5 ✅ 已全部满足

## 动机 (Why)

sros-sdk DSL-1~DSL-5 已全部交付：
- DSL-1: sros-sdk 仓库骨架 ✅
- DSL-2: `BrainGraphDataset` Fluent API ✅
- DSL-3: `GNNTrainer` (GraphSAGE/GAT/GCN + `infra_strategy="auto"`) ✅
- DSL-4: DuckDB 连接器 (`from_duckdb()` 列映射推断) ✅
- DSL-5: DSPy 断言嵌入 (对称正定 + gradient checkpointing) ✅

但 DSL 的最终验证标准不是单元测试，而是**在真实 SXMU_MDD 数据上跑通 GNN 训练的端到端链路**。DSL-6 是 sros-sdk 从"可用的 SDK"到"已验证的科学编译器"的关键一步。

**前置条件全部满足**：GraphMRI-Lite CLI `--raw` JSON contract 稳定，DuckDB 连接器就绪，GNNTrainer 就绪。DSL-6 无需任何新基础设施，纯整合验证。

## 提议内容

### 编写 Jupyter Notebook: `sros-sdk/examples/sxmu_mdd_dtms_e2e.ipynb`

用 DSL 重写 dTMS 106 例 GNN 训练管线，完整覆盖 4 个步骤：

```python
# Step 1: 从 DuckDB 加载 dTMS 106 例队列
from sros.brain import BrainGraphDataset

cohort = (
    BrainGraphDataset
    .from_duckdb(
        "SELECT * FROM mdd_cohort WHERE intervention_type = 'dTMS'",
        db_path="/data/sxmu_mdd/duckdb/mdd_twin.db"
    )
    # 等价于：106 例被试，每例含 pre/post T1 + DTI + rs-fMRI
)
print(f"Cohort size: {len(cohort)} subjects")  # 预期：106

# Step 2: 应用预处理管线
cohort = cohort.apply_pipeline(
    "fmriprep",
    resolution="2mm",
    output_dir="/data/sxmu_mdd/derivatives/dsl_test"
)
# 等价于：对 106 例逐例调用 graphmri --raw preprocess

# Step 3: 提取脑网络连接矩阵
cohort = cohort.extract_connectome(
    atlas="aal",          # AAL 116 区脑图谱
    kind="correlation",   # 皮尔逊相关矩阵
    vectorize=True        # 上三角向量化 → ML 特征
)
# DSPy 硬断言：每个连接矩阵必须对称正定

# Step 4: 训练 GNN 预测 HAMD 改善率
from sros.ml import GNNTrainer

trainer = GNNTrainer(cohort)
results = trainer.train(
    model="GraphSAGE",
    target="HAMD_improvement_pct",  # 治疗后 HAMD 改善百分比
    infra_strategy="auto",          # 自动检测 GPU/Slurm
    epochs=100,
    k_fold=5
)

print(f"Test R²: {results.test_r2:.3f}")
print(f"Test MAE: {results.test_mae:.2f}%")
```

### DSL 链路完整性验证

| 链式调用 | 底层实际调用 | 验证点 |
|----------|------------|--------|
| `.from_duckdb()` | SROS DuckDB connector → SQL → subject list | 106 例被试完整加载 |
| `.apply_pipeline("fmriprep")` | `graphmri --raw preprocess` (per-subject) | JSON stdout contract 正常 |
| `.extract_connectome(atlas="aal")` | `graphmri --raw build-network` (per-subject) | 输出 116×116 对称正定矩阵 |
| `GNNTrainer.train()` | `graphmri --raw predict` (group-level) | infra_strategy 正确分发 |

### DSL vs 原生 CLI 对比验证

在 Notebook 中并行运行两种方式，对比输出一致性：

```python
# DSL 路径
dsl_results = trainer.train(model="GraphSAGE", target="HAMD_improvement_pct")

# 原生 CLI 路径 (等价调用)
# graphmri --raw predict --connectome ... --labels ... --model GraphSAGE --target HAMD_improvement_pct
cli_results = subprocess_run_graphmri_predict(...)

# 断言：DSL 结果与 CLI 结果一致 (R² 误差 < 1e-6)
assert abs(dsl_results.test_r2 - cli_results.test_r2) < 1e-6
```

## 验收标准

- [ ] `sros-sdk/examples/sxmu_mdd_dtms_e2e.ipynb` 文件存在
- [ ] Notebook 可从头到尾无错误执行（Cell → Run All）
- [ ] `.from_duckdb()` 成功加载 dTMS 106 例被试
- [ ] `.apply_pipeline("fmriprep")` 对全部 106 例正确生成预处理 NIfTI
- [ ] `.extract_connectome(atlas="aal")` 输出通过 DSPy 对称正定硬断言
- [ ] `GNNTrainer.train(infra_strategy="auto")` 正确检测执行环境
- [ ] DSL 结果与等价 CLI 结果一致（R² 误差 < 1e-6）
- [ ] `infra_strategy="auto"` 的 strategy_reason 字段正确记录分发决策
- [ ] SROS ROADMAP.md 中 DSL-6 标记为 ✅

## 参考实现 (Don't Guess, Copy)

| 新功能 | 参考源 | 关键复用点 |
|--------|--------|----------|
| BrainGraphDataset.from_duckdb() | `sros-sdk/src/sros/brain/dataset.py` — DSL-2 | 已有完整 Fluent API 链式调用实现 |
| GNNTrainer.train() | `sros-sdk/src/sros/ml/trainer.py` — DSL-3 | 已有 GraphSAGE/GAT/GCN/BrainGNN 四模型 + auto strategy |
| DuckDB 连接器 | `sros-sdk/src/sros/data/duckdb.py` — DSL-4 | 已有 SQL → subject list 列映射推断 |
| DSPy 断言 | `sros-sdk/src/sros/dspy/assertions.py` — DSL-5 | 已有对称正定硬断言 + gradient_checkpointing 软建议 |
| graphmri CLI contract | GraphMRI-Lite `cli/main.py` — `--raw` JSON | 已有 4 子命令 stdout JSON schema |
| GraphMRI-Lite CLI 调用 | `sros-sdk/src/sros/brain/backends/graphmri.py` | DSL-2 已封装 subprocess 调用 + JSON 解析 |
