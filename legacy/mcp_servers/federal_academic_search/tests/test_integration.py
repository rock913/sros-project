"""
Integration tests for Federal Academic Search MCP Server
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_servers.federal_academic_search.core.manager import AcademicSearchManager
from mcp_servers.federal_academic_search.providers.openalex import OpenAlexProvider
from mcp_servers.federal_academic_search.providers.unpaywall import UnpaywallProvider
from mcp_servers.federal_academic_search.providers.semantic_scholar import SemanticScholarProvider
from mcp_servers.federal_academic_search.transformers.result_transformer import ResultTransformer
from mcp_servers.federal_academic_search.cache.manager import CacheManager
from mcp_servers.federal_academic_search.config import FederalAcademicSearchConfig


class TestFederalAcademicSearchIntegration(unittest.TestCase):
    """Test integration of Federal Academic Search components."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables for testing
        os.environ['OPENALEX_EMAIL'] = 'test@example.com'
        os.environ['UNPAYWALL_EMAIL'] = 'test@example.com'
        
        self.config = FederalAcademicSearchConfig()
        self.manager = AcademicSearchManager(self.config)

    def test_component_initialization(self):
        """Test that all components initialize correctly."""
        # Test manager
        self.assertIsInstance(self.manager, AcademicSearchManager)
        
        # Test providers
        self.assertIsInstance(self.manager.openalex_provider, OpenAlexProvider)
        self.assertIsInstance(self.manager.unpaywall_provider, UnpaywallProvider)
        self.assertIsInstance(self.manager.s2_provider, SemanticScholarProvider)
        
        # Test transformer
        self.assertIsInstance(self.manager.transformer, ResultTransformer)
        
        # Test cache manager
        self.assertIsInstance(self.manager.cache_manager, CacheManager)

    def test_config_loading(self):
        """Test that configuration loads correctly."""
        self.assertEqual(self.config.openalex_base_url, 'https://api.openalex.org')
        self.assertEqual(self.config.unpaywall_base_url, 'https://api.unpaywall.org/v2')
        self.assertIsNotNone(self.config.openalex_email)
        self.assertIsNotNone(self.config.unpaywall_email)

    def test_headers_generation(self):
        """Test that headers are generated correctly."""
        openalex_headers = self.config.get_openalex_headers()
        unpaywall_headers = self.config.get_unpaywall_headers()
        s2_headers = self.config.get_s2_headers()
        
        self.assertIn('User-Agent', openalex_headers)
        self.assertIn('User-Agent', unpaywall_headers)
        self.assertIn('User-Agent', s2_headers)
        self.assertIn('mailto', openalex_headers)

    @patch('mcp_servers.federal_academic_search.providers.base.aiohttp.ClientSession')
    def test_provider_context_management(self, mock_session_class):
        """Test provider context management."""
        mock_session = MagicMock()
        # Create async mock for close method
        async def async_close():
            pass
        mock_session.close = async_close
        mock_session_class.return_value = mock_session
        
        # Test OpenAlex provider
        provider = OpenAlexProvider(self.config)
        self.assertIsNone(provider.session)
        
        # Test async context manager
        import asyncio
        async def test_context():
            async with provider as p:
                self.assertIsNotNone(p.session)
                return p.session
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        session = loop.run_until_complete(test_context())
        loop.close()
        
        self.assertEqual(session, mock_session)

    def test_result_transformer_methods(self):
        """Test result transformer methods exist."""
        transformer = ResultTransformer()
        
        # Test that all expected methods exist
        expected_methods = [
            'transform_search_results',
            'transform_paper_details',
            'transform_references',
            'transform_citation_contexts',
            'ensure_s2_compatibility'
        ]
        
        for method_name in expected_methods:
            self.assertTrue(hasattr(transformer, method_name), 
                          f"Transformer should have method {method_name}")

    def test_cache_manager_basic_operations(self):
        """Test basic cache manager operations."""
        cache = CacheManager(db_path='.test_cache/test.db', ttl=1)
        
        # Test set and get
        test_key = 'test_key'
        test_value = {'test': 'value'}
        
        result = cache.set(test_key, test_value)
        self.assertTrue(result)
        
        cached_value = cache.get(test_key)
        self.assertEqual(cached_value, test_value)
        
        # Test delete
        result = cache.delete(test_key)
        self.assertTrue(result)
        
        cached_value = cache.get(test_key)
        self.assertIsNone(cached_value)
        
        # Clean up
        cache.clear_all()


if __name__ == '__main__':
    unittest.main()