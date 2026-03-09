import asyncio
import json
import sys
from typing import List, Dict, Any
from mcp.server import Server
from mcp.types import CallToolResult, TextContent
from sros.domain.ports import ManuscriptProtocol
from sros.domain.schemas import GapAnalysisResult, OutlineNode

# 延迟导入以满足性能要求
def get_manuscript_service() -> ManuscriptProtocol:
    try:
        from sros.servers.manuscript.handler import ManuscriptHandler
        return ManuscriptHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize manuscript service: {str(e)}") from e

def create_manuscript_server():
    """创建稿件 MCP 服务器"""
    server = Server("mcp-manuscript")

    @server.tool("find_gaps")
    async def find_gaps_tool(context, *, file_path: str) -> CallToolResult:
        """基于规则识别待办项"""
        try:
            service = get_manuscript_service()
            gaps = service.find_gaps(file_path)
            
            # 将 GapAnalysisResult 转换为 JSON 可序列化的格式
            gaps_data = [gap.dict() for gap in gaps]
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(gaps_data, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in find_gaps: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("get_outline_tree")
    async def get_outline_tree_tool(context, *, file_path: str) -> CallToolResult:
        """返回 Markdown/AST 的树状结构"""
        try:
            service = get_manuscript_service()
            outline = service.get_outline_tree(file_path)
            
            outline_data = outline.dict()
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(outline_data, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in get_outline_tree: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("insert_section")
    async def insert_section_tool(context, *, target: str, content: str, citations: List[str]) -> CallToolResult:
        """带引用的增量写入"""
        try:
            service = get_manuscript_service()
            success = service.insert_section(target, content, citations)
            
            result = {"success": success, "target": target, "content_length": len(content)}
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in insert_section: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    @server.tool("patch_draft")
    async def patch_draft_tool(context, *, patches: List[Dict[str, Any]]) -> CallToolResult:
        """批量更新稿件内容"""
        try:
            service = get_manuscript_service()
            success = service.patch_draft(patches)
            
            result = {"success": success, "patches_count": len(patches)}
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )],
                is_error=False
            )
        except Exception as e:
            error_msg = f"Error in patch_draft: {str(e)}"
            return CallToolResult(
                content=[TextContent(type="text", text=error_msg)],
                is_error=True
            )

    return server

async def main():
    """主函数 - 启动 MCP 服务器"""
    server = create_manuscript_server()
    
    # 使用 stdin/stdout 进行通信
    async with server.stdio():
        await server.run_and_wait_shutdown()

if __name__ == "__main__":
    asyncio.run(main())