---
kind: entity
type: function
aliases:
- OOM retry submission
tags: []
---

# submit_with_oom_retry

## 概要 (Description)
Submit job and if OOM is detected, retry with increased memory. Uses _oom_retry_count and _oom_retry_mem dicts.

## 关系 (Relations)
- (calls) [[submit]] — submit_with_oom_retry calls submit to initially submit the job.
- (calls) [[check_oom]] — submit_with_oom_retry calls check_oom to detect OOM after job completion.
- (calls) [[HPCHandler]] — submit_with_oom_retry updates _oom_retry_count and _oom_retry_mem dicts on HPCHandler.
- (calls) [[check_oom]] — 重试时先通过 check_oom 判断是否 OOM
## 关联 (Related)
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[HPCHandler]]
- [[submit]]
- [[status]]
- [[cancel]]
- [[list_jobs]]
- [[check_oom]]
- [[_run]]
- [[Slurm 作业管理]]
- [[OOM 自动重试]]
- [[Dry-Run 模式]]
- [[logs]]
## Sources
- [[handler]]
