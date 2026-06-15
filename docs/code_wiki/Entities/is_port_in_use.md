---
kind: entity
type: function
aliases:
- 检查端口
tags: []
---

# is_port_in_use

## 概要 (Description)
检查指定端口是否被占用。通过创建socket连接localhost:port，如果连接成功则返回True，否则返回False
## 关联 (Related)
- [[端口扫描]]
- [[detect_free_port]]
- [[process_manager]]
- [[start_process]]
- [[端口探测]]
## Sources
- [[process_manager]]
- [[port_detector]]
