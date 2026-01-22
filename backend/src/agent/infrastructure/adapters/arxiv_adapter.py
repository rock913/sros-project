from typing import List

from agent.domain.ports.paper_searcher import PaperSearcher
from agent.domain.schemas.mcp import McpTool
from agent.domain.schemas.paper import Paper


class ArxivAdapter(PaperSearcher):
    def search(self, query: str, max_results: int = 5) -> List[Paper]:
        # Implementation will go here
        pass

def get_tool() -> McpTool:
    return McpTool(
        name="arxiv_search",
        description="Search for academic papers on Arxiv",
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        },
        handler=ArxivAdapter().search
    )
