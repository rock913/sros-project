from __future__ import annotations

import numpy as np
import pytest


class TestDuckDBConnectorColumnMapping:
    """D4: DuckDB connector — column name inference."""

    def test_column_mapping_subject_id(self):
        from sros.data.duckdb import _infer_column_mapping
        columns = ["subject_id", "bids_path", "age"]
        mapping = _infer_column_mapping(columns)
        assert mapping["subject_id"] == "subject_id"
        assert mapping["bids_path"] == "bids_path"

    def test_column_mapping_participant_id(self):
        from sros.data.duckdb import _infer_column_mapping
        columns = ["participant_id", "data_dir", "sex"]
        mapping = _infer_column_mapping(columns)
        assert mapping["subject_id"] == "participant_id"
        assert mapping["bids_path"] == "data_dir"

    def test_column_mapping_fuzzy(self):
        from sros.data.duckdb import _infer_column_mapping
        columns = ["sub_id", "bids_dir", "phenotype_HAMD"]
        mapping = _infer_column_mapping(columns)
        # sub_id should be recognized as subject identifier
        assert mapping["subject_id"] is not None
        # bids_dir should be recognized as path
        assert mapping["bids_path"] is not None

    def test_column_mapping_no_match(self):
        from sros.data.duckdb import _infer_column_mapping
        columns = ["foo", "bar", "baz"]
        mapping = _infer_column_mapping(columns)
        # No recognized columns — all should be None
        assert mapping["subject_id"] is None
        assert mapping["bids_path"] is None

    def test_phenotype_columns_detected(self):
        from sros.data.duckdb import _infer_column_mapping
        columns = ["sub_id", "phenotype_HAMD", "phenotype_age", "phenotype_BMI"]
        mapping = _infer_column_mapping(columns)
        assert "phenotype_HAMD" in mapping["phenotypes"]
        assert "phenotype_age" in mapping["phenotypes"]
        assert len(mapping["phenotypes"]) == 3


class TestDuckDBConnectorRowToSubject:
    """D4: Row dictionary → BrainGraphDataset subject dict."""

    def test_row_to_subject_basic(self):
        from sros.data.duckdb import _row_to_subject
        row = {"subject_id": "sub-01", "bids_path": "/data/sub-01", "age": 25}
        mapping = {"subject_id": "subject_id", "bids_path": "bids_path", "phenotypes": [], "extra": {}}
        subject = _row_to_subject(row, mapping)
        assert subject["subject_id"] == "sub-01"
        assert subject["bids_path"] == "/data/sub-01"
        assert subject["age"] == 25

    def test_row_to_subject_with_phenotypes(self):
        from sros.data.duckdb import _row_to_subject
        row = {"sub_id": "sub-02", "phenotype_HAMD": 17, "phenotype_BMI": 22.5}
        mapping = {
            "subject_id": "sub_id",
            "bids_path": None,
            "phenotypes": ["phenotype_HAMD", "phenotype_BMI"],
            "extra": {},
        }
        subject = _row_to_subject(row, mapping)
        assert subject["subject_id"] == "sub-02"
        assert subject["phenotypes"]["HAMD"] == 17
        assert subject["phenotypes"]["BMI"] == 22.5


class TestDuckDBConnectorIntegration:
    """D4: End-to-end from_duckdb() → BrainGraphDataset."""

    def test_from_duckdb_integration(self, monkeypatch):
        from sros.brain.dataset import BrainGraphDataset

        mock_columns = ["subject_id", "bids_path", "phenotype_age"]
        mock_rows = [
            ("sub-01", "/data/sub-01", 22),
            ("sub-02", "/data/sub-02", 28),
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
        assert ds.subjects[0]["phenotypes"]["age"] == 22
        # Non-phenotype fields preserved as-is
        assert ds.subjects[0]["bids_path"] == "/data/sub-01"
