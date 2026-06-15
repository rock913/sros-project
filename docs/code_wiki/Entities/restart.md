---
kind: entity
type: function
aliases: []
tags: []
---

# restart

## 概要 (Description)
Stops the current gateway and starts a new one with updated parameters. Parameters: workspace_dir, port, auto_port, timeout_s.

## 关系 (Relations)
- (calls) [[stop]] — restart calls stop(...)
- (calls) [[start]] — restart calls start(...)

## 关联 (Related)
- [[Workspace Initialization]]
- [[Gateway Lifecycle Management]]
- [[MCP Server Integration]]
- [[Environment Configuration]]
- [[app]]
- [[validate_workspace_dir]]
- [[init]]
- [[start]]
- [[doctor]]
- [[status]]
- [[stop]]
- [[Gateway Process Lifecycle]]
## Sources
- [[cli]]
