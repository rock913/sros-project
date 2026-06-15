# sros-sdk — AI4S DSL: Fluent API for scientific computing

> **SROS V4.2** | Phase 9 DSL 科学编译器

## Quick Start

```bash
cd sros-sdk
pip install -e ".[dev]"
pytest -v
```

## Usage

```python
from sros.brain import BrainGraphDataset
from sros.ml import GNNTrainer

# Chainable DSL for brain network analysis
cohort = (
    BrainGraphDataset
    .from_duckdb("SELECT * FROM mdd_cohort WHERE age > 60")
    .apply_pipeline("fmriprep", resolution="2mm")
    .extract_connectome(atlas="aal", kind="tangent")
)

# Train GNN with auto infrastructure detection
result = GNNTrainer(cohort).train(
    model="GraphSAGE",
    target="HAMD_score",
    infra_strategy="auto",
)
print(f"Accuracy: {result['accuracy']:.3f}")
print(f"Device: {result['device']}")
```

## Modules

| Module | Purpose |
|--------|---------|
| `sros.brain` | BrainGraphDataset Fluent API |
| `sros.ml` | GNNTrainer with auto infrastructure detection |
| `sros.data` | DuckDB → Dataset connector |
| `sros.dspy` | DSPy assertions for scientific constraints |

## Dependencies

- **Core**: duckdb, numpy, scipy
- **GNN training**: torch, torch_geometric (install with `[gnn]` extra)
- **DSPy assertions**: dspy-ai (install with `[dspy]` extra)
