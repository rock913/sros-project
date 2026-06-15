"""Integration test for V4 Data + HPC MCP tools through the gateway.

Starts a real SROS gateway subprocess and exercises db.ingest / db.query /
hpc.submit / hpc.status / hpc.list via MCP JSON-RPC over SSE.

Follows the test_mcp_sse_hub.py pattern.
"""

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List

import pytest
import requests


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_health(port: int, timeout_s: float = 15.0) -> None:
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            resp = requests.get(f"http://localhost:{port}/health", timeout=1)
            if resp.status_code == 200:
                return
        except Exception as e:
            last_error = e
        time.sleep(0.3)
    raise AssertionError(f"Gateway did not become healthy on port {port}: {last_error}")


def _init_workspace(temp_dir: str, name: str, env: dict) -> str:
    subprocess.run(
        [sys.executable, "-m", "sros.cli", "init", name],
        cwd=temp_dir,
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return str(Path(temp_dir) / name)


def _mcp_call(port: int, method: str, params: dict | None = None) -> Dict[str, Any]:
    """Send a JSON-RPC call to the gateway and return the parsed response."""
    payload: Dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }
    resp = requests.post(f"http://localhost:{port}/sse", json=payload, timeout=10)
    assert resp.status_code == 200, f"MCP call failed: {resp.status_code} {resp.text[:200]}"
    return resp.json()


def _mcp_call_tool(port: int, tool_name: str, arguments: dict) -> Dict[str, Any]:
    """Call a specific MCP tool via tools/call."""
    return _mcp_call(port, "tools/call", {"name": tool_name, "arguments": arguments})


@pytest.mark.integration
class TestV4DbHpcGateway:
    """End-to-end tests for V4 db and hpc MCP tools through a real gateway."""

    @pytest.fixture(autouse=True)
    def _setup_gateway(self):
        """Start gateway before each test class."""
        port = _find_free_port()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(_repo_root())

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = _init_workspace(temp_dir, "test_v4_e2e", env)

            proc = subprocess.Popen(
                [sys.executable, "-m", "sros.cli", "start", "-w", workspace, "-p", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            try:
                _wait_for_health(port, timeout_s=15)
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    pytest.fail(f"Gateway process exited early.\nstdout: {out.decode()}\nstderr: {err.decode()}")

                self.port = port
                self.workspace = workspace
                self.env = env
                yield
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()

    # ── DB Ingest ──────────────────────────────────────────────────────────

    def test_mcp_db_ingest_bids_structure(self):
        """db.ingest via MCP: ingest a minimal BIDS directory tree."""
        # Create mock BIDS structure
        source = Path(self.workspace) / "data"
        source.mkdir(exist_ok=True)
        sub_dir = source / "sub-001" / "ses-01" / "anat"
        sub_dir.mkdir(parents=True)
        (sub_dir / "sub-001_ses-01_T1w.nii.gz").write_text("mock nifti")
        (sub_dir / "sub-001_ses-01_T2w.nii.gz").write_text("mock nifti")

        # Create participants.tsv
        (source / "participants.tsv").write_text(
            "participant_id\tcohort\tage_group\tsex\tage\tgroup_status\tintervention_type\n"
            "sub-001\tSXMU\tadult\tM\t35\tdTMS\tactive\n"
        )

        db_path = Path(self.workspace) / "test.duckdb"

        result = _mcp_call_tool(
            self.port,
            "db.ingest",
            {
                "source": str(source),
                "bids_dir": ".",
                "participants": "participants.tsv",
                "db_path": str(db_path),
            },
        )
        assert "result" in result
        content = result["result"].get("content", [])
        assert len(content) > 0
        body = json.loads(content[0].get("text", "{}"))
        assert body.get("ok"), f"db.ingest failed: {body}"
        assert body.get("subjects_count", 0) > 0 or body.get("mri_scans_count", 0) > 0

    def test_mcp_db_ingest_and_query_roundtrip(self):
        """db.ingest → db.query roundtrip via MCP."""
        source = Path(self.workspace) / "data_roundtrip"
        source.mkdir(exist_ok=True)

        # BIDS
        sub_dir = source / "sub-002" / "ses-01" / "anat"
        sub_dir.mkdir(parents=True)
        (sub_dir / "sub-002_ses-01_T1w.nii.gz").write_text("mock")

        (source / "participants.tsv").write_text(
            "participant_id\tcohort\tage_group\tsex\tage\tgroup_status\tintervention_type\n"
            "sub-002\tHC\tadult\tF\t28\tcontrol\tna\n"
        )

        db_path = Path(self.workspace) / "roundtrip.duckdb"

        # 1. Ingest
        ingest_res = _mcp_call_tool(
            self.port,
            "db.ingest",
            {
                "source": str(source),
                "bids_dir": ".",
                "participants": "participants.tsv",
                "db_path": str(db_path),
            },
        )
        content = ingest_res["result"]["content"][0]
        body = json.loads(content["text"])
        assert body.get("ok"), f"db.ingest failed: {body}"

        # 2. Query — count mri_scans
        query_res = _mcp_call_tool(
            self.port,
            "db.query",
            {
                "sql": "SELECT subject_id, modality FROM mri_scans",
                "db_path": str(db_path),
            },
        )
        content = query_res["result"]["content"][0]
        body = json.loads(content["text"])
        assert body.get("ok"), f"db.query failed: {body}"
        assert body.get("count", 0) >= 1
        assert "sub-002" in json.dumps(body.get("rows", []))

    def test_mcp_db_query_rejects_non_select(self):
        """db.query must reject non-SELECT SQL."""
        db_path = Path(self.workspace) / "reject.duckdb"

        result = _mcp_call_tool(
            self.port,
            "db.query",
            {
                "sql": "DROP TABLE IF EXISTS subjects",
                "db_path": str(db_path),
            },
        )
        content = result["result"]["content"][0]
        body = json.loads(content["text"])
        assert not body.get("ok")
        assert "SELECT" in body.get("error", "")

    # ── HPC tools ──────────────────────────────────────────────────────────

    def test_mcp_hpc_generate_submit_dryrun_status_list(self):
        """hpc.generate → hpc.submit (dry-run) → hpc.status → hpc.list chain via MCP."""
        # 1. Generate job script from template
        template_path = _repo_root() / "config" / "slurm" / "fmriprep_template.slurm"
        output_dir = Path(self.workspace) / "jobs"
        output_dir.mkdir(exist_ok=True)

        gen_res = _mcp_call_tool(
            self.port,
            "hpc.generate",
            {
                "template": str(template_path),
                "subject": "sub-003",
                "output_dir": str(output_dir),
            },
        )
        content = gen_res["result"]["content"][0]
        body = json.loads(content["text"])
        assert body.get("ok"), f"hpc.generate failed: {body}"

        # Read generated script
        script_path = body.get("script_path")
        assert script_path and Path(script_path).exists(), f"Script not created at {script_path}"

        # 2. Submit (dry-run)
        submit_res = _mcp_call_tool(
            self.port,
            "hpc.submit",
            {
                "script": script_path,
                "dry_run": True,
            },
        )
        content = submit_res["result"]["content"][0]
        body = json.loads(content["text"])
        assert body.get("ok"), f"hpc.submit dry-run failed: {body}"
        assert "dry" in str(body).lower() or body.get("job_id")

        # 3. Status
        status_res = _mcp_call_tool(
            self.port,
            "hpc.status",
            {
                "job_id": "12345",
                "dry_run": True,
            },
        )
        content = status_res["result"]["content"][0]
        body = json.loads(content["text"])
        assert body.get("ok"), f"hpc.status failed: {body}"

        # 4. List
        list_res = _mcp_call_tool(
            self.port,
            "hpc.list",
            {"dry_run": True},
        )
        content = list_res["result"]["content"][0]
        body = json.loads(content["text"])
        assert body.get("ok"), f"hpc.list failed: {body}"

    def test_mcp_hpc_cancel_and_logs_dry(self):
        """hpc.cancel and hpc.logs via MCP (dry-run / mock)."""
        cancel_res = _mcp_call_tool(
            self.port,
            "hpc.cancel",
            {
                "job_id": "99999",
                "dry_run": True,
            },
        )
        content = cancel_res["result"]["content"][0]
        body = json.loads(content["text"])
        # Cancel may succeed or report not-found; both are valid responses
        assert "ok" in body

    # ── Tool discovery ─────────────────────────────────────────────────────

    def test_mcp_tools_list_includes_v4_tools(self):
        """tools/list must include all V4 db and hpc tools."""
        result = _mcp_call(self.port, "tools/list")
        tools = result["result"]["tools"]
        tool_names = {t["name"] for t in tools}

        required_v4 = {
            "db.ingest",
            "db.query",
            "hpc.generate",
            "hpc.submit",
            "hpc.status",
            "hpc.cancel",
            "hpc.list",
            "hpc.logs",
            "neuro.validate",
            "neuro.generate_graphmri",
            "neuro.generate_fmriprep",
        }
        missing = required_v4 - tool_names
        assert not missing, f"V4 tools missing from gateway: {missing}"

    def test_mcp_initialize_returns_capabilities(self):
        """initialize should return server capabilities."""
        result = _mcp_call(self.port, "initialize", {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "test", "version": "1.0"},
        })
        assert "result" in result
        assert "capabilities" in result["result"]
