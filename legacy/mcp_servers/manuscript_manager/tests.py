#!/usr/bin/env python3
"""
Tests for Manuscript Manager MCP Server
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from server import ManuscriptManagerServer

class TestManuscriptManagerServer(unittest.TestCase):
    """Test cases for ManuscriptManagerServer."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.manuscript_path = os.path.join(self.temp_dir, "test_draft.md")
        self.server = ManuscriptManagerServer(self.manuscript_path)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
    
    def test_initialize_manuscript(self):
        """Test that manuscript is created if it doesn't exist."""
        # Server should have created a default manuscript
        self.assertTrue(os.path.exists(self.manuscript_path))
        
        # Check that it has the expected structure
        with open(self.manuscript_path, 'r') as f:
            content = f.read()
        
        self.assertIn("# Research Draft", content)
        self.assertIn("## Introduction", content)
        self.assertIn("## Related Work", content)
    
    def test_get_structure(self):
        """Test getting manuscript structure."""
        structure = self.server.get_structure()
        
        self.assertIn("file", structure)
        self.assertIn("headers", structure)
        self.assertIn("sections", structure)
        
        # Check that we have the expected headers
        headers = structure["headers"]
        header_titles = [h["title"] for h in headers]
        
        self.assertIn("Introduction", header_titles)
        self.assertIn("Related Work", header_titles)
        self.assertIn("Methodology", header_titles)
        self.assertIn("Results", header_titles)
        self.assertIn("Conclusion", header_titles)
        self.assertIn("References", header_titles)
    
    def test_detect_explicit_gaps(self):
        """Test detecting explicit gaps (TODO markers)."""
        # The default manuscript should have TODO markers
        gaps = self.server.detect_gaps()
        
        # Filter for explicit gaps
        explicit_gaps = [g for g in gaps if g.get("type") == "explicit"]
        
        self.assertGreater(len(explicit_gaps), 0)
        
        # Check that gaps have expected properties
        for gap in explicit_gaps:
            self.assertIn("description", gap)
            self.assertIn("line_number", gap)
            self.assertIn("section", gap)
            self.assertIn("priority", gap)
    
    def test_edit_section_replace(self):
        """Test replacing section content."""
        # Replace the Introduction section
        new_content = "This is a completely new introduction."
        success = self.server.edit_section("Introduction", new_content, mode="replace")
        
        self.assertTrue(success)
        
        # Verify the content was replaced
        section_content = self.server.get_section_content("Introduction")
        self.assertEqual(section_content.strip(), new_content)
    
    def test_edit_section_append(self):
        """Test appending to section content."""
        original_content = self.server.get_section_content("Introduction")
        
        # Append to the Introduction section
        append_content = "\n\nThis is additional content."
        success = self.server.edit_section("Introduction", append_content, mode="append")
        
        self.assertTrue(success)
        
        # Verify the content was appended
        new_content = self.server.get_section_content("Introduction")
        self.assertIn(original_content, new_content)
        self.assertIn("This is additional content.", new_content)
    
    def test_edit_section_prepend(self):
        """Test prepending to section content."""
        original_content = self.server.get_section_content("Introduction")
        
        # Prepend to the Introduction section
        prepend_content = "This is prepended content.\n\n"
        success = self.server.edit_section("Introduction", prepend_content, mode="prepend")
        
        self.assertTrue(success)
        
        # Verify the content was prepended
        new_content = self.server.get_section_content("Introduction")
        self.assertIn(original_content, new_content)
        self.assertIn("This is prepended content.", new_content)
    
    def test_insert_content_with_citations(self):
        """Test inserting content with citations."""
        # Insert content with citations into the Introduction
        content = "This is cited content."
        citation_keys = ["doe2023", "smith2022"]
        
        success = self.server.insert_content("Introduction", content, citation_keys)
        self.assertTrue(success)
        
        # Verify the content and citations were inserted
        section_content = self.server.get_section_content("Introduction")
        self.assertIn("This is cited content.", section_content)
        self.assertIn("[@doe2023]", section_content)
        self.assertIn("[@smith2022]", section_content)
    
    def test_get_nonexistent_section(self):
        """Test getting content of a nonexistent section."""
        content = self.server.get_section_content("Nonexistent Section")
        self.assertIsNone(content)
    
    def test_edit_nonexistent_section(self):
        """Test editing a nonexistent section."""
        success = self.server.edit_section("Nonexistent Section", "Some content")
        self.assertFalse(success)
    
    def test_detect_implicit_gaps(self):
        """Test detecting implicit gaps."""
        # Create a manuscript with a very short section
        short_manuscript = """# Test Paper

## Introduction

This is a normal introduction.

## Very Short Section

Hi.

## Another Section

This is another section.
"""
        
        # Write the short manuscript
        with open(self.manuscript_path, 'w') as f:
            f.write(short_manuscript)
        
        # Reload the server with the new content
        self.server = ManuscriptManagerServer(self.manuscript_path)
        
        # Detect gaps
        gaps = self.server.detect_gaps()
        
        # Filter for implicit gaps
        implicit_gaps = [g for g in gaps if g.get("type") == "implicit"]
        
        # Should detect the very short section
        short_section_gaps = [g for g in implicit_gaps if "short" in g.get("description", "").lower()]
        self.assertGreater(len(short_section_gaps), 0)

if __name__ == "__main__":
    unittest.main()