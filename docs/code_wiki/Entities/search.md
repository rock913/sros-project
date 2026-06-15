---
kind: entity
type: function
aliases: []
tags: []
---

# search

## 概要 (Description)
执行搜索：构造请求参数（包括search、per-page、select和mailto），调用_get_json_with_retry获取结果，遍历每条work调用_transform_work转换格式。返回转换后的结果列表。

## 关系 (Relations)
- (calls) [[_get_json_with_retry]] — search方法中调用self._get_json_with_retry(url, params=params)
- (calls) [[_transform_work]] — search方法遍历work时调用self._transform_work(work)

## 关联 (Related)
- [[OpenAlex API]]
- [[重试与退避策略]]
- [[OpenAlexBackend]]
- [[__init__]]
- [[_get_json_with_retry]]
- [[_abstract_from_inverted_index]]
- [[_transform_work]]
- [[_get_env_int]]
- [[_get_env_float]]
- [[重试与限速策略]]
## Sources
- [[openalex_backend]]
