"""
Cache manager for Semantic Scholar MCP Server
"""
import os
import json
import hashlib
import time
from typing import Any, Optional

# Handle relative imports properly
try:
    from .config import SemanticScholarConfig
except (ImportError, ValueError):
    # Fallback for direct script execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from config import SemanticScholarConfig

class CacheManager:
    """Simple file-based cache manager for API responses."""
    
    def __init__(self, config: SemanticScholarConfig):
        self.config = config
        self.cache_dir = config.cache_dir
        self.enabled = config.cache_enabled
        self.ttl = config.cache_ttl
        
        # Create cache directory if it doesn't exist
        if self.enabled:
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, url: str, params: dict) -> str:
        """Generate a cache key from URL and parameters."""
        key_string = f"{url}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get the file path for a cache key."""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, url: str, params: dict) -> Optional[Any]:
        """Get cached response if available and not expired."""
        if not self.enabled:
            return None
            
        cache_key = self._get_cache_key(url, params)
        cache_path = self._get_cache_path(cache_key)
        
        if not os.path.exists(cache_path):
            return None
            
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                
            # Check if cache is expired
            if time.time() - cached_data['timestamp'] > self.ttl:
                os.remove(cache_path)  # Remove expired cache
                return None
                
            return cached_data['data']
        except (json.JSONDecodeError, KeyError, IOError):
            # If cache is corrupted, remove it
            if os.path.exists(cache_path):
                os.remove(cache_path)
            return None
    
    def set(self, url: str, params: dict, data: Any) -> bool:
        """Cache response data."""
        if not self.enabled:
            return False
            
        try:
            cache_key = self._get_cache_key(url, params)
            cache_path = self._get_cache_path(cache_key)
            
            cache_data = {
                'timestamp': time.time(),
                'url': url,
                'params': params,
                'data': data
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
                
            return True
        except (IOError, TypeError):
            return False
    
    def clear(self) -> bool:
        """Clear all cached data."""
        if not self.enabled:
            return False
            
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
            return True
        except OSError:
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        if not self.enabled:
            return {'enabled': False}
            
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            total_size = sum(os.path.getsize(os.path.join(self.cache_dir, f)) for f in cache_files)
            
            return {
                'enabled': True,
                'cache_dir': self.cache_dir,
                'cached_items': len(cache_files),
                'total_size_bytes': total_size,
                'ttl_seconds': self.ttl
            }
        except OSError:
            return {
                'enabled': True,
                'error': 'Unable to get cache statistics'
            }