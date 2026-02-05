from mcp.server import Server
import asyncio
from mcp.types import Tool, TextContent
import mcp.server.stdio
from .server import DuckDBMemoryServer
from .config import get_db_path
import json

# Initialize
db_path = get_db_path()
db_service = DuckDBMemoryServer(db_path)
# Ensure connection
_ = db_service.conn 

app = Server("duckdb-memory")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_paper",
            description="Create a new paper entry in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "abstract": {"type": "string"},
                    "year": {"type": "integer"},
                    "authors": {"type": "string"},
                    "venue": {"type": "string"},
                    "doi": {"type": "string"},
                    "citation_key": {"type": "string"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="search_papers",
            description="Search papers by keyword in title or abstract",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_paper",
            description="Retrieve paper details by ID, DOI or Citation Key",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string", "description": "ID, DOI or Citation Key"}
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="store_relation",
            description="Store a relationship (knowledge triple) between concepts or papers",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "predicate": {"type": "string"},
                    "object": {"type": "string"}
                },
                "required": ["subject", "predicate", "object"]
            }
        ),
        Tool(
            name="query_relations",
            description="Query relationships/knowledge graph",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject_query": {"type": "string", "description": "Filter by subject (partial match)"},
                    "predicate": {"type": "string", "description": "Filter by relationship type"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "create_paper":
            result = db_service.create_paper(
                title=arguments["title"],
                authors=arguments.get("authors"),
                year=arguments.get("year"),
                venue=arguments.get("venue"),
                doi=arguments.get("doi"),
                abstract=arguments.get("abstract"),
                citation_key=arguments.get("citation_key")
            )
            return [TextContent(type="text", text=str(result))]
        
        elif name == "search_papers":
            query_str = arguments["query"]
            limit = arguments.get("limit", 10)
            sql = "SELECT * FROM papers WHERE title ILIKE ? OR abstract ILIKE ? LIMIT ?"
            cursor = db_service.conn.execute(sql, (f"%{query_str}%", f"%{query_str}%", limit))
            columns = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
            return [TextContent(type="text", text=json.dumps(results, default=str))]
            
        elif name == "get_paper":
            pid = arguments["paper_id"]
            res = None
            if pid.isdigit():
                 res = db_service.get_paper_by_id(int(pid))
            
            if not res:
                 res = db_service.get_paper(pid) # Handles DOI/Key
            
            return [TextContent(type="text", text=json.dumps(res, default=str))]
        
        elif name == "store_relation":
            # Using abstract add_knowledge from server.py which inserts into 'relationships'
            db_service.add_knowledge(
                subject=arguments["subject"],
                predicate=arguments["predicate"],
                object=arguments["object"]
            )
            return [TextContent(type="text", text="Relationship stored successfully.")]

        elif name == "query_relations":
            subject_query = arguments.get("subject_query", "")
            predicate = arguments.get("predicate", "")
            limit = arguments.get("limit", 10)
            
            sql = "SELECT * FROM relationships WHERE 1=1"
            params = []
            if subject_query:
                sql += " AND evidence ILIKE ?"  # evidence combines sub/pred/obj usually
                params.append(f"%{subject_query}%")
            if predicate:
                sql += " AND relationship_type = ?"
                params.append(predicate)
            
            sql += " LIMIT ?"
            params.append(limit)
            
            cursor = db_service.conn.execute(sql, tuple(params))
            columns = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
            return [TextContent(type="text", text=json.dumps(results, default=str))]
            
        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
