---
kind: entity
type: function
aliases: []
tags: []
---

# write_pid_file

## 概要 (Description)
写入PID文件，包含pid、port和started_at。入参: workspace_dir, pid, port，出参: Optional[Path]。副作用：创建目录和文件。

## 关系 (Relations)
- (calls) [[pid_file_path]] — 内部使用pid_file_path计算路径，但直接构建Path
- (calls) [[pid_file_path]] — write_pid_file内部调用pid_file_path生成路径
- (manages) [[PID文件生命周期管理]] — 写入PID文件，管理生命周期中的创建状态
## 关联 (Related)
- [[PID文件管理]]
- [[进程健康检查]]
- [[资源清理]]
- [[PortOwner]]
- [[pid_file_path]]
- [[read_pid_file]]
- [[remove_pid_file]]
- [[is_pid_alive]]
- [[cleanup_zombie_pid_file]]
- [[find_port_owner]]
- [[PID文件生命周期管理]]
- [[进程存活检查与僵尸回收]]
- [[端口占用探测]]
## Sources
- [[gateway_process]]
