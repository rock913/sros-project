"""
Configuration for DuckDB Memory MCP Server
"""

import os
from pathlib import Path

# Default database path
DEFAULT_DB_PATH = os.getenv('SROS_DUCKDB_PATH', '.sros/graph.db')

# Database configuration
DB_CONFIG = {
    'path': DEFAULT_DB_PATH,
    'timeout': 30,  # Connection timeout in seconds
    'read_only': False
}

# Performance settings
PERFORMANCE_CONFIG = {
    'memory_limit': '1GB',  # DuckDB memory limit
    'threads': 4,  # Number of threads to use
    'enable_profiling': False  # Enable query profiling
}

# Logging configuration
LOGGING_CONFIG = {
    'level': os.getenv('SROS_LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.getenv('SROS_DUCKDB_LOG_FILE', '.sros/logs/duckdb.log')
}

def get_db_path() -> str:
    """Get the database path from environment or default."""
    return DEFAULT_DB_PATH

def ensure_sros_directory():
    """Ensure the SROS directory structure exists."""
    db_path = Path(get_db_path())
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create logs directory
    logs_dir = db_path.parent / 'logs'
    logs_dir.mkdir(exist_ok=True)