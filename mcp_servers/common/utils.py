"""Shared utility functions for SROS MCP servers."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Set up logging for an SROS component."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def ensure_directory_exists(path: str) -> None:
    """Ensure a directory exists, creating it if necessary."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to a maximum length and add ellipsis if truncated."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_env_var(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable with optional default."""
    return os.getenv(var_name, default)


def is_docker() -> bool:
    """Check if running inside a Docker container."""
    return os.path.exists('/.dockerenv')


def format_citation_key(authors: List[str], year: Optional[int], title: str) -> str:
    """Format a citation key in the style author_year_title."""
    if authors:
        first_author = authors[0].split()[-1].lower()
    else:
        first_author = "unknown"
    
    year_str = str(year) if year else "nd"
    title_words = ''.join(title.split()[:3]).lower()[:20]
    
    return f"{first_author}_{year_str}_{title_words}"