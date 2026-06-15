from __future__ import annotations

import os

import pytest


class TestGNNTrainerInit:
    """D3: GNNTrainer — construction and model registry."""

    def test_trainer_import(self):
        from sros.ml.trainer import GNNTrainer
        assert GNNTrainer is not None

    def test_trainer_init(self):
        from sros.brain.dataset import BrainGraphDataset
        from sros.ml.trainer import GNNTrainer

        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        trainer = GNNTrainer(ds)
        assert trainer.dataset is ds

    def test_supported_models(self):
        from sros.ml.trainer import SUPPORTED_MODELS
        assert "GraphSAGE" in SUPPORTED_MODELS
        assert "GAT" in SUPPORTED_MODELS
        assert "GCN" in SUPPORTED_MODELS
        assert "BrainGNN" in SUPPORTED_MODELS


class TestGNNTrainerInfraStrategy:
    """D3: infra_strategy="auto" — environment auto-detection."""

    def test_infra_strategy_auto_cpu_fallback(self, monkeypatch):
        """When no GPU / Slurm / Docker detected, default to CPU."""
        # Remove all GPU/Slurm/Docker indicators
        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
        monkeypatch.delenv("SLURM_JOB_ID", raising=False)
        # Ensure /.dockerenv doesn't exist
        monkeypatch.setattr(os.path, "exists", lambda p: False)

        from sros.ml.trainer import GNNTrainer, InfraStrategy

        strategy = GNNTrainer._detect_infra()
        assert strategy == InfraStrategy.CPU

    def test_infra_strategy_detects_gpu(self, monkeypatch):
        monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")
        monkeypatch.delenv("SLURM_JOB_ID", raising=False)
        monkeypatch.setattr(os.path, "exists", lambda p: False)

        from sros.ml.trainer import GNNTrainer, InfraStrategy

        strategy = GNNTrainer._detect_infra()
        assert strategy == InfraStrategy.SINGLE_GPU

    def test_infra_strategy_detects_multi_gpu(self, monkeypatch):
        monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0,1,2,3")
        monkeypatch.delenv("SLURM_JOB_ID", raising=False)
        monkeypatch.setattr(os.path, "exists", lambda p: False)

        from sros.ml.trainer import GNNTrainer, InfraStrategy

        strategy = GNNTrainer._detect_infra()
        assert strategy == InfraStrategy.MULTI_GPU

    def test_infra_strategy_detects_slurm(self, monkeypatch):
        monkeypatch.setenv("SLURM_JOB_ID", "12345")
        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
        monkeypatch.setattr(os.path, "exists", lambda p: False)

        from sros.ml.trainer import GNNTrainer, InfraStrategy

        strategy = GNNTrainer._detect_infra()
        assert strategy == InfraStrategy.SLURM

    def test_infra_strategy_detects_docker(self, monkeypatch):
        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
        monkeypatch.delenv("SLURM_JOB_ID", raising=False)
        # Simulate Docker env file exists
        monkeypatch.setattr(os.path, "exists", lambda p: p == "/.dockerenv")

        from sros.ml.trainer import GNNTrainer, InfraStrategy

        strategy = GNNTrainer._detect_infra()
        assert strategy == InfraStrategy.DOCKER_GPU

    def test_infra_strategy_explicit_override(self):
        """Explicit strategy parameter bypasses auto-detection."""
        from sros.ml.trainer import InfraStrategy

        strategy = InfraStrategy.from_string("cpu")
        assert strategy == InfraStrategy.CPU

        strategy = InfraStrategy.from_string("single_gpu")
        assert strategy == InfraStrategy.SINGLE_GPU

    def test_infra_strategy_invalid_raises(self):
        from sros.ml.trainer import InfraStrategy

        with pytest.raises(ValueError):
            InfraStrategy.from_string("quantum_computer")


class TestGNNTrainerTrain:
    """D3: train() — training invocation contract."""

    def test_train_no_connectome_raises(self):
        from sros.brain.dataset import BrainGraphDataset
        from sros.ml.trainer import GNNTrainer

        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        trainer = GNNTrainer(ds)
        with pytest.raises(ValueError, match="No connectome data"):
            trainer.train(model="GraphSAGE", target="HAMD_score")

    def test_train_mock(self, monkeypatch):
        import numpy as np
        from sros.brain.dataset import BrainGraphDataset
        from sros.ml.trainer import GNNTrainer

        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        ds._connectome_data = np.random.rand(10, 90)  # 10 subjects, 90 edges
        ds._labels = np.array([0, 1, 0, 1, 0, 0, 1, 0, 1, 0])

        # Mock the ML backend
        mock_result = {"accuracy": 0.85, "roc_auc": 0.91}

        def mock_fit(*args, **kwargs):
            return mock_result

        monkeypatch.setattr(
            "sros.ml.trainer.GNNTrainer._run_training", mock_fit,
        )

        trainer = GNNTrainer(ds)
        result = trainer.train(model="random_forest", target="response", infra_strategy="cpu")
        assert result["accuracy"] == 0.85
        assert result["roc_auc"] == 0.91
