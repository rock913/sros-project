"""Manuscript MCP Server"""

from .handler import ManuscriptHandler
from .server import create_manuscript_server

__all__ = ['ManuscriptHandler', 'create_manuscript_server']