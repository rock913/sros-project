"""
Tests for utility functions in Federal Academic Search MCP Server
"""
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_servers.federal_academic_search.utils.helpers import (
    normalize_doi,
    extract_paper_id_from_url,
    sanitize_query,
    merge_paper_data,
    format_authors,
    estimate_reading_time,
    is_valid_email,
    truncate_text
)


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_normalize_doi(self):
        """Test DOI normalization."""
        # Test normal DOI
        self.assertEqual(normalize_doi("10.1234/567890"), "10.1234/567890")
        
        # Test DOI with URL
        self.assertEqual(normalize_doi("https://doi.org/10.1234/567890"), "10.1234/567890")
        
        # Test DOI with doi: prefix
        self.assertEqual(normalize_doi("doi:10.1234/567890"), "10.1234/567890")
        
        # Test whitespace handling
        self.assertEqual(normalize_doi(" 10.1234/567890 "), "10.1234/567890")
        
        # Test None/empty
        self.assertIsNone(normalize_doi(None))
        self.assertEqual(normalize_doi(""), "")

    def test_extract_paper_id_from_url(self):
        """Test paper ID extraction from URLs."""
        # Test OpenAlex URL
        self.assertEqual(
            extract_paper_id_from_url("https://openalex.org/W1234567890"),
            "W1234567890"
        )
        
        # Test Semantic Scholar URL
        self.assertEqual(
            extract_paper_id_from_url("https://www.semanticscholar.org/paper/W1234567890"),
            "W1234567890"
        )
        
        # Test arXiv URL
        self.assertEqual(
            extract_paper_id_from_url("https://arxiv.org/abs/1234.56789"),
            "1234.56789"
        )
        
        # Test non-URL
        self.assertEqual(extract_paper_id_from_url("W1234567890"), "W1234567890")

    def test_sanitize_query(self):
        """Test query sanitization."""
        # Test normal query
        self.assertEqual(sanitize_query("machine learning"), "machine learning")
        
        # Test excessive whitespace
        self.assertEqual(sanitize_query("  machine   learning  "), "machine learning")
        
        # Test special characters
        self.assertEqual(sanitize_query("machine-learning"), "machine-learning")
        
        # Test very long query
        long_query = "a" * 600
        sanitized = sanitize_query(long_query)
        self.assertLessEqual(len(sanitized), 500)
        
        # Test None/empty
        self.assertEqual(sanitize_query(None), None)
        self.assertEqual(sanitize_query(""), "")

    def test_merge_paper_data(self):
        """Test paper data merging."""
        base = {
            "title": "Base Title",
            "abstract": "",
            "citationCount": None
        }
        
        additional = {
            "title": "Additional Title",
            "abstract": "Detailed abstract",
            "citationCount": 100
        }
        
        merged = merge_paper_data(base, additional)
        
        # Should prefer non-empty values
        self.assertEqual(merged["abstract"], "Detailed abstract")
        self.assertEqual(merged["citationCount"], 100)
        # Should prefer base value when both are non-empty
        self.assertEqual(merged["title"], "Base Title")

    def test_format_authors(self):
        """Test author formatting."""
        # Test single author
        self.assertEqual(format_authors(["John Doe"]), "John Doe")
        
        # Test two authors
        self.assertEqual(format_authors(["John Doe", "Jane Smith"]), "John Doe and Jane Smith")
        
        # Test three or more authors
        self.assertEqual(format_authors(["John Doe", "Jane Smith", "Bob Johnson"]), "John Doe et al.")
        
        # Test empty
        self.assertEqual(format_authors([]), "")

    def test_estimate_reading_time(self):
        """Test reading time estimation."""
        # Test less than 1 minute
        self.assertEqual(estimate_reading_time(50), "Less than 1 minute")
        
        # Test exactly 1 minute
        self.assertEqual(estimate_reading_time(200), "1 minute")
        
        # Test multiple minutes
        self.assertEqual(estimate_reading_time(600), "3 minutes")
        
        # Test None/zero
        self.assertEqual(estimate_reading_time(None), "Unknown")
        self.assertEqual(estimate_reading_time(0), "Unknown")

    def test_is_valid_email(self):
        """Test email validation."""
        # Test valid emails
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertTrue(is_valid_email("user.name@domain.co.uk"))
        
        # Test invalid emails
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertFalse(is_valid_email("@example.com"))
        self.assertFalse(is_valid_email("test@"))
        self.assertFalse(is_valid_email(""))
        self.assertFalse(is_valid_email(None))

    def test_truncate_text(self):
        """Test text truncation."""
        # Test short text
        self.assertEqual(truncate_text("Short text"), "Short text")
        
        # Test long text
        long_text = "This is a very long text that should be truncated to fit within the maximum length limit."
        truncated = truncate_text(long_text, 20)
        self.assertTrue(truncated.endswith("..."))
        self.assertLessEqual(len(truncated), 23)  # 20 + "..."
        
        # Test None/empty
        self.assertEqual(truncate_text(None), None)
        self.assertEqual(truncate_text(""), "")


if __name__ == '__main__':
    unittest.main()