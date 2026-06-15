---
kind: entity
type: function
aliases: []
tags: []
---

# __init__

## 概要 (Description)
Constructor, takes a db_path (string or Path). Creates parent directories and opens DuckDB connection.

## 关系 (Relations)
- (calls) [[_get_env_int]] — __init__中调用_get_env_int设置max_retries
- (calls) [[_get_env_float]] — __init__中调用_get_env_float设置timeout_s和retry_backoff_s
- (calls) [[ZoteroHandler]] — 构造函数，初始化实例状态
- (calls) [[SSEHandler]] — Called during instantiation.
- (depends_on) [[DBHandler]] — from .handler import DBHandler
- (calls) [[ZoteroHandler]] — self._initialize_schema()
## 关联 (Related)
- [[Data Ingestion Pipeline]]
- [[DBHandler]]
- [[close]]
- [[init_schema]]
- [[ingest]]
- [[query]]
- [[OpenAlex API]]
- [[重试与退避策略]]
- [[OpenAlexBackend]]
- [[search]]
- [[_get_json_with_retry]]
- [[_abstract_from_inverted_index]]
- [[_transform_work]]
- [[_get_env_int]]
- [[_get_env_float]]
- [[Schema Migration]]
- [[ZoteroHandler]]
- [[ZoteroProtocol]]
- [[Citation]]
- [[add_citation]]
- [[get_citation]]
- [[search_citations]]
- [[__del__]]
- [[Health State]]
- [[SSEHandler]]
- [[update_health]]
- [[get_health_info]]
- [[重试与限速策略]]
- [[持久化存储]]
## Sources
- [[__init__]]
- [[sse_handler]]
- [[openalex_backend]]
- [[handler]]
