"""Deprecated wrapper. Use tests/performance/stress_tests.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "tests" / "performance" / "stress_tests.py"
runpy.run_path(str(target), run_name="__main__")