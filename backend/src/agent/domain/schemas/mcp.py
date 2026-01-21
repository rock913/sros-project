from typing import Any, Callable, Dict, Optional
from pydantic import BaseModel, Field

class McpTool(BaseModel):
    """
    Domain representation of a Tool exposed via Model Context Protocol (MCP).
    
    This acts as a bridge between internal logic and the MCP SDK.
    """
    name: str = Field(..., description="Unique name of the tool (e.g., 'fetch-paper')")
    description: str = Field(..., description="Human-readable description for the LLM")
    input_schema: Dict[str, Any] = Field(..., description="JSON Schema defining the expected arguments")
    handler: Callable[..., Any] = Field(..., description="The function to execute when tool is called", exclude=True)
    
    class Config:
        arbitrary_types_allowed = True
