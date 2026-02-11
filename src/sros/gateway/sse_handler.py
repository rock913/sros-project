import asyncio
import json
import time
from typing import Dict, Any
from sros.gateway.config import GatewayConfig

class SSEHandler:
    """Shared health state for /health and SSE streams."""
    
    def __init__(self, config: GatewayConfig):
        self.config = config
        self.health_data = {
            "status": "healthy",
            "timestamp": None,
            "services": {}
        }
    
    def update_health(self, service_name: str, status: str):
        """更新服务健康状态"""
        self.health_data["services"][service_name] = status
        # Use wall-clock time to avoid event-loop availability issues.
        self.health_data["timestamp"] = time.time()
    
    def get_health_info(self) -> Dict[str, Any]:
        """获取健康检查信息"""
        return self.health_data