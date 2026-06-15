---
kind: entity
type: function
aliases: []
tags: []
---

# init

## 概要 (Description)
Initializes a new SROS project: creates workspace structure, .sros directory, config, pid file, .env, and optionally updates Roo modes and Claude instructions. Parameters: project_name, target, gateway_url, server_key, with_roomodes.

## 关系 (Relations)
- (calls) [[validate_workspace_dir]] — Called to validate workspace path during project init
- (calls) [[validate_workspace_dir]] — init calls validate_workspace_dir(project_dir)
- (implements) [[Workspace Initialization]] — init sets up workspace structure per the initialization pattern
## 关联 (Related)
- [[Workspace Initialization]]
- [[Gateway Lifecycle Management]]
- [[MCP Server Integration]]
- [[Environment Configuration]]
- [[app]]
- [[validate_workspace_dir]]
- [[start]]
- [[doctor]]
- [[status]]
- [[stop]]
- [[restart]]
- [[Gateway Process Lifecycle]]
## Sources
- [[cli]]
