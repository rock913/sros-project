"""DSPy assertions for scientific constraint validation.

Hard constraints (Assert) and soft suggestions (Suggest) embedded in
DSL operators to catch invalid scientific data early.

Reference: GraphMRI-Lite graphmri_lite/core/plugins/base.py
           (BasePipelineStage.validate_requirements)
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ConnectomeAssertions:
    """Scientific validity checks for brain connectome matrices.

    Hard assertions (Assert) halt execution on invalid data.
    Soft suggestions (Suggest) emit warnings for suboptimal configurations.
    """

    @staticmethod
    def assert_symmetric_positive_definite(matrix: np.ndarray) -> None:
        """Hard assertion: connectome matrix must be symmetric positive definite.

        Non-symmetric / non-SPD matrices indicate data corruption or wrong
        connectome kind parameter (e.g. using "correlation" where "tangent"
        is required).
        """
        # Symmetry check
        is_symmetric = np.allclose(matrix, matrix.T, atol=1e-6)
        if not is_symmetric:
            try:
                import dspy
                dspy.Assert(
                    is_symmetric,
                    msg=f"Connectome matrix must be symmetric. "
                        f"Max asymmetry: {np.max(np.abs(matrix - matrix.T)):.2e}",
                )
            except ImportError:
                logger.warning(
                    "Connectome matrix is not symmetric (max diff=%.2e). "
                    "Install dspy for hard enforcement.",
                    np.max(np.abs(matrix - matrix.T)),
                )

        # Positive definiteness check
        try:
            eigenvalues = np.linalg.eigvalsh(matrix)
            is_pd = np.all(eigenvalues > 0)
            if not is_pd:
                min_eig = np.min(eigenvalues)
                try:
                    import dspy
                    dspy.Assert(
                        is_pd,
                        msg=f"Connectome matrix must be positive definite. "
                            f"Min eigenvalue: {min_eig:.2e}",
                    )
                except ImportError:
                    logger.warning(
                        "Connectome matrix is not positive definite (min eig=%.2e). "
                        "Install dspy for hard enforcement.",
                        min_eig,
                    )
        except np.linalg.LinAlgError as e:
            logger.error("Eigenvalue computation failed: %s", e)

    @staticmethod
    def suggest_gradient_checkpointing(model_size_mb: float) -> None:
        """Soft suggestion: large models should enable gradient checkpointing.

        Only emits a warning/Suggest — does not halt execution.
        """
        if model_size_mb > 1000:
            msg = (
                f"Model size {model_size_mb:.0f} MB > 1 GB. "
                f"Consider setting gradient_checkpointing=True to reduce memory usage."
            )
            try:
                import dspy
                dspy.Suggest(False, msg=msg)
            except ImportError:
                logger.info(msg)
