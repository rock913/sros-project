from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sros.skills.cli import app


def test_hpc_submit_dry_run(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    script = tmp_path / "test_job.slurm"
    script.write_text("#!/bin/bash\n#SBATCH --job-name=test\n#SBATCH --mem=16G\n")

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "hpc", "submit",
        "--script", str(script),
        "--dry-run",
    ])
    assert result.exit_code == 0, f"CLI failed: {result.output}"
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True


def test_hpc_submit_missing_script(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "hpc", "submit",
        "--script", "/nonexistent/job.slurm",
    ])
    payload = json.loads(result.stdout) if result.stdout else {}
    assert payload.get("ok") is False


def test_hpc_status_dry_run(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "hpc", "status",
        "--job-id", "12345",
        "--dry-run",
    ])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True


def test_hpc_cancel_dry_run(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "hpc", "cancel",
        "--job-id", "12345",
        "--dry-run",
    ])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["cancelled"] is True


def test_hpc_list_dry_run(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "hpc", "list",
        "--dry-run",
    ])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True


def test_hpc_generate_template(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    template = tmp_path / "my_template.slurm"
    template.write_text("#!/bin/bash\n#SBATCH --job-name=test_sub-{SUBJECT}\nsrun echo {SUBJECT}\n")

    runner = CliRunner()
    result = runner.invoke(app, [
        "--raw", "hpc", "generate",
        "--template", str(template),
        "--subject", "sub-001",
        "--output-dir", str(tmp_path / "jobs"),
    ])
    assert result.exit_code == 0, f"CLI failed: {result.output}"
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert "sub-001" in payload["script_path"]
