---
kind: entity
type: function
aliases: []
tags: []
---

# get_outline_tree_tool

## 概要 (Description)
MCP tool: receives file_path, calls service.get_outline_tree, returns JSON serialized OutlineNode.

## 关系 (Relations)
- (calls) [[ManuscriptProtocol]] — Calls service.get_outline_tree(file_path).

## 关联 (Related)
- [[MCP Server]]
- [[get_manuscript_service]]
- [[create_manuscript_server]]
- [[main]]
- [[ManuscriptProtocol]]
- [[find_gaps_tool]]
- [[insert_section_tool]]
- [[patch_draft_tool]]
## Sources
- [[server]]
