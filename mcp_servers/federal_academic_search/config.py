"""
Configuration for Federal Academic Search MCP Server
"""
import os
from typing import Optional


class FederalAcademicSearchConfig:
    """Configuration class for Federal Academic Search API integration."""

    def __init__(self):
        # OpenAlex configuration
        self.openalex_base_url: str = os.getenv('OPENALEX_BASE_URL', 'https://api.openalex.org')
        self.openalex_email: Optional[str] = os.getenv('OPENALEX_EMAIL')
        self.openalex_timeout: int = int(os.getenv('OPENALEX_TIMEOUT', '30'))
        self.openalex_rate_limit_delay: float = float(os.getenv('OPENALEX_RATE_LIMIT_DELAY', '1.0'))
        self.openalex_max_retries: int = int(os.getenv('OPENALEX_MAX_RETRIES', '3'))

        # Unpaywall configuration
        self.unpaywall_base_url: str = os.getenv('UNPAYWALL_BASE_URL', 'https://api.unpaywall.org/v2')
        self.unpaywall_email: Optional[str] = os.getenv('UNPAYWALL_EMAIL')
        self.unpaywall_timeout: int = int(os.getenv('UNPAYWALL_TIMEOUT', '30'))
        self.unpaywall_rate_limit_delay: float = float(os.getenv('UNPAYWALL_RATE_LIMIT_DELAY', '1.0'))
        self.unpaywall_max_retries: int = int(os.getenv('UNPAYWALL_MAX_RETRIES', '3'))

        # Semantic Scholar configuration
        self.s2_api_key: Optional[str] = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
        self.s2_timeout: int = int(os.getenv('SEMANTIC_SCHOLAR_TIMEOUT', '30'))
        self.s2_rate_limit_delay: float = float(os.getenv('SEMANTIC_SCHOLAR_RATE_LIMIT_DELAY', '1.0'))
        self.s2_max_retries: int = int(os.getenv('SEMANTIC_SCHOLAR_MAX_RETRIES', '3'))

        # Cache configuration
        self.cache_enabled: bool = os.getenv('ACADEMIC_SEARCH_CACHE_ENABLED', 'true').lower() == 'true'
        self.cache_db_path: str = os.getenv('ACADEMIC_SEARCH_CACHE_DB_PATH', '.cache/academic_search.db')
        self.cache_ttl: int = int(os.getenv('ACADEMIC_SEARCH_CACHE_TTL', '3600'))  # 1 hour default

        # User agent
        self.user_agent: str = os.getenv('ACADEMIC_SEARCH_USER_AGENT', 'SROS-Federal-Academic-Search-MCP/1.0')

    def validate(self) -> bool:
        """Validate configuration settings."""
        # Email is required for OpenAlex and Unpaywall
        if not self.openalex_email:
            raise ValueError("OPENALEX_EMAIL is required for OpenAlex API access")
        if not self.unpaywall_email:
            raise ValueError("UNPAYWALL_EMAIL is required for Unpaywall API access")
        return True

    def get_openalex_headers(self) -> dict:
        """Get headers for OpenAlex API requests."""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent,
            'mailto': self.openalex_email
        }
        return headers

    def get_unpaywall_headers(self) -> dict:
        """Get headers for Unpaywall API requests."""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent
        }
        return headers

    def get_s2_headers(self) -> dict:
        """Get headers for Semantic Scholar API requests."""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent
        }
        if self.s2_api_key:
            headers['x-api-key'] = self.s2_api_key
        return headers