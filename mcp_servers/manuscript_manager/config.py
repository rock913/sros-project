"""
Configuration for Manuscript Manager MCP Server
"""

import os
from pathlib import Path

# Load environment variables from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not available, continue with system environment variables only
    pass

# Default manuscript path
DEFAULT_MANUSCRIPT_PATH = os.getenv('SROS_MANUSCRIPT_PATH', 'draft.md')

# Editing configuration
EDITING_CONFIG = {
    'atomic_edits': True,  # Ensure all edits are atomic
    'backup_on_edit': True,  # Create backup before editing
    'max_section_size': 10000,  # Maximum section size in characters
}

# Gap detection configuration
GAP_DETECTION_CONFIG = {
    'min_section_length': 50,  # Minimum section length to avoid flagging
    'citation_check_threshold': 100,  # Minimum length to check for citations
    'todo_keywords': ['TODO', 'FIXME', 'TBD'],  # Keywords to detect as explicit gaps
}

# Backup configuration
BACKUP_CONFIG = {
    'enabled': True,
    'backup_dir': '.sros/backups',
    'keep_backups': 5,  # Number of backups to keep
}

def get_manuscript_path() -> str:
    """Get the manuscript path from environment or default."""
    return DEFAULT_MANUSCRIPT_PATH

def ensure_sros_directory():
    """Ensure the SROS directory structure exists."""
    manuscript_path = Path(get_manuscript_path())
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create backups directory
    if BACKUP_CONFIG['enabled']:
        backup_dir = Path(BACKUP_CONFIG['backup_dir'])
        backup_dir.mkdir(parents=True, exist_ok=True)

def create_backup(manuscript_path: str) -> str:
    """Create a backup of the manuscript."""
    if not BACKUP_CONFIG['enabled']:
        return ""
    
    import shutil
    from datetime import datetime
    
    manuscript_file = Path(manuscript_path)
    if not manuscript_file.exists():
        return ""
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{manuscript_file.stem}_{timestamp}{manuscript_file.suffix}"
    backup_path = Path(BACKUP_CONFIG['backup_dir']) / backup_filename
    
    # Copy the file
    shutil.copy2(manuscript_path, backup_path)
    
    # Clean up old backups
    cleanup_old_backups()
    
    return str(backup_path)

def cleanup_old_backups():
    """Remove old backups, keeping only the configured number."""
    if not BACKUP_CONFIG['enabled']:
        return
    
    backup_dir = Path(BACKUP_CONFIG['backup_dir'])
    if not backup_dir.exists():
        return
    
    # Get all backup files
    backup_files = list(backup_dir.glob(f"{Path(get_manuscript_path()).stem}_*"))
    
    # Sort by modification time (oldest first)
    backup_files.sort(key=lambda x: x.stat().st_mtime)
    
    # Remove excess backups
    excess_count = len(backup_files) - BACKUP_CONFIG['keep_backups']
    for i in range(excess_count):
        if i < len(backup_files):
            backup_files[i].unlink()