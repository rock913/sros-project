"""
Configuration for Semantic Scholar MCP Server
"""
import os
from typing import Optional

class SemanticScholarConfig:
    """Configuration class for Semantic Scholar API integration."""
    
    def __init__(self):
        self.api_key: Optional[str] = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
        self.base_url: str = os.getenv('SEMANTIC_SCHOLAR_BASE_URL', 'https://api.semanticscholar.org/graph/v1')
        self.timeout: int = int(os.getenv('SEMANTIC_SCHOLAR_TIMEOUT', '30'))
        self.rate_limit_delay: float = float(os.getenv('SEMANTIC_SCHOLAR_RATE_LIMIT_DELAY', '1.0'))
        self.max_retries: int = int(os.getenv('SEMANTIC_SCHOLAR_MAX_RETRIES', '3'))
        self.cache_enabled: bool = os.getenv('SEMANTIC_SCHOLAR_CACHE_ENABLED', 'true').lower() == 'true'
        self.cache_ttl: int = int(os.getenv('SEMANTIC_SCHOLAR_CACHE_TTL', '3600'))  # 1 hour default
        self.cache_dir: str = os.getenv('SEMANTIC_SCHOLAR_CACHE_DIR', '.cache')
        self.user_agent: str = os.getenv('SEMANTIC_SCHOLAR_USER_AGENT', 'SROS-SemanticScholar-MCP/1.0')
        
    def validate(self) -> bool:
        """Validate configuration settings."""
        # API key is optional for some endpoints, but recommended
        return True
    
    def get_headers(self) -> dict:
        """Get headers for API requests."""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent
        }
        if self.api_key:
            headers['x-api-key'] = self.api_key
        return headers