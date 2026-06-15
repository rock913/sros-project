---
kind: entity
type: function
aliases: []
tags: []
---

# create_scholar_server

## 概要 (Description)
工厂函数，用于创建 scholar MCP 服务器实例，导入自 .server 模块。

## 关系 (Relations)
- (calls) [[brainstorm_perspectives_tool]] — 内部注册tool，创建闭包函数
- (calls) [[find_critiques_tool]] — 内部注册tool
- (calls) [[federated_search_tool]] — 内部注册tool
- (calls) [[get_scholar_service]] — 各工具函数内部调用get_scholar_service()获取服务实例
## 关联 (Related)
- [[__init__]]
- [[ScholarHandler]]
- [[MCP Tool]]
- [[get_scholar_service]]
- [[main]]
- [[brainstorm_perspectives_tool]]
- [[find_critiques_tool]]
- [[federated_search_tool]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[MCP服务器模式]]
- [[懒加载服务初始化]]
## Sources
- [[server]]
- [[__init__]]
