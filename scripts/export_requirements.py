#!/usr/bin/env python3
"""Export requirements files from pyproject.toml.

Why:
- Keep `pyproject.toml` as the single source of truth.
- Generate `requirements.txt` for environments that still expect a requirements file.

Usage:
  python scripts/export_requirements.py
  python scripts/export_requirements.py --output requirements.txt
  python scripts/export_requirements.py --extra test --output requirements-test.txt

Notes:
- Default export includes only `[project].dependencies`.
- Use `--extra <name>` to additionally include `[project.optional-dependencies].<name>`.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List


def _load_pyproject(pyproject_path: Path) -> dict:
    import tomllib

    return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))


def _unique_stable(items: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        item = item.strip()
        if not item:
            continue
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def export_requirements(pyproject_path: Path, extras: List[str]) -> List[str]:
    data = _load_pyproject(pyproject_path)

    project = data.get("project")
    if not isinstance(project, dict):
        raise SystemExit("Invalid pyproject.toml: missing [project]")

    deps = project.get("dependencies") or []
    if not isinstance(deps, list):
        raise SystemExit("Invalid pyproject.toml: [project].dependencies must be a list")

    optional = project.get("optional-dependencies") or {}
    if optional is None:
        optional = {}
    if not isinstance(optional, dict):
        raise SystemExit(
            "Invalid pyproject.toml: [project].optional-dependencies must be a table/dict"
        )

    extra_deps: List[str] = []
    for extra in extras:
        group = optional.get(extra)
        if group is None:
            raise SystemExit(f"Unknown extra '{extra}'. Available: {sorted(optional.keys())}")
        if not isinstance(group, list):
            raise SystemExit(
                f"Invalid pyproject.toml: optional-dependencies.{extra} must be a list"
            )
        extra_deps.extend(group)

    combined = _unique_stable([*deps, *extra_deps])

    # Deterministic order: keep the original order, but sort within a final stable pass
    # only when duplicates were removed. (We keep author intent/order for readability.)
    return combined


def render(requirements: List[str], *, source: str, extras: List[str]) -> str:
    extra_note = ""
    if extras:
        extra_note = f" (extras: {', '.join(extras)})"

    header = [
        "# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY",
        f"# Source: {source}{extra_note}",
        "# Regenerate: python scripts/export_requirements.py",
        "",
    ]
    return "\n".join(header + requirements + [""])


def main() -> int:
    parser = argparse.ArgumentParser(description="Export requirements from pyproject.toml")
    parser.add_argument(
        "--pyproject",
        default="pyproject.toml",
        help="Path to pyproject.toml (default: pyproject.toml)",
    )
    parser.add_argument(
        "--output",
        default="requirements.txt",
        help="Output requirements file (default: requirements.txt)",
    )
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        help="Optional extra group to include (repeatable), e.g. --extra test",
    )

    args = parser.parse_args()

    pyproject_path = Path(args.pyproject).resolve()
    output_path = Path(args.output).resolve()

    requirements = export_requirements(pyproject_path, extras=list(args.extra))
    output_path.write_text(
        render(requirements, source=str(pyproject_path), extras=list(args.extra)),
        encoding="utf-8",
    )

    print(f"Wrote {output_path} ({len(requirements)} deps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
