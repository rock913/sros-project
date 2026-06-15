---
kind: entity
type: function
aliases: []
tags: []
---

# update_health

## 概要 (Description)
Updates health status for a service and sets timestamp to current wall-clock time.

## 关系 (Relations)
- (calls) [[SSEHandler]] — Mutates self.health_data.

## 关联 (Related)
- [[Health State]]
- [[SSEHandler]]
- [[__init__]]
- [[get_health_info]]
## Sources
- [[sse_handler]]
