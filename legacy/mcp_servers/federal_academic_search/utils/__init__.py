"""
Utilities for Federal Academic Search MCP Server
"""

from .helpers import (
    normalize_doi,
    extract_paper_id_from_url,
    sanitize_query,
    merge_paper_data,
    format_authors,
    estimate_reading_time,
    is_valid_email,
    truncate_text
)

__all__ = [
    'normalize_doi',
    'extract_paper_id_from_url',
    'sanitize_query',
    'merge_paper_data',
    'format_authors',
    'estimate_reading_time',
    'is_valid_email',
    'truncate_text'
]