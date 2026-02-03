"""
Configuration for Zotero Expert MCP Server
"""
import os
from typing import Optional

class ZoteroExpertConfig:
    """Configuration class for Zotero Expert API integration."""
    
    def __init__(self):
        self.library_id: Optional[str] = os.getenv('ZOTERO_LIBRARY_ID')
        self.library_type: str = os.getenv('ZOTERO_LIBRARY_TYPE', 'user')
        self.api_key: Optional[str] = os.getenv('ZOTERO_API_KEY')
        self.base_url: str = os.getenv('ZOTERO_BASE_URL', 'https://api.zotero.org')
        self.timeout: int = int(os.getenv('ZOTERO_TIMEOUT', '30'))
        self.user_agent: str = os.getenv('ZOTERO_USER_AGENT', 'SROS-Zotero-Expert-MCP/1.0')
        
    def validate(self) -> bool:
        """Validate configuration settings."""
        # Library ID and API key are required for most operations
        return bool(self.library_id and self.api_key)
    
    def get_headers(self) -> dict:
        """Get headers for API requests."""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent
        }
        if self.api_key:
            headers['Zotero-API-Key'] = self.api_key
        return headers