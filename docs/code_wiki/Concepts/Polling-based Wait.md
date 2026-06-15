---
kind: concept
aliases: []
tags:
- architecture
---

# Polling-based Wait

## 概要 (Description)
The wait_task method polls get_task in a loop until the task state is 'succeeded' or 'failed' or a timeout occurs.
## 关联 (Related)
- [[Long-running Task]]
- [[TasksHandler]]
- [[run_plugin_async]]
- [[get_task]]
- [[list_tasks]]
- [[wait_task]]
## Sources
- [[handler]]
