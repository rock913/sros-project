---
kind: entity
type: function
aliases: []
tags: []
---

# call

## 概要 (Description)
执行技能调用，接收 tool_name (str) 和 arguments (Dict[str, Any])，返回 SkillCallResult；内部调用 sros.skills.rpc.dispatch_tool。
## 关联 (Related)
- [[进程内RPC]]
- [[SkillCallResult]]
- [[SkillReflector]]
- [[Reflection-based RPC]]
## Sources
- [[skill_reflector]]
