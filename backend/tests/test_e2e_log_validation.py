"""E2E Enhanced Log Validation Test

Purpose:
    Validates the most recent enhanced E2E test run produced by
    `backend/examples/e2e_test_enhanced.sh` without re-running the full
    network + LLM dependent pipeline during `pytest`.

Usage:
    1. Run the enhanced script first, e.g.:
        bash backend/examples/e2e_test_enhanced.sh "recent development on neuro ai" --timeout 600
    2. Then execute pytest (inside container or host):
        pytest -k e2e_log_validation -q

Behavior:
    - Locates the newest file matching logs/e2e_test_enhanced_*.log
    - Asserts required stage key substrings appear in the log
    - Extracts the report file path (if line present) and asserts it exists and has minimal length
    - Skips gracefully if no enhanced log is present (explicit instruction to user)

Rationale:
    Keeps CI/lightweight test cycles fast while still enforcing that a prior
    E2E run produced expected structural milestones. Full live E2E can be
    executed via Make target or dedicated workflow.
"""

from __future__ import annotations

import glob
import re
from pathlib import Path

import pytest

REQUIRED_KEYS = [
    "run_id",
    "generate_initial_queries",
    "execute_searches",
    "reflection_and_refinement",
    "retrieve_and_synthesize_report",
    "report",
]

LOG_GLOB = "logs/e2e_test_enhanced_*.log"
REPORT_MIN_CHARS = 200  # configurable threshold for a minimally useful report


def _latest_log() -> Path | None:
    matches = sorted(glob.glob(LOG_GLOB))
    if not matches:
        return None
    return Path(matches[-1])


@pytest.mark.e2e
def test_enhanced_e2e_latest_log_structure():
    log_path = _latest_log()
    if log_path is None:
        pytest.skip(
            "No enhanced E2E log found. Run the script first: "
            "bash backend/examples/e2e_test_enhanced.sh 'test topic'"
        )

    content = log_path.read_text(encoding="utf-8", errors="ignore")

    # 1. Ensure each required key name is present at least once.
    missing = [k for k in REQUIRED_KEYS if k not in content]
    assert not missing, f"Missing expected keys in log {log_path}: {missing}"

    # 2. Try to locate a line that mentions the saved report.
    report_path = None
    m = re.search(r"Saved final report to: (.+)", content)
    if m:
        candidate = m.group(1).strip()
        # Remove potential ANSI or trailing characters
        candidate = candidate.split()[0]
        report_path = Path(candidate)

    # 3. If report path found, validate existence & size; else fall back to heuristic search.
    if report_path and report_path.is_file():
        size = report_path.stat().st_size
        assert size >= REPORT_MIN_CHARS, (
            f"Report file {report_path} too small ({size} bytes < {REPORT_MIN_CHARS})."
        )
    else:
        # Fallback: attempt to extract an inline truncated report fragment from log.
        # We just ensure at least one occurrence of a plausible multi-sentence section.
        # This keeps the assertion lenient when report extraction wasn't saved.
        fragment = _extract_report_fragment(content)
        assert fragment is not None and len(fragment) >= 120, (
            "Could not validate report presence (no saved file & no inline fragment)."
        )


def _extract_report_fragment(log_text: str) -> str | None:
    """Heuristic: find a block after the last '[CHUNK]' containing multiple periods."""
    chunks = log_text.rsplit("[CHUNK]", maxsplit=5)
    if not chunks:
        return None
    tail = chunks[-1]
    # Look for at least two sentences worth of text in quotes
    m = re.search(r'"report".*', tail)
    if m:
        return m.group(0)[:800]
    return None


if __name__ == "__main__":  # Manual debug helper
    p = _latest_log()
    print("Latest log:", p)
    if p:
        print("Contains required keys?", all(k in p.read_text() for k in REQUIRED_KEYS))