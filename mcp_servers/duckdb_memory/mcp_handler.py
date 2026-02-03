"""
MCP Handler for DuckDB Memory Server
Implements the Model Context Protocol interface for the DuckDB Memory server.
"""

import json
from typing import Dict, Any, List
from .server import DuckDBMemoryServer
from .config import get_db_path

class DuckDBMemoryMCPHandler:
    """MCP Handler for DuckDB Memory Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        self.server = DuckDBMemoryServer(get_db_path())
    
    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP requests.
        
        Args:
            method: MCP method name
            params: Method parameters
            
        Returns:
            Response dictionary
        """
        try:
            if method == "initialize":
                return self._handle_initialize(params)
            elif method == "create_paper":
                return self._handle_create_paper(params)
            elif method == "get_paper":
                return self._handle_get_paper(params)
            elif method == "update_paper":
                return self._handle_update_paper(params)
            elif method == "create_citation":
                return self._handle_create_citation(params)
            elif method == "get_citations":
                return self._handle_get_citations(params)
            elif method == "create_relationship":
                return self._handle_create_relationship(params)
            elif method == "get_relationships":
                return self._handle_get_relationships(params)
            elif method == "create_research_gap":
                return self._handle_create_research_gap(params)
            elif method == "get_research_gaps":
                return self._handle_get_research_gaps(params)
            elif method == "update_research_gap":
                return self._handle_update_research_gap(params)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "result": {
                "capabilities": {
                    "paperManagement": True,
                    "citationTracking": True,
                    "relationshipMapping": True,
                    "researchGapTracking": True
                }
            }
        }
    
    def _handle_create_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_paper request."""
        try:
            paper_id = self.server.create_paper(
                title=params.get("title"),
                authors=params.get("authors"),
                year=params.get("year"),
                venue=params.get("venue"),
                doi=params.get("doi"),
                abstract=params.get("abstract"),
                citation_key=params.get("citation_key")
            )
            return {"result": {"id": paper_id}}
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Invalid params: {str(e)}"
                }
            }
    
    def _handle_get_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper request."""
        paper_id = params.get("id")
        doi = params.get("doi")
        citation_key = params.get("citation_key")
        
        paper = None
        if paper_id:
            paper = self.server.get_paper_by_id(paper_id)
        elif doi:
            paper = self.server.get_paper_by_doi(doi)
        elif citation_key:
            paper = self.server.get_paper_by_citation_key(citation_key)
        
        if paper:
            return {"result": paper}
        else:
            return {
                "error": {
                    "code": -32602,
                    "message": "Paper not found"
                }
            }
    
    def _handle_update_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_paper request."""
        paper_id = params.get("id")
        if not paper_id:
            return {
                "error": {
                    "code": -32602,
                    "message": "Missing paper ID"
                }
            }
        
        try:
            # Remove ID from update data
            update_data = {k: v for k, v in params.items() if k != "id"}
            success = self.server.update_paper(paper_id, **update_data)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Invalid params: {str(e)}"
                }
            }
    
    def _handle_create_citation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_citation request."""
        try:
            citing_paper_id = params["citing_paper_id"]
            cited_paper_id = params["cited_paper_id"]
            citation_context = params.get("citation_context")
            
            citation_id = self.server.create_citation(
                citing_paper_id, cited_paper_id, citation_context
            )
            return {"result": {"id": citation_id}}
        except KeyError as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Missing required parameter: {str(e)}"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Invalid params: {str(e)}"
                }
            }
    
    def _handle_get_citations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_citations request."""
        paper_id = params.get("paper_id")
        citing = params.get("citing", True)
        
        if not paper_id:
            return {
                "error": {
                    "code": -32602,
                    "message": "Missing paper ID"
                }
            }
        
        try:
            citations = self.server.get_citations_for_paper(paper_id, citing)
            return {"result": citations}
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error retrieving citations: {str(e)}"
                }
            }
    
    def _handle_create_relationship(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_relationship request."""
        try:
            subject_paper_id = params["subject_paper_id"]
            object_paper_id = params["object_paper_id"]
            relationship_type = params["relationship_type"]
            confidence_score = params.get("confidence_score")
            evidence = params.get("evidence")
            
            relationship_id = self.server.create_relationship(
                subject_paper_id, object_paper_id, relationship_type, 
                confidence_score, evidence
            )
            return {"result": {"id": relationship_id}}
        except KeyError as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Missing required parameter: {str(e)}"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Invalid params: {str(e)}"
                }
            }
    
    def _handle_get_relationships(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_relationships request."""
        paper_id = params.get("paper_id")
        subject = params.get("subject", True)
        relationship_type = params.get("relationship_type")
        
        try:
            if relationship_type:
                relationships = self.server.get_relationships_by_type(relationship_type)
            elif paper_id:
                relationships = self.server.get_relationships_for_paper(paper_id, subject)
            else:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Either paper_id or relationship_type must be specified"
                    }
                }
            
            return {"result": relationships}
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error retrieving relationships: {str(e)}"
                }
            }
    
    def _handle_create_research_gap(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_research_gap request."""
        try:
            manuscript_section = params["manuscript_section"]
            gap_description = params["gap_description"]
            priority = params.get("priority", 1)
            status = params.get("status", "open")
            
            gap_id = self.server.create_research_gap(
                manuscript_section, gap_description, priority, status
            )
            return {"result": {"id": gap_id}}
        except KeyError as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Missing required parameter: {str(e)}"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Invalid params: {str(e)}"
                }
            }
    
    def _handle_get_research_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_research_gaps request."""
        gap_id = params.get("id")
        open_gaps = params.get("open_only", False)
        
        try:
            if gap_id:
                gap = self.server.get_research_gap_by_id(gap_id)
                if gap:
                    return {"result": gap}
                else:
                    return {
                        "error": {
                            "code": -32602,
                            "message": "Research gap not found"
                        }
                    }
            elif open_gaps:
                gaps = self.server.get_open_research_gaps()
                return {"result": gaps}
            else:
                # TODO: Implement get all research gaps
                return {
                    "error": {
                        "code": -32602,
                        "message": "Not implemented"
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error retrieving research gaps: {str(e)}"
                }
            }
    
    def _handle_update_research_gap(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_research_gap request."""
        gap_id = params.get("id")
        status = params.get("status")
        priority = params.get("priority")
        
        if not gap_id:
            return {
                "error": {
                    "code": -32602,
                    "message": "Missing research gap ID"
                }
            }
        
        try:
            success = False
            if status:
                success = self.server.update_research_gap_status(gap_id, status)
            elif priority is not None:
                success = self.server.update_research_gap_priority(gap_id, priority)
            
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error updating research gap: {str(e)}"
                }
            }
    
    def close(self):
        """Close the server connection."""
        self.server.close()

# Global handler instance
_handler = None

def get_handler() -> DuckDBMemoryMCPHandler:
    """Get or create the global MCP handler instance."""
    global _handler
    if _handler is None:
        _handler = DuckDBMemoryMCPHandler()
    return _handler

def handle_mcp_request(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle an MCP request.
    
    Args:
        method: MCP method name
        params: Method parameters
        
    Returns:
        Response dictionary
    """
    handler = get_handler()
    return handler.handle_request(method, params)

if __name__ == "__main__":
    # Example usage
    handler = get_handler()
    print("DuckDB Memory MCP Handler initialized successfully!")