"""Deprecated wrapper. Use scripts/verify_production.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "scripts" / "verify_production.py"
runpy.run_path(str(target), run_name="__main__")

report_path = Path(__file__).resolve().parent / "logs" / "production_verification.json"
if report_path.exists():
	print(f"\nJSON report: {report_path}\n")
