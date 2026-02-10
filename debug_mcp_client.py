"""Deprecated wrapper. Use scripts/debug_mcp_client.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "scripts" / "debug_mcp_client.py"
runpy.run_path(str(target), run_name="__main__")
