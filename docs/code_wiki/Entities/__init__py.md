---
kind: entity
type: module
aliases:
- Zotero MCP Server包
- package initializer
tags: []
---

# __init__py

## 概要 (Description)
SROS 包的根模块，定义了版本、作者、描述等元数据，并导出了 cli 模块的 app 对象。

## 关系 (Relations)
- (depends_on) [[OpenAlexBackend]] — Import statement: from .openalex_backend import OpenAlexBackend
- (depends_on) [[ZoteroHandler]] — from .handler import ZoteroHandler
- (depends_on) [[create_zotero_server]] — from .server import create_zotero_server
- (depends_on) [[app]] — from .cli import app
## 关联 (Related)
- [[Expose main components]]
- [[app]]
- [[__init__]]
- [[Federated Search]]
- [[OpenAlexBackend]]
- [[ZoteroHandler]]
- [[create_zotero_server]]
- [[Python包结构]]
## Sources
- [[__init__]]
