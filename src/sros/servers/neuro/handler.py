"""Neuro handler: BIDS validation, graphmri script generation, fMRIPrep pipeline.

Provides MCP tools for neuroimaging workflow orchestration.
Follows the same handler pattern as DBHandler / HPCHandler.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BIDS_MODALITIES = {"anat", "func", "dwi", "fmap", "perf", "eeg", "meg", "ieeg", "beh"}
BIDS_REQUIRED_FILES = {"dataset_description.json"}
NIFTI_EXTENSIONS = {".nii", ".nii.gz"}
SUB_PATTERN = re.compile(r"^sub-[A-Za-z0-9]+$")
SES_PATTERN = re.compile(r"^ses-[A-Za-z0-9]+$")

GRAPHMRI_DEFAULT_CONFIG = {
    "atlas": "aal",
    "parcellation": 116,
    "edge_weights": ["fisher_z", "pearson", "partial"],
    "threshold": 0.3,
    "output_formats": ["csv", "mat", "json"],
}


def _run(cmd: List[str], timeout: int = 60) -> Dict[str, Any]:
    """Run a shell command and return standardized result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ},
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Command timed out after {timeout}s: {' '.join(cmd)}"}
    except FileNotFoundError:
        return {"ok": False, "error": f"Command not found: {cmd[0]}"}


class NeuroHandler:
    """Neuroimaging workflow handler.

    Capabilities:
    - BIDS directory structure validation (heuristic + optional bids-validator)
    - graphmri analysis script generation
    - fMRIPrep Slurm batch generation (delegates to HPCHandler for template work)
    """

    # ── BIDS Validation ───────────────────────────────────────────────────

    def validate_bids(self, bids_dir: str, use_validator: bool = False) -> Dict[str, Any]:
        """Validate a BIDS directory structure.

        Performs heuristic checks (subject/session directory naming, required files,
        NIfTI presence). Optionally invokes bids-validator if installed.

        Args:
            bids_dir: Path to the BIDS root directory.
            use_validator: If True, attempt to run bids-validator (requires npm).
        """
        root = Path(bids_dir)
        if not root.is_dir():
            return {"ok": False, "error": f"BIDS directory not found: {bids_dir}"}

        issues: List[Dict[str, str]] = []
        subjects: List[str] = []
        sessions: List[str] = []
        modalities: set[str] = set()
        nifti_count = 0

        # Check required files
        for req in BIDS_REQUIRED_FILES:
            if not (root / req).exists():
                issues.append({"level": "warning", "file": req, "issue": f"Missing recommended file: {req}"})

        # Walk subject directories
        for sub_path in sorted(root.glob("sub-*")):
            if not sub_path.is_dir():
                continue
            if not SUB_PATTERN.match(sub_path.name):
                issues.append({"level": "error", "file": str(sub_path.relative_to(root)),
                               "issue": f"Invalid subject directory name: {sub_path.name}"})
                continue

            subjects.append(sub_path.name)

            # Check for session directories
            ses_dirs = list(sub_path.glob("ses-*"))
            if ses_dirs:
                for ses_path in sorted(ses_dirs):
                    if not ses_path.is_dir():
                        continue
                    if not SES_PATTERN.match(ses_path.name):
                        issues.append({"level": "error", "file": str(ses_path.relative_to(root)),
                                       "issue": f"Invalid session directory name: {ses_path.name}"})
                        continue
                    sessions.append(ses_path.name)
                    m, n = self._scan_modality_dir(ses_path, root)
                    modalities.update(m)
                    nifti_count += n
            else:
                m, n = self._scan_modality_dir(sub_path, root)
                modalities.update(m)
                nifti_count += n

        # Deduplicate sessions
        sessions = sorted(set(sessions))

        # Run bids-validator if requested
        validator_result: Optional[Dict[str, Any]] = None
        if use_validator:
            validator_result = self._run_bids_validator(bids_dir)

        return {
            "ok": True,
            "bids_dir": str(root),
            "subject_count": len(subjects),
            "session_count": len(sessions),
            "modalities": sorted(modalities),
            "nifti_count": nifti_count,
            "subjects": sorted(subjects),
            "sessions": sessions,
            "issues": issues[:50],  # cap at 50
            "issue_count": len(issues),
            "valid": len([i for i in issues if i["level"] == "error"]) == 0,
            "bids_validator": validator_result,
        }

    def _scan_modality_dir(self, dir_path: Path, root: Path) -> tuple[set[str], int]:
        """Scan a subject/session directory for modality subdirectories and NIfTI files."""
        mods: set[str] = set()
        nifti_count = 0
        for item in sorted(dir_path.iterdir()):
            if item.is_dir() and item.name in BIDS_MODALITIES:
                mods.add(item.name)
                nifti_count += sum(1 for _ in item.glob("*.nii.gz"))
                nifti_count += sum(1 for _ in item.glob("*.nii"))
        return mods, nifti_count

    def _run_bids_validator(self, bids_dir: str) -> Optional[Dict[str, Any]]:
        """Attempt to run bids-validator (npm package)."""
        try:
            result = _run(["bids-validator", "--json", str(bids_dir)], timeout=120)
            if result["ok"]:
                try:
                    return json.loads(result["stdout"])
                except json.JSONDecodeError:
                    return {"raw_output": result["stdout"]}
            return {"error": result.get("stderr") or result.get("error")}
        except Exception as e:
            logger.warning("bids-validator not available: %s", e)
            return None

    # ── graphmri Script Generation ─────────────────────────────────────────

    def generate_graphmri_script(
        self,
        subject_id: str,
        bids_dir: str,
        output_dir: str,
        config: Dict[str, Any] | None = None,
        connectivity_matrices: List[str] | None = None,
    ) -> Dict[str, Any]:
        """Generate a Python script that runs graphmri analysis for a subject.

        The generated script calls graphmri CLI with the specified configuration.
        Intended for execution via `sros-skill data run-script` or Hermes Workflows.

        Args:
            subject_id: Subject label (e.g. sub-001).
            bids_dir: Path to BIDS directory.
            output_dir: Directory for output files.
            config: graphmri configuration dict (merged with defaults).
            connectivity_matrices: List of matrix types to compute.
        """
        cfg = dict(GRAPHMRI_DEFAULT_CONFIG)
        if config:
            cfg.update(config)

        matrices = connectivity_matrices or cfg["edge_weights"]
        if not matrices:
            matrices = ["fisher_z"]

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        script_lines = [
            "#!/usr/bin/env python3",
            '"""Auto-generated graphmri analysis script — SROS neuro server."""',
            "",
            "import json",
            "import sys",
            "from pathlib import Path",
            "",
            f"SUBJECT_ID = {json.dumps(subject_id)}",
            f"BIDS_DIR = {json.dumps(str(Path(bids_dir).resolve()))}",
            f"OUTPUT_DIR = {json.dumps(str(output_path.resolve()))}",
            f"CONFIG = {json.dumps(cfg, indent=2)}",
            "",
            "# Locate subject BIDS data",
            f"sub_path = Path(BIDS_DIR) / SUBJECT_ID",
            "if not sub_path.exists():",
            "    print(f'ERROR: Subject directory not found: {sub_path}')",
            "    sys.exit(1)",
            "",
            "# Find T1w image",
            "t1w_files = sorted(sub_path.glob('ses-*/anat/*T1w.nii.gz')) + sorted(sub_path.glob('anat/*T1w.nii.gz'))",
            "if not t1w_files:",
            "    print(f'WARNING: No T1w found for {SUBJECT_ID}')",
            "t1w_path = str(t1w_files[0]) if t1w_files else None",
            "",
            "# Determine atlas parcellation",
            f"atlas = CONFIG.get('atlas', 'aal')",
            f"n_rois = CONFIG.get('parcellation', 116)",
            "",
            'output_prefix = str(Path(OUTPUT_DIR) / f"{SUBJECT_ID}_graphmri")',
            "",
            "# Build graphmri command",
            "cmd = [",
            '    "graphmri",',
            '    "--subject", SUBJECT_ID,',
            '    "--atlas", atlas,',
            '    "--parcellation", str(n_rois),',
            '    "--output", output_prefix,',
            "]",
        ]

        for m in matrices:
            script_lines.append(f'cmd += ["--edge-weight", {json.dumps(m)}]')

        script_lines.extend([
            "",
            "if t1w_path:",
            '    cmd += ["--t1w", t1w_path]',
            "",
            "# Dry-run: print command (actual execution via Hermes or sros-skill)",
            "print('Generated graphmri command:')",
            "print(' '.join(cmd))",
            "",
            "# Output configuration for downstream consumers",
            "manifest = {",
            '    "subject_id": SUBJECT_ID,',
            '    "t1w_path": t1w_path,',
            '    "atlas": atlas,',
            '    "n_rois": n_rois,',
            "    'command': ' '.join(cmd),",
            "}",
            f"manifest_path = Path(OUTPUT_DIR) / f'{subject_id}_manifest.json'",
            "manifest_path.write_text(json.dumps(manifest, indent=2))",
            "print(f'Manifest -> {manifest_path}')",
        ])

        script_path = output_path / f"graphmri_{subject_id}.py"
        script_path.write_text("\n".join(script_lines) + "\n", encoding="utf-8")

        return {
            "ok": True,
            "subject_id": subject_id,
            "script_path": str(script_path),
            "bids_dir": str(Path(bids_dir).resolve()),
            "output_dir": str(output_path),
            "config": cfg,
            "matrices": matrices,
        }

    # ── fMRIPrep Batch ────────────────────────────────────────────────────

    def generate_fmriprep_batch(
        self,
        subject_ids: List[str],
        bids_dir: str,
        output_dir: str,
        work_dir: str | None = None,
        fs_license: str | None = None,
        template: str | None = None,
    ) -> Dict[str, Any]:
        """Generate fMRIPrep Slurm scripts for a list of subjects.

        Can use the built-in fMRIPrep template or a custom template.
        For individual subject script generation, delegates to HPCHandler.

        Args:
            subject_ids: List of subject labels.
            bids_dir: BIDS root directory.
            output_dir: Output directory for generated scripts.
            work_dir: fMRIPrep working directory.
            fs_license: Path to FreeSurfer license file.
            template: Optional custom Slurm template path.
        """
        from sros.servers.hpc.handler import HPCHandler

        script_paths: List[str] = []

        # Resolve template path
        if template:
            tmpl_path = template
        else:
            from sros.servers.hpc.handler import DEFAULT_TEMPLATE_DIR
            tmpl_path = str(DEFAULT_TEMPLATE_DIR / "fmriprep_template.slurm")

        if not Path(tmpl_path).exists():
            return {"ok": False, "error": f"Template not found: {tmpl_path}"}

        hpc = HPCHandler(dry_run=True)

        substitutions: Dict[str, str] = {
            "BIDS_DIR": str(Path(bids_dir).resolve()),
            "OUTPUT_DIR": str(Path(output_dir).resolve()),
        }
        if work_dir:
            substitutions["WORK_DIR"] = str(Path(work_dir).resolve())
        if fs_license:
            substitutions["FS_LICENSE"] = str(Path(fs_license).resolve())

        for sid in subject_ids:
            result = hpc.generate_job_script(
                template_path=tmpl_path,
                subject_id=sid,
                output_dir=str(Path(output_dir).resolve()),
                substitutions=substitutions,
            )
            if result.get("ok"):
                script_paths.append(result["script_path"])
            else:
                return {
                    "ok": False,
                    "error": f"Failed for {sid}: {result.get('error')}",
                    "scripts": script_paths,
                }

        return {
            "ok": True,
            "count": len(script_paths),
            "scripts": script_paths,
            "template": tmpl_path,
            "bids_dir": bids_dir,
            "output_dir": output_dir,
        }
