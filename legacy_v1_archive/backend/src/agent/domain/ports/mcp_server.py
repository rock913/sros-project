from typing import Protocol, List, Any
from agent.domain.schemas.mcp import McpTool

class McpServer(Protocol):
    """
    Protocol defining the capabilities of an MCP Server.
    
    This interface abstracts away the underlying library (e.g., mcp, fastmcp)
    allowing the domain layer to register capabilities without coupling.
    
    @TestScenarios
    1. Registration Success:
       - Input: Valid McpTool.
       - Expected: Tool is added to internal registry. 
       - Verification: list_tools() returns the registered tool.
       
    2. Duplicate Registration:
       - Input: Registering a tool with a name that already exists.
       - Expected: ValueError or Overwrite (implementation choice, let's genericize to Overwrite or warnings).
       - Decision: ValueError to prevent ambiguity.
       
    3. Tool Execution via Server (Simulated):
       - Input: Tool registered, mocked context tries to call it.
       - Expected: Handler is invoked.
       
    4. Lifecycle:
       - Test initialization and mocked start/serve methods.
    """
    
    def register_tool(self, tool: McpTool) -> None:
        """
        Register a tool capability with the server.
        
        Args:
            tool: The defined McpTool containing metadata and handler.
            
        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        ...
        
    def list_tools(self) -> List[McpTool]:
        """
        Return a list of currently registered tools.
        """
        ...

    async def start(self) -> None:
        """
        Start the MCP server (e.g. over Stdio or SSE).
        Implementation should be blocking or use async run loop depending on transport.
        """
        ...
