---
kind: entity
type: function
aliases:
- OOM detection
tags: []
---

# check_oom

## 概要 (Description)
Check if job stderr contains OOM patterns. Uses local OOM_PATTERNS list.

## 关系 (Relations)
- (depends_on) [[OOM Retry]] — check_oom provides OOM detection used by submit_with_oom_retry.
- (calls) [[status]] — check_oom 需调用 status 获取作业状态
## 关联 (Related)
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[HPCHandler]]
- [[submit]]
- [[status]]
- [[cancel]]
- [[list_jobs]]
- [[submit_with_oom_retry]]
- [[_run]]
- [[Slurm 作业管理]]
- [[OOM 自动重试]]
- [[Dry-Run 模式]]
- [[logs]]
## Sources
- [[handler]]
