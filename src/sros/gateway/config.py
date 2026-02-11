import os
from typing import Optional

class GatewayConfig:
    """Gateway 配置类"""
    
    # 默认端口
    DEFAULT_PORT = 8000
    
    # 端口设置
    port: int = DEFAULT_PORT
    
    # 服务地址
    host: str = "0.0.0.0"
    
    # SSE 相关配置
    sse_endpoint: str = "/sse"
    
    # MCP 服务配置
    mcp_servers: list = [
        "manuscript",
        "scholar", 
        "memory",
        "zotero"
    ]
    
    # 工作区路径
    workspace_dir: Optional[str] = None
    
    def __init__(self):
        self.port = int(os.getenv("SROS_PORT", self.DEFAULT_PORT))
        self.host = os.getenv("SROS_HOST", self.host)
        self.workspace_dir = os.getenv("SROS_WORKSPACE_DIR", None)