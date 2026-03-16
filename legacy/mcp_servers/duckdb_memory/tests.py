#!/usr/bin/env python3
"""
Tests for DuckDB Memory MCP Server
"""

import unittest
import tempfile
import os
from pathlib import Path
from server import DuckDBMemoryServer

class TestDuckDBMemoryServer(unittest.TestCase):
    """Test cases for DuckDBMemoryServer."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database for testing
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_graph.db")
        self.server = DuckDBMemoryServer(self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.server.close()
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
    
    def test_create_and_get_paper(self):
        """Test creating and retrieving a paper."""
        # Create a paper
        paper_id = self.server.create_paper(
            title="Test Paper",
            authors="John Doe",
            year=2023,
            venue="Test Conference",
            doi="10.1234/test.2023",
            abstract="This is a test paper.",
            citation_key="doe2023test"
        )
        
        # Verify the paper was created
        self.assertIsInstance(paper_id, int)
        self.assertGreater(paper_id, 0)
        
        # Retrieve the paper by ID
        paper = self.server.get_paper_by_id(paper_id)
        self.assertIsNotNone(paper)
        self.assertEqual(paper["title"], "Test Paper")
        self.assertEqual(paper["authors"], "John Doe")
        self.assertEqual(paper["year"], 2023)
        self.assertEqual(paper["venue"], "Test Conference")
        self.assertEqual(paper["doi"], "10.1234/test.2023")
        self.assertEqual(paper["abstract"], "This is a test paper.")
        self.assertEqual(paper["citation_key"], "doe2023test")
    
    def test_get_paper_by_doi(self):
        """Test retrieving a paper by DOI."""
        # Create a paper
        paper_id = self.server.create_paper(
            title="DOI Test Paper",
            doi="10.5678/doi.test.2023"
        )
        
        # Retrieve the paper by DOI
        paper = self.server.get_paper_by_doi("10.5678/doi.test.2023")
        self.assertIsNotNone(paper)
        self.assertEqual(paper["title"], "DOI Test Paper")
        self.assertEqual(paper["doi"], "10.5678/doi.test.2023")
    
    def test_get_paper_by_citation_key(self):
        """Test retrieving a paper by citation key."""
        # Create a paper
        paper_id = self.server.create_paper(
            title="Citation Key Test Paper",
            citation_key="test2023key"
        )
        
        # Retrieve the paper by citation key
        paper = self.server.get_paper_by_citation_key("test2023key")
        self.assertIsNotNone(paper)
        self.assertEqual(paper["title"], "Citation Key Test Paper")
        self.assertEqual(paper["citation_key"], "test2023key")
    
    def test_update_paper(self):
        """Test updating a paper."""
        # Create a paper
        paper_id = self.server.create_paper(
            title="Original Title",
            abstract="Original abstract"
        )
        
        # Update the paper
        success = self.server.update_paper(
            paper_id,
            title="Updated Title",
            abstract="Updated abstract"
        )
        
        self.assertTrue(success)
        
        # Verify the update
        paper = self.server.get_paper_by_id(paper_id)
        self.assertEqual(paper["title"], "Updated Title")
        self.assertEqual(paper["abstract"], "Updated abstract")
    
    def test_delete_paper(self):
        """Test deleting a paper."""
        # Create a paper
        paper_id = self.server.create_paper(title="To Be Deleted")
        
        # Delete the paper
        success = self.server.delete_paper(paper_id)
        self.assertTrue(success)
        
        # Verify the paper is deleted
        paper = self.server.get_paper_by_id(paper_id)
        self.assertIsNone(paper)
    
    def test_create_and_get_citation(self):
        """Test creating and retrieving citations."""
        # Create two papers
        paper1_id = self.server.create_paper(title="Paper 1")
        paper2_id = self.server.create_paper(title="Paper 2")
        
        # Create a citation
        citation_id = self.server.create_citation(
            citing_paper_id=paper1_id,
            cited_paper_id=paper2_id,
            citation_context="This paper builds on previous work."
        )
        
        # Verify the citation was created
        self.assertIsInstance(citation_id, int)
        self.assertGreater(citation_id, 0)
        
        # Retrieve citations for the citing paper
        citations = self.server.get_citations_for_paper(paper1_id, citing=True)
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0]["citing_paper_id"], paper1_id)
        self.assertEqual(citations[0]["cited_paper_id"], paper2_id)
        self.assertEqual(citations[0]["citation_context"], "This paper builds on previous work.")
        
        # Retrieve citations for the cited paper
        citations = self.server.get_citations_for_paper(paper2_id, citing=False)
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0]["citing_paper_id"], paper1_id)
        self.assertEqual(citations[0]["cited_paper_id"], paper2_id)
    
    def test_create_and_get_relationship(self):
        """Test creating and retrieving relationships."""
        # Create two papers
        paper1_id = self.server.create_paper(title="Paper A")
        paper2_id = self.server.create_paper(title="Paper B")
        
        # Create a relationship
        relationship_id = self.server.create_relationship(
            subject_paper_id=paper1_id,
            object_paper_id=paper2_id,
            relationship_type="critiques",
            confidence_score=0.85,
            evidence="Based on methodology comparison."
        )
        
        # Verify the relationship was created
        self.assertIsInstance(relationship_id, int)
        self.assertGreater(relationship_id, 0)
        
        # Retrieve relationships for the subject paper
        relationships = self.server.get_relationships_for_paper(paper1_id, subject=True)
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0]["subject_paper_id"], paper1_id)
        self.assertEqual(relationships[0]["object_paper_id"], paper2_id)
        self.assertEqual(relationships[0]["relationship_type"], "critiques")
        self.assertEqual(relationships[0]["confidence_score"], 0.85)
        self.assertEqual(relationships[0]["evidence"], "Based on methodology comparison.")
        
        # Retrieve relationships for the object paper
        relationships = self.server.get_relationships_for_paper(paper2_id, subject=False)
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0]["subject_paper_id"], paper1_id)
        self.assertEqual(relationships[0]["object_paper_id"], paper2_id)
        self.assertEqual(relationships[0]["relationship_type"], "critiques")
    
    def test_get_relationships_by_type(self):
        """Test retrieving relationships by type."""
        # Create papers and relationships
        paper1_id = self.server.create_paper(title="Paper 1")
        paper2_id = self.server.create_paper(title="Paper 2")
        paper3_id = self.server.create_paper(title="Paper 3")
        
        # Create different types of relationships
        self.server.create_relationship(paper1_id, paper2_id, "critiques")
        self.server.create_relationship(paper2_id, paper3_id, "extends")
        self.server.create_relationship(paper1_id, paper3_id, "critiques")
        
        # Retrieve relationships by type
        critiques = self.server.get_relationships_by_type("critiques")
        extends = self.server.get_relationships_by_type("extends")
        
        self.assertEqual(len(critiques), 2)
        self.assertEqual(len(extends), 1)
        
        # Verify all critiques relationships are of the correct type
        for rel in critiques:
            self.assertEqual(rel["relationship_type"], "critiques")
    
    def test_create_and_manage_research_gap(self):
        """Test creating and managing research gaps."""
        # Create a research gap
        gap_id = self.server.create_research_gap(
            manuscript_section="Introduction",
            gap_description="Lack of recent survey papers in this area",
            priority=2,
            status="open"
        )
        
        # Verify the gap was created
        self.assertIsInstance(gap_id, int)
        self.assertGreater(gap_id, 0)
        
        # Retrieve the gap by ID
        gap = self.server.get_research_gap_by_id(gap_id)
        self.assertIsNotNone(gap)
        self.assertEqual(gap["manuscript_section"], "Introduction")
        self.assertEqual(gap["gap_description"], "Lack of recent survey papers in this area")
        self.assertEqual(gap["priority"], 2)
        self.assertEqual(gap["status"], "open")
        
        # Retrieve open research gaps
        open_gaps = self.server.get_open_research_gaps()
        self.assertEqual(len(open_gaps), 1)
        self.assertEqual(open_gaps[0]["id"], gap_id)
        
        # Update gap status
        success = self.server.update_research_gap_status(gap_id, "researched")
        self.assertTrue(success)
        
        # Verify status update
        gap = self.server.get_research_gap_by_id(gap_id)
        self.assertEqual(gap["status"], "researched")
        
        # Update gap priority
        success = self.server.update_research_gap_priority(gap_id, 5)
        self.assertTrue(success)
        
        # Verify priority update
        gap = self.server.get_research_gap_by_id(gap_id)
        self.assertEqual(gap["priority"], 5)

if __name__ == "__main__":
    unittest.main()