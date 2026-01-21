"""Tools for interacting with Zotero via MCP."""

from agent.domain.schemas.mcp import McpTool
from agent.domain.schemas.paper import Paper
from agent.infrastructure.tools.zotero_adapter import ZoteroAdapter


class ZoteroMCPTool(McpTool):
    """Wrapper for ZoteroAdapter to be used as an MCP Tool."""
    
    def __init__(self):
        """Initialize the ZoteroMCPTool."""
        self.zotero_adapter = ZoteroAdapter()

    def name(self) -> str:
        """Return the name of the tool."""
        return "zotero_tool"

    def description(self) -> str:
        """Return the description of the tool."""
        return "Save a paper to Zotero."

    def execute(self, paper_data: dict) -> dict:
        """Execute the tool to save a paper to Zotero."""
        try:
            paper = Paper(**paper_data)
            result = self.zotero_adapter.save_paper(paper)
            return {"success": True, "message": result}
        except Exception as e:
            return {"success": False, "message": str(e)}
