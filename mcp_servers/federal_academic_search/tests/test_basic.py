"""
Basic tests for Federal Academic Search MCP Server
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_servers.federal_academic_search.server import FederalAcademicSearchServer
from mcp_servers.federal_academic_search.config import FederalAcademicSearchConfig


class TestFederalAcademicSearchServer(unittest.TestCase):
    """Test basic functionality of the Federal Academic Search Server."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables for testing
        os.environ['OPENALEX_EMAIL'] = 'test@example.com'
        os.environ['UNPAYWALL_EMAIL'] = 'test@example.com'
        
        self.server = FederalAcademicSearchServer()

    def test_server_initialization(self):
        """Test that server initializes correctly."""
        self.assertIsInstance(self.server, FederalAcademicSearchServer)
        self.assertFalse(self.server.is_initialized())

    @patch('mcp_servers.federal_academic_search.mcp_handler.asyncio.new_event_loop')
    def test_initialize_server(self, mock_loop):
        """Test server initialization."""
        # Mock the event loop
        mock_loop_instance = MagicMock()
        mock_loop.return_value = mock_loop_instance
        mock_loop_instance.run_until_complete.return_value = {
            "capabilities": {
                "search_papers": {}
            }
        }
        
        result = self.server.initialize()
        self.assertNotIn("error", result)
        self.assertTrue(self.server.is_initialized())

    def test_config_validation(self):
        """Test configuration validation."""
        config = FederalAcademicSearchConfig()
        
        # Should validate successfully with environment variables set
        try:
            config.validate()
            validation_passed = True
        except Exception:
            validation_passed = False
            
        self.assertTrue(validation_passed)

    def test_method_signatures(self):
        """Test that all expected methods exist."""
        expected_methods = [
            'search_papers',
            'get_paper_details', 
            'get_citation_context',
            'download_pdf',
            'search_by_author',
            'search_by_title',
            'get_paper_references',
            'get_tldr',
            'get_cache_stats',
            'clear_cache'
        ]
        
        for method_name in expected_methods:
            self.assertTrue(hasattr(self.server, method_name), 
                          f"Server should have method {method_name}")

    def test_config_has_required_attributes(self):
        """Test that config has all required attributes."""
        config = FederalAcademicSearchConfig()
        
        required_attrs = [
            'openalex_base_url',
            'openalex_email',
            'unpaywall_base_url', 
            'unpaywall_email',
            's2_api_key',
            'cache_enabled',
            'cache_db_path'
        ]
        
        for attr in required_attrs:
            self.assertTrue(hasattr(config, attr), 
                          f"Config should have attribute {attr}")


if __name__ == '__main__':
    unittest.main()