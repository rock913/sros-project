---
kind: entity
type: function
aliases: []
tags: []
---

# is_pid_alive

## 概要 (Description)
检查PID对应的进程是否存在。入参: pid，出参: bool。依赖psutil或os.kill。
## 关联 (Related)
- [[PID文件管理]]
- [[进程健康检查]]
- [[资源清理]]
- [[PortOwner]]
- [[pid_file_path]]
- [[read_pid_file]]
- [[write_pid_file]]
- [[remove_pid_file]]
- [[cleanup_zombie_pid_file]]
- [[find_port_owner]]
- [[PID文件生命周期管理]]
- [[进程存活检查与僵尸回收]]
- [[端口占用探测]]
## Sources
- [[gateway_process]]
