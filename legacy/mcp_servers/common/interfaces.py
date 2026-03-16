"""Abstract interfaces for SROS MCP servers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class MemoryStore(ABC):
    """Abstract interface for memory storage (DuckDB, SQLite, InMemory)."""
    
    @abstractmethod
    def add_knowledge(self, subject: str, predicate: str, object: str) -> None:
        """Add a knowledge triple to the store."""
        pass

    @abstractmethod
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results."""
        pass

    @abstractmethod
    def get_paper(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a paper by DOI, citation key, or other identifier."""
        pass

    @abstractmethod
    def create_paper(self, paper_data: Dict[str, Any]) -> str:
        """Create a new paper record and return its identifier."""
        pass


class ResearchTool(ABC):
    """Abstract interface for research tools."""
    
    @abstractmethod
    def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search for research items."""
        pass

    @abstractmethod
    def get_item(self, item_key: str) -> Optional[Dict[str, Any]]:
        """Get a specific item by key."""
        pass


class ManuscriptManager(ABC):
    """Abstract interface for manuscript management."""
    
    @abstractmethod
    def get_structure(self) -> Dict[str, Any]:
        """Get the structure of the manuscript."""
        pass

    @abstractmethod
    def detect_gaps(self) -> List[Dict[str, Any]]:
        """Detect gaps in the manuscript."""
        pass

    @abstractmethod
    def edit_section(self, section_path: str, content: str, mode: str = "append") -> bool:
        """Edit a section of the manuscript."""
        pass

    @abstractmethod
    def get_section_content(self, section_path: str) -> Optional[str]:
        """Get the content of a specific section."""
        pass