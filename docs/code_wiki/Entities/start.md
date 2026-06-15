---
kind: entity
type: function
aliases: []
tags: []
---

# start

## 概要 (Description)
Starts the SROS gateway: validates workspace, loads env, detects free port, starts gateway process, updates MCP/Claude configs. Parameters: workspace_dir, port, auto_port, reload, update_mcp_json, mcp_host, server_key, update_clauderc.

## 关系 (Relations)
- (calls) [[validate_workspace_dir]] — Called to validate workspace path before starting gateway
- (calls) [[validate_workspace_dir]] — start calls validate_workspace_dir(workspace_dir)
- (implements) [[Gateway Process Lifecycle]] — start manages gateway process startup
## 关联 (Related)
- [[Workspace Initialization]]
- [[Gateway Lifecycle Management]]
- [[MCP Server Integration]]
- [[Environment Configuration]]
- [[app]]
- [[validate_workspace_dir]]
- [[init]]
- [[doctor]]
- [[status]]
- [[stop]]
- [[restart]]
- [[Gateway Process Lifecycle]]
## Sources
- [[cli]]
