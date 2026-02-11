"""SROS - Scientific Research Assistant"""

__version__ = "2.3.2"

# 导出主要的入口点
from sros.cli import app as cli_app

# 为方便起见，也导出一些核心组件
from sros.gateway.main import SROSGateway
from sros.domain.ports.manuscript_protocol import ManuscriptProtocol
from sros.domain.ports.scholar_protocol import ScholarProtocol
from sros.domain.ports.memory_protocol import MemoryProtocol
from sros.domain.ports.zotero_protocol import ZoteroProtocol

__all__ = [
    "cli_app",
    "SROSGateway",
    "ManuscriptProtocol",
    "ScholarProtocol", 
    "MemoryProtocol",
    "ZoteroProtocol"
]