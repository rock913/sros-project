from __future__ import annotations

import json
from pathlib import Path

import pytest

from sros.servers.manuscript.handler import ManuscriptHandler


def _first_heading_child(outline_dict: dict) -> dict:
    # root.children[0] is the first heading in the document
    children = outline_dict.get("children") or []
    assert children, "outline must have children"
    return children[0]


def test_outline_tree_includes_anchor_hash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / "draft.md").write_text(
        "# Title\n\n## Introduction\n\nText.\n",
        encoding="utf-8",
    )

    h = ManuscriptHandler()
    outline = h.get_outline_tree("draft.md")
    d = outline.model_dump()

    intro = None
    for node in d.get("children", []):
        if node.get("title") == "Title":
            # descend to find Introduction
            for c in node.get("children", []):
                if c.get("title") == "Introduction":
                    intro = c
                    break
    assert intro is not None

    payload = json.loads(intro.get("content") or "{}")
    assert "anchor" in payload
    assert payload["anchor"]


def test_insert_section_anchor_hash_target(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text(
        "# Title\n\n## Introduction\n\nExisting.\n",
        encoding="utf-8",
    )

    h = ManuscriptHandler()
    outline = h.get_outline_tree("draft.md")
    d = outline.model_dump()

    # Find Introduction anchor hash from outline
    intro = None
    for node in d.get("children", []):
        for c in node.get("children", []):
            if c.get("title") == "Introduction":
                intro = c
                break
    assert intro is not None
    payload = json.loads(intro.get("content") or "{}")
    anchor = payload["anchor"]

    res = h.insert_section(
        target=f"anchor:{anchor}",
        content="Inserted.",
        citations=["doe2021"],
        file_path="draft.md",
    )
    assert isinstance(res, dict)
    assert res["ok"] is True

    updated = draft.read_text(encoding="utf-8")
    assert updated.find("Inserted.") > updated.find("## Introduction")
    assert updated.find("Inserted.") < updated.find("Existing.")


def test_insert_section_heading_fuzzy_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text(
        "# Title\n\n## Introduction\n\nExisting.\n",
        encoding="utf-8",
    )

    h = ManuscriptHandler()

    # Lowercase should match (case-insensitive)
    res1 = h.insert_section(
        target="heading:introduction",
        content="A.",
        citations=[],
        file_path="draft.md",
    )
    assert res1["ok"] is True

    # Small typo should match (fuzzy)
    res2 = h.insert_section(
        target="heading:Introducton",
        content="B.",
        citations=[],
        file_path="draft.md",
    )
    assert res2["ok"] is True


def test_insert_section_expected_sha256_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text(
        "# Title\n\n## Introduction\n\nExisting.\n",
        encoding="utf-8",
    )

    h = ManuscriptHandler()
    sha1 = h.get_file_sha256("draft.md")

    # Simulate user edits
    draft.write_text(
        "# Title\n\n## Introduction\n\nExisting.\n\nUser edit.\n",
        encoding="utf-8",
    )

    res = h.insert_section(
        target="heading:Introduction",
        content="Inserted.",
        citations=[],
        file_path="draft.md",
        expected_sha256=sha1,
    )

    assert res["ok"] is False
    assert "Version mismatch" in res["error"]
    assert "current_sha256" in res
