"""
Tests for Semantic Scholar MCP Server
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import tempfile
import shutil

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Handle imports properly
try:
    from .config import SemanticScholarConfig
    from .server import SemanticScholarServer
    from .mcp_handler import SemanticScholarMCPHandler
    from .cache import CacheManager
except (ImportError, ValueError):
    # Fallback for direct script execution
    from config import SemanticScholarConfig
    from server import SemanticScholarServer
    from mcp_handler import SemanticScholarMCPHandler
    from cache import CacheManager

class TestSemanticScholarConfig(unittest.TestCase):
    """Test configuration class."""
    
    def test_config_initialization(self):
        """Test configuration initialization."""
        config = SemanticScholarConfig()
        self.assertEqual(config.base_url, 'https://api.semanticscholar.org/graph/v1')
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.rate_limit_delay, 1.0)
        self.assertEqual(config.max_retries, 3)
        self.assertTrue(config.cache_enabled)
        self.assertEqual(config.cache_ttl, 3600)
        self.assertEqual(config.cache_dir, '.cache')
        
    def test_get_headers_without_api_key(self):
        """Test headers without API key."""
        config = SemanticScholarConfig()
        config.api_key = None
        headers = config.get_headers()
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertNotIn('x-api-key', headers)
        
    def test_get_headers_with_api_key(self):
        """Test headers with API key."""
        config = SemanticScholarConfig()
        config.api_key = 'test-key'
        headers = config.get_headers()
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['x-api-key'], 'test-key')

class TestCacheManager(unittest.TestCase):
    """Test cache manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config = SemanticScholarConfig()
        self.config.cache_dir = self.test_dir
        self.cache = CacheManager(self.config)
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
        
    def test_cache_key_generation(self):
        """Test cache key generation."""
        key1 = self.cache._get_cache_key("http://test.com", {"param": "value"})
        key2 = self.cache._get_cache_key("http://test.com", {"param": "value"})
        self.assertEqual(key1, key2)
        
    def test_cache_set_and_get(self):
        """Test cache set and get operations."""
        url = "http://test.com"
        params = {"param": "value"}
        data = {"test": "data"}
        
        # Set cache
        self.cache.set(url, params, data)
        
        # Get cache
        result = self.cache.get(url, params)
        self.assertEqual(result, data)
        
    def test_cache_miss(self):
        """Test cache miss."""
        result = self.cache.get("http://nonexistent.com", {"param": "value"})
        self.assertIsNone(result)
        
    def test_cache_clear(self):
        """Test cache clear."""
        url = "http://test.com"
        params = {"param": "value"}
        data = {"test": "data"}
        
        self.cache.set(url, params, data)
        self.assertTrue(self.cache.clear())
        self.assertIsNone(self.cache.get(url, params))

class TestSemanticScholarServer(unittest.TestCase):
    """Test server implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = SemanticScholarConfig()
        self.config.api_key = 'test-key'
        self.server = SemanticScholarServer()
        
    def test_server_initialization(self):
        """Test server initialization."""
        self.assertIsInstance(self.server.config, SemanticScholarConfig)
        self.assertIsNotNone(self.server.session)
        self.assertIsNotNone(self.server.cache)
        
    def test_all_methods_exist(self):
        """Test that all required methods exist."""
        methods = [
            'search_papers',
            'get_paper_details',
            'get_citation_context',
            'download_pdf',
            'search_by_author',
            'search_by_title',
            'get_paper_references',
            'get_cache_stats',
            'clear_cache'
        ]
        
        for method_name in methods:
            self.assertTrue(hasattr(self.server, method_name), f"Method {method_name} should exist")
            
    def test_make_request_with_retry_success(self):
        """Test successful request with retry."""
        with patch.object(self.server.session, 'request') as mock_request:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.status_code = 200
            mock_response.json.return_value = {"test": "data"}
            mock_request.return_value = mock_response
            
            result = self.server._make_request_with_retry("GET", "http://test.com")
            self.assertEqual(result, mock_response)

class TestSemanticScholarMCPHandler(unittest.TestCase):
    """Test MCP handler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = SemanticScholarMCPHandler()
        
    def test_handle_initialize(self):
        """Test initialize request handling."""
        result = self.handler.handle_request("initialize", {})
        self.assertIn("result", result)
        self.assertIn("capabilities", result["result"])
        capabilities = result["result"]["capabilities"]
        required_capabilities = [
            "paperSearch",
            "paperDetails",
            "citationContext",
            "pdfDownload",
            "authorSearch",
            "titleSearch",
            "paperReferences",
            "cacheManagement"
        ]
        
        for capability in required_capabilities:
            self.assertTrue(capabilities[capability], f"Capability {capability} should be True")
            
    def test_handle_all_methods(self):
        """Test that all methods are handled."""
        methods = [
            "search_papers",
            "get_paper_details",
            "get_citation_context",
            "download_pdf",
            "search_by_author",
            "search_by_title",
            "get_paper_references",
            "get_cache_stats",
            "clear_cache"
        ]
        
        for method in methods:
            result = self.handler.handle_request(method, {})
            # Should not return method not found error
            self.assertNotIn("error", result, f"Method {method} should be handled")

if __name__ == '__main__':
    unittest.main()