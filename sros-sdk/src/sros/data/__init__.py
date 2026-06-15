"""sros.data — Data connectors.

DuckDB query → BrainGraphDataset column mapping.
"""

from .duckdb import _infer_column_mapping, _row_to_subject

__all__ = ["_infer_column_mapping", "_row_to_subject"]
