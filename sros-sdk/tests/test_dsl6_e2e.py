"""DSL-6: SXMU_MDD dTMS 106 例 E2E regression test.

Validates the full DSL chain end-to-end:
  from_duckdb → apply_pipeline → extract_connectome → compute → to_dataloader → GNNTrainer.train

Both demo mode (synthetic data, offline) and contract verification.
"""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest


# ── Fixtures ────────────────────────────────────────────────────

@pytest.fixture
def demo_duckdb_path(tmp_path: Path) -> str:
    """Create a temporary DuckDB with synthetic dTMS cohort data.

    Simulates the SXMU_MDD 8-table schema subset relevant to DSL-6:
    106 subjects with phenotype_HAMD_improvement_pct labels.
    """
    import duckdb

    db_path = str(tmp_path / "mdd_twin.db")
    conn = duckdb.connect(db_path)

    # Create tables matching SROS 8-table DDL subset
    conn.execute("""
        CREATE TABLE subjects (
            subject_id VARCHAR PRIMARY KEY,
            bids_path VARCHAR,
            intervention_type VARCHAR,
            age INTEGER,
            sex VARCHAR
        )
    """)
    conn.execute("""
        CREATE TABLE phenotypes (
            subject_id VARCHAR,
            phenotype_HAMD_improvement_pct DOUBLE,
            phenotype_HAMD_baseline DOUBLE,
            phenotype_response INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)

    # Insert 106 dTMS subjects (matching real SXMU cohort structure)
    rng = np.random.default_rng(42)
    for i in range(106):
        sid = f"sub-{i + 1:03d}"
        bids = f"/data/sxmu_mdd/bids/{sid}"
        age = int(rng.integers(10, 24))
        sex = rng.choice(["M", "F"])
        hamd_imp = round(float(rng.uniform(5, 85)), 1)
        hamd_base = round(float(rng.uniform(14, 35)), 1)
        responder = 1 if hamd_imp >= 50 else 0

        conn.execute(
            "INSERT INTO subjects VALUES (?, ?, 'dTMS', ?, ?)",
            [sid, bids, age, sex],
        )
        conn.execute(
            "INSERT INTO phenotypes VALUES (?, ?, ?, ?)",
            [sid, hamd_imp, hamd_base, responder],
        )

    conn.close()
    return db_path


@pytest.fixture
def cohort_demo(demo_duckdb_path: str):
    """Load dTMS 106 cohort via from_duckdb in demo mode."""
    os.environ["SROS_SDK_DEMO"] = "1"
    from sros.brain.dataset import BrainGraphDataset

    cohort = BrainGraphDataset.from_duckdb(
        "SELECT s.*, p.phenotype_HAMD_improvement_pct, "
        "p.phenotype_HAMD_baseline, p.phenotype_response "
        "FROM subjects s JOIN phenotypes p ON s.subject_id = p.subject_id "
        "WHERE s.intervention_type = 'dTMS'",
        db_path=demo_duckdb_path,
    )
    return cohort


@pytest.fixture
def cohort_demo_small(demo_duckdb_path: str):
    """Load first 12 subjects for fast ML E2E tests."""
    os.environ["SROS_SDK_DEMO"] = "1"
    from sros.brain.dataset import BrainGraphDataset

    cohort = BrainGraphDataset.from_duckdb(
        "SELECT s.*, p.phenotype_HAMD_improvement_pct, "
        "p.phenotype_HAMD_baseline, p.phenotype_response "
        "FROM subjects s JOIN phenotypes p ON s.subject_id = p.subject_id "
        "WHERE s.intervention_type = 'dTMS' "
        "LIMIT 12",
        db_path=demo_duckdb_path,
    )
    return cohort


# ── Step 1: from_duckdb ─────────────────────────────────────────

class TestDSL6Step1FromDuckDB:
    """E2E Step 1: Load dTMS 106 cohort from DuckDB."""

    def test_loads_correct_count(self, cohort_demo):
        """Should load exactly 106 dTMS subjects."""
        assert len(cohort_demo.subjects) == 106

    def test_all_subjects_have_ids(self, cohort_demo):
        """Every subject must have a subject_id."""
        for s in cohort_demo.subjects:
            assert "subject_id" in s
            assert s["subject_id"].startswith("sub-")

    def test_phenotypes_preserved(self, cohort_demo):
        """Phenotype columns must be accessible via phenotypes dict."""
        subjects_with_phenotypes = sum(
            1 for s in cohort_demo.subjects
            if s.get("phenotypes") and "HAMD_improvement_pct" in s["phenotypes"]
        )
        assert subjects_with_phenotypes == 106

    def test_phenotype_range_valid(self, cohort_demo):
        """HAMD improvement should be in valid clinical range (0-100%)."""
        for s in cohort_demo.subjects:
            hamd = s.get("phenotypes", {}).get("HAMD_improvement_pct")
            if hamd is not None:
                assert 0 <= float(hamd) <= 100


# ── Step 2: apply_pipeline ──────────────────────────────────────

class TestDSL6Step2ApplyPipeline:
    """E2E Step 2: Apply preprocessing pipeline config."""

    def test_chain_after_from_duckdb(self, cohort_demo):
        """apply_pipeline is chainable after from_duckdb."""
        result = cohort_demo.apply_pipeline("fmriprep", resolution="2mm")
        assert result is cohort_demo  # returns self
        assert cohort_demo._pipeline == "fmriprep"
        assert cohort_demo._pipeline_kwargs["resolution"] == "2mm"

    def test_qsiprep_pipeline(self, cohort_demo):
        """qsiprep pipeline for DTI data."""
        cohort_demo.apply_pipeline("qsiprep", output_dir="/tmp/qsiprep")
        assert cohort_demo._pipeline == "qsiprep"


# ── Step 3: extract_connectome ──────────────────────────────────

class TestDSL6Step3ExtractConnectome:
    """E2E Step 3: Extract connectome from time series."""

    def test_extract_after_pipeline(self, cohort_demo):
        """extract_connectome chains after apply_pipeline."""
        cohort_demo.apply_pipeline("fmriprep", resolution="2mm")
        result = cohort_demo.extract_connectome(atlas="aal", kind="correlation")
        assert result is cohort_demo
        assert cohort_demo._atlas == "aal"
        assert cohort_demo._kind == "correlation"

    def test_atlas_sizes_known(self):
        """All known atlases have correct region counts."""
        from sros.brain.dataset import BrainGraphDataset

        ds = BrainGraphDataset([])
        assert ds._atlas_region_count() == 116  # aal default
        ds._atlas = "destrieux"
        assert ds._atlas_region_count() == 148
        ds._atlas = "craddock200"
        assert ds._atlas_region_count() == 200


# ── Step 4: compute (demo) ──────────────────────────────────────

class TestDSL6Step4Compute:
    """E2E Step 4a: Compute connectome (demo mode)."""

    def test_demo_compute_generates_data(self, cohort_demo):
        """compute() in demo mode generates valid connectome data."""
        cohort_demo.apply_pipeline("fmriprep").extract_connectome(atlas="aal")
        result = cohort_demo.compute(demo=True)

        assert result._connectome_data is not None
        assert result._connectome_data.shape[0] == 106  # 106 subjects
        # AAL 116 → lower triangle = 116*115/2 = 6670 edges
        assert result._connectome_data.shape[1] == 6670

    def test_demo_compute_generates_labels(self, cohort_demo):
        """Demo compute extracts labels from phenotype data."""
        cohort_demo.extract_connectome()
        cohort_demo.compute(demo=True)

        assert cohort_demo._labels is not None
        assert len(cohort_demo._labels) == 106

    def test_demo_compute_matrices_are_spd(self, cohort_demo_small):
        """Demo compute generates symmetric positive definite full matrices."""
        cohort_demo_small.extract_connectome(atlas="aal")
        cohort_demo_small.compute(demo=True)

        matrices = getattr(cohort_demo_small, "_connectome_matrices", None)
        assert matrices is not None
        n_subjects = len(cohort_demo_small.subjects)
        assert matrices.shape == (n_subjects, 116, 116)

        # Check first 5 matrices are SPD
        for i in range(min(5, n_subjects)):
            mat = matrices[i]
            assert np.allclose(mat, mat.T, atol=1e-10), f"Matrix {i} not symmetric"
            eigvals = np.linalg.eigvalsh(mat)
            assert np.all(eigvals > 0), f"Matrix {i} min eigenvalue = {np.min(eigvals)}"

    def test_demo_compute_vectorized_is_lower_triangle(self, cohort_demo_small):
        """Vectorized data matches the lower triangle of full matrices."""
        cohort_demo_small.extract_connectome(atlas="aal")
        cohort_demo_small.compute(demo=True)

        vec = cohort_demo_small._connectome_data
        mat = cohort_demo_small._connectome_matrices

        tri_rows, tri_cols = np.tril_indices(116, k=-1)
        for i in range(min(3, len(vec))):
            expected = mat[i][tri_rows, tri_cols]
            assert np.allclose(vec[i], expected, atol=1e-10)


# ── Step 4b: to_dataloader ──────────────────────────────────────

class TestDSL6Step4ToDataLoader:
    """E2E Step 4b: Convert connectome to PyTorch DataLoader."""

    def test_to_dataloader_after_compute(self, cohort_demo_small):
        """to_dataloader works after compute in demo mode."""
        try:
            import torch
        except ImportError:
            pytest.skip("torch not installed")

        cohort_demo_small.extract_connectome().compute(demo=True)
        loader = cohort_demo_small.to_dataloader(batch_size=4, shuffle=True)

        assert loader.batch_size == 4
        n_batches = sum(1 for _ in loader)
        assert n_batches == 3  # ceil(12/4)

    def test_to_dataloader_yields_correct_shapes(self, cohort_demo_small):
        """Each batch should have correct feature and label dimensions."""
        try:
            import torch
        except ImportError:
            pytest.skip("torch not installed")

        cohort_demo_small.extract_connectome().compute(demo=True)
        loader = cohort_demo_small.to_dataloader(batch_size=8)

        for features, labels in loader:
            assert features.ndim == 2
            assert features.shape[1] == 6670
            assert labels.ndim == 1
            assert features.shape[0] == labels.shape[0]
            break


# ── Step 5: GNNTrainer.train ────────────────────────────────────

class TestDSL6Step5GNNTrainer:
    """E2E Step 5: Train GNN on dTMS connectome data."""

    def test_train_graphsage_demo(self, cohort_demo_small):
        """Train on demo connectome data end-to-end."""
        from sros.ml.trainer import GNNTrainer

        cohort = (
            cohort_demo_small
            .apply_pipeline("fmriprep", resolution="2mm")
            .extract_connectome(atlas="aal", kind="correlation")
        )
        cohort.compute(demo=True)

        trainer = GNNTrainer(cohort)
        result = trainer.train(
            model="random_forest",
            target="HAMD_improvement_pct",
            infra_strategy="cpu",
        )

        assert "accuracy" in result
        assert "roc_auc" in result
        assert result["device"] == "cpu"
        assert result["strategy"] == "cpu"
        assert "strategy_reason" in result

    def test_train_multiple_models(self, cohort_demo_small):
        """Multiple model types should all train successfully."""
        from sros.ml.trainer import GNNTrainer

        cohort = cohort_demo_small.extract_connectome(atlas="aal", kind="tangent")
        cohort.compute(demo=True)

        for model in ["svc_rbf", "logistic_l1", "random_forest"]:
            trainer = GNNTrainer(cohort)
            result = trainer.train(
                model=model,
                target="HAMD_improvement_pct",
                infra_strategy="cpu",
            )
            assert result["strategy"] == "cpu"

    def test_infra_strategy_auto_in_demo(self, cohort_demo_small, monkeypatch):
        """infra_strategy='auto' detects environment correctly in demo."""
        from sros.ml.trainer import GNNTrainer

        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
        monkeypatch.delenv("SLURM_JOB_ID", raising=False)
        monkeypatch.setattr(os.path, "exists", lambda p: False)

        cohort = cohort_demo_small.extract_connectome()
        cohort.compute(demo=True)

        trainer = GNNTrainer(cohort)
        result = trainer.train(
            model="svc_rbf",
            target="HAMD_improvement_pct",
            infra_strategy="auto",
        )

        assert result["strategy_reason"] == "auto-detected"
        assert result["device"] in ["cpu", "single_gpu", "multi_gpu", "docker_gpu", "slurm"]

    def test_train_result_has_cv_scores(self, cohort_demo_small):
        """Training result should include cross-validation scores."""
        from sros.ml.trainer import GNNTrainer

        cohort = cohort_demo_small.extract_connectome().compute(demo=True)

        trainer = GNNTrainer(cohort)
        result = trainer.train(
            model="random_forest",
            target="HAMD_improvement_pct",
            infra_strategy="cpu",
        )

        assert "cv_scores" in result
        assert len(result["cv_scores"]) == 5


# ── DSL vs CLI contract ─────────────────────────────────────────

class TestDSL6ContractConsistency:
    """Verify DSL output contract matches graphmri CLI JSON schema."""

    def test_dsl_compute_contract_keys(self, cohort_demo_small):
        """compute() output should have the keys expected by downstream consumers."""
        cohort = (
            cohort_demo_small
            .apply_pipeline("fmriprep")
            .extract_connectome(atlas="aal")
            .compute(demo=True)
        )

        assert cohort._connectome_data is not None
        assert cohort._connectome_data.ndim == 2
        assert cohort._connectome_data.shape[0] == len(cohort.subjects)

    def test_train_result_contract_keys(self, cohort_demo_small):
        """train() result dict should have stable keys for downstream consumers."""
        from sros.ml.trainer import GNNTrainer

        cohort = cohort_demo_small.extract_connectome().compute(demo=True)
        trainer = GNNTrainer(cohort)
        result = trainer.train(
            model="svc_rbf",
            target="HAMD_improvement_pct",
            infra_strategy="cpu",
        )

        required_keys = {"accuracy", "roc_auc", "device", "strategy", "strategy_reason"}
        assert required_keys.issubset(set(result.keys()))

    def test_full_chain_idempotent(self, cohort_demo_small):
        """Running the full chain twice should not corrupt state."""
        from sros.ml.trainer import GNNTrainer

        def run_chain():
            c = (
                cohort_demo_small
                .apply_pipeline("fmriprep", resolution="2mm")
                .extract_connectome(atlas="aal", kind="correlation")
            )
            c.compute(demo=True)
            trainer = GNNTrainer(c)
            return trainer.train(model="svc_rbf", target="HAMD_improvement_pct", infra_strategy="cpu")

        r1 = run_chain()
        r2 = run_chain()

        assert abs(r1["accuracy"] - r2["accuracy"]) < 1e-6
        assert abs(r1["roc_auc"] - r2["roc_auc"]) < 1e-6


# ── Full Pipeline: DSL sentence ─────────────────────────────────

class TestDSL6FullPipeline:
    """The one-line DSL sentence — the ultimate E2E test."""

    def test_full_pipeline_one_liner(self, demo_duckdb_path, monkeypatch):
        """Reproduce the proposal's exact one-liner DSL usage."""
        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
        monkeypatch.delenv("SLURM_JOB_ID", raising=False)
        monkeypatch.setattr(os.path, "exists", lambda p: False)

        from sros.brain.dataset import BrainGraphDataset
        from sros.ml.trainer import GNNTrainer

        result = (
            GNNTrainer(
                BrainGraphDataset
                .from_duckdb(
                    "SELECT s.*, p.phenotype_HAMD_improvement_pct, "
                    "p.phenotype_HAMD_baseline, p.phenotype_response "
                    "FROM subjects s JOIN phenotypes p ON s.subject_id = p.subject_id "
                    "WHERE s.intervention_type = 'dTMS' "
                    "LIMIT 12",
                    db_path=demo_duckdb_path,
                )
                .apply_pipeline("fmriprep", resolution="2mm")
                .extract_connectome(atlas="aal", kind="correlation")
                .compute(demo=True)
            )
            .train(
                model="random_forest",
                target="HAMD_improvement_pct",
                infra_strategy="cpu",
            )
        )

        assert result["strategy"] == "cpu"
        print(f"\n  DSL-6 E2E: accuracy={result['accuracy']:.3f}, "
              f"roc_auc={result['roc_auc']:.3f}, "
              f"strategy={result['strategy']}")

    def test_cli_equivalent_output(self, cohort_demo_small):
        """DSL result should be structurally equivalent to graphmri CLI output."""
        from sros.ml.trainer import GNNTrainer

        cohort = cohort_demo_small.extract_connectome().compute(demo=True)
        trainer = GNNTrainer(cohort)
        dsl_result = trainer.train(
            model="svc_rbf",
            target="HAMD_improvement_pct",
            infra_strategy="cpu",
        )

        common_keys = {"accuracy", "roc_auc"}
        assert common_keys.issubset(set(dsl_result.keys()))
        assert isinstance(dsl_result["accuracy"], float)
        assert isinstance(dsl_result["roc_auc"], float)
