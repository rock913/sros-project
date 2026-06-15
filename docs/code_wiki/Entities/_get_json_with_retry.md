---
kind: entity
type: function
aliases: []
tags: []
---

# _get_json_with_retry

## 概要 (Description)
使用指数退避重试策略发送GET请求并解析JSON。最多重试max_retries次，两次重试间休眠当前退避时间（第一次0.75s，之后翻倍）。成功返回响应JSON，失败抛出RuntimeError。副作用：网络I/O。
## 关联 (Related)
- [[OpenAlex API]]
- [[重试与退避策略]]
- [[OpenAlexBackend]]
- [[__init__]]
- [[search]]
- [[_abstract_from_inverted_index]]
- [[_transform_work]]
- [[_get_env_int]]
- [[_get_env_float]]
- [[重试与限速策略]]
## Sources
- [[openalex_backend]]
