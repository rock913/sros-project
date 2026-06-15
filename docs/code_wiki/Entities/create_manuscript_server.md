---
kind: entity
type: function
aliases: []
tags: []
---

# create_manuscript_server

## 概要 (Description)
创建稿件 MCP 服务器的工厂函数，在 .server 模块中定义，具体入参和出参待查看实现。

## 关系 (Relations)
- (calls) [[get_manuscript_service]] — 在每个工具函数内部调用 get_manuscript_service() 获取服务实例。
- (calls) [[get_manuscript_service]] — Inside each tool handler, calls get_manuscript_service() to obtain service instance.
- (manages) [[MCP Server]] — Returns a configured Server instance with tools.
## 关联 (Related)
- [[__init__]]
- [[ManuscriptHandler]]
- [[MCP Tool]]
- [[ManuscriptProtocol]]
- [[get_manuscript_service]]
- [[main]]
- [[MCP Server]]
- [[find_gaps_tool]]
- [[get_outline_tree_tool]]
- [[insert_section_tool]]
- [[patch_draft_tool]]
## Sources
- [[server]]
- [[__init__]]
