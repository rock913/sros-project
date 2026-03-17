from __future__ import annotations

from typing import Any, Dict, List


def dispatch_tool(name: str, args: Dict[str, Any]) -> Any:
    """Dispatch an MCP tool call to the corresponding server handler.

    This module is the single place where tool-name → implementation mapping lives.
    The gateway can stay thin by calling this function.
    """

    args = args or {}

    # Slice 3: Dynamic plugins
    if name == "plugins.list":
        from sros.utils.plugin_loader import discover_plugins

        plugins = [
            {
                "name": p.name,
                "display_name": p.display_name or p.name,
                "description": p.description,
                "path": str(p.path),
                "input_schema": p.input_schema,
            }
            for p in discover_plugins()
        ]
        return {"ok": True, "plugins": plugins, "count": len(plugins)}

    if name == "plugins.run":
        from sros.utils.plugin_loader import run_plugin

        plugin = str(args.get("name") or "").strip()
        if not plugin:
            raise ValueError("Missing required arg: name")
        plugin_args = args.get("args") or {}
        if not isinstance(plugin_args, dict):
            raise ValueError("args must be an object")
        value = run_plugin(plugin, dict(plugin_args))
        return {"ok": True, "plugin": plugin, "result": value}

    if name.startswith("plugin."):
        from sros.utils.plugin_loader import run_plugin

        plugin = name.split(".", 1)[1].strip()
        if not plugin:
            raise ValueError("Invalid plugin tool name")
        if not isinstance(args, dict):
            raise ValueError("Plugin arguments must be an object")
        value = run_plugin(plugin, dict(args))
        return {"ok": True, "plugin": plugin, "result": value}

    # Slice 3: Long-running tasks
    if name == "tasks.run_plugin_async":
        from sros.servers.tasks.handler import TasksHandler

        plugin = str(args.get("plugin") or "").strip()
        if not plugin:
            raise ValueError("Missing required arg: plugin")
        plugin_args = args.get("args") or {}
        if not isinstance(plugin_args, dict):
            raise ValueError("args must be an object")
        return TasksHandler().run_plugin_async(plugin=plugin, args=dict(plugin_args))

    if name == "tasks.get":
        from sros.servers.tasks.handler import TasksHandler

        task_id = str(args.get("task_id") or "").strip()
        if not task_id:
            raise ValueError("Missing required arg: task_id")
        return TasksHandler().get_task(task_id)

    if name == "tasks.list":
        from sros.servers.tasks.handler import TasksHandler

        return TasksHandler().list_tasks()

    if name == "tasks.wait":
        from sros.servers.tasks.handler import TasksHandler

        task_id = str(args.get("task_id") or "").strip()
        if not task_id:
            raise ValueError("Missing required arg: task_id")
        timeout_s = float(args.get("timeout_s", 30.0))
        return TasksHandler().wait_task(task_id, timeout_s=timeout_s)

    if name == "manuscript.find_gaps":
        from sros.servers.manuscript.handler import ManuscriptHandler

        return ManuscriptHandler().find_gaps(args.get("file_path", "draft.md"))

    if name == "manuscript.get_outline_tree":
        from sros.servers.manuscript.handler import ManuscriptHandler

        return ManuscriptHandler().get_outline_tree(args.get("file_path", "draft.md"))

    if name == "manuscript.get_file_sha256":
        from sros.servers.manuscript.handler import ManuscriptHandler

        file_path = str(args.get("file_path", "draft.md"))
        sha = ManuscriptHandler().get_file_sha256(file_path)
        return {"file_path": file_path, "sha256": sha}

    if name == "manuscript.index_figure_references":
        from sros.servers.manuscript.handler import ManuscriptHandler

        return ManuscriptHandler().index_figure_references(str(args.get("file_path") or "draft.md"))

    if name == "manuscript.insert_section":
        from sros.servers.manuscript.handler import ManuscriptHandler

        missing = [k for k in ("target", "content", "citations", "file_path") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        return ManuscriptHandler().insert_section(
            target=str(args["target"]),
            content=str(args["content"]),
            citations=list(args.get("citations") or []),
            file_path=str(args.get("file_path") or "draft.md"),
            expected_sha256=args.get("expected_sha256"),
        )

    if name == "manuscript.patch_draft":
        from sros.servers.manuscript.handler import ManuscriptHandler

        missing = [k for k in ("patches", "file_path") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        return ManuscriptHandler().patch_draft(
            patches=list(args.get("patches") or []),
            file_path=str(args.get("file_path") or "draft.md"),
            expected_sha256=args.get("expected_sha256"),
        )

    if name == "scholar.federated_search":
        from sros.domain.schemas import SearchQuery
        from sros.servers.scholar.handler import ScholarHandler

        if "query" not in args:
            raise ValueError("Missing required arg: query")

        q = SearchQuery(
            query=str(args["query"]),
            max_results=int(args.get("max_results", 10)),
            filters=dict(args.get("filters", {}) or {}),
        )
        return ScholarHandler().federated_search(q)

    if name == "scholar.brainstorm_perspectives":
        from sros.servers.scholar.handler import ScholarHandler

        if "query" not in args:
            raise ValueError("Missing required arg: query")
        return ScholarHandler().brainstorm_perspectives(str(args["query"]))

    if name == "scholar.find_critiques":
        from sros.servers.scholar.handler import ScholarHandler

        if "paper_id" not in args:
            raise ValueError("Missing required arg: paper_id")
        return ScholarHandler().find_critiques(str(args["paper_id"]))

    if name == "memory.store_knowledge":
        from sros.domain.schemas import KnowledgeEdge
        from sros.servers.memory.handler import MemoryHandler

        missing = [k for k in ("nodes", "edges") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        nodes = list(args.get("nodes") or [])
        edges_in: List[Any] = list(args.get("edges") or [])
        edges = [KnowledgeEdge(**e) if isinstance(e, dict) else e for e in edges_in]
        ok = MemoryHandler().store_knowledge(nodes=nodes, edges=edges)
        return {"ok": bool(ok)}

    if name == "memory.query_knowledge":
        from sros.servers.memory.handler import MemoryHandler

        if "query" not in args:
            raise ValueError("Missing required arg: query")
        return MemoryHandler().query_knowledge(query=str(args["query"]), limit=int(args.get("limit", 10)))

    if name == "memory.get_citation_map":
        from sros.servers.memory.handler import MemoryHandler

        if "section_id" not in args:
            raise ValueError("Missing required arg: section_id")
        return MemoryHandler().get_citation_map(section_id=str(args["section_id"]))

    raise NotImplementedError(f"Tool not implemented: {name}")
