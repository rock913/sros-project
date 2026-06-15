---
kind: entity
type: function
aliases: []
tags: []
---

# web_scrape

## 概要 (Description)
静态方法，发送HTTP GET请求抓取网页内容，解析标题并去除HTML标签。入参：url, timeout_s；出参：同ExtHandler。副作用：网络请求（可monkeypatch）
## 关联 (Related)
- [[Deterministic external tool wrapper]]
- [[ExtHandler]]
- [[外部工具封装]]
- [[可测试性设计]]
## Sources
- [[handler]]
