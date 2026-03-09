import asyncio
import json
import sys
from typing import List, Dict, Any
from mcp.server import Server
from mcp.types import CallToolResult, TextContent
from sros.domain.ports import ScholarProtocol
from sros.domain.schemas import ResearchPerspective, SearchQuery

# 延迟导入以满足性能要求
def get_scholar_service() -> ScholarProtocol:
    try:
        from sros.servers.scholar.handler import ScholarHandler
        return ScholarHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize scholar service: {str(e)}") from e

def create_scholar_server():
    """创建学者 MCP 服务器"""
    server = Server("mcp-scholar")

    @server.tool("brainstorm_perspectives")
    async def brainstorm_perspectives_tool(context, *, query: str) -> CallToolResult:
        """Co-STORM 核心，生成多维研究视角"""
        try:
            service = get_scholar_service()
            perspectives = service.brainstorm_perspectives(query)
            
            # 将 ResearchPerspective 转换为 JSON 可序列化的格式
            perspectives_data = [perspective.dict() for perspective in perspectives]
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(perspectives_data, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in brainstorm_perspectives: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("find_critiques")
    async def find_critiques_tool(context, *, paper_id: str) -> CallToolResult:
        """CiTO 逻辑，寻找反驳/质疑类文献"""
        try:
            service = get_scholar_service()
            critiques = service.find_critiques(paper_id)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(critiques, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in find_critiques: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("federated_search")
    async def federated_search_tool(context, *, query: str, max_results: int = 10, filters: Dict[str, Any] = {}) -> CallToolResult:
        """联邦搜索多个学术数据库"""
        try:
            search_query = SearchQuery(query=query, max_results=max_results, filters=filters)
            service = get_scholar_service()
            results = service.federated_search(search_query)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(results, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in federated_search: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    return server

async def main():
    """主函数 - 启动 MCP 服务器"""
    server = create_scholar_server()
    
    # 使用 stdin/stdout 进行通信
    async with server.stdio():
        await server.run_and_wait_shutdown()

if __name__ == "__main__":
    asyncio.run(main())