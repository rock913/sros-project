"""Tools for interacting with Zotero via MCP."""

from pydantic import BaseModel

from agent.domain.schemas.mcp import McpTool
from agent.domain.schemas.paper import Paper
from agent.infrastructure.tools.zotero_adapter import ZoteroAdapter


class ZoteroSaveInput(BaseModel):
    """Input schema for the Zotero save MCP tool."""
    paper: Paper


def get_zotero_save_mcp_tool() -> McpTool:
    """Create and return an MCP tool for saving papers to Zotero."""
    adapter = ZoteroAdapter()

    def handler(input_data: dict | ZoteroSaveInput) -> dict:
        # Ensure input_data is an instance of ZoteroSaveInput
        if isinstance(input_data, dict):
            input_data = ZoteroSaveInput(**input_data)

        try:
            result = adapter.save_paper(input_data.paper)
            return {"success": True, "message": result}
        except Exception as e:
            return {"success": False, "message": str(e)}

    return McpTool(
        name="zotero-save-paper",
        description="Saves a paper to Zotero.",
        input_schema=ZoteroSaveInput.model_json_schema(),
        handler=handler
    )
