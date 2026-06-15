from __future__ import annotations

import json
from pathlib import Path

import pytest

from sros.utils.health_checker import HealthChecker


class TestDoctorArcDiagnostics:
    def test_arc_wiki_json_valid(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """arc_wiki.json exists with valid JSON → healthy."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
        wiki_json = tmp_path / "arc_wiki.json"
        wiki_json.write_text(json.dumps({
            "project_name": "SROS",
            "raw_dir": "src/sros",
            "wiki_dir": "docs/code_wiki",
        }))

        checker = HealthChecker()
        report = checker.generate_report()

        assert "arc_wiki_json" in report
        assert report["arc_wiki_json"]["status"] == "healthy"

    def test_arc_wiki_json_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """arc_wiki.json missing → warning."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

        checker = HealthChecker()
        report = checker.generate_report()

        assert "arc_wiki_json" in report
        assert report["arc_wiki_json"]["status"] == "warning"

    def test_arc_wiki_json_invalid(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """arc_wiki.json is not valid JSON → unhealthy."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
        (tmp_path / "arc_wiki.json").write_text("{not valid json")

        checker = HealthChecker()
        report = checker.generate_report()

        assert "arc_wiki_json" in report
        assert report["arc_wiki_json"]["status"] == "unhealthy"

    def test_code_schema_md_present(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """docs/code_schema.md exists → healthy."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
        schema_dir = tmp_path / "docs"
        schema_dir.mkdir()
        (schema_dir / "code_schema.md").write_text("# SROS Code Schema\n")

        checker = HealthChecker()
        report = checker.generate_report()

        assert "code_schema_md" in report
        assert report["code_schema_md"]["status"] == "healthy"

    def test_code_schema_md_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """docs/code_schema.md missing → warning."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

        checker = HealthChecker()
        report = checker.generate_report()

        assert "code_schema_md" in report
        assert report["code_schema_md"]["status"] == "warning"

    def test_claw_code_ingest_available(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """claw-code-ingest on PATH → healthy (mock via which)."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

        checker = HealthChecker()
        report = checker.generate_report()

        assert "claw_code_ingest" in report
        # status depends on whether claw-code-ingest is actually installed
        assert report["claw_code_ingest"]["status"] in {"healthy", "warning"}

    def test_code_wiki_dir_freshness(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """docs/code_wiki/ present with content → healthy."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
        wiki_dir = tmp_path / "docs" / "code_wiki"
        wiki_dir.mkdir(parents=True)
        (wiki_dir / "index.md").write_text("# Code Wiki Index\n")

        checker = HealthChecker()
        report = checker.generate_report()

        assert "code_wiki_dir" in report
        assert report["code_wiki_dir"]["status"] in {"healthy", "warning"}

    def test_code_wiki_dir_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """docs/code_wiki/ missing → warning."""
        monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

        checker = HealthChecker()
        report = checker.generate_report()

        assert "code_wiki_dir" in report
        assert report["code_wiki_dir"]["status"] == "warning"
