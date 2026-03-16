"""Deprecated wrapper. Use tests/performance/performance_tests.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "tests" / "performance" / "performance_tests.py"
runpy.run_path(str(target), run_name="__main__")