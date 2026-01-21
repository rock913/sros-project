from mcp import MCPTool, MCPToolResult

from agent.domain.schemas.paper import Paper
from agent.infrastructure.tools.zotero_adapter import ZoteroAdapter


class ZoteroMCPTool(MCPTool):
    """Wrapper for ZoteroAdapter to be used as an MCP Tool."""
    
    def __init__(self):
        """Initialize the ZoteroMCPTool.
        """
        self.zotero_adapter = ZoteroAdapter()

    def name(self) -> str:
        """Return the name of the tool.
        """
        return "zotero_tool"

    def description(self) -> str:
        """Return the description of the tool.
        """
        return "Save a paper to Zotero."

    def execute(self, paper_data: dict) -> MCPToolResult:
        """Execute the tool to save a paper to Zotero.
        """
        try:
            paper = Paper(**paper_data)
            result = self.zotero_adapter.save_paper(paper)
            return MCPToolResult(success=True, message=result)
        except Exception as e:
            return MCPToolResult(success=False, message=str(e))
