"""sros.ml — GNN trainer with auto infrastructure detection.

infra_strategy="auto" detects Slurm / Docker GPU / local GPU / CPU at runtime.
"""

from .trainer import GNNTrainer, InfraStrategy, SUPPORTED_MODELS

__all__ = ["GNNTrainer", "InfraStrategy", "SUPPORTED_MODELS"]
