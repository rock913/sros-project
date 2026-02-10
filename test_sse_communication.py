"""Deprecated wrapper. Use tests/integration/test_sse_communication.py instead."""
from pathlib import Path
import runpy

target = Path(__file__).resolve().parent / "tests" / "integration" / "test_sse_communication.py"
runpy.run_path(str(target), run_name="__main__")
    except Exception as e:
        print(f"\nError running tests: {e}")
        import traceback
        traceback.print_exc()