"""健康检查工具"""

import asyncio
import time
from typing import Dict, Any, Optional

class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        self.health_data = {
            "status": "unknown",
            "timestamp": None,
            "services": {},
            "errors": []
        }
    
    def update_service_status(self, service_name: str, status: str, error: Optional[str] = None):
        """更新服务状态"""
        self.health_data["services"][service_name] = {
            "status": status,
            "timestamp": time.time(),
            "error": error
        }
        # 更新总体状态
        self._update_overall_status()
    
    def _update_overall_status(self):
        """更新总体健康状态"""
        services = self.health_data["services"]
        if not services:
            self.health_data["status"] = "unknown"
            return
            
        # 如果有任何服务失败，则整体失败
        if any(service["status"] != "healthy" for service in services.values()):
            self.health_data["status"] = "unhealthy"
        else:
            self.health_data["status"] = "healthy"
    
    def get_health_report(self) -> Dict[str, Any]:
        """获取健康报告"""
        self.health_data["timestamp"] = time.time()
        return self.health_data.copy()
    
    async def check_service_health(self, service_name: str, check_func, *args, **kwargs):
        """异步检查服务健康状态"""
        try:
            result = await check_func(*args, **kwargs)
            self.update_service_status(service_name, "healthy")
            return True
        except Exception as e:
            error_msg = str(e)
            self.update_service_status(service_name, "unhealthy", error_msg)
            return False