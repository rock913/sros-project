"""Deprecated wrapper. Use tests/integration/test_gateway.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "tests" / "integration" / "test_gateway.py"
runpy.run_path(str(target), run_name="__main__")