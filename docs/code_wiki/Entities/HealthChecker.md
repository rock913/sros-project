---
kind: entity
type: class
aliases: []
tags: []
---

# HealthChecker

## 概要 (Description)
健康检查器，初始化health_data字典（status, timestamp, services, errors）。核心方法generate_report()生成完整报告，内部调用多种检查逻辑，无参数，返回Dict[str, Any]。
## 关联 (Related)
- [[健康检查]]
- [[generate_report]]
- [[健康报告]]
## Sources
- [[health_checker]]
