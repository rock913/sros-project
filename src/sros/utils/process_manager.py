"""进程管理工具"""

import subprocess
import sys
from typing import List, Optional

def start_process(command: List[str], cwd: Optional[str] = None) -> subprocess.Popen:
    """
    启动一个进程
    
    Args:
        command: 要执行的命令列表
        cwd: 工作目录
        
    Returns:
        subprocess.Popen 对象
    """
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        raise RuntimeError(f"Failed to start process: {e}")

def is_port_in_use(port: int) -> bool:
    """
    检查端口是否正在使用
    
    Args:
        port: 要检查的端口号
        
    Returns:
        如果端口正在使用则返回 True，否则返回 False
    """
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("localhost", port))
        sock.close()
        return result == 0
    except Exception:
        # 失败时保守认为端口被占用，避免启动时误覆盖其他服务
        return True