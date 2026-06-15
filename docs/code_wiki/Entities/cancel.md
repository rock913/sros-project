---
kind: entity
type: function
aliases:
- scancel
tags: []
---

# cancel

## 概要 (Description)
Cancel a job via scancel. Returns cancellation status.

## 关系 (Relations)
- (calls) [[_run]] — cancel calls _run with scancel command.

## 关联 (Related)
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[HPCHandler]]
- [[submit]]
- [[status]]
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
