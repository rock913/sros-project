from __future__ import annotations

import json
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from sros.skills.cli import app


def test_scholar_zotero_sync_writes_bib_and_db(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--raw",
            "scholar",
            "zotero-sync",
            "--citekeys",
            "smith2024transformer",
            "--citekeys",
            "doe2023lightcurve",
        ],
    )
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["ok"] is True

    bib = tmp_path / "references" / "zotero_library.bib"
    assert bib.exists()
    bib_text = bib.read_text(encoding="utf-8")
    assert "smith2024transformer" in bib_text
    assert "doe2023lightcurve" in bib_text

    con = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        rows = con.execute("SELECT citekey FROM citations ORDER BY citekey").fetchall()
        citekeys = [r[0] for r in rows]
        assert "smith2024transformer" in citekeys
        assert "doe2023lightcurve" in citekeys
    finally:
        con.close()
