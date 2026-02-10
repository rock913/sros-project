"""Deprecated wrapper. Use scripts/verify_production.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "scripts" / "verify_production.py"
runpy.run_path(str(target), run_name="__main__")
