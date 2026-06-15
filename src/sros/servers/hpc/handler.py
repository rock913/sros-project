from __future__ import annotations

import logging
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Default Slurm template directory (shipped with SROS)
DEFAULT_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "config" / "slurm"

# Slurm state constants
SLURM_STATES = {"PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED", "TIMEOUT", "COMPLETING", "CONFIGURING", "PREEMPTED"}

# Patterns for OOM detection in stderr
OOM_PATTERNS = [
    re.compile(r"oom[-_]kill", re.IGNORECASE),
    re.compile(r"Out\s*Of\s*Memory", re.IGNORECASE),
    re.compile(r"memory\s+exceeded", re.IGNORECASE),
    re.compile(r"slurmstepd.*oom", re.IGNORECASE),
    re.compile(r"exceeded\s+job\s+memory\s+limit", re.IGNORECASE),
]

# Pattern for parsing sbatch --mem value
MEM_PATTERN = re.compile(r"^#SBATCH\s+--mem=(\d+)([MG])", re.MULTILINE)
MEM_PER_CPU_PATTERN = re.compile(r"^#SBATCH\s+--mem-per-cpu=(\d+)([MG])", re.MULTILINE)


def _run(cmd: List[str], timeout: int = 30, dry_run: bool = False) -> Dict[str, Any]:
    """Run a shell command and return standardized result."""
    if dry_run:
        logger.info("[DRY-RUN] %s", " ".join(cmd))
        return {"ok": True, "dry_run": True, "command": " ".join(cmd)}

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ},
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Command timed out after {timeout}s: {' '.join(cmd)}"}
    except FileNotFoundError:
        return {"ok": False, "error": f"Command not found: {cmd[0]}. Is Slurm installed?"}


def _parse_sbatch_submitted(output: str) -> Optional[str]:
    """Extract job ID from sbatch 'Submitted batch job 12345'."""
    m = re.search(r"Submitted\s+batch\s+job\s+(\d+)", output)
    return m.group(1) if m else None


def _parse_squeue_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse one squeue -o line into a dict."""
    parts = line.strip().split("|")
    if len(parts) < 8:
        return None
    job_id, name, state, partition_name, nodes, cpus, elapsed, time_limit = parts[:8]
    return {
        "job_id": job_id.strip(),
        "name": name.strip(),
        "state": state.strip(),
        "partition": partition_name.strip(),
        "nodes": nodes.strip(),
        "cpus": cpus.strip(),
        "elapsed": elapsed.strip(),
        "time_limit": time_limit.strip(),
    }


class HPCHandler:
    """Slurm HPC job management handler.

    Wraps sbatch, squeue, scancel commands with JSON input/output.
    Supports dry-run mode for testing and environments without Slurm.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self._oom_retry_count: Dict[str, int] = {}
        self._oom_retry_mem: Dict[str, int] = {}

    # ── Core Slurm Commands ───────────────────────────────────────────────

    def submit(self, script_path: str, array_size: int | None = None) -> Dict[str, Any]:
        """Submit a Slurm script via sbatch.

        Args:
            script_path: Path to the .slurm script.
            array_size: If provided, submit as a job array (--array=1-N).
        """
        script = Path(script_path)
        if not script.exists():
            return {"ok": False, "error": f"Script not found: {script_path}"}

        cmd = ["sbatch"]
        if array_size and array_size > 1:
            cmd.append(f"--array=1-{int(array_size)}%50")  # max 50 concurrent
        cmd.append(str(script))

        result = _run(cmd, dry_run=self.dry_run)
        if result.get("dry_run"):
            return result

        if not result["ok"]:
            return {"ok": False, "error": result.get("stderr") or result.get("error", "sbatch failed")}

        job_id = _parse_sbatch_submitted(result["stdout"])
        if job_id:
            # Reset retry tracking for new jobs
            self._oom_retry_count.pop(job_id, None)
            self._oom_retry_mem.pop(job_id, None)
            return {
                "ok": True,
                "job_id": job_id,
                "array_size": array_size or 1,
                "estimated_completion": None,
                "stdout": result["stdout"],
            }
        return {"ok": False, "error": f"Could not parse job ID from: {result['stdout']}"}

    def status(self, job_id: str) -> Dict[str, Any]:
        """Query job status via squeue -j <job_id>."""
        # squeue -j <id> -o "%i|%j|%T|%P|%D|%C|%M|%l" --noheader
        cmd = [
            "squeue", "-j", str(job_id),
            "-o", "%i|%j|%T|%P|%D|%C|%M|%l",
            "--noheader",
        ]
        result = _run(cmd, dry_run=self.dry_run)
        if result.get("dry_run"):
            return result

        if not result["ok"]:
            # Check if job completed (no longer in queue)
            stderr = result.get("stderr", "")
            if "Invalid job id" in stderr or "slurm_load_jobs" in stderr:
                return {"ok": True, "job_id": job_id, "state": "COMPLETED", "in_queue": False}
            return {"ok": False, "error": result.get("stderr") or result.get("error", "squeue failed")}

        jobs: List[Dict[str, Any]] = []
        for line in result["stdout"].split("\n"):
            if not line.strip():
                continue
            parsed = _parse_squeue_line(line)
            if parsed:
                jobs.append(parsed)

        if not jobs:
            return {"ok": True, "job_id": job_id, "state": "COMPLETED", "in_queue": False}

        main_job = jobs[0]
        return {
            "ok": True,
            "job_id": main_job["job_id"],
            "name": main_job["name"],
            "state": main_job["state"],
            "partition": main_job["partition"],
            "nodes": main_job["nodes"],
            "cpus": main_job["cpus"],
            "elapsed": main_job["elapsed"],
            "time_limit": main_job["time_limit"],
            "array_tasks": len(jobs) if len(jobs) > 1 else None,
        }

    def cancel(self, job_id: str) -> Dict[str, Any]:
        """Cancel a job via scancel."""
        cmd = ["scancel", str(job_id)]
        result = _run(cmd, dry_run=self.dry_run)
        if result.get("dry_run"):
            return {"ok": True, "cancelled": True, "dry_run": True, "job_id": job_id}

        if result["ok"]:
            return {"ok": True, "cancelled": True, "job_id": job_id}
        return {"ok": False, "error": result.get("stderr") or result.get("error", "scancel failed")}

    def list_jobs(self, user: str | None = None) -> Dict[str, Any]:
        """List jobs for the current user or a specific user."""
        if user is None:
            user = os.environ.get("USER", os.environ.get("LOGNAME", ""))

        cmd = [
            "squeue", "-u", user,
            "-o", "%i|%j|%T|%P|%D|%C|%M|%l",
            "--noheader",
        ]
        result = _run(cmd, dry_run=self.dry_run)
        if result.get("dry_run"):
            return result

        if not result["ok"]:
            return {"ok": False, "error": result.get("stderr") or result.get("error", "squeue failed")}

        jobs: List[Dict[str, Any]] = []
        for line in result["stdout"].split("\n"):
            if not line.strip():
                continue
            parsed = _parse_squeue_line(line)
            if parsed:
                jobs.append(parsed)

        return {"ok": True, "jobs": jobs, "count": len(jobs)}

    def logs(self, job_id: str, log_dir: str = ".") -> Dict[str, Any]:
        """Read stdout and stderr logs for a given job."""
        log_path = Path(log_dir)
        out_files = sorted(log_path.glob(f"*{job_id}*.out"))
        err_files = sorted(log_path.glob(f"*{job_id}*.err"))

        stdout_text = ""
        stderr_text = ""

        for f in out_files:
            try:
                stdout_text += f.read_text(encoding="utf-8", errors="replace") + "\n"
            except Exception:
                pass

        for f in err_files:
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                stderr_text += content + "\n"
            except Exception:
                pass

        return {
            "ok": True,
            "job_id": job_id,
            "stdout": stdout_text.strip(),
            "stderr": stderr_text.strip(),
            "out_files": [str(f) for f in out_files],
            "err_files": [str(f) for f in err_files],
        }

    # ── OOM Detection & Self-Healing ──────────────────────────────────────

    @staticmethod
    def check_oom(stderr_text: str) -> bool:
        """Detect OOM/out-of-memory patterns in stderr text."""
        for pattern in OOM_PATTERNS:
            if pattern.search(stderr_text):
                return True
        return False

    @staticmethod
    def _parse_sbatch_mem(script_path: str) -> tuple[int, str]:
        """Parse #SBATCH --mem= value from a script. Returns (value_gb, unit)."""
        try:
            content = Path(script_path).read_text(encoding="utf-8")
        except Exception:
            return 0, "G"

        # Check --mem first
        m = MEM_PATTERN.search(content)
        if m:
            val = int(m.group(1))
            unit = m.group(2)
            if unit.upper() == "G":
                return val, "G"
            elif unit.upper() == "M":
                return max(1, val // 1024), "G"
            return val, "G"

        # Check --mem-per-cpu
        m = MEM_PER_CPU_PATTERN.search(content)
        if m:
            val = int(m.group(1))
            unit = m.group(2)
            if unit.upper() == "G":
                return val, "G"
            elif unit.upper() == "M":
                return max(1, val // 1024), "G"

        return 16, "G"  # default assumption

    def _rewrite_mem(self, script_path: str, new_mem_gb: int) -> str:
        """Create a new script with doubled --mem, return new path."""
        try:
            content = Path(script_path).read_text(encoding="utf-8")
        except Exception:
            return script_path

        def _replace_mem(match):
            return f"#SBATCH --mem={new_mem_gb}G"

        new_content = MEM_PATTERN.sub(_replace_mem, content)

        if new_content == content:
            # No replacement — add --mem line after last #SBATCH
            lines = content.split("\n")
            inserted = False
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                if not inserted and line.startswith("#SBATCH"):
                    # Insert after this SBATCH line if next is not SBATCH
                    if i + 1 >= len(lines) or not lines[i + 1].startswith("#SBATCH"):
                        new_lines.append(f"#SBATCH --mem={new_mem_gb}G")
                        inserted = True
            if not inserted:
                new_lines.append(f"#SBATCH --mem={new_mem_gb}G")
            new_content = "\n".join(new_lines)

        suffix = f"_mem{new_mem_gb}G"
        stem = Path(script_path).stem
        parent = Path(script_path).parent
        new_path = parent / f"{stem}{suffix}.slurm"
        new_path.write_text(new_content, encoding="utf-8")
        return str(new_path)

    def submit_with_oom_retry(self, script_path: str, max_retries: int = 3) -> Dict[str, Any]:
        """Submit a job with automatic OOM retry: double memory on each OOM failure.

        Strategy:
          - Submit job, wait for completion
          - Check .err for OOM patterns
          - If OOM detected: double --mem, resubmit (up to max_retries)
          - Memory escalation: 16G → 32G → 48G → FAILED_OOM
        """
        script = Path(script_path)
        if not script.exists():
            return {"ok": False, "error": f"Script not found: {script_path}"}

        current_script = str(script)
        current_mem, _ = self._parse_sbatch_mem(current_script)
        retries = 0
        history: List[Dict[str, Any]] = []

        while retries <= max_retries:
            result = self.submit(current_script)
            if not result["ok"]:
                return result

            job_id = result["job_id"]
            entry = {"attempt": retries + 1, "job_id": job_id, "mem_gb": current_mem, "script": current_script}
            history.append(entry)

            if retries >= max_retries:
                # Already at max retries — don't resubmit
                break

            # Poll for completion (synchronous, with timeout)
            max_poll_seconds = 300
            poll_interval = 10
            waited = 0
            job_state = "PENDING"
            while waited < max_poll_seconds:
                time.sleep(poll_interval)
                waited += poll_interval
                s = self.status(job_id)
                if not s.get("ok"):
                    break
                job_state = s.get("state", "")
                if job_state in ("COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"):
                    break

            if job_state == "COMPLETED":
                return {
                    "ok": True,
                    "job_id": job_id,
                    "state": "COMPLETED",
                    "oom_retries": retries,
                    "final_mem_gb": current_mem,
                    "history": history,
                }

            if job_state == "FAILED" or job_state != "COMPLETED":
                # Check for OOM in logs
                log_dir = script.parent / "logs"
                log_dir = log_dir if log_dir.exists() else Path(".")
                log_result = self.logs(job_id, str(log_dir))
                stderr_text = log_result.get("stderr", "")

                if self.check_oom(stderr_text):
                    retries += 1
                    if retries <= max_retries:
                        new_mem = current_mem * 2
                        logger.info("OOM detected for job %s, retry %d/%d: %dG → %dG",
                                     job_id, retries, max_retries, current_mem, new_mem)
                        if new_mem > 48:
                            new_mem = 48
                        try:
                            current_script = self._rewrite_mem(current_script, new_mem)
                            current_mem = new_mem
                        except Exception:
                            pass
                        continue  # resubmit with higher mem

                # Non-OOM failure or out of retries
                break

        return {
            "ok": False,
            "error": "FAILED_OOM" if retries >= max_retries else "FAILED",
            "oom_retries": retries,
            "final_mem_gb": current_mem,
            "history": history,
        }

    # ── Template-based Job Generation ─────────────────────────────────────

    def generate_job_script(
        self,
        template_path: str,
        subject_id: str,
        output_dir: str,
        substitutions: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """Generate a Slurm script from a template by substituting {SUBJECT} etc."""
        tmpl = Path(template_path)
        if not tmpl.exists():
            return {"ok": False, "error": f"Template not found: {template_path}"}

        try:
            content = tmpl.read_text(encoding="utf-8")
        except Exception as e:
            return {"ok": False, "error": str(e)}

        # Built-in substitution: {SUBJECT}
        content = content.replace("{SUBJECT}", subject_id)

        # Additional user-provided substitutions
        subs = dict(substitutions or {})
        for key, value in subs.items():
            content = content.replace("{" + key + "}", value)

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        script_name = Path(template_path).stem.replace("_template", f"_{subject_id}")
        output_path = out_dir / f"{script_name}.slurm"
        output_path.write_text(content, encoding="utf-8")

        return {
            "ok": True,
            "subject_id": subject_id,
            "script_path": str(output_path),
            "template": template_path,
        }

    def generate_job_array(
        self,
        template_path: str,
        subject_ids: List[str],
        output_dir: str,
        substitutions: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """Generate one Slurm script per subject from a template.

        Returns the generated scripts list and the first script path for submission.
        """
        scripts: List[str] = []
        for sid in subject_ids:
            result = self.generate_job_script(
                template_path=template_path,
                subject_id=sid,
                output_dir=output_dir,
                substitutions=substitutions,
            )
            if result["ok"]:
                scripts.append(result["script_path"])
            else:
                return {"ok": False, "error": f"Failed for subject {sid}: {result.get('error')}", "scripts": scripts}

        return {
            "ok": True,
            "count": len(scripts),
            "scripts": scripts,
            "template": template_path,
            "output_dir": output_dir,
        }
