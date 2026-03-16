from mcp.server import Server
import asyncio
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

# Initialize Server
app = Server("mock-researcher")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="federal_search_papers",
            description="[Mock] Search for academic papers in federal databases",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="manuscript_create_section",
            description="[Mock] Create a new section in the manuscript",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="zotero_get_bib",
            description="[Mock] Get bibliography from Zotero",
            inputSchema={"type": "object"}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "federal_search_papers":
        query = arguments.get("query")
        return [TextContent(
            type="text", 
            text=f"Mock Results for '{query}':\n1. AI Agents in 2026 (DOI: 10.1234/ai.2026)\n2. SROS Architecture (DOI: 10.1234/sros)"
        )]
    
    elif name == "manuscript_create_section":
        return [TextContent(type="text", text=f"Section '{arguments.get('title')}' created successfully.")]
        
    elif name == "zotero_get_bib":
        return [TextContent(type="text", text="@article{test2026, title={Test Paper}, author={Doe, John}}")]
        
    raise ValueError(f"Tool not found: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
