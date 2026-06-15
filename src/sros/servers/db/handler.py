from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)

# Default schema embedded in SROS package
DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "config" / "duckdb" / "schema.sql"


def _serialize_rows(rows) -> List[Any]:
    """Convert DuckDB result rows to JSON-serializable lists."""
    result = []
    for row in rows:
        converted = []
        for v in row:
            if hasattr(v, "isoformat"):
                converted.append(v.isoformat())
            elif isinstance(v, bytes):
                converted.append(v.decode("utf-8", errors="replace"))
            else:
                converted.append(v)
        result.append(converted)
    return result


class DBHandler:
    """DuckDB-backed data ingestion and query handler.

    Provides structured data ingestion from BIDS directories, TSV participants files,
    and Excel clinical scales into a DuckDB database, plus SQL query execution.
    """

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(self.db_path))

    def close(self):
        self.con.close()

    # ── Schema Initialization ──────────────────────────────────────────────

    def init_schema(self, schema_path: str | Path | None = None) -> Dict[str, Any]:
        """Execute DDL from a SQL schema file."""
        path = Path(schema_path) if schema_path else DEFAULT_SCHEMA_PATH
        if not path.exists():
            return {"ok": False, "error": f"Schema file not found: {path}"}
        try:
            sql = path.read_text(encoding="utf-8")
            self.con.execute(sql)
            return {"ok": True, "schema_path": str(path)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── Ingestion ──────────────────────────────────────────────────────────

    def ingest(
        self,
        source_dir: str | Path,
        bids_dir: str | None = None,
        participants: str | None = None,
        clinical: str | None = None,
        schema_path: str | Path | None = None,
    ) -> Dict[str, Any]:
        """Main ingestion entry point: BIDS + participants + clinical → DuckDB.

        Returns counts of ingested records per table.
        """
        source = Path(source_dir)
        if not source.exists():
            return {"ok": False, "error": f"Source directory not found: {source_dir}"}

        counts: Dict[str, int] = {}

        try:
            # 1. Initialize schema
            init_result = self.init_schema(schema_path)
            if not init_result["ok"]:
                return {"ok": False, "error": f"Schema init failed: {init_result['error']}"}

            # 2. Ingest participants
            if participants:
                parts_path = source / participants
                if parts_path.exists():
                    counts["subjects_count"] = self._ingest_participants(parts_path)
                else:
                    logger.warning("Participants file not found: %s", parts_path)

            # 3. Ingest BIDS directory
            if bids_dir:
                bids_path = source / bids_dir
                if bids_path.exists():
                    auto_generate_ids = participants is None
                    counts["mri_scans_count"] = self._ingest_bids(bids_path, auto_generate_subjects=auto_generate_ids)
                else:
                    logger.warning("BIDS directory not found: %s", bids_path)

            # 4. Ingest clinical Excel
            if clinical:
                clinical_path = source / clinical
                if clinical_path.exists():
                    counts["clinical_count"] = self._ingest_clinical(clinical_path)
                else:
                    logger.warning("Clinical file not found: %s", clinical_path)

            return {"ok": True, **counts}

        except Exception as e:
            logger.exception("Ingestion failed")
            return {"ok": False, "error": str(e)}

    def _ingest_participants(self, tsv_path: Path) -> int:
        """Parse participants.tsv and populate the subjects table."""
        df = pd.read_csv(tsv_path, sep="\t", dtype=str)
        rows = []
        for _, r in df.iterrows():
            subject_id = str(r.get("participant_id", ""))
            if not subject_id:
                continue
            rows.append({
                "subject_id": subject_id,
                "cohort": str(r.get("cohort", "")),
                "age_group": str(r.get("age_group", "")),
                "sex": str(r.get("sex", "")),
                "age_at_baseline": float(r.get("age", 0) or 0),
                "group_status": str(r.get("group_status", "")),
                "intervention_type": str(r.get("intervention_type", "")),
            })

        for row in rows:
            self.con.execute(
                """INSERT OR REPLACE INTO subjects
                   (subject_id, cohort, age_group, sex, age_at_baseline, group_status, intervention_type)
                   VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                [row["subject_id"], row["cohort"], row["age_group"], row["sex"],
                 row["age_at_baseline"], row["group_status"], row["intervention_type"]],
            )
        return len(rows)

    def _ingest_bids(self, bids_dir: Path, auto_generate_subjects: bool = False) -> int:
        """Walk BIDS directory tree and populate mri_scans table.

        Parses sub-*/ses-*/ directories and records file paths.
        """
        scan_id = 0
        count = 0
        subject_ids_seen: set[str] = set()

        for bids_path in sorted(bids_dir.glob("sub-*")):
            subject_id = bids_path.name
            if not bids_path.is_dir():
                continue

            for ses_path in sorted(bids_path.glob("ses-*")):
                session_label = ses_path.name.replace("ses-", "")
                for modality_dir in sorted(ses_path.iterdir()):
                    if not modality_dir.is_dir():
                        continue
                    modality = modality_dir.name
                    nifti_files = sorted(modality_dir.glob("*.nii.gz")) + sorted(modality_dir.glob("*.nii"))
                    for nii in nifti_files:
                        scan_id += 1
                        self.con.execute(
                            """INSERT OR REPLACE INTO mri_scans
                               (scan_id, subject_id, session_label, modality, bids_path, file_size_gb)
                               VALUES ($1, $2, $3, $4, $5, $6)""",
                            [
                                scan_id,
                                subject_id,
                                session_label,
                                modality,
                                str(nii.relative_to(bids_dir)),
                                nii.stat().st_size / (1024 ** 3) if nii.exists() else 0.0,
                            ],
                        )
                        count += 1
                        subject_ids_seen.add(subject_id)

                    # Also record the directory even if no .nii found (marker entry)
                    if not nifti_files:
                        scan_id += 1
                        self.con.execute(
                            """INSERT OR REPLACE INTO mri_scans
                               (scan_id, subject_id, session_label, modality, bids_path, file_size_gb)
                               VALUES ($1, $2, $3, $4, $5, 0.0)""",
                            [scan_id, subject_id, session_label, modality,
                             str(modality_dir.relative_to(bids_dir))],
                        )
                        count += 1
                        subject_ids_seen.add(subject_id)

        # Auto-generate subject entries for subjects found in BIDS but not in participants.tsv
        if auto_generate_subjects and subject_ids_seen:
            existing = {
                r[0] for r in
                self.con.execute("SELECT subject_id FROM subjects").fetchall()
            }
            for sid in subject_ids_seen - existing:
                self.con.execute(
                    """INSERT OR REPLACE INTO subjects (subject_id, cohort)
                       VALUES ($1, 'unknown')""",
                    [sid],
                )

        return count

    def _ingest_clinical(self, xlsx_path: Path) -> int:
        """Parse clinical Excel file and populate clinical_scales table."""
        df = pd.read_excel(xlsx_path, dtype=str)
        assessment_id = 0
        count = 0

        for _, r in df.iterrows():
            assessment_id += 1
            subject_id = str(r.get("subject_id", ""))
            if not subject_id:
                continue

            self.con.execute(
                """INSERT OR REPLACE INTO clinical_scales
                   (assessment_id, subject_id, session_label, scale_name, scale_score, assessment_date)
                   VALUES ($1, $2, $3, $4, $5, $6)""",
                [
                    assessment_id,
                    subject_id,
                    str(r.get("session_label", "")),
                    str(r.get("scale_name", "")),
                    float(r.get("scale_score", 0) or 0),
                    str(r.get("assessment_date", "")),
                ],
            )
            count += 1

        return count

    # ── SQL Query ──────────────────────────────────────────────────────────

    def query(
        self,
        sql: str,
        params: List[Any] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Execute a SELECT query and return JSON-serializable results."""
        try:
            sql_stripped = sql.strip().rstrip(";")
            upper = sql_stripped.upper()

            # Safety: only allow SELECT
            if not upper.startswith("SELECT"):
                return {"ok": False, "error": "Only SELECT queries are permitted"}

            # Add LIMIT/OFFSET if not present
            if "LIMIT" not in upper:
                sql_stripped += f" LIMIT {int(limit)}"
                if int(offset) > 0:
                    sql_stripped += f" OFFSET {int(offset)}"

            if params:
                result = self.con.execute(sql_stripped, list(params))
            else:
                result = self.con.execute(sql_stripped)

            columns = [desc[0] for desc in result.description]
            rows = _serialize_rows(result.fetchall())

            return {"ok": True, "columns": columns, "rows": rows, "count": len(rows)}

        except Exception as e:
            logger.exception("SQL query failed")
            return {"ok": False, "error": str(e)}
