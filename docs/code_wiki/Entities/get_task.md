---
kind: entity
type: function
aliases: []
tags: []
---

# get_task

## 概要 (Description)
根据 task_id 获取任务状态。入参：task_id（字符串）。出参：如果找到任务，返回包含 ok 和 task 字典的字典；否则返回包含 ok、error 和 task_id 的字典。
## 关联 (Related)
- [[Task Management]]
- [[TasksHandler]]
- [[run_plugin_async]]
- [[list_tasks]]
- [[wait_task]]
- [[Long-running Task]]
- [[Polling-based Wait]]
## Sources
- [[handler]]
