"""
Providers for Federal Academic Search MCP Server
"""

from .base import BaseProvider
from .openalex import OpenAlexProvider
from .unpaywall import UnpaywallProvider
from .semantic_scholar import SemanticScholarProvider

__all__ = [
    'BaseProvider',
    'OpenAlexProvider',
    'UnpaywallProvider',
    'SemanticScholarProvider'
]