import asyncio
import json
import sys
from typing import List, Dict, Any
from mcp.server import Server
from mcp.types import CallToolResult, TextContent
from sros.domain.ports import MemoryProtocol
from sros.domain.schemas import KnowledgeEdge

# 延迟导入以满足性能要求
def get_memory_service() -> MemoryProtocol:
    try:
        from sros.servers.memory.handler import MemoryHandler
        return MemoryHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize memory service: {str(e)}") from e

def create_memory_server():
    """创建记忆 MCP 服务器"""
    server = Server("mcp-memory")

    @server.tool("store_knowledge")
    async def store_knowledge_tool(context, *, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> CallToolResult:
        """存储知识节点和关系"""
        try:
            # 将 edges 转换为 KnowledgeEdge 对象
            knowledge_edges = [KnowledgeEdge(**edge) for edge in edges]
            
            service = get_memory_service()
            success = service.store_knowledge(nodes, knowledge_edges)
            
            result = {"success": success, "nodes_count": len(nodes), "edges_count": len(edges)}
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in store_knowledge: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("query_knowledge")
    async def query_knowledge_tool(context, *, query: str, limit: int = 10) -> CallToolResult:
        """查询知识图谱"""
        try:
            service = get_memory_service()
            results = service.query_knowledge(query, limit)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(results, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in query_knowledge: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("get_citation_map")
    async def get_citation_map_tool(context, *, section_id: str) -> CallToolResult:
        """获取特定章节的引用关系图"""
        try:
            service = get_memory_service()
            edges = service.get_citation_map(section_id)
            
            # 将 KnowledgeEdge 转换为 JSON 可序列化的格式
            edges_data = [edge.dict() for edge in edges]
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(edges_data, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in get_citation_map: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    return server

async def main():
    """主函数 - 启动 MCP 服务器"""
    server = create_memory_server()
    
    # 使用 stdin/stdout 进行通信
    async with server.stdio():
        await server.run_and_wait_shutdown()

if __name__ == "__main__":
    asyncio.run(main())