import asyncio
import json
import sys
from typing import List, Dict, Any
from mcp.server import Server
from mcp.types import CallToolResult, TextContent
from sros.domain.ports import ZoteroProtocol
from sros.domain.schemas import Citation

# 延迟导入以满足性能要求
def get_zotero_service() -> ZoteroProtocol:
    try:
        from sros.servers.zotero.handler import ZoteroHandler
        return ZoteroHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize zotero service: {str(e)}") from e

def create_zotero_server():
    """创建 Zotero MCP 服务器"""
    server = Server("mcp-zotero")

    @server.tool("add_citation")
    async def add_citation_tool(context, *, citekey: str, title: str, authors: List[str], year: int, journal: str, url: str, bibtex: str) -> CallToolResult:
        """添加引用到数据库"""
        try:
            citation = Citation(
                citekey=citekey,
                title=title,
                authors=authors,
                year=year,
                journal=journal,
                url=url,
                bibtex=bibtex
            )
            
            service = get_zotero_service()
            success = service.add_citation(citation)
            
            result = {"success": success, "citekey": citekey}
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in add_citation: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("get_citation")
    async def get_citation_tool(context, *, citekey: str) -> CallToolResult:
        """根据 citekey 获取引用信息"""
        try:
            service = get_zotero_service()
            citation = service.get_citation(citekey)
            
            citation_data = citation.dict()
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(citation_data, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in get_citation: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("search_citations")
    async def search_citations_tool(context, *, query: str) -> CallToolResult:
        """搜索引用"""
        try:
            service = get_zotero_service()
            citations = service.search_citations(query)
            
            # 将 Citation 转换为 JSON 可序列化的格式
            citations_data = [citation.dict() for citation in citations]
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(citations_data, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in search_citations: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    return server

async def main():
    """主函数 - 启动 MCP 服务器"""
    server = create_zotero_server()
    
    # 使用 stdin/stdout 进行通信
    async with server.stdio():
        await server.run_and_wait_shutdown()

if __name__ == "__main__":
    asyncio.run(main())