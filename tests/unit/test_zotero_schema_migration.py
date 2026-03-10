from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from sros.domain.schemas import Citation
from sros.servers.zotero.handler import ZoteroHandler


def _create_legacy_citations_table(conn: duckdb.DuckDBPyConnection) -> None:
    # Simulate an older workspace schema that predates the `year` column.
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS citations (
            citekey VARCHAR PRIMARY KEY,
            title VARCHAR,
            authors JSON,
            journal VARCHAR,
            url VARCHAR,
            bibtex TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def test_zotero_migrates_missing_year_column(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    db_path = tmp_path / ".sros" / "graph.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a legacy schema upfront.
    conn = duckdb.connect(str(db_path))
    _create_legacy_citations_table(conn)
    conn.close()

    # Handler init should migrate without raising.
    handler = ZoteroHandler()

    cols = handler.conn.execute("PRAGMA table_info('citations')").fetchall()
    col_names = {row[1] for row in cols}
    assert "year" in col_names

    ok = handler.add_citation(
        Citation(
            citekey="test:2026",
            title="A Test Citation",
            authors=["Alice"],
            year=2026,
            journal="Test Journal",
            url="https://example.org",
            bibtex="@article{test:2026, title={A Test Citation}}",
        )
    )
    assert ok is True
