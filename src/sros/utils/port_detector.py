"""端口检测工具"""

import socket
from typing import Tuple, Optional

def detect_free_port(start_port: int = 8000, max_ports: int = 100) -> Optional[int]:
    """
    检测可用端口
    
    Args:
        start_port: 开始检测的端口号
        max_ports: 最大检测端口数量
        
    Returns:
        可用端口号，如果没有找到则返回 None
    """
    for port in range(start_port, start_port + max_ports):
        if not is_port_in_use(port):
            return port
    return None

def is_port_in_use(port: int) -> bool:
    """
    检查端口是否正在使用
    
    Args:
        port: 要检查的端口号
        
    Returns:
        如果端口正在使用则返回 True，否则返回 False
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("localhost", port))
        sock.close()
        return result == 0
    except Exception:
        return True