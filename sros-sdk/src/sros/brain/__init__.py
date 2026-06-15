"""sros.brain — Brain network dataset DSL.

Chainable Fluent API wrapping GraphMRI-Lite CLI for connectome extraction.
"""

from .dataset import BrainGraphDataset

__all__ = ["BrainGraphDataset"]
