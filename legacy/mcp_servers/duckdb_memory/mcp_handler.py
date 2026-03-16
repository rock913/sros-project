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
                # Ensure we return valid initialize response
                return {
                    "protocolVersion": "2024-11-05", # Updated
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {}
                    },
                    "serverInfo": {
                        "name": "DuckDB Memory",
                        "version": "1.0.0"
                    }
                }
            elif method == "notifications/initialized":
                return None
            elif method == "tools/list":
                return {
                    "tools": [
                        {"name": "duckdb_create_paper", "description": "Create a new paper entry", "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}, "abstract": {"type": "string"}, "year": {"type": "integer"}}}},
                        {"name": "duckdb_search_papers", "description": "Search papers", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}}},
                    ]
                }
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
            elif method == "get_papers_by_year":
                return self._handle_get_papers_by_year(params)
            elif method == "get_citations_by_paper":
                return self._handle_get_citations_by_paper(params)
            elif method == "get_relationships_by_paper":
                return self._handle_get_relationships_by_paper(params)
            elif method == "search_papers":
                return self._handle_search_papers(params)
            elif method == "get_paper_statistics":
                return self._handle_get_paper_statistics(params)
            elif method == "batch_create_papers":
                return self._handle_batch_create_papers(params)
            elif method == "delete_paper":
                return self._handle_delete_paper(params)
            elif method == "get_related_papers":
                return self._handle_get_related_papers(params)
            elif method == "export_data":
                return self._handle_export_data(params)
            elif method == "import_data":
                return self._handle_import_data(params)
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
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "DuckDB Memory MCP Server",
                    "version": "1.0.0"
                },
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
            paper_data = params.get("paper", {})
            paper_id = self.server.create_paper(paper_data)
            return {"result": {"id": paper_id}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to create paper: {str(e)}"
                }
            }
    
    def _handle_get_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper request."""
        try:
            paper_id = params.get("id")
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: id"
                    }
                }
            
            paper = self.server.get_paper(paper_id)
            if paper:
                return {"result": paper}
            else:
                return {
                    "error": {
                        "code": -32603,
                        "message": f"Paper not found: {paper_id}"
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get paper: {str(e)}"
                }
            }
    
    def _handle_update_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_paper request."""
        try:
            paper_id = params.get("id")
            paper_data = params.get("paper", {})
            
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: id"
                    }
                }
            
            success = self.server.update_paper(paper_id, paper_data)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to update paper: {str(e)}"
                }
            }
    
    def _handle_create_citation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_citation request."""
        try:
            citing_paper_id = params.get("citing_paper_id")
            cited_paper_id = params.get("cited_paper_id")
            citation_data = params.get("citation", {})
            
            if not citing_paper_id or not cited_paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: citing_paper_id and cited_paper_id"
                    }
                }
            
            citation_id = self.server.create_citation(citing_paper_id, cited_paper_id, citation_data)
            return {"result": {"id": citation_id}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to create citation: {str(e)}"
                }
            }
    
    def _handle_get_citations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_citations request."""
        try:
            paper_id = params.get("paper_id")
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: paper_id"
                    }
                }
            
            citations = self.server.get_citations(paper_id)
            return {"result": citations}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get citations: {str(e)}"
                }
            }
    
    def _handle_create_relationship(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_relationship request."""
        try:
            paper1_id = params.get("paper1_id")
            paper2_id = params.get("paper2_id")
            relationship_type = params.get("relationship_type")
            relationship_data = params.get("relationship", {})
            
            if not paper1_id or not paper2_id or not relationship_type:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: paper1_id, paper2_id, and relationship_type"
                    }
                }
            
            relationship_id = self.server.create_relationship(paper1_id, paper2_id, relationship_type, relationship_data)
            return {"result": {"id": relationship_id}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to create relationship: {str(e)}"
                }
            }
    
    def _handle_get_relationships(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_relationships request."""
        try:
            paper_id = params.get("paper_id")
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: paper_id"
                    }
                }
            
            relationships = self.server.get_relationships(paper_id)
            return {"result": relationships}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get relationships: {str(e)}"
                }
            }
    
    def _handle_create_research_gap(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_research_gap request."""
        try:
            gap_data = params.get("gap", {})
            gap_id = self.server.create_research_gap(gap_data)
            return {"result": {"id": gap_id}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to create research gap: {str(e)}"
                }
            }
    
    def _handle_get_research_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_research_gaps request."""
        try:
            gaps = self.server.get_research_gaps()
            return {"result": gaps}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get research gaps: {str(e)}"
                }
            }
    
    def _handle_update_research_gap(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_research_gap request."""
        try:
            gap_id = params.get("id")
            gap_data = params.get("gap", {})
            
            if not gap_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: id"
                    }
                }
            
            success = self.server.update_research_gap(gap_id, gap_data)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to update research gap: {str(e)}"
                }
            }
    
    def _handle_get_papers_by_year(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_papers_by_year request."""
        try:
            year = params.get("year")
            if year is None:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: year"
                    }
                }
            
            papers = self.server.get_papers_by_year(year)
            return {"result": papers}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get papers by year: {str(e)}"
                }
            }
    
    def _handle_get_citations_by_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_citations_by_paper request."""
        try:
            paper_id = params.get("paper_id")
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: paper_id"
                    }
                }
            
            citations = self.server.get_citations_by_paper(paper_id)
            return {"result": citations}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get citations by paper: {str(e)}"
                }
            }
    
    def _handle_get_relationships_by_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_relationships_by_paper request."""
        try:
            paper_id = params.get("paper_id")
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: paper_id"
                    }
                }
            
            relationships = self.server.get_relationships_by_paper(paper_id)
            return {"result": relationships}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get relationships by paper: {str(e)}"
                }
            }
    
    def _handle_search_papers(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_papers request."""
        try:
            query = params.get("query", "")
            limit = params.get("limit", 10)
            
            if not query:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: query"
                    }
                }
            
            results = self.server.search_papers(query, limit)
            return {"result": results}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to search papers: {str(e)}"
                }
            }
    
    def _handle_get_paper_statistics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper_statistics request."""
        try:
            stats = self.server.get_paper_statistics()
            return {"result": stats}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get paper statistics: {str(e)}"
                }
            }
    
    def _handle_batch_create_papers(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle batch_create_papers request."""
        try:
            papers = params.get("papers", [])
            if not papers:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: papers"
                    }
                }
            
            results = self.server.batch_create_papers(papers)
            return {"result": results}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to batch create papers: {str(e)}"
                }
            }
    
    def _handle_delete_paper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle delete_paper request."""
        try:
            paper_id = params.get("id")
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: id"
                    }
                }
            
            success = self.server.delete_paper(paper_id)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to delete paper: {str(e)}"
                }
            }
    
    def _handle_get_related_papers(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_related_papers request."""
        try:
            paper_id = params.get("paper_id")
            limit = params.get("limit", 10)
            
            if not paper_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: paper_id"
                    }
                }
            
            related_papers = self.server.get_related_papers(paper_id, limit)
            return {"result": related_papers}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get related papers: {str(e)}"
                }
            }
    
    def _handle_export_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle export_data request."""
        try:
            format_type = params.get("format", "json")
            data = self.server.export_data(format_type)
            return {"result": {"data": data}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to export data: {str(e)}"
                }
            }
    
    def _handle_import_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle import_data request."""
        try:
            data = params.get("data", {})
            format_type = params.get("format", "json")
            success = self.server.import_data(data, format_type)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to import data: {str(e)}"
                }
            }

def get_handler() -> DuckDBMemoryMCPHandler:
    """Get singleton instance of the handler."""
    if not hasattr(get_handler, '_instance'):
        get_handler._instance = DuckDBMemoryMCPHandler()
    return get_handler._instance

def handle_mcp_request(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request using singleton handler."""
    handler = get_handler()
    return handler.handle_request(method, params)