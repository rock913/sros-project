---
kind: entity
type: function
aliases:
- 启动进程
tags: []
---

# start_process

## 概要 (Description)
启动一个子进程，返回Popen对象。入参：command(List[str])命令列表，cwd(Optional[str])工作目录。出参：subprocess.Popen对象。副作用：启动系统进程。
## 关联 (Related)
- [[process_manager]]
- [[is_port_in_use]]
## Sources
- [[process_manager]]
