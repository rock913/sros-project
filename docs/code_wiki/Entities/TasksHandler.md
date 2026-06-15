---
kind: entity
type: class
aliases:
- task handler
tags: []
---

# TasksHandler

## 概要 (Description)
任务API的入口，提供运行插件任务、获取任务状态、列出所有任务和等待任务完成的方法。所有方法返回包含 ok 标志和结果或错误信息的字典。
## 关联 (Related)
- [[Task Management]]
- [[run_plugin_async]]
- [[get_task]]
- [[list_tasks]]
- [[wait_task]]
- [[Tool Dispatch Pattern]]
- [[Plugin System]]
- [[Manuscript Service]]
- [[External RAG Services]]
- [[dispatch_tool]]
- [[discover_plugins]]
- [[run_plugin]]
- [[ManuscriptHandler]]
- [[ExtHandler]]
- [[RagHandler]]
- [[ScholarHandler]]
- [[Long-running Task]]
- [[Polling-based Wait]]
## Sources
- [[rpc]]
- [[handler]]
