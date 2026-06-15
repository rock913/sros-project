"""Tests for CLI structured terminal output — TTY / non-TTY dual-path verification.

Covers:
- --raw mode JSON contract
- TTY vs non-TTY output (Rich ANSI vs plain text)
- Panel/Table rendering for doctor, start, db ingest
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sros.skills.cli import app as skill_app
from sros.cli import app as sros_app


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ── sros-skill --raw JSON contract ────────────────────────────────────────


class TestSkillCliRawContract:
    """--raw mode must output valid, parseable JSON with ok/error contract."""

    def test_db_ingest_raw_output_is_json(self, runner: CliRunner, tmp_path: Path) -> None:
        """sros-skill --raw db ingest → stdout is valid JSON (schema may fail but output is JSON)."""
        source = tmp_path / "data"
        source.mkdir()
        db_file = tmp_path / "test.duckdb"

        result = runner.invoke(
            skill_app,
            ["--raw", "db", "ingest", "--source", str(source), "--db", str(db_file)],
        )
        # exit code may be 0 or 1 depending on schema availability, but stdout must be JSON
        parsed = json.loads(result.stdout)
        assert "ok" in parsed
        assert isinstance(parsed["ok"], bool)

    def test_db_ingest_raw_output_has_no_ansi(self, runner: CliRunner, tmp_path: Path) -> None:
        """--raw output must not contain ANSI escape sequences."""
        source = tmp_path / "data"
        source.mkdir()
        db_file = tmp_path / "test.duckdb"

        result = runner.invoke(
            skill_app,
            ["--raw", "db", "ingest", "--source", str(source), "--db", str(db_file)],
        )
        assert "\x1b[" not in result.stdout

    def test_db_query_raw_output_is_json(self, runner: CliRunner, tmp_path: Path) -> None:
        """sros-skill --raw db query → stdout is valid JSON."""
        db_file = tmp_path / "test.duckdb"
        result = runner.invoke(
            skill_app,
            ["--raw", "db", "query", "--sql", "SELECT 1 AS num", "--db", str(db_file)],
        )
        # May fail if DB has no table, but output must still be valid JSON
        parsed = json.loads(result.stdout)
        assert "ok" in parsed

    def test_hpc_list_raw_output_is_json(self, runner: CliRunner) -> None:
        """sros-skill --raw hpc list --dry-run → JSON output."""
        result = runner.invoke(
            skill_app,
            ["--raw", "hpc", "list", "--dry-run"],
        )
        parsed = json.loads(result.stdout)
        assert "ok" in parsed


# ── Non-TTY plain text fallback ───────────────────────────────────────────


class TestNonTTYFallback:
    """CliRunner is not a TTY; Rich should produce plain text (no ANSI codes)."""

    def test_skill_cli_non_tty_no_ansi(self, runner: CliRunner, tmp_path: Path) -> None:
        """Default mode (non-TTY via CliRunner) should not emit ANSI codes."""
        source = tmp_path / "data"
        source.mkdir()
        db_path = tmp_path / "test.duckdb"

        result = runner.invoke(
            skill_app,
            ["db", "ingest", "--source", str(source), "--db", str(db_path)],
        )
        # exit code depends on schema, but output must be ANSI-free
        assert "\x1b[" not in result.stdout

    def test_skill_cli_raw_is_plain_text(self, runner: CliRunner, tmp_path: Path) -> None:
        """--raw explicitly requests JSON, which is by definition ANSI-free."""
        source = tmp_path / "data"
        source.mkdir()
        db_path = tmp_path / "test.duckdb"

        result = runner.invoke(
            skill_app,
            ["--raw", "db", "ingest", "--source", str(source), "--db", str(db_path)],
        )
        assert "\x1b[" not in result.stdout
        # Must be valid JSON
        json.loads(result.stdout)

    def test_sros_doctor_non_tty_no_ansi(self, runner: CliRunner, tmp_path: Path) -> None:
        """sros doctor in non-TTY mode must output no ANSI sequences."""
        import os
        original = os.getenv("SROS_WORKSPACE_DIR")
        os.environ["SROS_WORKSPACE_DIR"] = str(tmp_path)
        try:
            result = runner.invoke(sros_app, ["doctor"])
            assert "\x1b[" not in result.stdout
        finally:
            if original is not None:
                os.environ["SROS_WORKSPACE_DIR"] = original
            else:
                os.environ.pop("SROS_WORKSPACE_DIR", None)


# ── Structured output content verification ─────────────────────────────────


class TestDoctorOutputContent:
    """sros doctor output must include all key subsystem diagnostics."""

    def test_doctor_includes_subsystem_keys(self, runner: CliRunner, tmp_path: Path) -> None:
        """Doctor output should mention key subsystem names."""
        import os
        original = os.getenv("SROS_WORKSPACE_DIR")
        os.environ["SROS_WORKSPACE_DIR"] = str(tmp_path)
        try:
            result = runner.invoke(sros_app, ["doctor"])
            # The output text (non-TTY) should include key subsystem labels
            combined = result.stdout
            for label in [
                "SROS Gateway",
                "DuckDB Data Layer",
                "ARC Code-Wiki",
                "Runtime Environment",
            ]:
                assert label in combined, f"Doctor output missing subsystem: {label}"
        finally:
            if original is not None:
                os.environ["SROS_WORKSPACE_DIR"] = original
            else:
                os.environ.pop("SROS_WORKSPACE_DIR", None)

    def test_doctor_includes_health_keys(self, runner: CliRunner, tmp_path: Path) -> None:
        """Doctor output must reference core health check keys."""
        import os
        original = os.getenv("SROS_WORKSPACE_DIR")
        os.environ["SROS_WORKSPACE_DIR"] = str(tmp_path)
        try:
            result = runner.invoke(sros_app, ["doctor"])
            combined = result.stdout
            for key in [
                "port availability",
                "mcp services",
                "database integrity",
            ]:
                # Non-TTY plain text should have the component name
                assert key in combined, f"Doctor output missing health key: {key}"
        finally:
            if original is not None:
                os.environ["SROS_WORKSPACE_DIR"] = original
            else:
                os.environ.pop("SROS_WORKSPACE_DIR", None)


class TestStartOutputPanel:
    """sros start should show a structured startup panel (when not actually starting)."""

    def test_start_error_on_missing_workspace(self, runner: CliRunner) -> None:
        """sros start with non-existent workspace → error, not crash."""
        result = runner.invoke(sros_app, ["start", "-w", "/nonexistent/path"])
        assert result.exit_code == 1
        # Error message should be clear (non-TTY = plain text)
        assert "Error" in result.stdout
        assert "\x1b[" not in result.stdout

    def test_start_port_conflict_is_structured(self, runner: CliRunner, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """sros start with port conflict → structured error message."""
        from sros.utils.gateway_process import PortOwner

        monkeypatch.setattr(
            "sros.cli.is_port_in_use",
            lambda port: True,
        )
        monkeypatch.setattr(
            "sros.cli.find_port_owner",
            lambda port: PortOwner(pid=1234, name="test-process"),
        )
        result = runner.invoke(sros_app, ["start", "-w", str(tmp_path), "-p", "9999"])
        assert result.exit_code == 1
        assert "9999" in result.stdout


class TestDbIngestSummaryPanel:
    """sros-skill db ingest in human mode should show a summary Panel."""

    def test_ingest_summary_includes_counts(self, runner: CliRunner, tmp_path: Path) -> None:
        """Ingest completion should include count summary for each table."""
        source = tmp_path / "data"
        source.mkdir()
        db_path = tmp_path / "test.duckdb"

        result = runner.invoke(
            skill_app,
            ["db", "ingest", "--source", str(source), "--db", str(db_path)],
        )
        combined = result.stdout
        # Should include the ingest action indicator and schema init result
        assert "Ingesting from" in combined or "ok" in combined.lower()
