---
kind: entity
type: function
aliases: []
tags: []
---

# cleanup_zombie_pid_file

## 概要 (Description)
清理指向已不存在进程的PID文件。入参: workspace_dir，出参: bool（是否清理了僵尸文件）。

## 关系 (Relations)
- (calls) [[read_pid_file]] — 调用read_pid_file读取数据
- (calls) [[is_pid_alive]] — 调用is_pid_alive检查进程
- (calls) [[remove_pid_file]] — 在进程不存在时调用remove_pid_file
- (calls) [[read_pid_file]] — cleanup_zombie_pid_file调用read_pid_file获取数据
- (calls) [[is_pid_alive]] — cleanup_zombie_pid_file调用is_pid_alive判断进程存活
- (calls) [[remove_pid_file]] — 在进程不存在时调用remove_pid_file删除文件
- (manages) [[进程存活检查与僵尸回收]] — 实现了僵尸PID文件回收逻辑
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
- [[find_port_owner]]
- [[PID文件生命周期管理]]
- [[进程存活检查与僵尸回收]]
- [[端口占用探测]]
## Sources
- [[gateway_process]]
