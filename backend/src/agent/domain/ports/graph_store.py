from typing import List, Protocol, Dict, Any, Optional
from agent.domain.schemas.knowledge_graph import GraphNode, GraphEdge, KnowledgeTriplet

class GraphStore(Protocol):
    """
    Protocol for interacting with a Graph Database (e.g., Neo4j).
    
    @TestScenarios
    1. Add Node:
       - Input: GraphNode(id="p1", label="Paper", properties={"title": "A"}).
       - Expected: Node persistence verified by subsequent fetch.
       
    2. Add Relationship:
       - Input: Two existing nodes, create edge.
       - Expected: Edge exists.
       
    3. Query Subgraph:
       - Input: Root node ID, depth.
       - Expected: List of related nodes and edges.
    """
    
    def add_node(self, node: GraphNode) -> None:
        """Add or update a node in the graph."""
        ...
        
    def add_edge(self, edge: GraphEdge) -> None:
        """Add a directed edge between two nodes."""
        ...
        
    def add_triplet(self, triplet: KnowledgeTriplet) -> None:
        """Convenience method to add subject, object and their relationship."""
        ...
        
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Retrieve a node by its ID."""
        ...
        
    def get_neighbors(self, node_id: str, relation_type: Optional[str] = None) -> List[GraphNode]:
        """Get adjacent nodes, optionally filtered by relationship type."""
        ...
        
    def query(self, query_str: str, params: Dict[str, Any] = None) -> Any:
        """Execute a raw query (e.g., Cypher) against the store."""
        ...
