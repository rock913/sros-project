---
kind: entity
type: function
aliases:
- squeue list
tags: []
---

# list_jobs

## 概要 (Description)
List jobs for a user (default: current user) via squeue -u. Returns list of jobs and count.

## 关系 (Relations)
- (calls) [[_run]] — list_jobs calls _run with squeue -u command.

## 关联 (Related)
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[HPCHandler]]
- [[submit]]
- [[status]]
- [[cancel]]
- [[check_oom]]
- [[submit_with_oom_retry]]
- [[_run]]
- [[Slurm 作业管理]]
- [[OOM 自动重试]]
- [[Dry-Run 模式]]
- [[logs]]
## Sources
- [[handler]]
