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

    def run_script(self, script_path: str, dataset_paths: List[str] | None = None) -> Dict[str, Any]:
        """
        Execute a Python script and register any generated figures in the knowledge graph.
        """
        workspace_dir = Path(os.getenv("SROS_WORKSPACE_DIR", "."))
        dataset_paths = list(dataset_paths or [])

        script = Path(script_path)
        if not script.is_absolute():
            script = workspace_dir / script
        if not script.exists():
            return {"ok": False, "error": f"Script not found: {script_path}"}

        resolved_datasets: List[Path] = []
        for dataset_path in dataset_paths:
            dataset = Path(dataset_path)
            if not dataset.is_absolute():
                dataset = workspace_dir / dataset
            if not dataset.exists():
                return {"ok": False, "error": f"Dataset not found: {dataset_path}"}
            resolved_datasets.append(dataset)

        figures_dir = workspace_dir / "figures"
        figures_dir.mkdir(exist_ok=True)

        # Snapshot figures before execution (path -> (mtime_ns, size))
        def _sig(p: Path) -> tuple[int, int]:
            st = p.stat()
            return (getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9)), int(st.st_size))

        existing_figures: Dict[Path, tuple[int, int]] = {}
        for p in figures_dir.glob("*"):
            if p.is_file():
                try:
                    existing_figures[p] = _sig(p)
                except Exception:
                    continue

        try:
            # Execute the script
            argv = [sys.executable, str(script)] + [str(p) for p in resolved_datasets]

            # Environment hardening: force a headless matplotlib backend unless user explicitly overrides.
            env = os.environ.copy()
            env.setdefault("MPLBACKEND", "Agg")

            result = subprocess.run(
                argv,
                cwd=workspace_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=300  # 5 minutes timeout
            )

            if result.returncode != 0:
                details = (result.stderr or result.stdout or "").strip()
                return {"ok": False, "error": f"Script execution failed: {details}"}

            # Check for new OR modified figures
            generated_figures: List[Path] = []
            for p in figures_dir.glob("*"):
                if not p.is_file():
                    continue
                try:
                    sig = _sig(p)
                except Exception:
                    continue
                if p not in existing_figures or existing_figures.get(p) != sig:
                    generated_figures.append(p)

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

            # Register dataset nodes and ANALYZES edges (optional)
            for dataset in resolved_datasets:
                dataset_id = f"dataset_{dataset.name}"
                nodes.append({
                    "id": dataset_id,
                    "type": "Dataset",
                    "title": dataset.name,
                    "content": {"path": str(dataset)}
                })
                edges.append(KnowledgeEdge(
                    source=script_id,
                    target=dataset_id,
                    relationship="ANALYZES",
                    confidence=1.0,
                ))

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
                "datasets": [str(p) for p in resolved_datasets],
                "generated_figures": [str(f) for f in generated_figures]
            }

        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Script execution timed out"}
        except Exception as e:
            return {"ok": False, "error": str(e)}