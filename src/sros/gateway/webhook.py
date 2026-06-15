"""Feishu Webhook endpoint — SROS-side control plane for Feishu Bitable → GraphMRI-Lite.

Receives webhook POST from Feishu automation rules, translates feishu fields
to GraphMRI-Lite job config, and submits via background task (non-blocking).

Reference: meta-docs/proposals/pending/GraphMRI-Lite-Feishu-Control-Plane.md
"""

from __future__ import annotations

import logging
import os
import uuid
from typing import Any

import requests
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["feishu"])

# GraphMRI-Lite job submission endpoint (configurable)
GRAPHMRI_LITE_URL = os.environ.get("GRAPHMRI_LITE_URL", "http://localhost:9021")
GRAPHMRI_LITE_TIMEOUT = int(os.environ.get("GRAPHMRI_LITE_TIMEOUT", "30"))


class FeishuWebhookPayload(BaseModel):
    """Payload from Feishu automation webhook trigger.

    Feishu bitable automation rule:
      Condition: status = "request_execute"
      Action: POST webhook → SROS /webhook/execute
    """

    record_id: str
    table_id: str
    fields: dict[str, Any]


# ── Field translation ────────────────────────────────────────────

# Maps feishu bitable field names → GraphMRI-Lite job config keys
_FIELD_MAP: dict[str, str] = {
    "project": "project",
    "analysis_type": "analysis_type",
    "subject_filter_sql": "subject_filter_sql",
    "atlas": "atlas",
    "model": "model",
    "target": "target",
    "被试筛选SQL": "subject_filter_sql",
    "分析类型": "analysis_type",
    "图谱": "atlas",
    "模型": "model",
    "预测目标": "target",
    "项目": "project",
    "被试数": "n_subjects",
}

# Analysis type → GraphMRI-Lite pipeline mapping
_PIPELINE_MAP: dict[str, str] = {
    "预处理": "fmriprep",
    "preprocess": "fmriprep",
    "脑网络": "build_network",
    "brain_network": "build_network",
    "GNN预测": "gnn_predict",
    "gnn_predict": "gnn_predict",
    "GWAS": "gwas",
    "gwas": "gwas",
    "多组学整合": "multiomics",
    "multiomics": "multiomics",
}


def _translate_feishu_fields_to_job_config(fields: dict[str, Any]) -> dict[str, Any]:
    """Translate Feishu bitable row fields → GraphMRI-Lite job submission JSON.

    Handles both English and Chinese field names via _FIELD_MAP.
    """
    config: dict[str, Any] = {}

    # Direct field mapping
    for feishu_key, job_key in _FIELD_MAP.items():
        if feishu_key in fields and fields[feishu_key]:
            config[job_key] = fields[feishu_key]

    # Map analysis_type → pipeline selection
    analysis_type = config.pop("analysis_type", None)
    if analysis_type is not None:
        pipeline = _PIPELINE_MAP.get(analysis_type)
        if pipeline:
            config["pipeline"] = pipeline
        else:
            config["pipeline"] = analysis_type

    # Always include record_id for result callback
    config["feishu_record_id"] = fields.get("record_id", "")
    config["feishu_table_id"] = fields.get("table_id", "")

    return config


# ── Background job submission ────────────────────────────────────


def _submit_and_track_job(job_id: str, job_config: dict[str, Any]) -> None:
    """Submit job to GraphMRI-Lite and track completion (runs in background).

    This runs in a FastAPI BackgroundTasks thread — failures are logged
    but never propagate to the webhook caller.
    """
    try:
        submit_url = f"{GRAPHMRI_LITE_URL}/api/jobs/submit"
        resp = requests.post(
            submit_url,
            json={"job_id": job_id, **job_config},
            timeout=GRAPHMRI_LITE_TIMEOUT,
        )
        resp.raise_for_status()
        logger.info("Job %s submitted to GraphMRI-Lite: %s", job_id, resp.json())
    except requests.exceptions.Timeout:
        logger.warning(
            "GraphMRI-Lite submit timeout for job %s (URL: %s, timeout: %ds)",
            job_id,
            submit_url,
            GRAPHMRI_LITE_TIMEOUT,
        )
    except requests.exceptions.ConnectionError:
        logger.warning(
            "GraphMRI-Lite unreachable for job %s (URL: %s)",
            job_id,
            submit_url,
        )
    except Exception:
        logger.exception("Failed to submit job %s to GraphMRI-Lite", job_id)


# ── Webhook endpoint ─────────────────────────────────────────────


@router.post("/execute")
async def handle_feishu_execute(
    payload: FeishuWebhookPayload,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Receive Feishu webhook, trigger GraphMRI-Lite job asynchronously.

    Flow:
    1. Parse feishu bitable fields → job config
    2. Allocate job_id
    3. Enqueue background submission to GraphMRI-Lite
    4. Return 202 Accepted immediately

    Feishu webhook timeout is ~3s; this handler returns in <50ms.
    """
    fields = dict(payload.fields)
    fields["record_id"] = payload.record_id
    fields["table_id"] = payload.table_id

    job_config = _translate_feishu_fields_to_job_config(fields)
    job_id = str(uuid.uuid4())

    background_tasks.add_task(_submit_and_track_job, job_id, job_config)

    logger.info(
        "Webhook accepted: record=%s table=%s → job_id=%s pipeline=%s",
        payload.record_id,
        payload.table_id,
        job_id,
        job_config.get("pipeline", "unknown"),
    )

    return {
        "code": 0,
        "msg": "accepted",
        "data": {"job_id": job_id, "status": "queued"},
    }
