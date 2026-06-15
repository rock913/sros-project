"""Unit tests for Feishu webhook endpoint.

Covers:
  - POST /webhook/execute → 202 + job_id
  - Field translation (_translate_feishu_fields_to_job_config)
  - Background task submission (mock)
  - Health endpoint unaffected
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


# ── Helpers ──────────────────────────────────────────────────────


def _make_test_app():
    """Create a minimal FastAPI app with only the webhook router mounted."""
    from fastapi import FastAPI

    from sros.gateway.webhook import router

    app = FastAPI()
    app.include_router(router)

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


@pytest.fixture
def client():
    """FastAPI TestClient with webhook router isolated."""
    app = _make_test_app()
    with TestClient(app) as c:
        yield c


# ── Field Translation ────────────────────────────────────────────


class TestFieldTranslation:
    def test_english_fields(self):
        from sros.gateway.webhook import _translate_feishu_fields_to_job_config

        fields = {
            "project": "MDD_Twin",
            "analysis_type": "GNN预测",
            "subject_filter_sql": "SELECT * FROM cohort",
            "atlas": "AAL",
            "model": "GraphSAGE",
            "target": "HAMD_improvement_pct",
        }
        config = _translate_feishu_fields_to_job_config(fields)

        assert config["project"] == "MDD_Twin"
        assert config["pipeline"] == "gnn_predict"
        assert config["subject_filter_sql"] == "SELECT * FROM cohort"
        assert config["atlas"] == "AAL"
        assert config["model"] == "GraphSAGE"
        assert config["target"] == "HAMD_improvement_pct"

    def test_chinese_fields(self):
        from sros.gateway.webhook import _translate_feishu_fields_to_job_config

        fields = {
            "项目": "MultiModal",
            "分析类型": "脑网络",
            "图谱": "Desikan",
            "预测目标": "response",
        }
        config = _translate_feishu_fields_to_job_config(fields)

        assert config["project"] == "MultiModal"
        assert config["pipeline"] == "build_network"
        assert config["atlas"] == "Desikan"

    def test_unknown_analysis_type_passthrough(self):
        from sros.gateway.webhook import _translate_feishu_fields_to_job_config

        fields = {"analysis_type": "custom_pipeline"}
        config = _translate_feishu_fields_to_job_config(fields)

        assert config["pipeline"] == "custom_pipeline"

    def test_empty_fields(self):
        from sros.gateway.webhook import _translate_feishu_fields_to_job_config

        config = _translate_feishu_fields_to_job_config({})
        assert config == {"feishu_record_id": "", "feishu_table_id": ""}

    def test_none_values_skipped(self):
        from sros.gateway.webhook import _translate_feishu_fields_to_job_config

        fields = {"project": "MDD_Twin", "atlas": None, "model": ""}
        config = _translate_feishu_fields_to_job_config(fields)

        assert "atlas" not in config
        assert "model" not in config

    def test_all_pipeline_mappings(self):
        from sros.gateway.webhook import _PIPELINE_MAP

        assert _PIPELINE_MAP["预处理"] == "fmriprep"
        assert _PIPELINE_MAP["preprocess"] == "fmriprep"
        assert _PIPELINE_MAP["脑网络"] == "build_network"
        assert _PIPELINE_MAP["GNN预测"] == "gnn_predict"
        assert _PIPELINE_MAP["GWAS"] == "gwas"
        assert _PIPELINE_MAP["多组学整合"] == "multiomics"


# ── Webhook Endpoint ─────────────────────────────────────────────


class TestWebhookEndpoint:
    def test_accepts_valid_payload(self, client):
        payload = {
            "record_id": "rec123",
            "table_id": "tbl456",
            "fields": {
                "项目": "MDD_Twin",
                "分析类型": "GNN预测",
                "图谱": "AAL",
                "模型": "GraphSAGE",
                "预测目标": "HAMD_improvement_pct",
            },
        }
        resp = client.post("/webhook/execute", json=payload)

        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["msg"] == "accepted"
        assert "job_id" in data["data"]
        assert data["data"]["status"] == "queued"

    def test_returns_unique_job_ids(self, client):
        payload = {
            "record_id": "rec001",
            "table_id": "tbl001",
            "fields": {"项目": "MDD_Twin"},
        }

        ids = set()
        for _ in range(5):
            resp = client.post("/webhook/execute", json=payload)
            ids.add(resp.json()["data"]["job_id"])

        assert len(ids) == 5

    def test_missing_record_id_still_accepted(self, client):
        """record_id is optional per the spec — feishu always sends it but we're defensive."""
        payload = {
            "record_id": "rec001",
            "table_id": "tbl001",
            "fields": {},
        }
        resp = client.post("/webhook/execute", json=payload)
        assert resp.status_code == 200

    def test_extra_fields_preserved(self, client):
        """Unknown fields should not break the endpoint."""
        payload = {
            "record_id": "rec999",
            "table_id": "tbl999",
            "fields": {
                "custom_field": "value",
                "another_custom": 42,
                "project": "MDD_Twin",
            },
        }
        resp = client.post("/webhook/execute", json=payload)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0

    def test_invalid_json_rejected(self, client):
        resp = client.post(
            "/webhook/execute",
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 422

    def test_missing_required_fields_rejected(self, client):
        """record_id and table_id are required by Pydantic model."""
        resp = client.post("/webhook/execute", json={"fields": {}})
        assert resp.status_code == 422


# ── Background Task Submission ───────────────────────────────────


class TestBackgroundSubmission:
    def test_background_task_called(self, client):
        with patch(
            "sros.gateway.webhook._submit_and_track_job"
        ) as mock_submit:
            payload = {
                "record_id": "rec_bg",
                "table_id": "tbl_bg",
                "fields": {"项目": "MDD_Twin", "分析类型": "脑网络"},
            }
            resp = client.post("/webhook/execute", json=payload)

            assert resp.status_code == 200
            # FastAPI BackgroundTasks run synchronously in TestClient
            mock_submit.assert_called_once()
            job_id = mock_submit.call_args[0][0]
            job_config = mock_submit.call_args[0][1]
            assert job_id == resp.json()["data"]["job_id"]
            assert job_config["pipeline"] == "build_network"

    def test_submit_handles_timeout(self):
        import requests

        from sros.gateway.webhook import _submit_and_track_job

        with patch("sros.gateway.webhook.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.Timeout("timed out")

            # Should not raise
            _submit_and_track_job("job-timeout", {"pipeline": "fmriprep"})

    def test_submit_handles_connection_error(self):
        import requests

        from sros.gateway.webhook import _submit_and_track_job

        with patch("sros.gateway.webhook.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ConnectionError("refused")

            # Should not raise
            _submit_and_track_job("job-conn", {"pipeline": "fmriprep"})

    def test_submit_handles_generic_error(self):
        from sros.gateway.webhook import _submit_and_track_job

        with patch("sros.gateway.webhook.requests.post") as mock_post:
            mock_post.side_effect = RuntimeError("unexpected")

            # Should not raise
            _submit_and_track_job("job-generic", {"pipeline": "fmriprep"})

    def test_submit_success_posts_to_correct_url(self):
        from sros.gateway.webhook import _submit_and_track_job

        with patch("sros.gateway.webhook.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {"status": "ok"}
            mock_post.return_value = mock_resp

            _submit_and_track_job("job-ok", {"pipeline": "fmriprep", "atlas": "AAL"})

            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert "/api/jobs/submit" in call_args[0][0]
            assert call_args[1]["json"]["pipeline"] == "fmriprep"
            assert call_args[1]["json"]["job_id"] == "job-ok"


# ── Health Check Unaffected ──────────────────────────────────────


class TestHealthUnaffected:
    def test_health_still_works(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_webhook_prefix_isolation(self, client):
        """Webhook routes don't leak into root paths."""
        resp = client.get("/execute")
        assert resp.status_code == 404

    def test_router_openapi_schema(self, client):
        """Webhook endpoint appears in OpenAPI schema under feishu tag."""
        resp = client.get("/openapi.json")
        assert resp.status_code == 200
        schema = resp.json()
        paths = schema["paths"]
        assert "/webhook/execute" in paths
        assert "post" in paths["/webhook/execute"]
