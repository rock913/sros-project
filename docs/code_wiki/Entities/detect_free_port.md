---
kind: entity
type: function
aliases: []
tags: []
---

# detect_free_port

## 概要 (Description)
检测指定范围内第一个可用的端口号。开始端口start_port（默认8000），最大检测数量max_ports（默认100）。返回可用端口号或None

## 关系 (Relations)
- (calls) [[is_port_in_use]] — detect_free_port在循环中调用is_port_in_use检查每个端口
- (calls) [[is_port_in_use]] — 在for循环中调用is_port_in_use(port)以检查端口状态
## 关联 (Related)
- [[端口扫描]]
- [[is_port_in_use]]
- [[端口探测]]
## Sources
- [[port_detector]]
