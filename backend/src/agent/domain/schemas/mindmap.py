"""
MindMap Schema for Co-STORM Discovery Engine

This module defines the data structures for the collaborative STORM (Co-STORM) mind mapping
and perspective generation system used in Phase 5.2 draft-driven research.

@Co-STORM Algorithm:
1. User provides topic -> Generate 3-5 distinct research perspectives (e.g., Historical, Methodological, Applications)
2. Each perspective becomes a "PerspectiveNode" in the MindMap with description and query keywords
3. Librarian and Analyst engage in discourse to unearth "unknown unknowns"
4. Gap Finder compares Outline vs. Content, flagging evidence gaps
5. Incremental Writer fills gaps with cited paragraphs

@Hexagonal Architecture:
- This is pure domain logic (no I/O)
- Used by application layer for LLM prompting and state management
- Tested independently without infrastructure dependencies
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from agent.domain.schemas.paper import Paper


class PerspectiveNode(BaseModel):
    """A research perspective node in the Co-STORM mind map.

    Each node represents a unique angle or approach to researching the topic,
    complete with description and search keywords for Librarian discovery.

    @TestScenarios
    - Create node with id="methodological", name="Methodological", description="...", query_keywords=["methods", "algorithms", "techniques"]
    - Validate unique_id: no duplicate IDs in same MindMap
    - Validate keywords: minimum 3, maximum 5 keywords
    - LLM generated: valid JSON output for 3-5 nodes per topic
    """
    id: str = Field(..., description="Unique node identifier (e.g., 'methodological', 'historical')")
    name: str = Field(..., max_length=50, description="Human-readable node name (e.g., 'Methodological Perspective')")
    description: str = Field(..., max_length=500, description="Brief explanation of this research angle")
    query_keywords: List[str] = Field(..., description="Search keywords for this perspective")
    papers: Optional[List[Paper]] = Field(default_factory=list, description="Papers found via Librarian search")
    summary: Optional[str] = Field(None, description="Perspective summary created by Analyst")

    @field_validator('query_keywords')
    @classmethod
    def validate_query_keywords(cls, v):
        """Ensure query keywords are valid and unique."""
        if len(v) != len(set(v)):
            raise ValueError('query_keywords must be unique')
        return v

    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """Ensure id is lowercase and contains no spaces."""
        if ' ' in v:
            raise ValueError('id must not contain spaces')
        return v.lower()

    @field_validator('query_keywords', mode='before')
    @classmethod
    def ensure_list(cls, v):
        """Convert comma-separated string to list if necessary."""
        if isinstance(v, str):
            return [keyword.strip() for keyword in v.split(',')]
        return v


class MindMap(BaseModel):
    """The complete Co-STORM mind map starting from a root research topic.

    Co-STORM generates 3-5 PerspectiveNodes to create diverse research angles,
    enabling Librarian-Analyst discourse to find unknown unknowns.

    @TestScenarios
    - From topic="Quantum Computing": generates nodes for ['methodological', 'historical', 'applications']
    - Validate: exactly 3-5 nodes, no duplicate IDs, non-empty root_topic
    - Used in LLM structured output for perspective generation
    - Serializable via model_dump_json() for MCP updates
    """
    root_topic: str = Field(..., max_length=200, description="The original research topic")
    nodes: List[PerspectiveNode] = Field(..., min_items=3, max_items=5, description="Generated research perspectives")

    @model_validator(mode='after')
    def validate_unique_node_ids(self):
        """Ensure all node IDs are unique."""
        ids = [node.id for node in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError('All nodes must have unique IDs')
        return self

    @model_validator(mode='after')
    def validate_sufficient_perspectives(self):
        """Ensure we have the optimal number of perspectives for Co-STORM."""
        if not (3 <= len(self.nodes) <= 5):
            raise ValueError('MindMap must have 3-5 perspectives for effective Co-STORM discussion')
        return self
