"""
Base Provider for Federal Academic Search MCP Server
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import aiohttp
import time
import random

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """Base class for all academic search providers."""

    def __init__(self, config):
        self.config = config
        self.session = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def _make_request_with_retry(self, method: str, url: str, headers: dict, **kwargs) -> Optional[aiohttp.ClientResponse]:
        """Make HTTP request with retry logic."""
        last_exception = None
        
        max_retries = getattr(self.config, 'openalex_max_retries', 3)
        rate_limit_delay = getattr(self.config, 'openalex_rate_limit_delay', 1.0)
        timeout = getattr(self.config, 'openalex_timeout', 30)
        
        # Set timeout
        if 'timeout' not in kwargs:
            kwargs['timeout'] = aiohttp.ClientTimeout(total=timeout)
        
        for attempt in range(max_retries + 1):
            try:
                # Add rate limiting delay
                if attempt > 0:
                    delay = rate_limit_delay * (2 ** (attempt - 1))  # Exponential backoff
                    delay += random.uniform(0, 0.1)  # Add jitter
                    await asyncio.sleep(delay)
                
                response = await self.session.request(method, url, headers=headers, **kwargs)
                
                # Handle rate limiting
                if response.status == 429:
                    logger.warning(f"Rate limited on attempt {attempt + 1} for {url}")
                    if attempt < max_retries:
                        continue
                    else:
                        response.raise_for_status()
                elif response.status >= 500:
                    logger.warning(f"Server error {response.status} on attempt {attempt + 1} for {url}")
                    if attempt < max_retries:
                        continue
                    else:
                        response.raise_for_status()
                else:
                    return response
                    
            except aiohttp.ClientError as e:
                last_exception = e
                logger.warning(f"Request failed on attempt {attempt + 1} for {url}: {str(e)}")
                if attempt >= max_retries:
                    raise e
            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error on attempt {attempt + 1} for {url}: {str(e)}")
                if attempt >= max_retries:
                    raise e
                    
        raise last_exception

    @abstractmethod
    async def search_papers(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for academic papers."""
        pass

    @abstractmethod
    async def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific paper."""
        pass