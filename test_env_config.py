"""Deprecated wrapper. Use tests/unit/test_env_config.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "tests" / "unit" / "test_env_config.py"
runpy.run_path(str(target), run_name="__main__")