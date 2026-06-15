from __future__ import annotations

from pathlib import Path

from sros.servers.hpc.handler import HPCHandler


def test_check_oom_in_log_content():
    stderr = """
slurmstepd: error: Detected 1 oom-kill event(s) in StepId=12345.batch.
Some of your processes may have been killed by the cgroup out-of-memory handler.
Memory used: 32768MB, limit: 32768MB
"""
    assert HPCHandler.check_oom(stderr) is True


def test_check_oom_false_for_normal_error():
    stderr = """
FileNotFoundError: [Errno 2] No such file or directory: '/data/sub-001/T1w.nii.gz'
srun: error: task 0 exited with code 1
"""
    assert HPCHandler.check_oom(stderr) is False


def test_oom_pattern_variants():
    test_cases = [
        ("oom-kill event", True),
        ("exceeded job memory limit for job 12345", True),
        ("OutOfMemoryError", True),
        ("slurmstepd: oom", True),
        ("Job finished successfully", False),
        ("Segmentation fault (core dumped)", False),
        ("Illegal instruction", False),
        ("", False),
    ]
    for text, expected in test_cases:
        assert HPCHandler.check_oom(text) == expected, f"Failed for: {text!r}"


def test_mem_parse_with_oom_quick(tmp_path: Path):
    """Memory parsing works for a typical Slurm script."""
    script = tmp_path / "test_oom.slurm"
    script.write_text("#!/bin/bash\n#SBATCH --job-name=fmriprep\n#SBATCH --mem=16G\n#SBATCH --cpus-per-task=8\n\nmodule load apptainer\napptainer run ...\n")
    mem, unit = HPCHandler._parse_sbatch_mem(str(script))
    assert mem == 16

    h = HPCHandler(dry_run=True)
    new_path = h._rewrite_mem(str(script), 32)
    content = Path(new_path).read_text()
    assert "--mem=32G" in content
    assert "--mem=16G" not in content


def test_double_mem_multiple_times(tmp_path: Path):
    """Memory can be rewritten multiple times (16G → 32G → 48G)."""
    script = tmp_path / "multi_oom.slurm"
    script.write_text("#!/bin/bash\n#SBATCH --mem=16G\n")

    h = HPCHandler(dry_run=True)

    # 16G → 32G
    p1 = h._rewrite_mem(str(script), 32)
    assert "--mem=32G" in Path(p1).read_text()

    # 32G → 48G
    p2 = h._rewrite_mem(p1, 48)
    assert "--mem=48G" in Path(p2).read_text()
    assert "--mem=32G" not in Path(p2).read_text()


def test_submit_with_oom_retry_missing_script(tmp_path: Path):
    """OOM retry handles missing script gracefully."""
    h = HPCHandler(dry_run=False)
    result = h.submit_with_oom_retry(str(tmp_path / "nonexistent.slurm"))
    assert result["ok"] is False
