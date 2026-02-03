#!/usr/bin/env python3
"""
Comprehensive test for the enhanced Zotero Expert MCP Server functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import ZoteroExpertServer
from mcp_handler import ZoteroExpertMCPHandler
from config import ZoteroExpertConfig

class TestEnhancedZoteroExpert(unittest.TestCase):
    """Test the enhanced Zotero Expert functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a server with mocked configuration
        self.server = ZoteroExpertServer()
        self.server.config.library_id = 'test-lib'
        self.server.config.api_key = 'test-key'
        self.server.config.library_type = 'user'
        
        # Mock the pyzotero client
        self.mock_zotero_client = MagicMock()
        self.server.zotero_client = self.mock_zotero_client
        
        self.handler = ZoteroExpertMCPHandler()

    def test_enhanced_server_methods_exist(self):
        """Test that all enhanced server methods exist."""
        enhanced_methods = [
            'validate_citation_keys',
            'sync_ai_notes', 
            'generate_smart_bibliography',
            'get_item_metadata',
            'search_advanced',
            'read_local_library',
            'get_library_statistics'
        ]
        
        for method_name in enhanced_methods:
            self.assertTrue(hasattr(self.server, method_name), f"Method {method_name} should exist")

    def test_enhanced_mcp_methods_handled(self):
        """Test that enhanced MCP methods are handled."""
        enhanced_methods = [
            ("validate_citation_keys", {"items": []}),
            ("sync_ai_notes", {"item_key": "test-key", "ai_notes": []}),
            ("generate_smart_bibliography", {"item_keys": ["test-key"]}),
            ("get_item_metadata", {"item_key": "test-key"}),
            ("search_advanced", {"query": "test"}),
            ("read_local_library", {"limit": 10}),
            ("get_library_statistics", {})
        ]
        
        for method, params in enhanced_methods:
            result = self.handler.handle_request(method, params)
            # Should not return method not found error
            self.assertNotIn("error", result, f"Method {method} should be handled")

    def test_citation_key_validation_logic(self):
        """Test citation key validation logic."""
        # Mock the config validation
        self.server.config.validate = lambda: True
        
        # Test with conflicting citation keys
        items_with_conflicts = [
            {"key": "item1", "data": {"citationKey": "smith2020"}},
            {"key": "item2", "data": {"citationKey": "jones2021"}},
            {"key": "item3", "data": {"citationKey": "smith2020"}},  # Duplicate
        ]
        
        result = self.server.validate_citation_keys(items_with_conflicts)
        self.assertIn("valid", result)
        self.assertIn("conflicts", result)
        self.assertFalse(result["valid"])  # Should be invalid due to conflicts
        
        # Test with unique citation keys
        items_unique = [
            {"key": "item1", "data": {"citationKey": "smith2020"}},
            {"key": "item2", "data": {"citationKey": "jones2021"}},
            {"key": "item3", "data": {"citationKey": "brown2022"}},
        ]
        
        result = self.server.validate_citation_keys(items_unique)
        self.assertTrue(result["valid"])  # Should be valid
        self.assertEqual(len(result["conflicts"]), 0)  # No conflicts

    def test_smart_bibliography_generation(self):
        """Test smart bibliography generation parameters."""
        # Mock the config validation
        self.server.config.validate = lambda: True
        
        # Test with format options
        item_keys = ["key1", "key2", "key3"]
        style = "chicago"
        format_options = {"locale": "en-US", "includeAnnots": True}
        
        with patch.object(self.server, '_make_request') as mock_request:
            mock_response = MagicMock()
            mock_response.text = "<div>Test bibliography</div>"
            mock_request.return_value = mock_response
            
            result = self.server.generate_smart_bibliography(item_keys, style, format_options)
        
        # Should contain the parameters in the result
        self.assertEqual(result.get("style"), style)
        self.assertEqual(result.get("item_count"), len(item_keys))
        self.assertEqual(result.get("format_options"), format_options)

    def test_advanced_search_parameters(self):
        """Test advanced search parameter handling."""
        # Mock the config validation
        self.server.config.validate = lambda: True
        
        query = "machine learning"
        item_type = "journalArticle"
        collection_key = "ABC123"
        limit = 25
        
        # Since we can't actually make API calls in tests, we'll test the parameter handling
        # by mocking the _make_request method
        with patch.object(self.server, '_make_request') as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"results": []}
            mock_request.return_value = mock_response
            
            result = self.server.search_advanced(query, item_type, collection_key, limit)
            
            # Verify the parameters were passed correctly
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            self.assertEqual(args[0], "GET")  # Method
            self.assertIn("q", kwargs.get("params", {}))
            self.assertEqual(kwargs["params"]["q"], query)
            self.assertEqual(kwargs["params"]["limit"], limit)

    def test_local_library_reading(self):
        """Test local library reading functionality."""
        # Mock the config validation
        self.server.config.validate = lambda: True
        
        # Mock the pyzotero client methods
        mock_items = [
            {"key": "item1", "data": {"title": "Test Paper 1"}},
            {"key": "item2", "data": {"title": "Test Paper 2"}}
        ]
        self.mock_zotero_client.items.return_value = mock_items
        
        # Test reading local library
        result = self.server.read_local_library(limit=10, start=0)
        
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["limit"], 10)
        self.assertEqual(result["start"], 0)
        self.assertEqual(len(result["items"]), 2)

    def test_library_statistics(self):
        """Test library statistics functionality."""
        # Mock the config validation
        self.server.config.validate = lambda: True
        
        # Mock the pyzotero client methods
        mock_items = [
            {"data": {"itemType": "journalArticle"}},
            {"data": {"itemType": "book"}},
            {"data": {"itemType": "journalArticle"}}
        ]
        mock_collections = [{"key": "col1"}, {"key": "col2"}]
        
        self.mock_zotero_client.items.return_value = mock_items
        self.mock_zotero_client.collections.return_value = mock_collections
        self.mock_zotero_client.last_modified_version = 12345
        
        # Test getting library statistics
        result = self.server.get_library_statistics()
        
        self.assertEqual(result["total_items"], 3)
        self.assertEqual(result["total_collections"], 2)
        self.assertIn("journalArticle", result["item_types"])
        self.assertEqual(result["item_types"]["journalArticle"], 2)
        self.assertEqual(result["item_types"]["book"], 1)

if __name__ == '__main__':
    unittest.main()