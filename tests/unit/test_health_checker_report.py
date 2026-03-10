from __future__ import annotations

from pathlib import Path

import pytest

from sros.utils.health_checker import HealthChecker


def test_health_checker_report_includes_workspace_and_backend(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    monkeypatch.setenv("SROS_SCHOLAR_BACKEND", "openalex")
    monkeypatch.delenv("OPENALEX_EMAIL", raising=False)
    monkeypatch.delenv("SROS_OPENALEX_MAILTO", raising=False)
    monkeypatch.delenv("SROS_OPENALEX_EMAIL", raising=False)

    checker = HealthChecker()
    report = checker.generate_report()

    assert "workspace" in report
    assert str(tmp_path) in report["workspace"]["details"]

    assert "scholar_backend" in report
    assert report["scholar_backend"]["status"] in {"warning", "healthy"}
