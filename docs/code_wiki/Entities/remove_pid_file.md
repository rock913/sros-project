---
kind: entity
type: function
aliases: []
tags: []
---

# remove_pid_file

## 概要 (Description)
删除PID文件，忽略不存在的错误。入参: workspace_dir。副作用：删除文件。

## 关系 (Relations)
- (calls) [[pid_file_path]] — 内部调用pid_file_path获取路径
- (calls) [[pid_file_path]] — remove_pid_file内部调用pid_file_path生成路径
- (manages) [[PID文件生命周期管理]] — 删除PID文件，管理生命周期中的销毁状态
## 关联 (Related)
- [[PID文件管理]]
- [[进程健康检查]]
- [[资源清理]]
- [[PortOwner]]
- [[pid_file_path]]
- [[read_pid_file]]
- [[write_pid_file]]
- [[is_pid_alive]]
- [[cleanup_zombie_pid_file]]
- [[find_port_owner]]
- [[PID文件生命周期管理]]
- [[进程存活检查与僵尸回收]]
- [[端口占用探测]]
## Sources
- [[gateway_process]]
