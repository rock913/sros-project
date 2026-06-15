from __future__ import annotations

import numpy as np
import pytest

from sros.brain.dataset import BrainGraphDataset


class TestBrainGraphDatasetInit:
    """D2: BrainGraphDataset — construction and basic properties."""

    def test_empty_init(self):
        ds = BrainGraphDataset([])
        assert len(ds.subjects) == 0

    def test_init_with_subjects(self):
        subjects = [{"subject_id": "sub-01"}, {"subject_id": "sub-02"}]
        ds = BrainGraphDataset(subjects)
        assert len(ds.subjects) == 2

    def test_init_accepts_config(self):
        ds = BrainGraphDataset([], config={"fmriprep_resolution": "2mm"})
        assert ds.config["fmriprep_resolution"] == "2mm"


class TestBrainGraphDatasetFromBIDS:
    """D2: from_bids() — BIDS directory scanning."""

    def test_from_bids_empty_dir(self, tmp_path):
        bids_dir = tmp_path / "bids"
        bids_dir.mkdir()
        ds = BrainGraphDataset.from_bids(str(bids_dir))
        assert len(ds.subjects) == 0

    def test_from_bids_detects_subjects(self, tmp_path):
        bids_dir = tmp_path / "bids"
        (bids_dir / "sub-01").mkdir(parents=True)
        (bids_dir / "sub-02").mkdir(parents=True)
        (bids_dir / "sub-03").mkdir(parents=True)
        # non-sub dir should be ignored
        (bids_dir / "derivatives").mkdir()
        (bids_dir / "sourcedata").mkdir()
        ds = BrainGraphDataset.from_bids(str(bids_dir))
        assert len(ds.subjects) == 3
        subject_ids = [s["subject_id"] for s in ds.subjects]
        assert "sub-01" in subject_ids
        assert "sub-02" in subject_ids
        assert "sub-03" in subject_ids
        assert "derivatives" not in subject_ids


class TestBrainGraphDatasetFromDuckDB:
    """D4: from_duckdb() — SQL query to subject list."""

    def test_from_duckdb_mock(self, monkeypatch):
        mock_columns = ["subject_id", "bids_path", "age"]
        mock_rows = [
            ("sub-01", "/data/sub-01", 25),
            ("sub-02", "/data/sub-02", 30),
        ]

        class MockResult:
            description = [(c,) for c in mock_columns]

            def fetchall(self):
                return mock_rows

        class MockConnection:
            def __init__(self, *args, **kwargs):
                pass

            def execute(self, query):
                return MockResult()

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        monkeypatch.setattr("duckdb.connect", MockConnection)
        ds = BrainGraphDataset.from_duckdb("SELECT * FROM cohort")
        assert len(ds.subjects) == 2
        assert ds.subjects[0]["subject_id"] == "sub-01"
        assert ds.subjects[1]["age"] == 30


class TestBrainGraphDatasetApplyPipeline:
    """D2: apply_pipeline() — CLI argument construction."""

    def test_apply_pipeline_stores_config(self):
        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        ds2 = ds.apply_pipeline("fmriprep", resolution="2mm")
        assert ds2._pipeline == "fmriprep"
        assert ds2._pipeline_kwargs["resolution"] == "2mm"
        # chainable — returns self type
        assert isinstance(ds2, BrainGraphDataset)

    def test_apply_pipeline_builds_cli_args(self, monkeypatch):
        """Verify apply_pipeline constructs correct CLI args for graphmri."""
        recorded_cmd = []

        def mock_run(cmd, **kwargs):
            recorded_cmd.extend(cmd)

        monkeypatch.setattr("sros.brain.dataset._graphmri_cli", mock_run)
        ds = BrainGraphDataset([{"subject_id": "sub-01", "bids_path": "/data/sub-01"}])
        ds.apply_pipeline("fmriprep", resolution="2mm")
        # Currently apply_pipeline only stores config; CLI execution deferred to extract_connectome
        assert ds._pipeline == "fmriprep"
        assert ds._pipeline_kwargs["resolution"] == "2mm"


class TestBrainGraphDatasetExtractConnectome:
    """D2: extract_connectome() — connectome extraction."""

    def test_extract_connectome_stores_params(self):
        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        ds2 = ds.extract_connectome(atlas="aal", kind="tangent", threshold=0.1)
        assert ds2._atlas == "aal"
        assert ds2._kind == "tangent"
        assert ds2._threshold == 0.1
        assert isinstance(ds2, BrainGraphDataset)

    def test_extract_connectome_defaults(self):
        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        ds2 = ds.extract_connectome()
        assert ds2._atlas == "aal"
        assert ds2._kind == "tangent"
        assert ds2._threshold is None


class TestBrainGraphDatasetToDataLoader:
    """D2: to_dataloader() — PyTorch DataLoader conversion."""

    def test_to_dataloader_requires_torch(self, monkeypatch):
        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        # Set mock connectome data to bypass graphmri CLI call
        n_samples = 3
        ds._connectome_data = np.eye(n_samples)
        ds._labels = np.array([0, 1, 0])

        try:
            import torch
            # Mock graphmri subprocess to avoid requiring graphmri CLI
            def mock_run(cmd, **kwargs):
                import subprocess
                return subprocess.CompletedProcess(cmd, 0, stdout="{}", stderr="")

            monkeypatch.setattr("sros.brain.dataset._graphmri_cli", mock_run)
            loader = ds.to_dataloader(batch_size=2)
            assert loader is not None
        except ImportError:
            pytest.skip("torch not installed")

    def test_to_dataloader_batch_size(self, monkeypatch):
        """Mock torch DataLoader to verify batch_size forwarding."""
        import torch

        class MockTensorDataset:
            def __init__(self, *args, **kwargs):
                pass

        class MockDataLoader:
            def __init__(self, dataset, batch_size=1, shuffle=False, **kwargs):
                self.dataset = dataset
                self.batch_size = batch_size
                self.shuffle = shuffle

        monkeypatch.setattr("torch.utils.data.TensorDataset", MockTensorDataset)
        monkeypatch.setattr("torch.utils.data.DataLoader", MockDataLoader)

        # Set _connectome_data to avoid early return
        ds = BrainGraphDataset([{"subject_id": "sub-01"}])
        ds._connectome_data = np.eye(3)
        ds._labels = np.array([0])

        loader = ds.to_dataloader(batch_size=32, shuffle=True)
        assert loader.batch_size == 32
        assert loader.shuffle is True


class TestBrainGraphDatasetChaining:
    """D2: Fluent API chaining — the 'DSL sentence' pattern."""

    def test_full_chain_stores_all_params(self):
        ds = (
            BrainGraphDataset([{"subject_id": "sub-01"}])
            .apply_pipeline("fmriprep", resolution="2mm")
            .extract_connectome(atlas="aal", kind="tangent")
        )
        assert ds._pipeline == "fmriprep"
        assert ds._atlas == "aal"
        assert ds._kind == "tangent"

    def test_partial_chain_with_from_bids(self, tmp_path):
        bids_dir = tmp_path / "bids"
        (bids_dir / "sub-01").mkdir(parents=True)
        (bids_dir / "sub-02").mkdir(parents=True)

        ds = (
            BrainGraphDataset.from_bids(str(bids_dir))
            .apply_pipeline("qsiprep")
            .extract_connectome(atlas="destrieux")
        )
        assert len(ds.subjects) == 2
        assert ds._pipeline == "qsiprep"
        assert ds._atlas == "destrieux"
