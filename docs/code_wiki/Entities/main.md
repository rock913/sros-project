---
kind: entity
type: function
aliases: []
tags: []
---

# main

## 概要 (Description)
Async entry point: loads GatewayConfig, creates SROSGateway, and starts uvicorn server with SSE transport.

## 关系 (Relations)
- (calls) [[GatewayConfig]] — main(config: GatewayConfig)
- (calls) [[SROSGateway]] — gateway = SROSGateway(config)
- (calls) [[create_manuscript_server]] — main() 中调用 create_manuscript_server() 创建服务器。
- (calls) [[create_memory_server]] — async def main中调用create_memory_server()
- (calls) [[create_scholar_server]] — 调用create_scholar_server()创建server
- (calls) [[create_zotero_server]] — main 函数中调用 create_zotero_server() 创建服务器
- (calls) [[create_manuscript_server]] — Async main calls create_manuscript_server() to instantiate server.
- (calls) [[create_memory_server]] — main函数中调用create_memory_server()创建服务器
- (calls) [[create_scholar_server]] — main中调用create_scholar_server()获取server对象
- (calls) [[create_zotero_server]] — main 函数中调用 create_zotero_server()
- (calls) [[app]] — def main() -> None: app()
## 关联 (Related)
- [[SSE Transport]]
- [[Tool Registry]]
- [[Reflection Call]]
- [[Thread-Bridge Notification]]
- [[SROSGateway]]
- [[create_app]]
- [[STATIC_TOOLS]]
- [[SkillReflector]]
- [[GatewayConfig]]
- [[mcp_list_tools]]
- [[dispatch_jsonrpc]]
- [[MCP Tool]]
- [[ManuscriptProtocol]]
- [[get_manuscript_service]]
- [[create_manuscript_server]]
- [[MCP服务器]]
- [[工具注册模式]]
- [[get_memory_service]]
- [[create_memory_server]]
- [[store_knowledge_tool]]
- [[query_knowledge_tool]]
- [[get_citation_map_tool]]
- [[get_scholar_service]]
- [[create_scholar_server]]
- [[brainstorm_perspectives_tool]]
- [[find_critiques_tool]]
- [[federated_search_tool]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[get_zotero_service]]
- [[create_zotero_server]]
- [[add_citation_tool]]
- [[get_citation_tool]]
- [[search_citations_tool]]
- [[__main__]]
- [[SSE Hub]]
- [[Thin Reflector]]
- [[SROSGateway__init__]]
- [[SROSGatewaymcp_list_tools]]
- [[SROSGatewaydispatch_jsonrpc]]
- [[SROSGatewaystart]]
- [[MCP Server]]
- [[find_gaps_tool]]
- [[get_outline_tree_tool]]
- [[insert_section_tool]]
- [[patch_draft_tool]]
- [[模型上下文协议MCP服务器]]
- [[MemoryProtocol]]
- [[KnowledgeEdge]]
- [[MCP服务器模式]]
- [[懒加载服务初始化]]
- [[延迟导入以满足性能要求]]
- [[app]]
## Sources
- [[__main__]]
- [[server]]
- [[main]]
