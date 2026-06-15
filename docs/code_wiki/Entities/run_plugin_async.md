---
kind: entity
type: function
aliases: []
tags: []
---

# run_plugin_async

## 概要 (Description)
异步运行插件任务。入参：plugin（字符串）、args（字典）。出参：包含 ok 和 task_id 的字典。副作用：通过任务管理器启动新线程执行任务。
## 关联 (Related)
- [[Task Management]]
- [[TasksHandler]]
- [[get_task]]
- [[list_tasks]]
- [[wait_task]]
- [[Long-running Task]]
- [[Polling-based Wait]]
## Sources
- [[handler]]
