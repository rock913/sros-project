from typing import Dict, List, Any
from pydantic import BaseModel, Field, ConfigDict

class GraphNode(BaseModel):
    """Represents a node in the knowledge graph."""
    id: str = Field(..., description="Unique identifier within the graph")
    label: str = Field(..., description="Node label (e.g., Paper, Concept, Author)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Node properties")
    
    model_config = ConfigDict(extra='allow')

class GraphEdge(BaseModel):
    """Represents an edge/relationship in the knowledge graph."""
    source_id: str = Field(..., description="ID of the source node")
    target_id: str = Field(..., description="ID of the target node")
    relation_type: str = Field(..., description="Type of relationship (e.g., CITES, AUTHORED_BY)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Edge properties")

class KnowledgeTriplet(BaseModel):
    """A simplified representation of knowledge: (Subject, Predicate, Object)."""
    subject: GraphNode
    predicate: str
    object: GraphNode
