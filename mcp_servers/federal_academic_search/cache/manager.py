"""
Cache Manager for Federal Academic Search MCP Server
"""
import sqlite3
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import os
import threading

logger = logging.getLogger(__name__)


class CacheManager:
    """SQLite-based cache manager for academic search results."""

    def __init__(self, db_path: str = ".cache/academic_search.db", ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            db_path: Path to SQLite database file
            ttl: Time to live in seconds (default: 1 hour)
        """
        self.db_path = db_path
        self.ttl = ttl
        self.lock = threading.Lock()
        
        # Ensure cache directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        
        # Initialize database
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database with required tables."""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_search_cache_accessed 
                ON search_cache(accessed_at)
            """)
            
            conn.commit()
            conn.close()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached value by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT value, created_at FROM search_cache 
                    WHERE key = ? AND created_at > datetime('now', '-{} seconds')
                """.format(self.ttl), (key,))
                
                row = cursor.fetchone()
                if row:
                    # Update access time
                    cursor.execute("""
                        UPDATE search_cache SET accessed_at = CURRENT_TIMESTAMP 
                        WHERE key = ?
                    """, (key,))
                    
                    conn.commit()
                    conn.close()
                    
                    value_str, created_at = row
                    return json.loads(value_str)
                else:
                    conn.close()
                    return None
                    
            except Exception as e:
                logger.error(f"Error getting cache entry: {str(e)}")
                return None

    def set(self, key: str, value: Dict[str, Any]) -> bool:
        """
        Set cache value by key.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Convert value to JSON
                value_str = json.dumps(value, ensure_ascii=False)
                
                # Insert or replace
                cursor.execute("""
                    INSERT OR REPLACE INTO search_cache (key, value, created_at, accessed_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, (key, value_str))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                logger.error(f"Error setting cache entry: {str(e)}")
                return False

    def delete(self, key: str) -> bool:
        """
        Delete cache entry by key.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM search_cache WHERE key = ?", (key,))
                
                conn.commit()
                conn.close()
                return cursor.rowcount > 0
                
            except Exception as e:
                logger.error(f"Error deleting cache entry: {str(e)}")
                return False

    def clear_expired(self) -> int:
        """
        Clear expired cache entries.
        
        Returns:
            Number of entries deleted
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM search_cache 
                    WHERE created_at <= datetime('now', '-{} seconds')
                """.format(self.ttl))
                
                count = cursor.rowcount
                conn.commit()
                conn.close()
                
                logger.info(f"Cleared {count} expired cache entries")
                return count
                
            except Exception as e:
                logger.error(f"Error clearing expired cache entries: {str(e)}")
                return 0

    def clear_all(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries deleted
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM search_cache")
                
                count = cursor.rowcount
                conn.commit()
                conn.close()
                
                logger.info(f"Cleared all {count} cache entries")
                return count
                
            except Exception as e:
                logger.error(f"Error clearing all cache entries: {str(e)}")
                return 0

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Total entries
                cursor.execute("SELECT COUNT(*) FROM search_cache")
                total_entries = cursor.fetchone()[0]
                
                # Expired entries
                cursor.execute("""
                    SELECT COUNT(*) FROM search_cache 
                    WHERE created_at <= datetime('now', '-{} seconds')
                """.format(self.ttl))
                expired_entries = cursor.fetchone()[0]
                
                # Recently accessed (last hour)
                cursor.execute("""
                    SELECT COUNT(*) FROM search_cache 
                    WHERE accessed_at >= datetime('now', '-3600 seconds')
                """)
                recent_access = cursor.fetchone()[0]
                
                conn.close()
                
                return {
                    "total_entries": total_entries,
                    "expired_entries": expired_entries,
                    "active_entries": total_entries - expired_entries,
                    "recently_accessed": recent_access,
                    "ttl_seconds": self.ttl,
                    "db_path": self.db_path
                }
                
            except Exception as e:
                logger.error(f"Error getting cache stats: {str(e)}")
                return {
                    "error": str(e),
                    "total_entries": 0,
                    "expired_entries": 0,
                    "active_entries": 0,
                    "recently_accessed": 0,
                    "ttl_seconds": self.ttl,
                    "db_path": self.db_path
                }

    def _generate_key(self, prefix: str, **kwargs) -> str:
        """
        Generate cache key from parameters.
        
        Args:
            prefix: Key prefix
            **kwargs: Parameters to include in key
            
        Returns:
            Generated cache key
        """
        # Sort kwargs for consistent key generation
        sorted_items = sorted(kwargs.items())
        key_parts = [prefix] + [f"{k}={v}" for k, v in sorted_items]
        return ":".join(key_parts)