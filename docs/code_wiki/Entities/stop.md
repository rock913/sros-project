---
kind: entity
type: function
aliases: []
tags: []
---

# stop

## 概要 (Description)
Stops the SROS gateway process gracefully with timeout, optionally killing port owners. Parameters: workspace_dir, timeout_s, port, kill_port_owner.

## 关系 (Relations)
- (calls) [[validate_workspace_dir]] — stop calls validate_workspace_dir(workspace_dir)

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
- [[restart]]
- [[Gateway Process Lifecycle]]
## Sources
- [[cli]]
