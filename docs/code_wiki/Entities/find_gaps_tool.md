---
kind: entity
type: function
aliases: []
tags: []
---

# find_gaps_tool

## 概要 (Description)
MCP tool: receives file_path, calls service.find_gaps, returns JSON serialized list of GapAnalysisResult.

## 关系 (Relations)
- (calls) [[ManuscriptProtocol]] — Calls service.find_gaps(file_path) after obtaining service from get_manuscript_service().

## 关联 (Related)
- [[MCP Server]]
- [[get_manuscript_service]]
- [[create_manuscript_server]]
- [[main]]
- [[ManuscriptProtocol]]
- [[get_outline_tree_tool]]
- [[insert_section_tool]]
- [[patch_draft_tool]]
## Sources
- [[server]]
