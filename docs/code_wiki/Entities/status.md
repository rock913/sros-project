---
kind: entity
type: function
aliases:
- squeue status
tags: []
---

# status

## 概要 (Description)
Displays the current status of the SROS gateway process: PID, port, uptime from the PID file.

## 关系 (Relations)
- (calls) [[_run]] — status calls _run with squeue command.
- (depends_on) [[cancel]] — status 中可能间接触发 cancel 逻辑（未显式，但从上下文推断）
## 关联 (Related)
- [[Workspace Initialization]]
- [[Gateway Lifecycle Management]]
- [[MCP Server Integration]]
- [[Environment Configuration]]
- [[app]]
- [[validate_workspace_dir]]
- [[init]]
- [[start]]
- [[doctor]]
- [[stop]]
- [[restart]]
- [[OOM Retry]]
- [[Dry-Run Mode]]
- [[Slurm State Model]]
- [[HPCHandler]]
- [[submit]]
- [[cancel]]
- [[list_jobs]]
- [[check_oom]]
- [[submit_with_oom_retry]]
- [[_run]]
- [[Gateway Process Lifecycle]]
- [[Slurm 作业管理]]
- [[OOM 自动重试]]
- [[Dry-Run 模式]]
- [[logs]]
## Sources
- [[handler]]
- [[cli]]
