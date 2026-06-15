---
kind: entity
type: function
aliases:
- sbatch submit
tags: []
---

# submit

## 概要 (Description)
Submit a Slurm script via sbatch. Accepts script_path and optional array_size. Returns job_id or error. Side effect: updates _oom_retry_count/mem dicts.

## 关系 (Relations)
- (calls) [[_run]] — submit calls _run with sbatch command.

## 关联 (Related)
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[HPCHandler]]
- [[status]]
- [[cancel]]
- [[list_jobs]]
- [[check_oom]]
- [[submit_with_oom_retry]]
- [[_run]]
- [[Slurm 作业管理]]
- [[OOM 自动重试]]
- [[Dry-Run 模式]]
- [[logs]]
## Sources
- [[handler]]
