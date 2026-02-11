#!/usr/bin/env python3
"""One-shot Inspector checks for SROS.

This script automates the repeatable parts of the Inspector checklist:
- Run smoke_test.py
- Run `sros init` into a temp directory and validate generated .roo/mcp.json schema
- Start gateway via `sros start` and probe /health, /tools, /sse?once=1

Exit code:
- 0: all checks passed
- 2: blocker found
- 3: unexpected error (script failure)

Design goals:
- Stdlib-only (no requests dependency)
- Deterministic, bounded time (timeouts everywhere)
- Evidence-first reporting
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


BLOCKER_EXIT_CODE = 2
SCRIPT_ERROR_EXIT_CODE = 3


@dataclass
class CheckResult:
    name: str
    ok: bool
    evidence: str
    guidance: str = ""


def _run(
    args: List[str],
    *,
    cwd: Optional[str] = None,
    timeout_s: int = 120,
    env: Optional[Dict[str, str]] = None,
) -> Tuple[int, str]:
    """Run a subprocess and capture combined stdout/stderr."""
    proc = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout_s,
    )
    return proc.returncode, proc.stdout


def _which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def _http_get(url: str, *, timeout_s: float) -> Tuple[int, Dict[str, str], str]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            status = int(getattr(resp, "status", 200))
            headers = {k.lower(): v for k, v in resp.headers.items()}
            body_bytes = resp.read(64 * 1024)
            body_text = body_bytes.decode("utf-8", errors="replace")
            return status, headers, body_text
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return int(e.code), headers, body


def _summarize_headers(headers: Dict[str, str], keys: List[str]) -> str:
    out = []
    for k in keys:
        if k in headers:
            out.append(f"{k}: {headers[k]}")
    return "\n".join(out)


def check_smoke(repo_root: str, python_exe: str) -> CheckResult:
    rc, out = _run([python_exe, os.path.join(repo_root, "smoke_test.py")], cwd=repo_root, timeout_s=240)
    ok = rc == 0 and "All MVP Requirements Passed" in out
    guidance = "Run `python smoke_test.py` and fix the first failing section." if not ok else ""
    return CheckResult(
        name="smoke_test",
        ok=ok,
        evidence=out.strip()[-4000:],
        guidance=guidance,
    )


def _run_sros_cmd(repo_root: str, python_exe: str, sros_args: List[str], timeout_s: int) -> Tuple[int, str]:
    """Run sros CLI in a way that works even if console script isn't on PATH."""
    sros_bin = _which("sros")
    if sros_bin:
        return _run([sros_bin, *sros_args], cwd=repo_root, timeout_s=timeout_s)
    # Fallback: run as module.
    return _run([python_exe, "-m", "sros.cli", *sros_args], cwd=repo_root, timeout_s=timeout_s)


def check_sros_init_schema(repo_root: str, python_exe: str) -> CheckResult:
    with tempfile.TemporaryDirectory(prefix="sros_inspector_") as td:
        # `sros init` expects the target directory to NOT exist.
        workspace_dir = os.path.join(td, "workspace")
        rc, out = _run_sros_cmd(repo_root, python_exe, ["init", workspace_dir], timeout_s=60)
        if rc != 0:
            return CheckResult(
                name="sros_init",
                ok=False,
                evidence=out.strip()[-4000:],
                guidance="Fix `sros init` so it exits 0 and writes workspace files.",
            )

        mcp_path = os.path.join(workspace_dir, ".roo", "mcp.json")
        if not os.path.exists(mcp_path):
            return CheckResult(
                name="mcp.json",
                ok=False,
                evidence=f"Missing file: {mcp_path}\nCLI output:\n{out.strip()[-2000:]}",
                guidance="Ensure `sros init` creates `.roo/mcp.json`.",
            )

        try:
            with open(mcp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return CheckResult(
                name="mcp.json",
                ok=False,
                evidence=f"Failed to parse JSON: {e}\nPath: {mcp_path}",
                guidance="Write valid JSON to `.roo/mcp.json`.",
            )

        problems: List[str] = []
        if not isinstance(data, dict) or "mcpServers" not in data or not isinstance(data.get("mcpServers"), dict):
            problems.append("Top-level must contain object key `mcpServers`.")
        else:
            servers = data["mcpServers"]
            if "sros-gateway" not in servers:
                problems.append("`mcpServers` must include `sros-gateway`.")
            else:
                gw = servers["sros-gateway"]
                if not isinstance(gw, dict):
                    problems.append("`mcpServers.sros-gateway` must be an object.")
                else:
                    if gw.get("type") != "sse":
                        problems.append("`mcpServers.sros-gateway.type` must be 'sse'.")
                    url = gw.get("url")
                    if not isinstance(url, str) or not url.endswith("/sse"):
                        problems.append("`mcpServers.sros-gateway.url` must be a URL ending with '/sse'.")

        ok = len(problems) == 0
        evidence = f"Workspace: {workspace_dir}\nPath: {mcp_path}\n" + json.dumps(data, ensure_ascii=False, indent=2)
        guidance = "Fix generator in sros CLI to match Roo schema (mcpServers/sros-gateway)." if not ok else ""
        if problems:
            evidence += "\n\nProblems:\n- " + "\n- ".join(problems)

        return CheckResult(name="mcp.json schema", ok=ok, evidence=evidence[-4000:], guidance=guidance)


def _terminate_process(proc: subprocess.Popen, timeout_s: float) -> None:
    if proc.poll() is not None:
        return
    try:
        proc.send_signal(signal.SIGINT)
        proc.wait(timeout=timeout_s)
        return
    except Exception:
        pass

    try:
        proc.terminate()
        proc.wait(timeout=timeout_s)
        return
    except Exception:
        pass

    try:
        proc.kill()
    except Exception:
        pass


def check_gateway_endpoints(repo_root: str, python_exe: str, host: str, port: int) -> CheckResult:
    url_base = f"http://{host}:{port}"

    sros_bin = _which("sros")
    if sros_bin:
        cmd = [sros_bin, "start"]
    else:
        cmd = [python_exe, "-m", "sros.cli", "start"]

    proc = subprocess.Popen(
        cmd,
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    log_lines: List[str] = []
    started = False
    start_deadline = time.time() + 8.0

    try:
        # Wait until /health answers or timeout.
        while time.time() < start_deadline:
            if proc.poll() is not None:
                break
            try:
                status, _, _ = _http_get(url_base + "/health", timeout_s=0.6)
                if status == 200:
                    started = True
                    break
            except Exception:
                pass
            time.sleep(0.2)

        # Drain a small portion of logs for evidence.
        if proc.stdout is not None:
            t0 = time.time()
            while time.time() - t0 < 1.0:
                line = proc.stdout.readline()
                if not line:
                    break
                log_lines.append(line.rstrip("\n"))

        if not started:
            # Collect remaining logs quickly.
            if proc.stdout is not None:
                for _ in range(80):
                    line = proc.stdout.readline()
                    if not line:
                        break
                    log_lines.append(line.rstrip("\n"))

            return CheckResult(
                name="gateway_start",
                ok=False,
                evidence="\n".join(log_lines)[-4000:] or "Gateway did not become healthy in time.",
                guidance="Check `sros start` logs and ensure the server binds and /health returns 200.",
            )

        # /health
        health_status, health_headers, health_body = _http_get(url_base + "/health", timeout_s=2.0)
        # /tools
        tools_status, tools_headers, tools_body = _http_get(url_base + "/tools", timeout_s=2.0)
        # /sse?once=1
        sse_status, sse_headers, sse_body = _http_get(url_base + "/sse?once=1", timeout_s=3.0)

        problems: List[str] = []
        if health_status != 200:
            problems.append(f"/health expected 200, got {health_status}")
        if tools_status != 200:
            problems.append(f"/tools expected 200, got {tools_status}")
        if sse_status != 200:
            problems.append(f"/sse?once=1 expected 200, got {sse_status}")
        ct = sse_headers.get("content-type", "")
        if "text/event-stream" not in ct:
            problems.append(f"/sse content-type must include text/event-stream (got {ct})")
        if "event: ready" not in sse_body:
            problems.append("/sse?once=1 must include an initial `event: ready`.")

        ok = len(problems) == 0
        evidence_parts = [
            "Gateway command: " + " ".join(cmd),
            "--- /health ---",
            f"status: {health_status}",
            _summarize_headers(health_headers, ["content-type"]),
            health_body.strip()[:500],
            "--- /tools ---",
            f"status: {tools_status}",
            _summarize_headers(tools_headers, ["content-type"]),
            tools_body.strip()[:800],
            "--- /sse?once=1 ---",
            f"status: {sse_status}",
            _summarize_headers(sse_headers, ["content-type", "cache-control"]),
            sse_body.strip()[:800],
            "--- logs (partial) ---",
            "\n".join(log_lines[-40:]),
        ]
        if problems:
            evidence_parts.append("--- problems ---\n- " + "\n- ".join(problems))

        return CheckResult(
            name="gateway_endpoints",
            ok=ok,
            evidence="\n".join([p for p in evidence_parts if p]).strip()[-4000:],
            guidance="Fix gateway startup/errors or SSE semantics in gateway implementation." if not ok else "",
        )
    finally:
        _terminate_process(proc, timeout_s=2.0)


def render_report_md(results: List[CheckResult]) -> str:
    blockers = [r for r in results if not r.ok]
    status = "PASS" if not blockers else "FAIL"

    lines: List[str] = []
    lines.append(f"# SROS Inspector Check Report\n")
    lines.append(f"Overall: **{status}**\n")
    lines.append("## Results")
    for r in results:
        lines.append(f"- {'PASS' if r.ok else 'FAIL'}: {r.name}")
    lines.append("")

    lines.append("## Evidence")
    for r in results:
        lines.append(f"### {r.name}")
        lines.append("```")
        lines.append(r.evidence.strip())
        lines.append("```")
        if r.guidance:
            lines.append("Guidance:")
            lines.append(r.guidance)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Automated Inspector checks for SROS")
    parser.add_argument("--repo-root", default=os.getcwd(), help="Repository root (default: cwd)")
    parser.add_argument("--python", default=sys.executable, help="Python executable (default: current interpreter)")
    parser.add_argument("--skip-smoke", action="store_true", help="Skip smoke_test.py")
    parser.add_argument("--skip-gateway", action="store_true", help="Skip live gateway start + HTTP probes")
    parser.add_argument("--host", default="localhost", help="Gateway host to probe")
    parser.add_argument("--port", type=int, default=8000, help="Gateway port to probe")
    parser.add_argument("--report", default="/tmp/sros_inspector_report.md", help="Where to write the markdown report")

    args = parser.parse_args()

    results: List[CheckResult] = []
    repo_root = os.path.abspath(args.repo_root)

    try:
        if not args.skip_smoke:
            results.append(check_smoke(repo_root, args.python))

        results.append(check_sros_init_schema(repo_root, args.python))

        if not args.skip_gateway:
            results.append(check_gateway_endpoints(repo_root, args.python, args.host, args.port))

        report = render_report_md(results)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)

        failed = [r for r in results if not r.ok]
        if failed:
            return BLOCKER_EXIT_CODE
        return 0

    except subprocess.TimeoutExpired as e:
        msg = f"Timeout running: {e.cmd}\nAfter: {e.timeout}s"
        report = render_report_md(results + [CheckResult(name="timeout", ok=False, evidence=msg)])
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        return BLOCKER_EXIT_CODE

    except Exception as e:
        report = render_report_md(results + [CheckResult(name="script_error", ok=False, evidence=str(e))])
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        return SCRIPT_ERROR_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
