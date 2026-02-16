"""健康检查工具"""

import asyncio
import time
import sys
import subprocess
from pathlib import Path
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
    
    def generate_report(self) -> Dict[str, Any]:
        """生成完整的健康报告"""
        report = {}
        
        # Python 环境检查
        try:
            import sys
            report["python_environment"] = {
                "status": "healthy",
                "details": f"Python {sys.version}"
            }
        except Exception as e:
            report["python_environment"] = {
                "status": "unhealthy",
                "details": str(e)
            }
        
        # 依赖检查
        try:
            import typer
            import fastapi
            import mcp
            import duckdb
            report["dependencies"] = {
                "status": "healthy",
                "details": "All required packages available"
            }
        except ImportError as e:
            report["dependencies"] = {
                "status": "unhealthy",
                "details": f"Missing dependency: {str(e)}"
            }
        
        # 端口检查
        try:
            from sros.utils.process_manager import is_port_in_use
            port_8000_used = is_port_in_use(8000)
            report["port_availability"] = {
                "status": "unhealthy" if port_8000_used else "healthy",
                "details": f"Port 8000 {'in use' if port_8000_used else 'available'}"
            }
        except Exception as e:
            report["port_availability"] = {
                "status": "unhealthy",
                "details": str(e)
            }
        
        # 数据库完整性检查
        try:
            workspace_db = Path.cwd() / ".sros" / "graph.db"
            if workspace_db.exists():
                report["database_integrity"] = {
                    "status": "healthy",
                    "details": f"Database exists at {workspace_db}"
                }
            else:
                report["database_integrity"] = {
                    "status": "warning",
                    "details": "Database not found in current directory"
                }
        except Exception as e:
            report["database_integrity"] = {
                "status": "unhealthy",
                "details": str(e)
            }
        
        # MCP 服务连通性检查
        try:
            # 检查是否有正在运行的服务
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 8000))
            sock.close()
            
            if result == 0:
                report["mcp_services"] = {
                    "status": "healthy",
                    "details": "Service running on localhost:8000"
                }
            else:
                report["mcp_services"] = {
                    "status": "warning",
                    "details": "No service running on localhost:8000"
                }
        except Exception as e:
            report["mcp_services"] = {
                "status": "unhealthy",
                "details": str(e)
            }
        
        return report
    
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