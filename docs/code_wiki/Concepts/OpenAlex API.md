---
kind: concept
aliases: []
tags:
- architecture
---

# OpenAlex API

## 概要 (Description)
OpenAlex提供的开放学术数据API，用于搜索学术作品。本模块通过`requests`库同步调用其`/works`端点。
## 关联 (Related)
- [[重试与退避策略]]
- [[OpenAlexBackend]]
- [[__init__]]
- [[search]]
- [[_get_json_with_retry]]
- [[_abstract_from_inverted_index]]
- [[_transform_work]]
- [[_get_env_int]]
- [[_get_env_float]]
## Sources
- [[openalex_backend]]
