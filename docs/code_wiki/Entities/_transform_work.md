---
kind: entity
type: function
aliases: []
tags: []
---

# _transform_work

## 概要 (Description)
静态方法：将单个work记录转换为统一格式的字典。提取authors、venue（先primary_location后best_oa_location）、abstract、url等字段，并添加source='openalex'。

## 关系 (Relations)
- (calls) [[_abstract_from_inverted_index]] — _transform_work中调用OpenAlexBackend._abstract_from_inverted_index(work.get('abstract_inverted_index'))

## 关联 (Related)
- [[OpenAlex API]]
- [[重试与退避策略]]
- [[OpenAlexBackend]]
- [[__init__]]
- [[search]]
- [[_get_json_with_retry]]
- [[_abstract_from_inverted_index]]
- [[_get_env_int]]
- [[_get_env_float]]
- [[重试与限速策略]]
## Sources
- [[openalex_backend]]
