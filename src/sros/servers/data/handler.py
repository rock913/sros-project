from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
import subprocess
import sys
import os
from sros.servers.memory.handler import MemoryHandler
from sros.domain.schemas import KnowledgeEdge


class DataHandler:
    def preview_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Preview a CSV file: return summary stats, column info, and sample rows.
        """
        path = Path(file_path)
        if not path.exists():
            return {"ok": False, "error": f"File not found: {file_path}"}

        try:
            df = pd.read_csv(path)
            summary = {
                "file_path": str(path),
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "sample_rows": df.head(5).to_dict(orient="records"),
                "null_counts": df.isnull().sum().to_dict(),
            }
            return {"ok": True, "summary": summary}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def run_script(self, script_path: str) -> Dict[str, Any]:
        """
        Execute a Python script and register any generated figures in the knowledge graph.
        """
        script = Path(script_path)
        if not script.exists():
            return {"ok": False, "error": f"Script not found: {script_path}"}

        workspace_dir = Path(os.getenv("SROS_WORKSPACE_DIR", "."))
        figures_dir = workspace_dir / "figures"
        figures_dir.mkdir(exist_ok=True)

        # Get existing figures before execution
        existing_figures = set(figures_dir.glob("*"))

        try:
            # Execute the script
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=workspace_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            if result.returncode != 0:
                return {"ok": False, "error": f"Script execution failed: {result.stderr}"}

            # Check for new figures
            new_figures = set(figures_dir.glob("*")) - existing_figures
            generated_figures = [f for f in new_figures if f.is_file()]

            # Register in knowledge graph
            memory = MemoryHandler()
            nodes = []
            edges = []

            # Register script node if not exists
            script_id = f"script_{script.name}"
            nodes.append({
                "id": script_id,
                "type": "Script",
                "title": script.name,
                "content": {"path": str(script), "execution_output": result.stdout}
            })

            # Register figure nodes and edges
            for fig in generated_figures:
                fig_id = f"figure_{fig.name}"
                nodes.append({
                    "id": fig_id,
                    "type": "Figure",
                    "title": fig.name,
                    "content": {"path": str(fig)}
                })
                # Script GENERATES Figure
                edges.append(KnowledgeEdge(
                    source=script_id,
                    target=fig_id,
                    relationship="GENERATES",
                    confidence=1.0
                ))

            if nodes or edges:
                success = memory.store_knowledge(nodes, edges)
                if not success:
                    return {"ok": False, "error": "Failed to store knowledge"}

            return {
                "ok": True,
                "script": str(script),
                "execution": {
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                },
                "generated_figures": [str(f) for f in generated_figures]
            }

        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Script execution timed out"}
        except Exception as e:
            return {"ok": False, "error": str(e)}