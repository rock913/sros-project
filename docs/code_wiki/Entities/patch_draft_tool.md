---
kind: entity
type: function
aliases: []
tags: []
---

# patch_draft_tool

## 概要 (Description)
MCP tool: receives patches list, file_path, expected_sha256; calls service.patch_draft; returns JSON result dict.

## 关系 (Relations)
- (calls) [[ManuscriptProtocol]] — Calls service.patch_draft(...).

## 关联 (Related)
- [[MCP Server]]
- [[get_manuscript_service]]
- [[create_manuscript_server]]
- [[main]]
- [[ManuscriptProtocol]]
- [[find_gaps_tool]]
- [[get_outline_tree_tool]]
- [[insert_section_tool]]
## Sources
- [[server]]
