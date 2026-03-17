#!/usr/bin/env python3
"""
MCP SSE Hub Gateway - MCP Aggregation Server
Implements Playbook A: Gateway as MCP SSE Hub
"""

import asyncio
import json
import logging
import os
import queue
import sys
import time
import uuid
from typing import Dict, Any, Callable, Optional, List
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn

from sros.gateway.config import GatewayConfig
from sros.gateway.skill_reflector import SkillReflector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

STATIC_TOOLS = {
    # Manuscript
    "manuscript.find_gaps",
    "manuscript.get_outline_tree",
    "manuscript.get_file_sha256",
    "manuscript.index_figure_references",
    "manuscript.insert_section",
    "manuscript.patch_draft",
    # Scholar
    "scholar.brainstorm_perspectives",
    "scholar.find_critiques",
    "scholar.federated_search",
    # Memory
    "memory.store_knowledge",
    "memory.query_knowledge",
    "memory.get_citation_map",
}

class SROSGateway:
    """SROS Gateway 主类 - MCP SSE Hub Implementation"""
    
    def __init__(self, config: GatewayConfig = None):
        try:
            self.config = config or GatewayConfig()
            self.app = FastAPI(title="SROS Gateway")
            self.running = False

            # SSE transport session queues (session_id -> asyncio.Queue[str])
            self._sse_sessions: Dict[str, asyncio.Queue[str]] = {}
            self._sse_sessions_lock = asyncio.Lock()
            
            # V3: gateway is a thin reflector; dispatch happens in `sros.skills`.
            self.zotero = None
            self._reflector = SkillReflector()

            # Bridge notifications from threaded tasks into the asyncio world.
            self._thread_notifications: queue.Queue[str] = queue.Queue()

            try:
                from sros.utils.task_manager import get_task_manager

                get_task_manager().set_notifier(self._enqueue_task_event)
            except Exception as e:
                logger.warning(f"Failed to wire task notifier: {e}")

            def _make_tool(tool_name: str):
                def _call(**kwargs):
                    return self._reflector.call(tool_name, kwargs).value

                return _call

            self._make_tool = _make_tool
            self.TOOLS: Dict[str, Callable[..., Any]] = {}
            self._refresh_tools()
            
            self._setup_routes()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize SROS Gateway: {str(e)}") from e

    def _enqueue_task_event(self, payload: Dict[str, Any]) -> None:
        """Receive task events from the task manager (may be called from threads)."""
        notification = {
            "jsonrpc": "2.0",
            "method": "sros.task.completed",
            "params": payload,
        }
        self._thread_notifications.put(json.dumps(notification, default=str))

    def _refresh_tools(self) -> None:
        """Rebuild tool registry (static + dynamic plugins + tasks)."""
        tools: Dict[str, Callable[..., Any]] = {}

        # Core static tools
        for name in sorted(STATIC_TOOLS):
            tools[name] = self._make_tool(name)

        # Slice 3 tools
        for name in [
            "plugins.list",
            "plugins.run",
            "tasks.run_plugin_async",
            "tasks.get",
            "tasks.list",
            "tasks.wait",
        ]:
            tools[name] = self._make_tool(name)

        # Dynamic per-plugin tools: plugin.<id>
        try:
            from sros.utils.plugin_loader import discover_plugins

            for p in discover_plugins():
                tools[f"plugin.{p.name}"] = self._make_tool(f"plugin.{p.name}")
        except Exception:
            # If workspace is not set, simply omit plugin tools.
            pass

        self.TOOLS = tools

    async def _broadcast_to_sessions(self, payload: str) -> None:
        async with self._sse_sessions_lock:
            queues = list(self._sse_sessions.values())
        for q in queues:
            try:
                await q.put(payload)
            except Exception:
                continue

    async def _pump_notifications(self) -> None:
        """Async pump to broadcast thread-emitted notifications to SSE sessions."""
        while True:
            drained = 0
            while True:
                try:
                    payload = self._thread_notifications.get_nowait()
                except queue.Empty:
                    break
                drained += 1
                await self._broadcast_to_sessions(payload)
            # Sleep briefly when idle
            await asyncio.sleep(0.05 if drained == 0 else 0)
        
    def mcp_list_tools(self):
        """Return MCP tool definitions with precise inputSchema"""
        self._refresh_tools()
        tools = []
        
        # Define precise schemas for each tool
        tool_schemas: Dict[str, Dict[str, Any]] = {
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
            "manuscript.index_figure_references": {
                "name": "manuscript.index_figure_references",
                "description": "Scan a draft markdown file and index figure references into the DuckDB knowledge graph",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Workspace-relative path to the draft markdown file (default: draft.md)",
                            "default": "draft.md",
                        }
                    },
                    "required": ["file_path"],
                    "additionalProperties": False,
                },
            },
            "manuscript.insert_section": {
                "name": "manuscript.insert_section",
                "description": "Insert a new section into a manuscript file with optional citations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": "Target location for insertion (append/end/anchor:<hash>/heading:<Title>/heading-<line_no>/line:<n>)"
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
                        },
                        "expected_sha256": {
                            "type": "string",
                            "description": "Optional optimistic concurrency guard. If provided and does not match current file sha256, the call returns ok=false with a Version mismatch error."
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
                        },
                        "expected_sha256": {
                            "type": "string",
                            "description": "Optional optimistic concurrency guard. If provided and does not match current file sha256, the call returns ok=false with a Version mismatch error."
                        }
                    },
                    "required": ["patches", "file_path"],
                    "additionalProperties": False
                }
            },
            "manuscript.get_file_sha256": {
                "name": "manuscript.get_file_sha256",
                "description": "Compute sha256 of a manuscript file (empty file if missing)",
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
            "scholar.brainstorm_perspectives": {
                "name": "scholar.brainstorm_perspectives",
                "description": "Generate different academic perspectives on a topic",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Research topic or question to generate perspectives for",
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                }
            },
            "scholar.find_critiques": {
                "name": "scholar.find_critiques",
                "description": "Find critiques / counter-arguments for a paper (CiTO-inspired)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "paper_id": {
                            "type": "string",
                            "description": "Paper identifier (DOI, internal id, etc)",
                        }
                    },
                    "required": ["paper_id"],
                    "additionalProperties": False,
                },
            },
            "scholar.federated_search": {
                "name": "scholar.federated_search",
                "description": "Federated search across academic sources",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "description": "Maximum results to return", "default": 10},
                        "filters": {"type": "object", "description": "Optional filters", "default": {}},
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
            "memory.store_knowledge": {
                "name": "memory.store_knowledge",
                "description": "Store knowledge in the memory system",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "nodes": {
                            "type": "array",
                            "description": "Knowledge nodes to store (free-form objects; must include at least an id)",
                            "items": {"type": "object"},
                        },
                        "edges": {
                            "type": "array",
                            "description": "Knowledge edges to store",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "source": {"type": "string"},
                                    "target": {"type": "string"},
                                    "relationship": {"type": "string"},
                                    "confidence": {"type": "number"},
                                },
                                "required": ["source", "target", "relationship", "confidence"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["nodes", "edges"],
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
            ,
            "memory.get_citation_map": {
                "name": "memory.get_citation_map",
                "description": "Get citation edges for a draft section (DraftSection → CITES → Paper)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "section_id": {
                            "type": "string",
                            "description": "Section node id, e.g. 'draft_section:draft.md#heading-12'",
                        }
                    },
                    "required": ["section_id"],
                    "additionalProperties": False,
                },
            }
        }

        # Slice 3: task tools
        tool_schemas.update(
            {
                "plugins.list": {
                    "name": "plugins.list",
                    "description": "List workspace plugins under .sros/plugins (static metadata; no code execution)",
                    "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                },
                "plugins.run": {
                    "name": "plugins.run",
                    "description": "Run a workspace plugin by filename stem (executes plugin code)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Plugin id (filename stem)"},
                            "args": {"type": "object", "description": "Arguments passed to plugin run(args)", "default": {}},
                        },
                        "required": ["name"],
                        "additionalProperties": False,
                    },
                },
                "tasks.run_plugin_async": {
                    "name": "tasks.run_plugin_async",
                    "description": "Run a plugin as a long-running background task; completion emits SSE JSON-RPC notification sros.task.completed",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "plugin": {"type": "string", "description": "Plugin id (filename stem)"},
                            "args": {"type": "object", "description": "Arguments passed to plugin run(args)", "default": {}},
                        },
                        "required": ["plugin"],
                        "additionalProperties": False,
                    },
                },
                "tasks.get": {
                    "name": "tasks.get",
                    "description": "Get task status/result by task_id",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"task_id": {"type": "string"}},
                        "required": ["task_id"],
                        "additionalProperties": False,
                    },
                },
                "tasks.list": {
                    "name": "tasks.list",
                    "description": "List known tasks in this gateway process",
                    "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                },
                "tasks.wait": {
                    "name": "tasks.wait",
                    "description": "Wait (poll) until a task completes or timeout",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "timeout_s": {"type": "number", "default": 30.0},
                        },
                        "required": ["task_id"],
                        "additionalProperties": False,
                    },
                },
            }
        )

        # Slice 3: dynamic per-plugin tools
        try:
            from sros.utils.plugin_loader import discover_plugins

            for p in discover_plugins():
                tool_name = f"plugin.{p.name}"
                schema = p.input_schema if isinstance(p.input_schema, dict) else None
                tool_schemas[tool_name] = {
                    "name": tool_name,
                    "description": (p.description or f"Workspace plugin: {p.display_name or p.name}").strip(),
                    "inputSchema": schema
                    if schema
                    else {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": True,
                    },
                }
        except Exception:
            pass
        
        # Filter to only include tools that actually exist
        for tool_name, schema in tool_schemas.items():
            if tool_name in self.TOOLS:
                tools.append(schema)
        
        return {"tools": tools}
    
    def _setup_routes(self):
        """设置路由"""
        try:
            @self.app.on_event("startup")
            async def _startup():
                asyncio.create_task(self._pump_notifications())

                # V3 enhancement: persist gateway pid/port for workspace-level governance.
                try:
                    if self.config and self.config.workspace_dir:
                        from sros.utils.gateway_process import write_pid_file

                        write_pid_file(self.config.workspace_dir, os.getpid(), int(self.config.port))
                except Exception:
                    # Never block gateway startup on pid persistence.
                    pass

            @self.app.on_event("shutdown")
            async def _shutdown():
                try:
                    if self.config and self.config.workspace_dir:
                        from sros.utils.gateway_process import remove_pid_file

                        remove_pid_file(self.config.workspace_dir)
                except Exception:
                    # Never block shutdown on pid cleanup.
                    pass

            @self.app.get("/")
            async def root():
                return {"message": "SROS Gateway MCP SSE Hub is running"}
                
            @self.app.get("/health")
            async def health():
                return {"status": "healthy", "timestamp": time.time()}

            @self.app.get("/tools")
            async def list_tools():
                """列出所有可用的 MCP 工具 - 保持向后兼容"""
                self._refresh_tools()
                tools = {
                    "manuscript": [
                        "find_gaps",
                        "get_outline_tree", 
                        "index_figure_references",
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
                    "plugins": [p.split(".", 1)[1] for p in sorted(self.TOOLS) if p.startswith("plugin.")],
                    "tasks": [
                        "run_plugin_async",
                        "get",
                        "list",
                        "wait",
                    ],
                }
                return tools

            @self.app.get(self.config.sse_endpoint)
            async def sse_stream(request: Request):
                """SSE 流端点 - 用于 MCP 通信"""
                async def event_generator():
                    once = str(request.query_params.get("once", "")).lower() in {"1", "true", "yes"}

                    session_id = uuid.uuid4().hex
                    queue: asyncio.Queue[str] = asyncio.Queue()
                    async with self._sse_sessions_lock:
                        self._sse_sessions[session_id] = queue

                    try:
                        # MCP reference SSE transport expects an `endpoint` event first.
                        # The Python `mcp.client.sse.sse_client` will POST JSON-RPC messages
                        # to this endpoint URL after connecting.
                        yield f"event: endpoint\ndata: /messages?session_id={session_id}\n\n"

                        if once:
                            # One-shot mode: emit a keep-alive message and close.
                            yield "event: message\ndata:\n\n"
                            return

                        # Stream responses as JSON-RPC messages, keep-alive when idle.
                        while True:
                            if await request.is_disconnected():
                                break
                            try:
                                payload = await asyncio.wait_for(queue.get(), timeout=30)
                                yield f"event: message\ndata: {payload}\n\n"
                            except asyncio.TimeoutError:
                                # Empty message acts as keep-alive; the MCP client ignores it.
                                yield "event: message\ndata:\n\n"
                            except Exception as e:
                                logger.error(f"SSE stream error: {e}")
                                break
                    finally:
                        async with self._sse_sessions_lock:
                            self._sse_sessions.pop(session_id, None)
                
                return StreamingResponse(
                    event_generator(),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Access-Control-Allow-Origin": "*",
                    },
                )


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

            @self.app.post("/messages")
            async def handle_messages(request: Request):
                """Handle MCP JSON-RPC messages.

                Roo Code (and the reference MCP SSE transport) commonly POST JSON-RPC messages
                to /messages while using /sse for the event-stream.
                """
                session_id = request.query_params.get("session_id")
                if not session_id:
                    # Backward compatible: allow simple request/response over HTTP
                    return await handle_jsonrpc(request)

                async with self._sse_sessions_lock:
                    queue = self._sse_sessions.get(session_id)

                if queue is None:
                    return {
                        "jsonrpc": "2.0",
                        "error": {"code": -32000, "message": "Unknown or expired SSE session"},
                        "id": None,
                    }

                body = await request.json()
                response = self.dispatch_jsonrpc(body)

                # JSON-RPC notifications (no id) don't get a response.
                if isinstance(body, dict) and body.get("id") is None:
                    return {"ok": True}

                await queue.put(json.dumps(response))
                return {"ok": True}
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
                try:
                    from sros import __version__ as sros_version
                except Exception:
                    sros_version = "unknown"
                # Return capabilities
                result = {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "SROS Gateway",
                        "version": sros_version
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
                
                self._refresh_tools()
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
                if tool_name in [
                    "manuscript.find_gaps",
                    "manuscript.get_outline_tree",
                    "manuscript.get_file_sha256",
                    "manuscript.index_figure_references",
                    "manuscript.insert_section",
                    "manuscript.patch_draft",
                ]:
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
                    elif tool_name == "manuscript.get_file_sha256":
                        if "file_path" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'file_path' for tool '{tool_name}'. Example params: {{'file_path': 'draft.md'}}"
                                },
                                "id": request_id
                            }
                    elif tool_name == "scholar.brainstorm_perspectives":
                        if "query" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'query' for tool '{tool_name}'. Example params: {{'query': 'your research topic'}}"
                                },
                                "id": request_id
                            }

                    elif tool_name == "scholar.find_critiques":
                        if "paper_id" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'paper_id' for tool '{tool_name}'. Example params: {{'paper_id': '10.1000/xyz123'}}",
                                },
                                "id": request_id,
                            }

                    elif tool_name == "scholar.federated_search":
                        if "query" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'query' for tool '{tool_name}'. Example params: {{'query': 'transformer attention', 'max_results': 10, 'filters': {{}}}}",
                                },
                                "id": request_id,
                            }

                    elif tool_name == "memory.store_knowledge":
                        missing = [k for k in ("nodes", "edges") if k not in arguments]
                        if missing:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required arguments for tool '{tool_name}': {missing}. Example params: nodes=[{{'id':'n1','type':'note','title':'...'}}], edges=[{{'source':'n1','target':'n2','relationship':'RELATED_TO','confidence':0.8}}]"
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

                    elif tool_name == "memory.get_citation_map":
                        if "section_id" not in arguments:
                            return {
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": f"Missing required argument 'section_id' for tool '{tool_name}'. Example params: {{'section_id': 'draft_section:draft.md#heading-12'}}",
                                },
                                "id": request_id,
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


def create_app():
    """Uvicorn app factory.

    This enables `uvicorn ... --factory --reload` while keeping our existing
    config mechanism based on environment variables (`SROS_WORKSPACE_DIR`, etc.).
    """
    config = GatewayConfig()
    return SROSGateway(config).app

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
