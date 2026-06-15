---
kind: entity
type: function
aliases: []
tags: []
---

# read_pid_file

## 概要 (Description)
读取并解析PID文件，返回字典或None。入参: workspace_dir，出参: Optional[Dict]。

## 关系 (Relations)
- (calls) [[pid_file_path]] — 内部调用pid_file_path获取路径
- (calls) [[pid_file_path]] — read_pid_file内部调用pid_file_path生成路径
- (manages) [[PID文件生命周期管理]] — 读取PID文件，管理生命周期中的读取状态
## 关联 (Related)
- [[PID文件管理]]
- [[进程健康检查]]
- [[资源清理]]
- [[PortOwner]]
- [[pid_file_path]]
- [[write_pid_file]]
- [[remove_pid_file]]
- [[is_pid_alive]]
- [[cleanup_zombie_pid_file]]
- [[find_port_owner]]
- [[PID文件生命周期管理]]
- [[进程存活检查与僵尸回收]]
- [[端口占用探测]]
## Sources
- [[gateway_process]]
