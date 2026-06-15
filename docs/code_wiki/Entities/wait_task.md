---
kind: entity
type: function
aliases: []
tags: []
---

# wait_task

## 概要 (Description)
等待任务完成（状态为 succeeded 或 failed），支持超时和轮询间隔。入参：task_id（字符串）、timeout_s（浮点数，默认30.0）、poll_interval_s（浮点数，默认0.05）。出参：轮询到任务完成时返回 get_task 的结果；超时返回包含 ok、error 和 task_id 的字典。

## 关系 (Relations)
- (calls) [[get_task]] — 在循环中调用 self.get_task() 轮询任务状态
- (calls) [[get_task]] — got = self.get_task(task_id)
## 关联 (Related)
- [[Task Management]]
- [[TasksHandler]]
- [[run_plugin_async]]
- [[get_task]]
- [[list_tasks]]
- [[Long-running Task]]
- [[Polling-based Wait]]
## Sources
- [[handler]]
