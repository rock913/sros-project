"""Test-friendly mock implementations for SROS MCP servers."""

from typing import List, Dict, Any, Optional
from mcp_servers.common.interfaces import MemoryStore, ResearchTool, ManuscriptManager


class InMemoryStore(MemoryStore):
    """A pure Python dictionary implementation for testing."""
    
    def __init__(self):
        self.papers = {}
        self.relationships = []
        self.knowledge_triples = []
        self.next_paper_id = 1
    
    def add_knowledge(self, subject: str, predicate: str, object: str) -> None:
        """Add a knowledge triple to the store."""
        self.knowledge_triples.append((subject, predicate, object))
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return mock results."""
        # Simple mock implementation - return some mock data
        return [{"mock": "data", "sql": sql}]
    
    def get_paper(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a paper by identifier."""
        # Return a mock paper if it exists
        for paper in self.papers.values():
            if paper.get('doi') == identifier or paper.get('citation_key') == identifier:
                return paper
        return None
    
    def create_paper(self, paper_data: Dict[str, Any]) -> str:
        """Create a new paper record and return its identifier."""
        paper_id = str(self.next_paper_id)
        self.next_paper_id += 1
        paper_data['id'] = paper_id
        self.papers[paper_id] = paper_data
        return paper_id


class MockResearchTool(ResearchTool):
    """Mock research tool for testing."""
    
    def __init__(self, mock_results: List[Dict[str, Any]] = None):
        self.mock_results = mock_results or []
        self.search_calls = []
    
    def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Mock search implementation."""
        self.search_calls.append({'query': query, 'limit': limit})
        return self.mock_results[:limit]
    
    def get_item(self, item_key: str) -> Optional[Dict[str, Any]]:
        """Mock get_item implementation."""
        # Return the first item that matches the key
        for item in self.mock_results:
            if item.get('key') == item_key or item.get('id') == item_key:
                return item
        return None


class MockManuscriptManager(ManuscriptManager):
    """Mock manuscript manager for testing."""
    
    def __init__(self):
        self.structure = {
            "headers": [],
            "sections": {}
        }
        self.section_edits = []
    
    def get_structure(self) -> Dict[str, Any]:
        """Mock get_structure implementation."""
        return self.structure
    
    def detect_gaps(self) -> List[Dict[str, Any]]:
        """Mock detect_gaps implementation."""
        return []
    
    def edit_section(self, section_path: str, content: str, mode: str = "append") -> bool:
        """Mock edit_section implementation."""
        self.section_edits.append({
            'section_path': section_path,
            'content': content,
            'mode': mode
        })
        return True
    
    def get_section_content(self, section_path: str) -> Optional[str]:
        """Mock get_section_content implementation."""
        if section_path in self.structure.get('sections', {}):
            return self.structure['sections'][section_path].get('content')
        return None