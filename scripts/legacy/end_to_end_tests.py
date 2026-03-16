"""Deprecated wrapper. Use tests/integration/end_to_end_tests.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "tests" / "integration" / "end_to_end_tests.py"
runpy.run_path(str(target), run_name="__main__")