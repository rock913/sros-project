from mcp.server import Server
import asyncio
from mcp.types import Tool, TextContent
import mcp.server.stdio
import json

# Lazy loader
_handler_instance = None

def get_handler():
    global _handler_instance
    if _handler_instance is None:
        from .mcp_handler import FederalAcademicSearchMCPHandler
        _handler_instance = FederalAcademicSearchMCPHandler()
    return _handler_instance

app = Server("federal-academic-search")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_papers",
            description="Search for academic papers using OpenAlex, Unpaywall, and Semantic Scholar.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 10},
                    "enrich": {"type": "boolean", "default": True, "description": "Enrich with extra metadata"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_paper_details",
            description="Get detailed metadata for a specific paper.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string", "description": "OpenAlex ID or DOI"}
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="get_citation_context",
            description="Get context where this paper is cited (citation sentences).",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="download_pdf",
            description="Get the PDF URL for a paper if open access.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string"}
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="search_by_author",
            description="Search for papers by a specific author.",
            inputSchema={
                "type": "object",
                "properties": {
                    "author_name": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["author_name"]
            }
        ),
         Tool(
            name="get_paper_references",
            description="Get list of papers referenced by this paper.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="get_tldr",
            description="Get a TLDR (Too Long; Didn't Read) summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string"}
                },
                "required": ["paper_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        handler = get_handler()
        
        # Helper to extract result
        def extract_result(response):
             if "result" in response:
                 return json.dumps(response["result"], default=str)
             if "error" in response:
                 return f"Error: {response['error']}"
             return str(response)

        if name == "search_papers":
            resp = handler.handle_request("search_papers", arguments)
            return [TextContent(type="text", text=extract_result(resp))]
            
        elif name == "get_paper_details":
            resp = handler.handle_request("get_paper_details", arguments)
            return [TextContent(type="text", text=extract_result(resp))]
            
        elif name == "get_citation_context":
            resp = handler.handle_request("get_citation_context", arguments)
            return [TextContent(type="text", text=extract_result(resp))]
        
        elif name == "download_pdf":
            resp = handler.handle_request("download_pdf", arguments)
            return [TextContent(type="text", text=extract_result(resp))]

        elif name == "search_by_author":
            resp = handler.handle_request("search_by_author", arguments)
            return [TextContent(type="text", text=extract_result(resp))]
            
        elif name == "get_paper_references":
            resp = handler.handle_request("get_paper_references", arguments)
            return [TextContent(type="text", text=extract_result(resp))]
            
        elif name == "get_tldr":
            resp = handler.handle_request("get_tldr", arguments)
            return [TextContent(type="text", text=extract_result(resp))]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(type="text", text=f"Error processing {name}: {str(e)}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
