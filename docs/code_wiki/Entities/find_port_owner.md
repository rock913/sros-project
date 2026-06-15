---
kind: entity
type: function
aliases: []
tags: []
---

# find_port_owner

## 概要 (Description)
查找监听指定TCP端口的进程。入参: port，出参: PortOwner。依赖psutil。

## 关系 (Relations)
- (depends_on) [[PortOwner]] — find_port_owner返回PortOwner实例

## 关联 (Related)
- [[PID文件管理]]
- [[进程健康检查]]
- [[资源清理]]
- [[PortOwner]]
- [[pid_file_path]]
- [[read_pid_file]]
- [[write_pid_file]]
- [[remove_pid_file]]
- [[is_pid_alive]]
- [[cleanup_zombie_pid_file]]
- [[PID文件生命周期管理]]
- [[进程存活检查与僵尸回收]]
- [[端口占用探测]]
## Sources
- [[gateway_process]]
