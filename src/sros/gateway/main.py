import asyncio
import uvicorn
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from sros.gateway.config import GatewayConfig
from sros.gateway.sse_handler import SSEHandler
from sros.domain.ports.manuscript_protocol import ManuscriptProtocol
from sros.domain.ports.scholar_protocol import ScholarProtocol
from sros.domain.ports.memory_protocol import MemoryProtocol
from sros.domain.ports.zotero_protocol import ZoteroProtocol

# 延迟导入以满足性能要求
def get_manuscript_service() -> ManuscriptProtocol:
    """获取稿件服务实例"""
    from sros.servers.manuscript.handler import ManuscriptHandler
    return ManuscriptHandler()

def get_scholar_service() -> ScholarProtocol:
    """获取学者服务实例"""
    from sros.servers.scholar.handler import ScholarHandler
    return ScholarHandler()

def get_memory_service() -> MemoryProtocol:
    """获取记忆服务实例"""
    from sros.servers.memory.handler import MemoryHandler
    return MemoryHandler()

def get_zotero_service() -> ZoteroProtocol:
    """获取 Zotero 服务实例"""
    from sros.servers.zotero.handler import ZoteroHandler
    return ZoteroHandler()

class SROSGateway:
    """SROS Gateway 主类"""
    
    def __init__(self):
        self.config = GatewayConfig()
        self.app = FastAPI(title="SROS Gateway")
        self.sse_handler = SSEHandler(self.config)
        self._setup_routes()
        
    def _setup_routes(self):
        """设置路由"""
        @self.app.get("/")
        async def root():
            return {"message": "SROS Gateway is running"}
            
        @self.app.get("/health")
        async def health():
            # Keep health info fresh even without a background loop.
            self.sse_handler.update_health("gateway", "healthy")
            return self.sse_handler.get_health_info()

        @self.app.get("/sse")
        async def sse_stream(once: bool = False):
            """Server-Sent Events (SSE) endpoint."""

            async def event_generator():
                # Send an immediate event so clients can validate the stream.
                yield "event: ready\ndata: {}\n\n"

                # One-shot mode is intended for tests/smoke checks.
                if once:
                    return

                # Periodically push health updates.
                while True:
                    self.sse_handler.update_health("gateway", "healthy")
                    health_json = json.dumps(self.sse_handler.get_health_info())
                    yield f"event: health\ndata: {health_json}\n\n"
                    await asyncio.sleep(5)

            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache"},
            )
                
        @self.app.get("/tools")
        async def list_tools():
            """列出所有可用的 MCP 工具"""
            tools = {
                "manuscript": [
                    "find_gaps",
                    "get_outline_tree", 
                    "insert_section",
                    "patch_draft"
                ],
                "scholar": [
                    "brainstorm_perspectives",
                    "find_critiques",
                    "federated_search"
                ],
                "memory": [
                    "store_knowledge",
                    "query_knowledge",
                    "get_citation_map"
                ],
                "zotero": [
                    "add_citation",
                    "get_citation",
                    "search_citations"
                ]
            }
            return tools
    
    async def start(self):
        """启动网关服务"""
        # 启动 FastAPI 应用
        config = uvicorn.Config(
            self.app,
            host=self.config.host,
            port=self.config.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        print("SYSTEM READY")
        await server.serve()

# 创建全局实例
gateway_instance = SROSGateway()

async def main():
    """主函数"""
    await gateway_instance.start()

if __name__ == "__main__":
    asyncio.run(main())