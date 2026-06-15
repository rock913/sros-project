from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pandas as pd
from typer.testing import CliRunner

from sros.skills.cli import app


def _make_bids_tree(base: Path) -> None:
    """Create a minimal BIDS directory tree with subject/session folders."""
    for sub_id in ["sub-001", "sub-002", "sub-003"]:
        for ses_label in ["ses-baseline", "ses-week8"]:
            anat_dir = base / sub_id / ses_label / "anat"
            func_dir = base / sub_id / ses_label / "func"
            anat_dir.mkdir(parents=True, exist_ok=True)
            func_dir.mkdir(parents=True, exist_ok=True)
            (anat_dir / f"{sub_id}_{ses_label}_T1w.nii.gz").write_text("mock")
            (func_dir / f"{sub_id}_{ses_label}_task-rest_bold.nii.gz").write_text("mock")


def _make_participants_tsv(path: Path) -> None:
    df = pd.DataFrame({
        "participant_id": ["sub-001", "sub-002", "sub-003"],
        "cohort": ["Adult_MDD", "Adult_HC", "Adolescent_MDD"],
        "age_group": ["adult", "adult", "adolescent"],
        "sex": ["F", "M", "F"],
        "age": [32.0, 28.0, 16.5],
        "group_status": ["dTMS", "HC", "SR"],
        "intervention_type": ["dTMS", "none", "SSRIs"],
    })
    df.to_csv(path, sep="\t", index=False)


def _make_clinical_xlsx(path: Path) -> None:
    df = pd.DataFrame({
        "subject_id": ["sub-001", "sub-001", "sub-002", "sub-003", "sub-003"],
        "session_label": ["baseline", "week8", "baseline", "baseline", "week8"],
        "scale_name": ["HAMD", "HAMD", "HAMD", "CTQ", "CTQ"],
        "scale_score": [22.0, 15.0, 3.5, 68.0, 55.0],
        "assessment_date": ["2024-01-15", "2024-03-20", "2024-02-10", "2024-01-18", "2024-03-22"],
    })
    df.to_excel(path, index=False)


def test_db_ingest_end_to_end(tmp_path: Path, monkeypatch):
    """Full pipeline: BIDS + participants + clinical -> DuckDB tables."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    source = tmp_path / "source"
    source.mkdir()
    bids_root = source / "Bids_data"
    bids_root.mkdir()
    _make_bids_tree(bids_root)

    participants_path = source / "participants.tsv"
    _make_participants_tsv(participants_path)

    clinical_path = source / "clinical_scales.xlsx"
    _make_clinical_xlsx(clinical_path)

    db_path = tmp_path / "test.duckdb"
    config_schema = Path(__file__).resolve().parent.parent.parent / "config" / "duckdb" / "schema.sql"

    runner = CliRunner()
    args = [
        "--raw", "db", "ingest",
        "--source", str(source),
        "--bids-dir", "Bids_data",
        "--participants", "participants.tsv",
        "--clinical", "clinical_scales.xlsx",
        "--db", str(db_path),
        "--schema", str(config_schema),
    ]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    payload = json.loads(result.stdout)
    assert payload["ok"] is True, payload
    assert payload.get("subjects_count") == 3
    assert payload.get("mri_scans_count") >= 6  # 3 subjects × 2 sessions × at least 1 modality
    assert payload.get("clinical_count") == 5

    # Verify DuckDB tables
    con = duckdb.connect(str(db_path))
    try:
        tables = [r[0] for r in con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()]
        for name in ["subjects", "mri_scans", "clinical_scales"]:
            assert name in tables, f"Table {name} not found in {tables}"

        subj_cnt = con.execute("SELECT count(*) FROM subjects").fetchone()[0]
        assert subj_cnt == 3

        mri_cnt = con.execute("SELECT count(*) FROM mri_scans").fetchone()[0]
        assert mri_cnt >= 6

        clinical_cnt = con.execute("SELECT count(*) FROM clinical_scales").fetchone()[0]
        assert clinical_cnt == 5

        # Verify a JOIN works
        join_rows = con.execute(
            "SELECT s.subject_id, s.cohort, m.bids_path FROM subjects s "
            "JOIN mri_scans m ON s.subject_id = m.subject_id "
            "WHERE s.group_status = 'dTMS'"
        ).fetchall()
        assert len(join_rows) > 0
    finally:
        con.close()


def test_db_ingest_bids_only(tmp_path: Path, monkeypatch):
    """Ingest only BIDS data without clinical info."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    source = tmp_path / "source"
    source.mkdir()
    bids_root = source / "Bids_data"
    bids_root.mkdir()
    _make_bids_tree(bids_root)

    participants_path = source / "participants.tsv"
    _make_participants_tsv(participants_path)

    db_path = tmp_path / "test_bids.duckdb"
    config_schema = Path(__file__).resolve().parent.parent.parent / "config" / "duckdb" / "schema.sql"

    runner = CliRunner()
    args = [
        "--raw", "db", "ingest",
        "--source", str(source),
        "--bids-dir", "Bids_data",
        "--participants", "participants.tsv",
        "--db", str(db_path),
        "--schema", str(config_schema),
    ]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload.get("subjects_count") == 3

    con = duckdb.connect(str(db_path))
    try:
        subj_cnt = con.execute("SELECT count(*) FROM subjects").fetchone()[0]
        assert subj_cnt == 3
        # clinical_scales table should exist but be empty
        clinical_cnt = con.execute("SELECT count(*) FROM clinical_scales").fetchone()[0]
        assert clinical_cnt == 0
    finally:
        con.close()


def test_db_ingest_missing_source(tmp_path: Path, monkeypatch):
    """Graceful error when source directory doesn't exist."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    args = [
        "--raw", "db", "ingest",
        "--source", str(tmp_path / "nonexistent"),
    ]
    result = runner.invoke(app, args)
    payload = json.loads(result.stdout) if result.stdout else {}
    assert payload.get("ok") is False
