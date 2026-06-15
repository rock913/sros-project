# SROS Code-Wiki

## 快速上下文（给 AI Agent）

Scientific Research Operating System — AI-native research assistant for academic writing, data ingestion, and HPC scheduling

**核心设计模式**：Contract-First（`emit_ok`/`emit_error` 契约）、Offline-First（Mock 可测）、Backend Strategy（可插拔后端）、Hash Trap（`compiler_version` 触发重编译）。

## 按模块架构导航

### domain (src/sros/domain) — 10 files

**核心概念**：[[Data Modeling]]、[[Expose main components]]、[[Federated Search]]、[[Pydantic v2 note Recursive models need to be rebuilt after module loading]]、[[Python包结构]]、[[Scholarly Research Protocol]]、[[memory_models]]、[[乐观并发控制]]、[[内存协议契约]]、[[协议接口]]、[[协议约定]]、[[在线离线策略]]
  ... 等 20 个概念
**核心实体**：[[Backend]]、[[GapAnalysisResult]]、[[MemoryHandler]]、[[OutlineNode]]、[[ResearchPerspective]]、[[ScholarProtocol]]、[[SearchQuery]]、[[ZoteroProtocol]]、[[__init__]]、[[__init__py]]、[[find_gaps]]、[[get_citation_map]]、[[get_file_sha256]]、[[get_outline_tree]]、[[insert_section]]、[[patch_draft]]
  ... 等 18 个实体

### gateway (src/sros/gateway) — 5 files

**核心概念**：[[Health State]]、[[Reflection Call]]、[[Reflection-based RPC]]、[[SSE Hub]]、[[SSE Transport]]、[[Thin Reflector]]、[[Thread-Bridge Notification]]、[[Tool Registry]]、[[config]]、[[环境变量覆盖]]、[[进程内RPC]]
**核心实体**：[[GatewayConfig]]、[[SROSGateway]]、[[SROSGateway__init__]]、[[SROSGatewaydispatch_jsonrpc]]、[[SROSGatewaymcp_list_tools]]、[[SROSGatewaystart]]、[[SSEHandler]]、[[STATIC_TOOLS]]、[[SkillCallResult]]、[[SkillReflector]]、[[call]]、[[create_app]]、[[dispatch_jsonrpc]]、[[get_health_info]]、[[mcp_list_tools]]、[[update_health]]

### servers (src/sros/servers) — 23 files

**核心概念**：[[Citation validation]]、[[Data Ingestion Pipeline]]、[[Deterministic external tool wrapper]]、[[Dry-Run Mode]]、[[Dry-Run 模式]]、[[DuckDB持久化]]、[[Execution Sandbox]]、[[External RAG Services]]、[[Figure reference indexing]]、[[Knowledge Graph Integration]]、[[Knowledge Graph Model]]、[[Knowledge Graph Registry]]
  ... 等 43 个概念
**核心实体**：[[Citation]]、[[DBHandler]]、[[DataHandler]]、[[HPCHandler]]、[[KnowledgeEdge]]、[[ManuscriptProtocol]]、[[MemoryHandler__del__]]、[[MemoryHandler__init__]]、[[MemoryHandlerget_citation_map]]、[[MemoryHandlerquery_knowledge]]、[[MemoryHandlerstore_knowledge]]、[[MemoryProtocol]]、[[OpenAlexBackend]]、[[RagChunk]]、[[RagHandler_chunk_text]]、[[RagHandler_ensure_schema]]
  ... 等 85 个实体

### skills (src/sros/skills) — 4 files

**核心概念**：[[CLI Routing]]、[[Environment Configuration]]、[[Gateway Lifecycle Management]]、[[Gateway Process Lifecycle]]、[[MCP Server Integration]]、[[Manuscript Service]]、[[Output Formatting]]、[[Plugin System]]、[[Raw vs Human Output]]、[[Reflection Gateway Input]]、[[Skill-based CLI V3]]、[[Task Management]]
  ... 等 15 个概念
**核心实体**：[[ExtHandler]]、[[ManuscriptHandler]]、[[RagHandler]]、[[ScholarHandler]]、[[TasksHandler]]、[[app]]、[[dispatch_tool]]、[[doctor]]、[[init]]、[[main]]、[[manuscript_find_gaps]]、[[manuscript_get_file_sha256_compat]]、[[manuscript_get_outline_tree_compat]]、[[manuscript_index_figures]]、[[manuscript_insert]]、[[manuscript_outline]]
  ... 等 22 个实体

### utils (src/sros/utils) — 7 files

**核心概念**：[[Global Singleton]]、[[Notifier Pattern]]、[[PID文件生命周期管理]]、[[PID文件管理]]、[[Plugin Lifecycle]]、[[Plugin Metadata Protocol]]、[[Safe Plugin Loading]]、[[Workspace Layout Convention]]、[[process_manager]]、[[任务生命周期]]、[[健康报告]]、[[健康检查]]
  ... 等 19 个概念
**核心实体**：[[HealthChecker]]、[[Notifier]]、[[PluginInfo]]、[[PluginLoadError]]、[[PortOwner]]、[[TaskManager]]、[[TaskRecord]]、[[TaskRecordstate]]、[[TaskState]]、[[cleanup_zombie_pid_file]]、[[detect_free_port]]、[[discover_plugins]]、[[find_port_owner]]、[[generate_report]]、[[get_plugins_dir]]、[[get_task_manager]]
  ... 等 27 个实体

## 概念 (Concepts)

- [[__main__]] 🟠
- [[Citation validation]] 🟡
- [[CLI Routing]] 🟠
- [[config]] 🟢
- [[Data Ingestion Pipeline]] 🟡
- [[Data Modeling]] 🔵
- [[Deterministic external tool wrapper]] 🟡
- [[Dry-Run Mode]] 🟡
- [[Dry-Run 模式]] 🟡
- [[DuckDB持久化]] 🟡
- [[Environment Configuration]] 🟠
- [[Execution Sandbox]] 🟡
- [[Expose main components]] 🔵
- [[External RAG Services]] 🟡
- [[Federated Search]] 🔵
- [[Figure reference indexing]] 🟡
- [[Gateway Lifecycle Management]] 🟠
- [[Gateway Process Lifecycle]] 🟠
- [[Global Singleton]] 🟣
- [[Health State]] 🟢
- [[Knowledge Graph Integration]] 🟡
- [[Knowledge Graph Model]] 🟡
- [[Knowledge Graph Registry]] 🟡
- [[Long-running Task]] 🟡
- [[Manuscript Service]] 🟠
- [[MCP Server]] 🟡
- [[MCP Server Integration]] 🟠
- [[MCP Tool]] 🟡
- [[MCP服务器]] 🟡
- [[MCP服务器模式]] 🟡
- [[memory_models]] 🔵
- [[Notifier Pattern]] 🟣
- [[OOM Retry]] 🟡
- [[OOM 自动重试]] 🟡
- [[OpenAlex API]] 🟡
- [[Output Formatting]] 🟠
- [[Persistence Pattern]] 🟡
- [[PID文件生命周期管理]] 🟣
- [[PID文件管理]] 🟣
- [[Plugin Lifecycle]] 🟣
- [[Plugin Metadata Protocol]] 🟣
- [[Plugin System]] 🟠
- [[Polling-based Wait]] 🟡
- [[process_manager]] 🟣
- [[Pydantic v2 note Recursive models need to be rebuilt after module loading]] 🔵
- [[Python包结构]] 🔵
- [[Raw vs Human Output]] 🟠
- [[Reflection Call]] 🟢
- [[Reflection Gateway Input]] 🟠
- [[Reflection-based RPC]] 🟢
- [[Safe Plugin Loading]] 🟣
- [[Schema Migration]] 🟡
- [[Scholarly Research Protocol]] 🔵
- [[Secure Script Execution]] 🟡
- [[Skill-based CLI V3]] 🟠
- [[Slurm State Model]] 🟡
- [[Slurm 作业管理]] 🟡
- [[SSE Hub]] 🟢
- [[SSE Transport]] 🟢
- [[Task Management]] 🟠
- [[Thin Reflector]] 🟢
- [[Thread-Bridge Notification]] 🟢
- [[Token Matching Retrieval]] 🟡
- [[Tool Dispatch Pattern]] 🟠
- [[Tool Registry]] 🟢
- [[Workspace Initialization]] 🟠
- [[Workspace Layout Convention]] 🟣
- [[Workspace-Relative Path Resolution]] 🟡
- [[Workspace-relative path resolution]] 🟡
- [[Workspace-Relative Path Validation]] 🟡
- [[乐观并发控制]] 🔵
- [[任务生命周期]] 🟣
- [[健康报告]] 🟣
- [[健康检查]] 🟣
- [[内存协议契约]] 🔵
- [[协议接口]] 🔵
- [[协议约定]] 🔵
- [[可测试性设计]] 🟡
- [[后端切换策略]] 🟡
- [[后端选择与回退策略]] 🟡
- [[在线离线策略]] 🔵
- [[外部工具封装]] 🟡
- [[工具注册模式]] 🟡
- [[延迟导入以满足性能要求]] 🟡
- [[懒加载服务初始化]] 🟡
- [[持久化存储]] 🟡
- [[数据摄取工作流]] 🟡
- [[数据模型]] 🔵
- [[数据模型定义]] 🔵
- [[模型上下文协议MCP服务器]] 🟡
- [[环境变量覆盖]] 🟢
- [[知识图谱存储协议]] 🔵
- [[知识图谱模式]] 🟡
- [[知识图谱边类型枚举]] 🔵
- [[研究协议模式]] 🔵
- [[端口占用探测]] 🟣
- [[端口扫描]] 🟣
- [[端口探测]] 🟣
- [[结构化返回]] 🔵
- [[联邦搜索]] 🔵
- [[资源清理]] 🟣
- [[进程健康检查]] 🟣
- [[进程内RPC]] 🟢
- [[进程存活检查与僵尸回收]] 🟣
- [[递归数据模型]] 🔵
- [[通知机制]] 🟣
- [[重试与退避策略]] 🟡
- [[重试与限速策略]] 🟡

## 实体 (Entities)

- [[__del__]] 🟡
- [[__init__]] 🔵
- [[__init__py]] 🔵
- [[_abstract_from_inverted_index]] 🟡
- [[_chunk_text]] 🟡
- [[_get_env_float]] 🟡
- [[_get_env_int]] 🟡
- [[_get_json_with_retry]] 🟡
- [[_ingest_bids]] 🟡
- [[_ingest_clinical]] 🟡
- [[_ingest_participants]] 🟡
- [[_iter_files]] 🟡
- [[_resolve_ws_path]] 🟡
- [[_run]] 🟡
- [[_serialize_rows]] 🟡
- [[_transform_work]] 🟡
- [[_validate_citekeys_exist]] 🟡
- [[_workspace_root]] 🟡
- [[add_citation]] 🟡
- [[add_citation_tool]] 🟡
- [[app]] 🟠
- [[Backend]] 🔵
- [[brainstorm_perspectives]] 🟡
- [[brainstorm_perspectives_tool]] 🟡
- [[build]] 🟡
- [[call]] 🟢
- [[cancel]] 🟡
- [[check_oom]] 🟡
- [[Citation]] 🟡
- [[cleanup_zombie_pid_file]] 🟣
- [[close]] 🟡
- [[create_app]] 🟢
- [[create_manuscript_server]] 🟡
- [[create_memory_server]] 🟡
- [[create_scholar_server]] 🟡
- [[create_zotero_server]] 🟡
- [[DataHandler]] 🟡
- [[DBHandler]] 🟡
- [[detect_free_port]] 🟣
- [[discover_plugins]] 🟣
- [[dispatch_jsonrpc]] 🟢
- [[dispatch_tool]] 🟠
- [[doctor]] 🟠
- [[ExtHandler]] 🟠
- [[federated_search]] 🟡
- [[federated_search_tool]] 🟡
- [[find_critiques]] 🟡
- [[find_critiques_tool]] 🟡
- [[find_gaps]] 🔵
- [[find_gaps_tool]] 🟡
- [[find_port_owner]] 🟣
- [[GapAnalysisResult]] 🔵
- [[GatewayConfig]] 🟢
- [[generate_report]] 🟣
- [[get_citation]] 🟡
- [[get_citation_map]] 🔵
- [[get_citation_map_tool]] 🟡
- [[get_citation_tool]] 🟡
- [[get_file_sha256]] 🔵
- [[get_health_info]] 🟢
- [[get_manuscript_service]] 🟡
- [[get_memory_service]] 🟡
- [[get_outline_tree]] 🔵
- [[get_outline_tree_tool]] 🟡
- [[get_plugins_dir]] 🟣
- [[get_scholar_service]] 🟡
- [[get_task]] 🟡
- [[get_task_manager]] 🟣
- [[get_workspace_dir]] 🟣
- [[get_zotero_service]] 🟡
- [[HealthChecker]] 🟣
- [[HPCHandler]] 🟡
- [[index_figure_references]] 🟡
- [[ingest]] 🟡
- [[init]] 🟠
- [[init_schema]] 🟡
- [[insert_section]] 🔵
- [[insert_section_tool]] 🟡
- [[is_pid_alive]] 🟣
- [[is_port_in_use]] 🟣
- [[KnowledgeEdge]] 🟡
- [[list_jobs]] 🟡
- [[list_tasks]] 🟡
- [[load_plugin]] 🟣
- [[logs]] 🟡
- [[main]] 🟠
- [[manuscript_find_gaps]] 🟠
- [[manuscript_get_file_sha256_compat]] 🟠
- [[manuscript_get_outline_tree_compat]] 🟠
- [[manuscript_index_figures]] 🟠
- [[manuscript_insert]] 🟠
- [[manuscript_outline]] 🟠
- [[manuscript_refactor]] 🟠
- [[manuscript_sha256]] 🟠
- [[ManuscriptHandler]] 🟠
- [[ManuscriptProtocol]] 🟡
- [[mcp_list_tools]] 🟢
- [[MemoryHandler]] 🔵
- [[MemoryHandler__del__]] 🟡
- [[MemoryHandler__init__]] 🟡
- [[MemoryHandlerget_citation_map]] 🟡
- [[MemoryHandlerquery_knowledge]] 🟡
- [[MemoryHandlerstore_knowledge]] 🟡
- [[MemoryProtocol]] 🟡
- [[Notifier]] 🟣
- [[OpenAlexBackend]] 🟡
- [[OutlineNode]] 🔵
- [[parse_plugin_metadata]] 🟣
- [[patch_draft]] 🔵
- [[patch_draft_tool]] 🟡
- [[pid_file_path]] 🟣
- [[PluginInfo]] 🟣
- [[PluginLoadError]] 🟣
- [[PortOwner]] 🟣
- [[preview_csv]] 🟡
- [[query]] 🟡
- [[query_knowledge]] 🔵
- [[query_knowledge_tool]] 🟡
- [[RagChunk]] 🟡
- [[RagHandler]] 🟠
- [[RagHandler_chunk_text]] 🟡
- [[RagHandler_ensure_schema]] 🟡
- [[RagHandler_iter_files]] 🟡
- [[RagHandlerbuild]] 🟡
- [[RagHandlerquery]] 🟡
- [[read_pid_file]] 🟣
- [[remove_pid_file]] 🟣
- [[ResearchPerspective]] 🔵
- [[resolve_workspace_path]] 🟡
- [[restart]] 🟠
- [[run_plugin]] 🟣
- [[run_plugin_async]] 🟡
- [[run_script]] 🟡
- [[ScholarHandler]] 🟠
- [[ScholarProtocol]] 🔵
- [[search]] 🟡
- [[search_citations]] 🟡
- [[search_citations_tool]] 🟡
- [[SearchQuery]] 🔵
- [[SkillCallResult]] 🟢
- [[SkillReflector]] 🟢
- [[SROSGateway]] 🟢
- [[SROSGateway__init__]] 🟢
- [[SROSGatewaydispatch_jsonrpc]] 🟢
- [[SROSGatewaymcp_list_tools]] 🟢
- [[SROSGatewaystart]] 🟢
- [[SSEHandler]] 🟢
- [[start]] 🟠
- [[start_process]] 🟣
- [[STATIC_TOOLS]] 🟢
- [[status]] 🟡
- [[stop]] 🟠
- [[store_knowledge]] 🔵
- [[store_knowledge_tool]] 🟡
- [[submit]] 🟡
- [[submit_with_oom_retry]] 🟡
- [[TaskManager]] 🟣
- [[TaskRecord]] 🟣
- [[TaskRecordstate]] 🟣
- [[TasksHandler]] 🟠
- [[TaskState]] 🟣
- [[update_health]] 🟢
- [[validate_workspace_dir]] 🟠
- [[wait_task]] 🟡
- [[web_scrape]] 🟡
- [[write_pid_file]] 🟣
- [[ZoteroHandler]] 🟡
- [[ZoteroProtocol]] 🔵

## 综合 (Synthesis)
