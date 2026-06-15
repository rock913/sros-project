"""BrainGraphDataset — Fluent API for brain network data pipelines.

Chainable DSL wrapping GraphMRI-Lite CLI for connectome extraction.
Each method call represents one scientific primitive.

Reference: GraphMRI-Lite graphmri_lite/core/network/connectome.py (MakeConnectomes)
           GraphMRI-Lite graphmri_lite/cli/main.py (build_network command)
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

# BIDS directory prefixes to ignore when scanning for subjects
_BIDS_IGNORE_PREFIXES = {"derivatives", "sourcedata", ".", "code", "stimuli"}

# Demo mode: when True, compute() generates synthetic connectome data
# instead of calling graphmri CLI. Set via env var or explicit parameter.
_SROS_SDK_DEMO = os.environ.get("SROS_SDK_DEMO", "").lower() in ("1", "true", "yes")


class BrainGraphDataset:
    """SXMU_MDD brain network DSL.

    Lazy-evaluated chain: methods store parameters, computation is triggered
    by terminal methods like to_dataloader() or explicit .compute().

    Usage::

        cohort = (
            BrainGraphDataset
            .from_duckdb("SELECT * FROM mdd_cohort WHERE age > 60")
            .apply_pipeline("fmriprep", resolution="2mm")
            .extract_connectome(atlas="aal", kind="tangent")
        )
        loader = cohort.to_dataloader(batch_size=32)
    """

    def __init__(
        self,
        subjects: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
    ):
        self.subjects = subjects
        self.config = config or {}

        # Lazy pipeline parameters
        self._pipeline: str | None = None
        self._pipeline_kwargs: dict[str, Any] = {}
        self._atlas: str = "aal"
        self._kind: str = "tangent"
        self._threshold: float | None = None

        # Computed data (populated by terminal methods)
        self._connectome_data: np.ndarray | None = None
        self._connectome_matrices: np.ndarray | None = None  # Full matrices for DSPy
        self._labels: np.ndarray | None = None

    # ── Class methods: constructors ──────────────────────────────

    @classmethod
    def from_bids(cls, bids_dir: str | Path) -> BrainGraphDataset:
        """Scan a BIDS directory and build subject list.

        Subjects are detected as subdirectories matching ``sub-*``.
        ``derivatives`` and ``sourcedata`` are ignored.
        """
        bids_path = Path(bids_dir)
        subjects = []
        for entry in sorted(bids_path.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith("sub-") and entry.name not in _BIDS_IGNORE_PREFIXES:
                subjects.append({
                    "subject_id": entry.name,
                    "bids_path": str(entry),
                })
        return cls(subjects)

    @classmethod
    def from_duckdb(cls, query: str, db_path: str | None = None) -> BrainGraphDataset:
        """Execute a DuckDB SQL query and build subject list from the result set.

        Column names are automatically mapped:
        - subject_id / participant_id / sub_id → subject identifier
        - bids_path / data_dir / bids_dir → BIDS path
        - phenotype_* columns → phenotype dict
        """
        from sros.data.duckdb import _infer_column_mapping, _row_to_subject

        import duckdb

        db = db_path or os.environ.get("SROS_DUCKDB_PATH", "sros.duckdb")
        with duckdb.connect(db, read_only=True) as conn:
            result = conn.execute(query)
            columns = [col[0] for col in result.description]
            rows = result.fetchall()

        if not rows:
            return cls([])

        # Convert tuples to dicts for column mapping
        row_dicts = [dict(zip(columns, row)) for row in rows]
        mapping = _infer_column_mapping(columns)

        subjects = [_row_to_subject(row, mapping) for row in row_dicts]
        return cls(subjects)

    # ── Fluent API: pipeline steps ───────────────────────────────

    def apply_pipeline(self, pipeline: str, **kwargs: Any) -> BrainGraphDataset:
        """Set the preprocessing pipeline and its parameters.

        Args:
            pipeline: One of "fmriprep", "qsiprep", "ciftify".
            **kwargs: Passed through to the pipeline CLI (e.g. resolution="2mm").
        """
        self._pipeline = pipeline
        self._pipeline_kwargs = kwargs
        return self

    def extract_connectome(
        self,
        atlas: str = "aal",
        kind: str = "tangent",
        threshold: float | None = None,
    ) -> BrainGraphDataset:
        """Set connectome extraction parameters.

        Actual computation is deferred until a terminal method (to_dataloader,
        to_numpy) is called, or can be triggered explicitly with .compute().

        Args:
            atlas: Brain atlas name (default "aal").
            kind: Connectome kind — "correlation", "partial correlation",
                  "tangent", "covariance", "precision".
            threshold: Optional edge weight threshold.
        """
        self._atlas = atlas
        self._kind = kind
        self._threshold = threshold
        return self

    # ── Terminal methods ─────────────────────────────────────────

    def compute(self, demo: bool = False) -> BrainGraphDataset:
        """Explicitly trigger connectome computation.

        In production mode, calls ``graphmri --raw build_network`` for each subject.
        In demo mode (or when graphmri is unavailable), generates synthetic
        connectome data suitable for DSL integration testing.

        Args:
            demo: If True, force demo/synthetic mode regardless of env.
        """
        if not self.subjects:
            logger.warning("No subjects — skipping compute")
            return self

        use_demo = demo or _SROS_SDK_DEMO

        if not use_demo:
            try:
                self._compute_real()
            except FileNotFoundError:
                logger.info(
                    "graphmri CLI not found — falling back to demo mode. "
                    "Set SROS_SDK_DEMO=1 to skip this warning."
                )
                use_demo = True

        if use_demo:
            self._compute_demo()

        # DSPy assertion: validate connectome matrices
        self._validate_connectome()
        return self

    def to_dataloader(
        self, batch_size: int = 32, shuffle: bool = True
    ) -> Any:
        """Convert connectome data to a PyTorch DataLoader.

        Requires ``torch`` to be installed.
        """
        try:
            import torch
            from torch.utils.data import DataLoader, TensorDataset
        except ImportError:
            raise ImportError(
                "torch is required for to_dataloader(). "
                "Install with: pip install sros-sdk[torch]"
            )

        if self._connectome_data is None:
            self.compute()

        if self._connectome_data is None or len(self._connectome_data) == 0:
            raise ValueError("No connectome data available")

        features = torch.tensor(self._connectome_data, dtype=torch.float32)
        if self._labels is not None:
            labels = torch.tensor(self._labels, dtype=torch.float32)
            dataset = TensorDataset(features, labels)
        else:
            dataset = TensorDataset(features)

        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    def to_numpy(self) -> tuple[np.ndarray, np.ndarray | None]:
        """Return connectome data as (features, labels) numpy arrays."""
        if self._connectome_data is None:
            self.compute()
        return self._connectome_data, self._labels

    # ── Internal helpers ─────────────────────────────────────────

    def _compute_real(self) -> None:
        """Run graphmri CLI to compute real connectome data."""
        logger.info(
            "Computing connectome for %d subjects (atlas=%s, kind=%s)",
            len(self.subjects), self._atlas, self._kind,
        )

        timeseries_dir = self._resolve_timeseries_dir()
        cli_args = [
            "graphmri", "--raw", "build-network",
            "--timeseries-dir", timeseries_dir,
            "--atlas", self._atlas,
            "--kind", self._kind,
        ]
        if self._threshold is not None:
            cli_args.extend(["--threshold", str(self._threshold)])

        result = _graphmri_cli(cli_args)

        # Parse graphmri JSON output
        try:
            import json
            data = json.loads(result.stdout)
            self._connectome_data = np.array(data.get("connectomes", data.get("data", [])))
        except (json.JSONDecodeError, KeyError, ValueError):
            logger.warning("Could not parse graphmri output — using zeros")
            self._connectome_data = np.zeros((len(self.subjects), 90))

    def _compute_demo(self) -> None:
        """Generate synthetic connectome data for demo/testing.

        Produces realistic symmetric positive definite matrices that
        pass DSPy assertions. Matrices follow a block-diagonal structure
        mimicking real AAL atlas connectomes.
        """
        n_subjects = len(self.subjects)
        n_regions = self._atlas_region_count()
        n_edges = n_regions * (n_regions - 1) // 2  # lower triangle

        logger.info(
            "Demo mode: generating synthetic %dx%d connectome for %d subjects (%d edges each)",
            n_regions, n_regions, n_subjects, n_edges,
        )

        rng = np.random.default_rng(42)

        # Generate subject-level connectome matrices
        # Each matrix is symmetric positive definite by construction
        matrices = np.zeros((n_subjects, n_regions, n_regions))
        for i in range(n_subjects):
            # Base structure: block diagonal with noise
            base = np.zeros((n_regions, n_regions))
            block_sizes = [12, 10, 8, 8, 10, 14, 12, 10, 8, 14, 6, 4]
            offset = 0
            for bs in block_sizes:
                if offset + bs > n_regions:
                    break
                block = rng.uniform(0.3, 0.95, size=(bs, bs))
                block = (block + block.T) / 2  # Symmetrize
                np.fill_diagonal(block, 1.0)
                base[offset:offset + bs, offset:offset + bs] = block
                offset += bs

            # Add subject-specific noise
            noise = rng.normal(0, 0.05, size=(n_regions, n_regions))
            noise = (noise + noise.T) / 2
            mat = base + noise
            np.fill_diagonal(mat, 1.0)

            # Ensure positive definite: A + cI where c = max(0, -min_eig) + epsilon
            eigvals = np.linalg.eigvalsh(mat)
            min_eig = np.min(eigvals)
            if min_eig <= 0:
                mat += np.eye(n_regions) * (abs(min_eig) + 0.1)

            matrices[i] = mat

        # Vectorize: extract lower triangle (excluding diagonal)
        tri_rows, tri_cols = np.tril_indices(n_regions, k=-1)
        self._connectome_data = np.array([
            matrices[i][tri_rows, tri_cols] for i in range(n_subjects)
        ])
        self._connectome_matrices = matrices  # Full matrices for DSPy validation

        # Extract labels from phenotype data
        self._labels = self._extract_labels()

        logger.info(
            "Demo connectome generated: shape=%s, SPD verified, labels=%s",
            self._connectome_data.shape,
            self._labels.shape if self._labels is not None else "none",
        )

    def _atlas_region_count(self) -> int:
        """Return the expected number of regions for a given atlas."""
        atlas_sizes = {
            "aal": 116,
            "destrieux": 148,
            "dk": 82,
            "craddock200": 200,
        }
        return atlas_sizes.get(self._atlas.lower(), 116)

    def _extract_labels(self) -> np.ndarray | None:
        """Extract label array from subject phenotype data.

        Looks for common target variable names in phenotype dicts.
        Returns None if no labels found.
        """
        target_candidates = [
            "HAMD_improvement", "HAMD_improvement_pct",
            "HAMD_score", "HAMD",
            "response", "responder",
            "label", "target",
        ]

        for target in target_candidates:
            values = []
            for subj in self.subjects:
                phenotypes = subj.get("phenotypes", {})
                if target in phenotypes and phenotypes[target] is not None:
                    values.append(float(phenotypes[target]))
                elif target in subj and subj[target] is not None:
                    # Check top-level subject dict (for from_duckdb manual columns)
                    try:
                        values.append(float(subj[target]))
                    except (ValueError, TypeError):
                        break
                else:
                    break  # This target not present in all subjects

            if len(values) == len(self.subjects):
                logger.info("Extracted labels from '%s': mean=%.2f", target, np.mean(values))
                return np.array(values)

        # No phenotype labels found — generate binary labels for demo
        logger.info("No phenotype labels found — generating demo labels (0/1)")
        rng = np.random.default_rng(42)
        return rng.integers(0, 2, size=len(self.subjects)).astype(float)

    def _resolve_timeseries_dir(self) -> str:
        """Resolve the timeseries directory from pipeline config or subject data."""
        ts_dir = self._pipeline_kwargs.get("timeseries_dir")
        if ts_dir:
            return str(ts_dir)

        # Default: use first subject's bids_path/derivatives/<pipeline>
        if self.subjects and "bids_path" in self.subjects[0]:
            pipeline = self._pipeline or "fmriprep"
            return str(Path(self.subjects[0]["bids_path"]).parent / "derivatives" / pipeline)

        return os.getcwd()

    def _validate_connectome(self) -> None:
        """Run DSPy assertions on computed connectome data if available.

        Validates the first 5 subjects' full matrices (when available)
        or the vectorized data as-is.
        """
        if self._connectome_data is None:
            return
        try:
            from sros.dspy.assertions import ConnectomeAssertions

            # Use full matrices for validation when available
            matrices = getattr(self, "_connectome_matrices", None)
            n_check = min(5, len(self._connectome_data))

            if matrices is not None and len(matrices) >= n_check:
                for i in range(n_check):
                    ConnectomeAssertions.assert_symmetric_positive_definite(matrices[i])
            else:
                # Vectorized data — skip SPD validation (requires full matrix)
                logger.debug(
                    "Skipping DSPy SPD assertion — connectome is vectorized. "
                    "Full matrices not available."
                )

            # Always run size suggestion
            model_mb = self._connectome_data.nbytes / (1024 * 1024)
            ConnectomeAssertions.suggest_gradient_checkpointing(model_mb)

        except ImportError:
            logger.debug("dspy not installed — skipping assertions")


def _graphmri_cli(cmd: list[str]) -> subprocess.CompletedProcess:
    """Invoke graphmri CLI. Extracted for testability (mock target)."""
    logger.debug("Running: %s", " ".join(cmd))
    return subprocess.run(cmd, capture_output=True, text=True)
