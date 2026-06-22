> 本文档从 Meta 层 proposal 下沉而来。原文件：meta-docs/proposals/delivered/SROS-sros-sdk-Bootstrap.md。下沉日期：2026-06-21。

# SROS PRD 更新提案：sros-sdk 子模块创建与 BrainGraphDataset DSL 破冰

> 目标主 PRD：`01-Core_Infra/SROS/doc/SROS_V4.0.md`
> 提案日期：2026-06-01
> 驱动来源：总 PRD Phase 9 — AI4S DSL 科学编译器，五份重构战略整合结论

## 动机 (Why)

五份重构战略文档从哲学、技术、生态、商业角度得出统一结论：**在现有 SROS/GraphMRI 底盘之上，构建 AI4S DSL 抽象层，让科学家和 AI Agent 用声明式语义表达科学意图，而非手写 PyTorch/CUDA 胶水代码。**

当前痛点：
- 科学家或 Hermes Agent 处理 fMRI 数据时，仍需手写大量前置 Python 代码（坐标系对齐、信噪比过滤、连接组提取）
- LLM 直接写 PyTorch 极易产生幻觉（张量维度不匹配、编造不存在的 API）
- "科学原语"到"计算原语"的编译链条太长，试错周期以天为单位

**Viaweb 飞轮效应**：科学家每踩过一个坑 → 固化为 DSL 算子；每次崩溃解决 → 固化为 SRE 规则。几个月后，外部机构复现实验需要几周，内部科学家只需对着 SROS 说几句话。

## 提议内容

### D1: sros-sdk 子模块骨架 (0.5d)

在 `01-Core_Infra/SROS/` 下创建 `sros-sdk/` 子目录：

```
sros-sdk/
├── pyproject.toml
├── README.md
├── src/sros/
│   ├── __init__.py
│   ├── brain/
│   │   ├── __init__.py
│   │   └── dataset.py          # BrainGraphDataset Fluent API
│   ├── ml/
│   │   ├── __init__.py
│   │   └── trainer.py          # GNNTrainer + infra_strategy
│   ├── data/
│   │   ├── __init__.py
│   │   └── duckdb.py           # from_duckdb() 连接器
│   └── dspy/
│       ├── __init__.py
│       └── assertions.py       # 对称正定矩阵硬断言
└── tests/
    ├── test_brain_dataset.py
    ├── test_trainer.py
    └── test_duckdb_connector.py
```

`pyproject.toml` 依赖：
- `graphmri-lite` (核心算法，本地路径引用)
- `duckdb` (数据查询)
- `torch` + `torch_geometric` (GNN 训练)
- `dspy-ai` (断言约束，可选依赖)
- `numpy`, `scipy` (矩阵计算)

### D2: BrainGraphDataset Fluent API (3d)

**接口契约** — 基于 GraphMRI-Lite 实际调用链一对一映射：

```python
from sros.brain import BrainGraphDataset

# 链式调用 — 每一步对应一个科学原语
cohort = (
    BrainGraphDataset
    .from_duckdb("SELECT * FROM mdd_cohort WHERE age > 60")  # SQL → 数据管道
    .apply_pipeline("fmriprep", resolution="2mm")            # → graphmri preprocess
    .extract_connectome(atlas="aal", kind="tangent")         # → graphmri build_network
)
```

**类设计**：

```python
class BrainGraphDataset:
    """SXMU_MDD 专用脑网络 DSL。底层调用 GraphMRI-Lite CLI + Python API。"""
    
    def __init__(self, subjects: list[dict], config: PipelineConfig | None = None): ...
    
    @classmethod
    def from_duckdb(cls, query: str, db_path: str | None = None) -> "BrainGraphDataset":
        """从 SROS DuckDB 查询被试队列。返回预填充的 Dataset。"""
        ...
    
    @classmethod
    def from_bids(cls, bids_dir: str | Path) -> "BrainGraphDataset":
        """从本地 BIDS 目录扫描被试（向后兼容）。"""
        ...
    
    def apply_pipeline(self, pipeline: str, **kwargs) -> "BrainGraphDataset":
        """应用预处理管线 (fmriprep / qsiprep / ciftify)。
        底层调用 GraphMRI-Lite CLI: graphmri --raw preprocess ..."""
        ...
    
    def extract_connectome(
        self, atlas: str = "aal", kind: str = "tangent", threshold: float | None = None
    ) -> "BrainGraphDataset":
        """提取脑连接组矩阵。
        底层调用 GraphMRI-Lite: graphmri --raw build_network ...
        内部硬断言：输出矩阵必须对称正定。"""
        ...
    
    def to_dataloader(self, batch_size: int = 32, shuffle: bool = True) -> DataLoader:
        """转换为 PyTorch DataLoader（为 GNNTrainer 准备）。"""
        ...
    
    def to_huggingface(self) -> "Dataset":
        """向下兼容 HF Datasets 生态。"""
        ...
```

### D3: GNNTrainer 训练器 (2d)

```python
from sros.ml import GNNTrainer

trainer = GNNTrainer(cohort).train(
    model="GraphSAGE",          # 或 "GAT", "GCN", "BrainGNN"
    target="HAMD_score",        # 预测目标
    infra_strategy="auto"       # 自动侦测 Slurm vs Docker GPU vs CPU
)
```

**GNNTrainer 类设计**：

```python
class GNNTrainer:
    """GNN 训练器 — 封装 BrainGNNClassifier + sklearn EstimatorCV。
    infra_strategy="auto" 自动侦测执行环境并选择最优分布式策略。"""
    
    def __init__(self, dataset: BrainGraphDataset): ...
    
    def train(
        self,
        model: str = "GraphSAGE",
        target: str = "HAMD_score",
        infra_strategy: str = "auto",  # "auto" | "single_gpu" | "multi_gpu" | "cpu"
        **model_kwargs
    ) -> "TrainResult": ...
    
    # infra_strategy="auto" 的分发逻辑：
    # 1. 检查 CUDA_VISIBLE_DEVICES → GPU 数量
    # 2. 检查 SLURM_JOB_ID → Slurm 环境 → 翻译为 sros-hpc-server 任务
    # 3. 检查 docker/.dockerenv → Docker GPU 环境
    # 4. Fallback → CPU
```

### D4: DuckDB 连接器 (1d)

```python
# sros/data/duckdb.py
def from_duckdb(query: str, db_path: str | None = None) -> "BrainGraphDataset":
    """从 SROS DuckDB 执行 SQL，返回 BrainGraphDataset。
    
    自动推断列映射：
    - subject_id / participant_id → subject identifier
    - bids_path / data_dir → BIDS 路径
    - phenotype_* → 表型数据
    """
    ...
```

### D5: DSPy 断言嵌入 (1.5d，可并行)

```python
# sros/dspy/assertions.py
import dspy

class ConnectomeAssertions:
    """脑连接组 DSL 算子的硬约束。"""
    
    @staticmethod
    def assert_symmetric_positive_definite(matrix: np.ndarray):
        """硬断言：连接矩阵必须对称正定。错误在 DSL 层被拦截。"""
        dspy.Assert(
            np.allclose(matrix, matrix.T),
            msg="Connectome matrix must be symmetric"
        )
        dspy.Assert(
            np.all(np.linalg.eigvalsh(matrix) > 0),
            msg="Connectome matrix must be positive definite"
        )
    
    @staticmethod
    def suggest_gradient_checkpointing(model_size_mb: float):
        """软建议：大模型建议开启 gradient checkpointing。"""
        if model_size_mb > 1000:
            dspy.Suggest(
                False,  # 不强制，但强烈建议
                msg=f"Model size {model_size_mb}MB > 1GB. Consider gradient_checkpointing=True"
            )
```

### D6: SXMU_MDD 端到端验证 (1d)

用 DSL 重写 dTMS 106 例 GNN 训练管线，在 Jupyter Notebook 中验证：

```python
# 过去（原生 GraphMRI-Lite CLI）：
# $ graphmri --raw preprocess --bids-dir /data/sxmu --subjects sub-01,sub-02,...
# $ graphmri --raw build_network --timeseries-dir /output/timeseries --atlas aal
# $ graphmri --raw predict --connectome conn.npy --model BrainGNN --labels labels.csv

# 现在（SROS DSL）：
from sros.brain import BrainGraphDataset
from sros.ml import GNNTrainer

result = (
    BrainGraphDataset
    .from_duckdb("SELECT * FROM sxmu_dtms_cohort WHERE responder IS NOT NULL")
    .apply_pipeline("fmriprep", resolution="2mm")
    .extract_connectome(atlas="aal", kind="tangent")
    .pipe(GNNTrainer)
    .train(model="BrainGNN", target="HAMD_improvement", infra_strategy="auto")
)

print(f"Test accuracy: {result.metrics['accuracy']:.3f}")
print(f"Device used: {result.device}")
```

## 验收标准

- [ ] `01-Core_Infra/SROS/sros-sdk/` 目录骨架创建，pyproject.toml 可解析
- [ ] `from sros.brain import BrainGraphDataset` 导入成功
- [ ] `BrainGraphDataset.from_duckdb(query)` 执行 SQL 并返回预设被试列表
- [ ] `BrainGraphDataset.from_bids(bids_dir)` 扫描 BIDS 目录并返回被试列表
- [ ] `.apply_pipeline("fmriprep", resolution="2mm")` 构造正确的 graphmri preprocess CLI 参数
- [ ] `.extract_connectome(atlas="aal", kind="tangent")` 调用 GraphMRI-Lite 并返回连接矩阵
- [ ] `.to_dataloader(batch_size=32)` 返回 PyTorch DataLoader
- [ ] `GNNTrainer(cohort).train(model="GraphSAGE", target="...", infra_strategy="auto")` 成功启动训练
- [ ] `infra_strategy="auto"` 正确侦测执行环境（至少覆盖 Docker GPU 和 CPU fallback）
- [ ] `.extract_connectome()` 对非对称/非正定矩阵触发 DSPy Assert（若 dspy 已安装）
- [ ] tests/ 目录至少含 3 个 pytest（BrainGraphDataset + GNNTrainer + DuckDB 连接器）
- [ ] GNNTrainer 使用 GraphMRI-Lite BrainGNNClassifier 完成至少 1 个 epoch 训练不报错
- [ ] DSL 链式调用可脱离 Jupyter 在纯 Python 脚本中运行（无隐式状态依赖）
- [ ] SROS ROADMAP.md 中新增 DSL-1/DSL-2 任务行并标记为 ✅

## 参考实现 (Don't Guess, Copy)

| 新模块 | 参考源 | 关键复用点 |
|--------|--------|----------|
| `sros/brain/dataset.py` | `01-Core_Infra/GraphMRI-Lite/graphmri_lite/core/network/connectome.py` | `MakeConnectomes(ts, kind, vectorize)`, `ConnectivityMeasure.fit_transform()` |
| `sros/brain/dataset.py` | `01-Core_Infra/GraphMRI-Lite/graphmri_lite/core/network/graph_theory.py` | `matrix_to_graph()`, `compute_all_metrics()` |
| `sros/brain/dataset.py` | `01-Core_Infra/GraphMRI-Lite/graphmri_lite/cli/main.py` | `build_network` 命令参数映射 + `--raw` JSON 输出模式 |
| `sros/ml/trainer.py` | `01-Core_Infra/GraphMRI-Lite/graphmri_lite/core/ml/classifiers.py` | `BrainGNNClassifier.__init__()` 参数签名 + `fit()`/`predict()` 接口 |
| `sros/ml/trainer.py` | `01-Core_Infra/GraphMRI-Lite/graphmri_lite/core/ml/classifiers.py` | `EstimatorCV.__init__()` sklearn CV wrapper, `estimate_active()` 多分类器编排 |
| `sros/ml/trainer.py` | `01-Core_Infra/SROS/src/sros/skills/rpc.py` | `dispatch_tool()` → infra_strategy 分发模式 |
| `sros/data/duckdb.py` | `01-Core_Infra/SROS/src/sros/domain/schemas/` | DuckDB schema 8 表 DDL — subject/phenotype 列名约定 |
| `sros/dspy/assertions.py` | `01-Core_Infra/GraphMRI-Lite/graphmri_lite/core/plugins/base.py` | `BasePipelineStage.validate_requirements()` 前置约束模式 |
| `sros/__init__.py` | `01-Core_Infra/SROS/src/sros/__init__.py` | SROS 包命名约定 + 导出模式 |
| `pyproject.toml` | `01-Core_Infra/GraphMRI-Lite/pyproject.toml` | 本地包依赖声明模式 (`graphmri-lite @ file:///../GraphMRI-Lite`) |

## 不做的事 (Out of Scope)

- **不做全盘通用化**：首期仅 `sros.brain.BrainGraphDataset`，不做 `sros.astro.AstroCube`
- **不做 Awkward Array 深度集成**：首期使用 numpy/torch tensor 作为中间表示
- **不做 DeepSpeed 集成**：`infra_strategy="auto"` 首期仅覆盖单卡/CPU，多卡分布式留给 Phase 9 后续迭代
- **不做 Hermes Agent 联动**：DSL 首期面向人类科学家 + Jupyter Notebook，Agent 代码生成模式留给 Phase 5 H6
- **不修改 GraphMRI-Lite 源码**：DSL 是封装层，通过 CLI `--raw` + Python API 调用，不侵入子项目
