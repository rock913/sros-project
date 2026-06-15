---
kind: entity
type: class
aliases: []
tags: []
---

# SSEHandler

## 概要 (Description)
Manages shared health state for the gateway. __init__(config: GatewayConfig) initializes health_data with default status; update_health(service_name: str, status: str) updates a service's status and records wall-clock timestamp; get_health_info() returns the full health_data dict.
## 关联 (Related)
- [[Health State]]
- [[__init__]]
- [[update_health]]
- [[get_health_info]]
## Sources
- [[sse_handler]]
