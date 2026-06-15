from __future__ import annotations

import subprocess
from pathlib import Path

from sros.servers.hpc.handler import (
    HPCHandler,
    _parse_sbatch_submitted,
    _parse_squeue_line,
)


class MockCompleted:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def mock_run_ok(cmd, **kwargs):
    cmd_str = " ".join(cmd)
    if cmd[0] == "sbatch":
        return MockCompleted(0, "Submitted batch job 12345", "")
    elif cmd[0] == "squeue":
        if "-j" in cmd:
            return MockCompleted(0, "12345|test_job|RUNNING|cpu|1|8|00:05:00|12:00:00", "")
        return MockCompleted(0, "12345|test_job|PENDING|cpu|1|8|00:00:00|12:00:00\n67890|job2|RUNNING|cpu|1|4|01:00:00|08:00:00", "")
    elif cmd[0] == "scancel":
        return MockCompleted(0, "", "")
    return MockCompleted(1, "", "unknown")


def test_parse_sbatch_submitted():
    assert _parse_sbatch_submitted("Submitted batch job 12345") == "12345"
    assert _parse_sbatch_submitted("Submitted batch job 99999 on cluster pi2") == "99999"
    assert _parse_sbatch_submitted("Error: job rejected") is None


def test_parse_squeue_line():
    line = "12345|fmriprep_sub-001|RUNNING|cpu|1|8|00:05:00|12:00:00"
    result = _parse_squeue_line(line)
    assert result is not None
    assert result["job_id"] == "12345"
    assert result["name"] == "fmriprep_sub-001"
    assert result["state"] == "RUNNING"
    assert result["partition"] == "cpu"


def test_hpc_submit_dry_run(tmp_path: Path):
    script = tmp_path / "test.slurm"
    script.write_text("#!/bin/bash\n#SBATCH --job-name=test\n")
    h = HPCHandler(dry_run=True)
    result = h.submit(str(script))
    assert result["ok"] is True
    assert result["dry_run"] is True
    assert "sbatch" in result["command"]


def test_hpc_submit_missing_script():
    h = HPCHandler(dry_run=False)
    result = h.submit("/nonexistent/script.slurm")
    assert result["ok"] is False


def test_hpc_status_dry_run():
    h = HPCHandler(dry_run=True)
    result = h.status("12345")
    assert result["ok"] is True
    assert result["dry_run"] is True


def test_hpc_list_dry_run():
    h = HPCHandler(dry_run=True)
    result = h.list_jobs()
    assert result["ok"] is True
    assert result["dry_run"] is True


def test_check_oom_patterns():
    assert HPCHandler.check_oom("oom-kill event detected in /sys/fs/cgroup") is True
    assert HPCHandler.check_oom("slurmstepd: error: Detected 1 oom-kill event") is True
    assert HPCHandler.check_oom("exceeded job memory limit") is True
    assert HPCHandler.check_oom("OutOfMemoryError: Java heap space") is True
    assert HPCHandler.check_oom("Job completed successfully") is False
    assert HPCHandler.check_oom("") is False


def test_parse_sbatch_mem():
    script = "/tmp/test.slurm"
    Path(script).write_text("#!/bin/bash\n#SBATCH --mem=32G\n#SBATCH --cpus-per-task=8\n")
    mem, unit = HPCHandler._parse_sbatch_mem(script)
    assert mem == 32
    assert unit == "G"

    Path(script).write_text("#!/bin/bash\n#SBATCH --mem=8192M\n")
    mem, unit = HPCHandler._parse_sbatch_mem(script)
    assert mem == 8  # converted to GB

    Path(script).write_text("#!/bin/bash\n#SBATCH --mem-per-cpu=4G\n")
    mem, unit = HPCHandler._parse_sbatch_mem(script)
    assert mem == 4

    # No mem line — default
    Path(script).write_text("#!/bin/bash\n#SBATCH --cpus-per-task=8\n")
    mem, unit = HPCHandler._parse_sbatch_mem(script)
    assert mem == 16  # default


def test_rewrite_mem(tmp_path: Path):
    script_path = tmp_path / "test.slurm"
    script_path.write_text("#!/bin/bash\n#SBATCH --job-name=test\n#SBATCH --mem=16G\n#SBATCH --cpus-per-task=4\n")
    h = HPCHandler(dry_run=True)
    new_path = h._rewrite_mem(str(script_path), 32)
    content = Path(new_path).read_text()
    assert "--mem=32G" in content
    assert "test_mem32G.slurm" in new_path


def test_generate_job_script(tmp_path: Path):
    template = tmp_path / "fmriprep_template.slurm"
    template.write_text("#!/bin/bash\n#SBATCH --job-name=fmriprep_{SUBJECT}\nsrun apptainer run container.sif {BIDS_DIR}/{SUBJECT}\n")
    h = HPCHandler(dry_run=True)
    result = h.generate_job_script(str(template), "sub-001", str(tmp_path / "jobs"), {"BIDS_DIR": "/data/bids"})
    assert result["ok"] is True
    assert "sub-001" in result["script_path"]
    content = Path(result["script_path"]).read_text()
    assert "sub-001" in content
    assert "/data/bids/sub-001" in content
