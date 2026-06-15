---
kind: entity
type: class
aliases: []
tags: []
---

# OpenAlexBackend

## 概要 (Description)
Implements a search backend that queries the OpenAlex API. Requires explicit enabling to perform network calls.

## 关系 (Relations)
- (depends_on) [[OpenAlex API]] — 调用https://api.openalex.org/works端点进行搜索
- (uses) [[重试与退避策略]] — _get_json_with_retry方法实现了指数退避的重试机制
- (calls) [[_get_env_int]] — __init__ 中调用 _get_env_int 获取 max_retries
- (calls) [[_get_env_float]] — __init__ 中调用 _get_env_float 获取 timeout_s 和 retry_backoff_s
## 关联 (Related)
- [[Federated Search]]
- [[__init__py]]
- [[OpenAlex API]]
- [[重试与退避策略]]
- [[__init__]]
- [[search]]
- [[_get_json_with_retry]]
- [[_abstract_from_inverted_index]]
- [[_transform_work]]
- [[_get_env_int]]
- [[_get_env_float]]
- [[后端切换策略]]
- [[联邦搜索]]
- [[ScholarHandler]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[SearchQuery]]
- [[在线离线策略]]
- [[Backend]]
- [[重试与限速策略]]
## Sources
- [[handler]]
- [[openalex_backend]]
- [[__init__]]
