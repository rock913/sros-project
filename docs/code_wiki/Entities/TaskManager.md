---
kind: entity
type: class
aliases: []
tags: []
---

# TaskManager

## 概要 (Description)
管理任务的容器，提供启动、获取、列出方法，内部使用锁和线程执行任务。

## 关系 (Relations)
- (manages) [[TaskRecord]] — TaskManager 内部维护 _tasks: Dict[str, TaskRecord] 并操作记录。
- (depends_on) [[TaskRecord]] — _manager._tasks 存储 TaskRecord 实例
## 关联 (Related)
- [[任务生命周期]]
- [[通知机制]]
- [[TaskRecord]]
- [[get_task_manager]]
- [[Global Singleton]]
- [[Notifier Pattern]]
- [[TaskState]]
- [[TaskRecordstate]]
- [[Notifier]]
## Sources
- [[task_manager]]
