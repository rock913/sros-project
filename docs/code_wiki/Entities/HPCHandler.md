---
kind: entity
type: class
aliases:
- Handler
- HPC Handler
tags: []
---

# HPCHandler

## 概要 (Description)
HPCHandler is the main class for HPC resource handling.

## 关系 (Relations)
- (calls) [[_run]] — All Slurm commands (submit, status, etc.) call _run to execute shell commands.
- (depends_on) [[Dry-Run Mode]] — HPCHandler uses dry_run flag to bypass actual Slurm commands.
- (depends_on) [[Slurm State Model]] — HPCHandler relies on Slurm states (PENDING, RUNNING, etc.) for job status.
- (calls) [[submit]] — HPCHandler.submit 被 HPCHandler.submit_with_oom_retry 调用以实现重试逻辑
## 关联 (Related)
- [[__init__]]
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[submit]]
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
- [[__init__]]
