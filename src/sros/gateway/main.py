#!/usr/bin/env python3
"""
MCP SSE Hub Gateway - MCP Aggregation Server
Implements Playbook A: Gateway as MCP SSE Hub
"""

import asyncio
import json
import logging
import sys
import time
from typing import Dict, Any, Callable, Optional, List
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn

from sros.gateway.config import GatewayConfig
from sros.domain.ports import ManuscriptProtocol, ScholarProtocol, MemoryProtocol, ZoteroProtocol

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 延迟导入以满足性能要求
def get_manuscript_service() -> ManuscriptProtocol:
    """获取稿件服务实例"""
    try:
        from sros.servers.manuscript.handler import ManuscriptHandler
        return ManuscriptHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize manuscript service: {str(e)}") from e

def get_scholar_service() -> ScholarProtocol:
    """获取学者服务实例"""
    try:
        from sros.servers.scholar.handler import ScholarHandler
        return ScholarHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize scholar service: {str(e)}") from e

def get_memory_service() -> MemoryProtocol:
    """获取记忆服务实例"""
    try:
        from sros.servers.memory.handler import MemoryHandler
        return MemoryHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize memory service: {str(e)}") from e

def get_zotero_service() -> ZoteroProtocol:
    """获取 Zotero 服务实例"""
    try:
        from sros.servers.zotero.handler import ZoteroHandler
        return ZoteroHandler()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize zotero service: {str(e)}") from e

class SROSGateway:
    """SROS Gateway 主类 - MCP SSE Hub Implementation"""
    
    def __init__(self, config: GatewayConfig = None):
        try:
            self.config = config or GatewayConfig()
            self.app = FastAPI(title="SROS Gateway")
            self.running = False
            
            # Build registry with error handling
            self.manuscript = get_manuscript_service()
            self.scholar = get_scholar_service()
            self.memory = get_memory_service()
            
            # Zotero might fail due to database schema issues, make it optional
            try:
                self.zotero = get_zotero_service()
                zotero_available = True
            except Exception as e:
                logger.warning(f"Zotero service failed to initialize: {e}")
                self.zotero = None
                zotero_available = False
            
            self.TOOLS: Dict[str, Callable] = {
                "manuscript.find_gaps": self.manuscript.find_gaps,
                "manuscript.get_outline_tree": self.manuscript.get_outline_tree,
                "manuscript.insert_section": self.manuscript.insert_section,
                "manuscript.patch_draft": self.manuscript.patch_draft,
                "scholar.brainstorm_perspectives": self.scholar.brainstorm_perspectives,
                "memory.store_knowledge": self.memory.store_knowledge,
                "memory.query_knowledge": self.memory.query_knowledge,
            }
            
            # Add zotero tools only if zotero is available
            if zotero_available and self.zotero:
                self.TOOLS["zotero.add_citation"] = self.zotero.add_citation
                self.TOOLS["zotero.search_citations"] = self.zotero.search_citations
            
            self._setup_routes()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize SROS Gateway: {str(e)}") from e
        
    def mcp_list_tools(self):
        """Return MCP tool definitions with precise inputSchema"""
        tools = []
        
        # Define precise schemas for each tool
        tool_schemas = {
            "manuscript.find_gaps": {
                "name": "manuscript.find_gaps",
                "description": "Analyze a manuscript file to identify gaps, missing sections, and TODO items",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Workspace-relative path to the manuscript file (default: draft.md)",
                            "default": "draft.md"
                        }
                    },
                    "required": ["file_path"],
                    "additionalProperties": False
                }
            },
            "manuscript.get_outline_tree": {
                "name": "manuscript.get_outline_tree",
                "description": "Parse a manuscript file and return its outline structure as a tree",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Workspace-relative path to the manuscript file (default: draft.md)",
                            "default": "draft.md"
                        }
                    },
                    "required": ["file_path"],
                    "additionalProperties": False
                }
            },
            "manuscript.insert_section": {
                "name": "manuscript.insert_section",
                "description": "Insert a new section into a manuscript file with optional citations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": "Target location for insertion"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to insert"
                        },
                        "citations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of citation keys to add"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Workspace-relative path to the manuscript file (default: draft.md)",
                            "default": "draft.md"
                        }
                    },
                    "required": ["target", "content", "citations", "file_path"],
                    "additionalProperties": False
                }
            },
            "manuscript.patch_draft": {
                "name": "manuscript.patch_draft",
                "description": "Apply patches to a manuscript file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "patches": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["append", "prepend"]},
                                    "content": {"type": "string"}
                                },
                                "required": ["action", "content"]
                            },
                            "description": "List of patches to apply"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Workspace-relative path to the manuscript file (default: draft.md)",
                            "default": "draft.md"
                        }
                    },
                    "required": ["patches", "file_path"],
                    "additionalProperties": False
                }
            },
            "scholar.brainstorm_perspectives": {
                "name": "scholar.brainstorm_perspectives",
                "description": "Generate different academic perspectives on a topic",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            },
            "memory.store_knowledge": {
                "name": "memory.store_knowledge",
                "description": "Store knowledge in the memory system",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Knowledge content to store"},
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Tags for categorization"
                        }
                    },
                    "required": ["content"],
                    "additionalProperties": False
                }
            },
            "memory.query_knowledge": {
                "name": "memory.query_knowledge",
                "description": "Query stored knowledge from the memory system",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Query to search for"}
                    },
                    "required": ["query"],
                    "additionalProperties": False
                }
            }
        }
        
        # Add zotero tools if available
        if hasattr(self, 'zotero') and self.zotero:
            tool_schemas.update({
                "zotero.add_citation": {
                    "name": "zotero.add_citation",
                    "description": "Add a citation to the Zotero library",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "citation_data": {
                                "type": "object",
                                "description": "Citation data to add"
                            }
                        },
                        "required": ["citation_data"],
                        "additionalProperties": False
                    }
                },
                "zotero.search_citations": {
                    "name": "zotero.search_citations",
                    "description": "Search for citations in the Zotero library",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"}
                        },
                        "required": ["query"],
                        "additionalProperties": False
                    }
                }
            })
        
        # Filter to only include tools that actually exist
        for tool_name, schema in tool_schemas.items():
            if tool_name in self.TOOLS:
                tools.append(schema)
        
        return {"tools": tools}
    
    def _setup_routes(self):
        """设置路由"""
        try:
            @self.app.get("/")
            async def root():
                return {"message": "SROS Gateway MCP SSE Hub is running"}
                
            @self.app.get("/health")
            async def health():
                return {"status": "healthy", "timestamp": time.time()}

            @self.app.get("/tools")
            async def list_tools():
                """列出所有可用的 MCP 工具 - 保持向后兼容"""
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
                    ] if hasattr(self, 'zotero') and self.zotero else []
                }
                return tools

            @self.app.get(self.config.sse_endpoint)
            async def sse_stream(request: Request):
                """SSE 流端点 - 用于 MCP 通信"""
                async def event_generator():
                    # Send initial connection event
                    yield f"data: {json.dumps({'event': 'connected', 'timestamp': time.time()})}\n\n"
                    
                    # Send endpoint discovery
                    yield f"data: {json.dumps({'event': 'endpoint_discovery', 'endpoints': ['/sse']})}\n\n"
                    
                    # Send heartbeat periodically
                    while True:
                        try:
                            # Check if client disconnected
                            if await request.is_disconnected():
                                break
                            
                            # Send heartbeat
                            yield f"data: {json.dumps({'event': 'heartbeat', 'timestamp': time.time()})}\n\n"
                            
                            # Sleep for 30 seconds between heartbeats
                            await asyncio.sleep(30)
                        except Exception as e:
                            logger.error(f"SSE stream error: {e}")
                            break
                
                return StreamingResponse(event_generator(), media_type="text/event-stream")

            @self.app.post(self.config.sse_endpoint)
            async def handle_jsonrpc(request: Request):
                """Handle JSON-RPC requests over HTTP POST"""
                try:
                    body = await request.json()
                    response = self.dispatch_jsonrpc(body)
                    return response
                except Exception as e:
                    logger.error(f"Error handling JSON-RPC request: {e}")
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        },
                        "id": None
                    }
        except Exception as e:
            raise RuntimeError(f"Failed to setup routes: {str(e)}") from e
    
    def dispatch_jsonrpc(self, request: Dict[str, Any]):
        """Dispatch JSON-RPC request to appropriate handler"""
        try:
            # Validate basic JSON-RPC structure
            if not isinstance(request, dict):
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request: Request must be a JSON object"
                    },
                    "id": None
                }
            
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})
            
            if not method:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request: Missing method"
                    },
                    "id": request_id
                }
            
            if method == "initialize":
                # Return capabilities
                result = {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "SROS Gateway",
                        "version": "2.3.2"
                    },
                    "capabilities": {
                        "methods": ["initialize", "tools/list", "tools/call"]
                    }
                }
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                }
            
            elif method == "tools/list":
                # Return tool list
                result = self.mcp_list_tools()
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                }
            
            elif method == "tools/call":
                # Extract tool name and arguments from params
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if not tool_name:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32602,
                            "message": "Missing tool name in parameters"
                        },
                        "id": request_id
                    }
                
                if tool_name not in self.TOOLS:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Tool '{tool_name}' not found. Available tools: {list(self.TOOLS.keys())}"
                        },
                        "id": request_id
                    }
                
                # Validate file_path parameter for manuscript tools if provided
                if tool_name in ["manuscript.find_gaps", "manuscript.get_outline_tree", "manuscript.insert_section", "manuscript.patch_draft"]:
                    if "file_path" in arguments:
                        file_path = arguments["file_path"]
                        if isinstance(file_path, str):
                            # Check for absolute paths or path traversal
                            if file_path.startswith("/") or ".." in file_path.split("/"):
                                return {
                                    "jsonrpc": "2.0",
                                    "error": {
                                        "code": -32602,
                                        "message": f"Invalid file_path for tool '{tool_name}': path must be workspace-relative (no absolute paths or '..'). Example: 'draft.md' or 'notes/draft.md'"
                                    },
                                    "id": request_id
                                }
                
                # Call the tool
                try:
                    tool_func = self.TOOLS[tool_name]
                    
                    # Validate required arguments for specific tools
                    if tool_name == "manuscript.insert_section":
                        required_args = ["target", "content", "citations", "file_path"]
                        missing_args = [arg for arg in required_args if arg not in arguments]
                        if missing_args:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required arguments for tool '{tool_name}': {missing_args}. Example params: {{'target': 'section1', 'content': 'new content', 'citations': ['cite1'], 'file_path': 'draft.md'}}"
                                },
                                "id": request_id
                            }
                    elif tool_name == "manuscript.patch_draft":
                        required_args = ["patches", "file_path"]
                        missing_args = [arg for arg in required_args if arg not in arguments]
                        if missing_args:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required arguments for tool '{tool_name}': {missing_args}. Example params: {{'patches': [{{'action': 'append', 'content': 'new content'}}], 'file_path': 'draft.md'}}"
                                },
                                "id": request_id
                            }
                    elif tool_name == "memory.store_knowledge":
                        if "content" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'content' for tool '{tool_name}'. Example params: {{'content': 'knowledge content', 'tags': ['tag1', 'tag2']}}"
                                },
                                "id": request_id
                            }
                    elif tool_name == "memory.query_knowledge":
                        if "query" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'query' for tool '{tool_name}'. Example params: {{'query': 'search query'}}"
                                },
                                "id": request_id
                            }
                    
                    # Call the function with arguments
                    result = tool_func(**arguments) if arguments else tool_func()
                    
                    # Format result as MCP content
                    formatted_result = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, default=str) if not isinstance(result, str) else result
                            }
                        ]
                    }
                    
                    return {
                        "jsonrpc": "2.0",
                        "result": formatted_result,
                        "id": request_id
                    }
                except TypeError as e:
                    # Handle argument-related errors
                    if "missing" in str(e) or "required" in str(e):
                        return {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32602,
                                "message": f"Missing required arguments for tool '{tool_name}': {str(e)}. Please check the tool's inputSchema for required parameters."
                            },
                            "id": request_id
                        }
                    else:
                        error_msg = f"Error calling tool '{tool_name}': {str(e)}. Please check parameters and try again."
                        logger.error(f"Tool call error: {error_msg}")
                        return {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32603,
                                "message": error_msg
                            },
                            "id": request_id
                        }
                except Exception as e:
                    error_msg = f"Error calling tool '{tool_name}': {str(e)}. Please check parameters and try again."
                    logger.error(f"Tool call error: {error_msg}")
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": error_msg
                        },
                        "id": request_id
                    }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not supported. Available methods: initialize, tools/list, tools/call"
                    },
                    "id": request_id
                }
                
        except Exception as e:
            logger.error(f"Error dispatching JSON-RPC request: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error processing request: {str(e)}. Please check the request format and try again."
                },
                "id": request.get("id")
            }
    
    async def start(self):
        """启动网关服务"""
        try:
            self.running = True
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
        except Exception as e:
            raise RuntimeError(f"Failed to start gateway server: {str(e)}") from e

async def main(config: GatewayConfig = None):
    """主函数"""
    try:
        gateway = SROSGateway(config)
        await gateway.start()
    except Exception as e:
        print(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
