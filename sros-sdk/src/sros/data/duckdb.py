"""DuckDB connector — SQL query to BrainGraphDataset column mapping.

Reference: SROS config/duckdb/schema.sql (8-table DDL)
           SROS src/sros/domain/schemas/ (Pydantic data models)
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Known column name variants for subject identifier
_SUBJECT_ID_CANDIDATES = [
    "subject_id",
    "participant_id",
    "sub_id",
    "subject",
    "participant",
    "sub",
]

# Known column name variants for BIDS/data path
_PATH_CANDIDATES = [
    "bids_path",
    "data_dir",
    "bids_dir",
    "path",
    "directory",
    "data_path",
    "bids",
]

# Columns that are detected as phenotype data
_PHENOTYPE_PREFIX = "phenotype_"


def _infer_column_mapping(columns: list[str]) -> dict[str, Any]:
    """Infer semantic meaning of column names.

    Returns:
        dict with keys:
        - subject_id: str | None
        - bids_path: str | None
        - phenotypes: list[str]
    """
    mapping: dict[str, Any] = {
        "subject_id": None,
        "bids_path": None,
        "phenotypes": [],
    }

    for col in columns:
        col_lower = col.lower().strip()

        # Check subject ID candidates
        if mapping["subject_id"] is None:
            for candidate in _SUBJECT_ID_CANDIDATES:
                if col_lower == candidate:
                    mapping["subject_id"] = col
                    break

        # Check path candidates
        if mapping["bids_path"] is None:
            for candidate in _PATH_CANDIDATES:
                if col_lower == candidate:
                    mapping["bids_path"] = col
                    break

        # Check phenotype columns
        if col_lower.startswith(_PHENOTYPE_PREFIX):
            mapping["phenotypes"].append(col)

    return mapping


def _row_to_subject(row: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    """Convert a DuckDB row dict to a BrainGraphDataset subject dict.

    Phenotype columns are extracted into a nested ``phenotypes`` dict
    with the ``phenotype_`` prefix stripped from keys.
    """
    subject: dict[str, Any] = {}

    # Map identifier
    subject["subject_id"] = row.get(mapping["subject_id"]) if mapping["subject_id"] else None

    # Map BIDS path
    if mapping["bids_path"]:
        subject["bids_path"] = row.get(mapping["bids_path"])

    # Map phenotypes
    phenotypes: dict[str, Any] = {}
    for pcol in mapping["phenotypes"]:
        key = pcol[len(_PHENOTYPE_PREFIX):]  # Strip prefix
        phenotypes[key] = row.get(pcol)
    if phenotypes:
        subject["phenotypes"] = phenotypes

    # Preserve all other columns as-is (non-phenotype metadata)
    phenotype_set = set(mapping["phenotypes"])
    for col, val in row.items():
        if col == mapping["subject_id"]:
            continue
        if col == mapping.get("bids_path"):
            continue
        if col in phenotype_set:
            continue
        subject[col] = val

    return subject
