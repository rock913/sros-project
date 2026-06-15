---
kind: concept
aliases: []
tags:
- architecture
---

# OOM 自动重试

## 概要 (Description)
在作业因内存不足失败时自动递增内存重试，通过 _oom_retry_count 和 _oom_retry_mem 字典跟踪重试次数与内存增量。
## 关联 (Related)
- [[Slurm 作业管理]]
- [[Dry-Run 模式]]
- [[HPCHandler]]
- [[submit]]
- [[status]]
- [[cancel]]
- [[list_jobs]]
- [[logs]]
- [[check_oom]]
- [[submit_with_oom_retry]]
## Sources
- [[handler]]
