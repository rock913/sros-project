#!/usr/bin/env python3
"""
DuckDB Memory MCP Server
Provides local knowledge graph storage using DuckDB for the SROS system.
"""

import os
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

# Lazy loading for duckdb dependency
HAS_DUCKDB = None  # Check on demand

# Import the common interface
from mcp_servers.common.interfaces import MemoryStore

class DuckDBMemoryServer(MemoryStore):
    """DuckDB Memory MCP Server implementation."""
    
    def __init__(self, db_path: str = ".sros/graph.db"):
        """
        Initialize the DuckDB Memory server.
        
        Args:
            db_path: Path to the DuckDB database file
        """
        self.db_path = db_path
        self._conn = None
        self._ensure_db_directory()
        # Don't initialize database connection here - lazy loading
    
    @property
    def conn(self):
        """Lazy loading: Only import duckdb when actually needed, not at module level."""
        global HAS_DUCKDB
        
        if self._conn is None:
            # Import duckdb inside the method
            try:
                import duckdb
                HAS_DUCKDB = True
            except ImportError:
                HAS_DUCKDB = False
                logging.error("DuckDB not installed. Feature unavailable.")
                raise RuntimeError("DuckDB dependency missing. Please install it with: pip install duckdb")
            
            try:
                self._conn = duckdb.connect(self.db_path)
                # Initialize the database schema
                self._initialize_database_schema()
            except Exception as e:
                logging.error(f"Failed to connect to DuckDB: {e}")
                raise RuntimeError(f"Failed to initialize DuckDB connection: {e}")
        return self._conn
    
    def _initialize_database_schema(self):
        """Initialize the DuckDB database with CiTO schema."""
        # Load the CiTO schema
        schema_path = Path(__file__).parent / "cito_schema.sql"
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute the schema creation statements
        self._conn.execute(schema_sql)
        self._conn.commit()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_database(self):
        """Initialize the DuckDB database with CiTO schema."""
        # This method is now deprecated - schema initialization happens in conn property
        pass
    
    def close(self):
        """Close the database connection."""
        if self._conn:
            self._conn.close()
    
    # Implement abstract methods from MemoryStore interface
    def add_knowledge(self, subject: str, predicate: str, object: str) -> None:
        """Add a knowledge triple to the store."""
        # For now, we'll store this in a simple table
        query = """
        INSERT INTO relationships (subject_paper_id, object_paper_id, relationship_type, evidence)
        VALUES (?, ?, ?, ?)
        """
        # Since we don't have paper IDs, we'll use the subject/object as identifiers
        # In a real implementation, this would be more sophisticated
        self.conn.execute(query, (hash(subject) % 1000000, hash(object) % 1000000, predicate, f"{subject} {predicate} {object}"))
        self.conn.commit()
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results."""
        cursor = self.conn.execute(sql)
        rows = cursor.fetchall()
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    def get_paper(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get a paper by DOI, citation key, or other identifier."""
        # Try to find by DOI first
        query = "SELECT * FROM papers WHERE doi = ? OR citation_key = ?"
        cursor = self.conn.execute(query, (identifier, identifier))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def create_paper(self, paper_data: Dict[str, Any]) -> str:
        """Create a new paper record and return its identifier."""
        query = """
        INSERT INTO papers (title, authors, year, venue, doi, abstract, citation_key)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """
        cursor = self.conn.execute(query, (
            paper_data.get('title'),
            paper_data.get('authors'),
            paper_data.get('year'),
            paper_data.get('venue'),
            paper_data.get('doi'),
            paper_data.get('abstract'),
            paper_data.get('citation_key')
        ))
        paper_id = cursor.fetchone()[0]
        self.conn.commit()
        return str(paper_id)
    
    # Papers table operations
    def create_paper(self, title: str, authors: str = None, year: int = None, 
                     venue: str = None, doi: str = None, abstract: str = None, 
                     citation_key: str = None) -> int:
        """
        Create a new paper record.
        
        Args:
            title: Paper title
            authors: Authors list
            year: Publication year
            venue: Publication venue
            doi: DOI identifier
            abstract: Paper abstract
            citation_key: Citation key
            
        Returns:
            ID of the created paper
        """
        query = """
        INSERT INTO papers (title, authors, year, venue, doi, abstract, citation_key)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """
        cursor = self.conn.execute(query, (title, authors, year, venue, doi, abstract, citation_key))
        paper_id = cursor.fetchone()[0]
        self.conn.commit()
        return paper_id
    
    def get_paper_by_id(self, paper_id: int) -> Optional[Dict[str, Any]]:
        """
        Get paper by ID.
        
        Args:
            paper_id: Paper ID
            
        Returns:
            Paper record or None if not found
        """
        query = "SELECT * FROM papers WHERE id = ?"
        cursor = self.conn.execute(query, (paper_id,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def get_paper_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        Get paper by DOI.
        
        Args:
            doi: DOI identifier
            
        Returns:
            Paper record or None if not found
        """
        query = "SELECT * FROM papers WHERE doi = ?"
        cursor = self.conn.execute(query, (doi,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def get_paper_by_citation_key(self, citation_key: str) -> Optional[Dict[str, Any]]:
        """
        Get paper by citation key.
        
        Args:
            citation_key: Citation key
            
        Returns:
            Paper record or None if not found
        """
        query = "SELECT * FROM papers WHERE citation_key = ?"
        cursor = self.conn.execute(query, (citation_key,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def update_paper(self, paper_id: int, **kwargs) -> bool:
        """
        Update paper record.
        
        Args:
            paper_id: Paper ID
            **kwargs: Fields to update
            
        Returns:
            True if updated, False if paper not found
        """
        if not kwargs:
            return False
            
        # Build dynamic UPDATE query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['title', 'authors', 'year', 'venue', 'doi', 'abstract', 'citation_key']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
            
        query = f"UPDATE papers SET {', '.join(fields)} WHERE id = ?"
        values.append(paper_id)
        
        cursor = self.conn.execute(query, values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_paper(self, paper_id: int) -> bool:
        """
        Delete paper record.
        
        Args:
            paper_id: Paper ID
            
        Returns:
            True if deleted, False if paper not found
        """
        query = "DELETE FROM papers WHERE id = ?"
        cursor = self.conn.execute(query, (paper_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # Citations table operations
    def create_citation(self, citing_paper_id: int, cited_paper_id: int, 
                       citation_context: str = None) -> int:
        """
        Create a new citation record.
        
        Args:
            citing_paper_id: ID of the paper that cites
            cited_paper_id: ID of the paper that is cited
            citation_context: Context of the citation
            
        Returns:
            ID of the created citation
        """
        query = """
        INSERT INTO citations (citing_paper_id, cited_paper_id, citation_context)
        VALUES (?, ?, ?)
        RETURNING id
        """
        cursor = self.conn.execute(query, (citing_paper_id, cited_paper_id, citation_context))
        citation_id = cursor.fetchone()[0]
        self.conn.commit()
        return citation_id
    
    def get_citations_for_paper(self, paper_id: int, citing: bool = True) -> List[Dict[str, Any]]:
        """
        Get citations for a paper.
        
        Args:
            paper_id: Paper ID
            citing: If True, get citations made by this paper. If False, get citations to this paper.
            
        Returns:
            List of citation records
        """
        if citing:
            query = "SELECT * FROM citations WHERE citing_paper_id = ?"
            param = paper_id
        else:
            query = "SELECT * FROM citations WHERE cited_paper_id = ?"
            param = paper_id
            
        cursor = self.conn.execute(query, (param,))
        rows = cursor.fetchall()
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    # Relationships table operations
    def create_relationship(self, subject_paper_id: int, object_paper_id: int, 
                          relationship_type: str, confidence_score: float = None, 
                          evidence: str = None) -> int:
        """
        Create a new relationship record.
        
        Args:
            subject_paper_id: ID of the subject paper
            object_paper_id: ID of the object paper
            relationship_type: Type of relationship (e.g., 'critiques', 'extends', 'usesMethodFrom')
            confidence_score: Confidence score
            evidence: Evidence for the relationship
            
        Returns:
            ID of the created relationship
        """
        query = """
        INSERT INTO relationships (subject_paper_id, object_paper_id, relationship_type, 
                                 confidence_score, evidence)
        VALUES (?, ?, ?, ?, ?)
        RETURNING id
        """
        cursor = self.conn.execute(query, (subject_paper_id, object_paper_id, relationship_type, 
                                         confidence_score, evidence))
        relationship_id = cursor.fetchone()[0]
        self.conn.commit()
        return relationship_id
    
    def get_relationships_for_paper(self, paper_id: int, subject: bool = True) -> List[Dict[str, Any]]:
        """
        Get relationships for a paper.
        
        Args:
            paper_id: Paper ID
            subject: If True, get relationships where this paper is the subject. 
                    If False, get relationships where this paper is the object.
            
        Returns:
            List of relationship records
        """
        if subject:
            query = "SELECT * FROM relationships WHERE subject_paper_id = ?"
            param = paper_id
        else:
            query = "SELECT * FROM relationships WHERE object_paper_id = ?"
            param = paper_id
            
        cursor = self.conn.execute(query, (param,))
        rows = cursor.fetchall()
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    def get_relationships_by_type(self, relationship_type: str) -> List[Dict[str, Any]]:
        """
        Get relationships by type.
        
        Args:
            relationship_type: Type of relationship
            
        Returns:
            List of relationship records
        """
        query = "SELECT * FROM relationships WHERE relationship_type = ?"
        cursor = self.conn.execute(query, (relationship_type,))
        rows = cursor.fetchall()
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    # Research gaps table operations
    def create_research_gap(self, manuscript_section: str, gap_description: str, 
                          priority: int = 1, status: str = 'open') -> int:
        """
        Create a new research gap record.
        
        Args:
            manuscript_section: Section of the manuscript
            gap_description: Description of the gap
            priority: Priority level
            status: Status ('open', 'researched', 'addressed')
            
        Returns:
            ID of the created research gap
        """
        query = """
        INSERT INTO research_gaps (manuscript_section, gap_description, priority, status)
        VALUES (?, ?, ?, ?)
        RETURNING id
        """
        cursor = self.conn.execute(query, (manuscript_section, gap_description, priority, status))
        gap_id = cursor.fetchone()[0]
        self.conn.commit()
        return gap_id
    
    def get_research_gap_by_id(self, gap_id: int) -> Optional[Dict[str, Any]]:
        """
        Get research gap by ID.
        
        Args:
            gap_id: Research gap ID
            
        Returns:
            Research gap record or None if not found
        """
        query = "SELECT * FROM research_gaps WHERE id = ?"
        cursor = self.conn.execute(query, (gap_id,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def get_open_research_gaps(self) -> List[Dict[str, Any]]:
        """
        Get all open research gaps.
        
        Returns:
            List of open research gap records
        """
        query = "SELECT * FROM research_gaps WHERE status = 'open' ORDER BY priority DESC"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    def update_research_gap_status(self, gap_id: int, status: str) -> bool:
        """
        Update research gap status.
        
        Args:
            gap_id: Research gap ID
            status: New status ('open', 'researched', 'addressed')
            
        Returns:
            True if updated, False if gap not found
        """
        query = "UPDATE research_gaps SET status = ?, updated_at = ? WHERE id = ?"
        cursor = self.conn.execute(query, (status, datetime.now(), gap_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_research_gap_priority(self, gap_id: int, priority: int) -> bool:
        """
        Update research gap priority.
        
        Args:
            gap_id: Research gap ID
            priority: New priority level
            
        Returns:
            True if updated, False if gap not found
        """
        query = "UPDATE research_gaps SET priority = ?, updated_at = ? WHERE id = ?"
        cursor = self.conn.execute(query, (priority, datetime.now(), gap_id))
        self.conn.commit()
        return cursor.rowcount > 0

# Server initialization for MCP
def create_server(db_path: str = ".sros/graph.db") -> DuckDBMemoryServer:
    """
    Create and initialize the DuckDB Memory server.
    
    Args:
        db_path: Path to the DuckDB database file
        
    Returns:
        Initialized DuckDBMemoryServer instance
    """
    return DuckDBMemoryServer(db_path)

if __name__ == "__main__":
    # Example usage
    server = create_server()
    print("DuckDB Memory Server initialized successfully!")
    server.close()