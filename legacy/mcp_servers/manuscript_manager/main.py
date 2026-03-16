from mcp.server import Server
import asyncio
from mcp.types import Tool, TextContent
import mcp.server.stdio
import json
import os

# Global instance for lazy loading
_server_instance = None

def get_server():
    global _server_instance
    if _server_instance is None:
        # Import here to avoid heavy load at startup
        from .server import ManuscriptManagerServer
        _server_instance = ManuscriptManagerServer()
    return _server_instance

app = Server("manuscript-manager")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_structure",
            description="Get the current structure of the manuscript (headers, sections)",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="detect_gaps",
            description="Detect missing sections, TODOs, or logical gaps in the manuscript",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="edit_section",
            description="Edit a specific section of the manuscript. Supports append, replace, or prepend modes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_path": {
                        "type": "string",
                        "description": "Path to section, e.g. 'Introduction > Background' or just 'Background'"
                    },
                    "content": {
                        "type": "string",
                        "description": "The markdown content"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["append", "replace", "prepend"],
                        "default": "append",
                        "description": "How to apply the edit"
                    }
                },
                "required": ["section_path", "content"]
            }
        ),
        Tool(
            name="get_section_content",
            description="Get the content of a specific section",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_path": {
                        "type": "string",
                        "description": "Path to section"
                    }
                },
                "required": ["section_path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        srv = get_server()
        
        if name == "get_structure":
            structure = srv.get_structure()
            return [TextContent(type="text", text=json.dumps(structure, indent=2))]
        
        elif name == "detect_gaps":
            gaps = srv.detect_gaps()
            return [TextContent(type="text", text=json.dumps(gaps, indent=2))]
        
        elif name == "edit_section":
            path = arguments.get("section_path")
            content = arguments.get("content")
            mode = arguments.get("mode", "append")
            success = srv.edit_section(path, content, mode)
            if success:
                return [TextContent(type="text", text=f"Successfully edited section '{path}' in mode '{mode}'.")]
            else:
                return [TextContent(type="text", text=f"Failed to edit section '{path}'. Section not found or file error.")]
        
        elif name == "get_section_content":
            path = arguments.get("section_path")
            content = srv.get_section_content(path)
            if content is None:
                 return [TextContent(type="text", text=f"Section '{path}' not found.")]
            return [TextContent(type="text", text=content)]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(type="text", text=f"Error processing {name}: {str(e)}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
