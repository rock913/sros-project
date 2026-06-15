---
kind: entity
type: function
aliases: []
tags: []
---

# get_task_manager

## 概要 (Description)
返回全局唯一的 TaskManager 实例（单例模式）。

## 关系 (Relations)
- (calls) [[TaskManager]] — get_task_manager 创建或返回全局 _GLOBAL_TASK_MANAGER 实例。
- (calls) [[TaskManager]] — get_task_manager 创建/返回全局 TaskManager 实例
## 关联 (Related)
- [[任务生命周期]]
- [[通知机制]]
- [[TaskRecord]]
- [[TaskManager]]
- [[Global Singleton]]
- [[Notifier Pattern]]
- [[TaskState]]
- [[TaskRecordstate]]
- [[Notifier]]
## Sources
- [[task_manager]]
