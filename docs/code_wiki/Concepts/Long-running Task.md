---
kind: concept
aliases:
- async task
tags:
- architecture
---

# Long-running Task

## 概要 (Description)
Tasks run in-process in a separate thread; completion may be broadcast via SSE as a JSON-RPC notification.
## 关联 (Related)
- [[Polling-based Wait]]
- [[TasksHandler]]
- [[run_plugin_async]]
- [[get_task]]
- [[list_tasks]]
- [[wait_task]]
## Sources
- [[handler]]
