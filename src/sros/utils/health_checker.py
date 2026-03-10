"""健康检查工具"""

import time
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

        workspace_dir = Path(
            (Path(str(Path.cwd())).resolve())
        )
        try:
            import os

            env_workspace = os.getenv("SROS_WORKSPACE_DIR")
            if env_workspace:
                workspace_dir = Path(env_workspace).expanduser().resolve()
        except Exception:
            pass

        report["workspace"] = {
            "status": "healthy",
            "details": str(workspace_dir),
        }
        
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
        
        # 数据库完整性/可用性检查
        try:
            workspace_db = workspace_dir / ".sros" / "graph.db"
            if workspace_db.exists():
                db_details = f"Database exists at {workspace_db}"
                db_status = "healthy"
                try:
                    import duckdb

                    # Read-only connect to avoid acquiring an exclusive lock.
                    conn = duckdb.connect(str(workspace_db), read_only=True)
                    conn.execute("SELECT 1").fetchone()
                    conn.close()
                except Exception as db_exc:
                    msg = str(db_exc)
                    db_status = "warning"
                    if "Conflicting lock" in msg or "Could not set lock" in msg:
                        db_details = f"Database exists but appears locked by another process. {msg}"
                    else:
                        db_details = f"Database exists but could not be opened read-only. {msg}"

                report["database_integrity"] = {
                    "status": db_status,
                    "details": db_details,
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

        # Scholar/OpenAlex 配置检查（不触发网络）
        try:
            import os

            backend = (os.getenv("SROS_SCHOLAR_BACKEND") or "mock").strip().lower()
            mailto = (
                os.getenv("SROS_OPENALEX_MAILTO")
                or os.getenv("SROS_OPENALEX_EMAIL")
                or os.getenv("OPENALEX_EMAIL")
            )

            if backend == "openalex":
                if mailto:
                    report["scholar_backend"] = {
                        "status": "healthy",
                        "details": f"SROS_SCHOLAR_BACKEND=openalex (mailto configured)",
                    }
                else:
                    report["scholar_backend"] = {
                        "status": "warning",
                        "details": "SROS_SCHOLAR_BACKEND=openalex but OPENALEX_EMAIL/SROS_OPENALEX_MAILTO is not set",
                    }
            else:
                report["scholar_backend"] = {
                    "status": "healthy",
                    "details": f"SROS_SCHOLAR_BACKEND={backend}",
                }
        except Exception as e:
            report["scholar_backend"] = {
                "status": "warning",
                "details": str(e),
            }
        
        # MCP 服务连通性检查（/health + /sse?once=1 语义）
        try:
            import requests

            health_ok = False
            sse_ok = False
            details = []

            try:
                resp = requests.get("http://localhost:8000/health", timeout=1)
                health_ok = resp.status_code == 200
                details.append(f"/health={resp.status_code}")
            except Exception as e:
                details.append(f"/health error: {e}")

            try:
                resp = requests.get("http://localhost:8000/sse?once=1", timeout=2)
                if resp.status_code == 200 and "text/event-stream" in resp.headers.get("content-type", ""):
                    body = resp.text
                    # MCP SSE transport expects an endpoint event.
                    sse_ok = "event: endpoint" in body and "data: /messages" in body
                details.append(f"/sse?once=1={resp.status_code}")
            except Exception as e:
                details.append(f"/sse error: {e}")

            if health_ok and sse_ok:
                report["mcp_services"] = {
                    "status": "healthy",
                    "details": "; ".join(details),
                }
            elif health_ok or sse_ok:
                report["mcp_services"] = {
                    "status": "warning",
                    "details": "; ".join(details),
                }
            else:
                report["mcp_services"] = {
                    "status": "warning",
                    "details": "; ".join(details),
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