"""
Tests for Zotero Expert MCP Server
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Handle imports properly
try:
    from .config import ZoteroExpertConfig
    from .server import ZoteroExpertServer
    from .mcp_handler import ZoteroExpertMCPHandler
except (ImportError, ValueError):
    # Fallback for direct script execution
    from config import ZoteroExpertConfig
    from server import ZoteroExpertServer
    from mcp_handler import ZoteroExpertMCPHandler

class TestZoteroExpertConfig(unittest.TestCase):
    """Test configuration class."""
    
    def test_config_initialization(self):
        """Test configuration initialization."""
        config = ZoteroExpertConfig()
        self.assertEqual(config.library_type, 'user')
        self.assertEqual(config.base_url, 'https://api.zotero.org')
        self.assertEqual(config.timeout, 30)
        
    def test_get_headers_without_api_key(self):
        """Test headers without API key."""
        config = ZoteroExpertConfig()
        config.api_key = None
        headers = config.get_headers()
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertNotIn('Zotero-API-Key', headers)
        
    def test_get_headers_with_api_key(self):
        """Test headers with API key."""
        config = ZoteroExpertConfig()
        config.api_key = 'test-key'
        headers = config.get_headers()
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Zotero-API-Key'], 'test-key')

class TestZoteroExpertServer(unittest.TestCase):
    """Test server implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.server = ZoteroExpertServer()
        
    def test_server_initialization(self):
        """Test server initialization."""
        self.assertIsInstance(self.server.config, ZoteroExpertConfig)
        self.assertIsNotNone(self.server.session)
        
    def test_all_methods_exist(self):
        """Test that all required methods exist."""
        methods = [
            'get_library_items',
            'get_item',
            'search_items',
            'get_collections',
            'get_item_children',
            'create_note',
            'update_item',
            'get_bibliography',
            'validate_citation_keys',
            'sync_ai_notes',
            'generate_smart_bibliography',
            'get_item_metadata',
            'search_advanced'
        ]
        
        for method_name in methods:
            self.assertTrue(hasattr(self.server, method_name), f"Method {method_name} should exist")
    
    def test_library_methods_exist(self):
        """Test that library-specific methods exist."""
        methods = [
            'read_local_library',
            'get_library_statistics'
        ]
        
        for method_name in methods:
            self.assertTrue(hasattr(self.server, method_name), f"Method {method_name} should exist")
            
    def test_make_request_success(self):
        """Test successful request."""
        with patch.object(self.server.session, 'request') as mock_request:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.status_code = 200
            mock_response.json.return_value = {"test": "data"}
            mock_request.return_value = mock_response
            
            result = self.server._make_request("GET", "http://test.com")
            self.assertEqual(result, mock_response)

class TestZoteroExpertMCPHandler(unittest.TestCase):
    """Test MCP handler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = ZoteroExpertMCPHandler()
        
    def test_handle_initialize(self):
        """Test initialize request handling."""
        result = self.handler.handle_request("initialize", {})
        self.assertIn("result", result)
        self.assertIn("capabilities", result["result"])
        capabilities = result["result"]["capabilities"]
        required_capabilities = [
            "libraryAccess",
            "itemSearch",
            "collectionManagement",
            "noteCreation",
            "bibliographyGeneration"
        ]
        
        for capability in required_capabilities:
            self.assertTrue(capabilities[capability], f"Capability {capability} should be True")
            
    def test_handle_all_methods(self):
        """Test that all methods are handled."""
        test_cases = [
            ("get_library_items", {}),
            ("get_item", {"item_key": "test-key"}),
            ("search_items", {"query": "test"}),
            ("get_collections", {}),
            ("get_item_children", {"item_key": "test-key"}),
            ("create_note", {"parent_item_key": "test-key", "note_content": "test note"}),
            ("update_item", {"item_key": "test-key", "item_data": {"title": "test"}}),
            ("get_bibliography", {"item_keys": ["test-key"]})
        ]
        
        for method, params in test_cases:
            result = self.handler.handle_request(method, params)
            # Should not return method not found error
            self.assertNotIn("error", result, f"Method {method} should be handled")

    def test_handle_new_methods(self):
        """Test that new methods are handled."""
        test_cases = [
            ("validate_citation_keys", {"items": []}),
            ("sync_ai_notes", {"item_key": "test-key", "ai_notes": []}),
            ("generate_smart_bibliography", {"item_keys": ["test-key"]}),
            ("get_item_metadata", {"item_key": "test-key"}),
            ("search_advanced", {"query": "test"})
        ]
        
        for method, params in test_cases:
            result = self.handler.handle_request(method, params)
            # Should not return method not found error
            self.assertNotIn("error", result, f"Method {method} should be handled")

    def test_handle_library_methods(self):
        """Test that library methods are handled."""
        test_cases = [
            ("read_local_library", {"limit": 10}),
            ("get_library_statistics", {})
        ]
        
        for method, params in test_cases:
            result = self.handler.handle_request(method, params)
            # Should not return method not found error
            self.assertNotIn("error", result, f"Method {method} should be handled")

if __name__ == '__main__':
    unittest.main()