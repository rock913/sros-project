---
kind: entity
type: function
aliases: []
tags: []
---

# generate_report

## 概要 (Description)
生成完整的健康报告，无参数，返回Dict[str, Any]。包含workspace、python_environment、dependencies、port_availability、database_integrity及ARC Code-Wiki相关检查。

## 关系 (Relations)
- (calls) [[HealthChecker]] — generate_report是HealthChecker的方法

## 关联 (Related)
- [[健康检查]]
- [[HealthChecker]]
## Sources
- [[health_checker]]
