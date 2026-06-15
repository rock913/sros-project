from __future__ import annotations

import json
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from sros.skills.cli import app


def _setup_db_with_data(db_path: Path) -> None:
    """Create a DuckDB with the SROS schema and sample data."""
    schema_path = Path(__file__).resolve().parent.parent.parent / "config" / "duckdb" / "schema.sql"
    con = duckdb.connect(str(db_path))
    try:
        con.execute(schema_path.read_text(encoding="utf-8"))
        con.execute("INSERT INTO subjects VALUES ('sub-001', 'Adult_MDD', 'adult', 'F', 32.0, 'dTMS', 'dTMS', CURRENT_TIMESTAMP)")
        con.execute("INSERT INTO subjects VALUES ('sub-002', 'Adult_HC', 'adult', 'M', 28.0, 'HC', 'none', CURRENT_TIMESTAMP)")
        con.execute("INSERT INTO mri_scans VALUES (1, 'sub-001', 'baseline', 'anat', 'sub-001/ses-baseline/anat/sub-001_T1w.nii.gz', NULL, NULL, 0.02, CURRENT_TIMESTAMP)")
        con.execute("INSERT INTO mri_scans VALUES (2, 'sub-001', 'baseline', 'func', 'sub-001/ses-baseline/func/sub-001_bold.nii.gz', NULL, NULL, 0.05, CURRENT_TIMESTAMP)")
        con.execute("INSERT INTO mri_scans VALUES (3, 'sub-002', 'baseline', 'anat', 'sub-002/ses-baseline/anat/sub-002_T1w.nii.gz', NULL, NULL, 0.02, CURRENT_TIMESTAMP)")
    finally:
        con.close()


def test_db_query_simple_select(tmp_path: Path, monkeypatch):
    """Simple SELECT query returns JSON rows."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    db_path = tmp_path / "test_query.duckdb"
    _setup_db_with_data(db_path)

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "db", "query",
        "--sql", "SELECT * FROM subjects",
        "--db", str(db_path),
    ])
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    payload = json.loads(result.stdout)
    assert payload["ok"] is True, payload
    assert len(payload["rows"]) == 2
    assert payload["count"] == 2
    assert "subject_id" in payload["columns"]


def test_db_query_join(tmp_path: Path, monkeypatch):
    """JOIN query across subjects and mri_scans returns correct results."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    db_path = tmp_path / "test_join.duckdb"
    _setup_db_with_data(db_path)

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "db", "query",
        "--sql", "SELECT s.subject_id, s.group_status, m.bids_path FROM subjects s JOIN mri_scans m ON s.subject_id = m.subject_id WHERE s.group_status = 'dTMS'",
        "--db", str(db_path),
    ])
    assert result.exit_code == 0, f"CLI failed: {result.output}"

    payload = json.loads(result.stdout)
    assert payload["ok"] is True, payload
    rows = payload["rows"]
    assert len(rows) == 2  # sub-001 has 2 MRI scans
    for row in rows:
        assert row[0] == "sub-001"  # subject_id


def test_db_query_non_select_rejected(tmp_path: Path, monkeypatch):
    """Non-SELECT queries are rejected for safety."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    db_path = tmp_path / "test_reject.duckdb"
    _setup_db_with_data(db_path)

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "db", "query",
        "--sql", "DROP TABLE subjects",
        "--db", str(db_path),
    ])
    payload = json.loads(result.stdout) if result.stdout else {}
    assert payload.get("ok") is False


def test_db_query_limit_offset(tmp_path: Path, monkeypatch):
    """LIMIT and OFFSET are applied correctly."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    db_path = tmp_path / "test_limit.duckdb"
    _setup_db_with_data(db_path)

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "db", "query",
        "--sql", "SELECT * FROM mri_scans",
        "--limit", "1",
        "--offset", "0",
        "--db", str(db_path),
    ])
    assert result.exit_code == 0

    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["count"] == 1


def test_db_query_invalid_sql(tmp_path: Path, monkeypatch):
    """Invalid SQL returns error."""
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    db_path = tmp_path / "test_invalid.duckdb"
    _setup_db_with_data(db_path)

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "db", "query",
        "--sql", "SELECT * FROM nonexistent_table",
        "--db", str(db_path),
    ])
    payload = json.loads(result.stdout) if result.stdout else {}
    assert payload.get("ok") is False
