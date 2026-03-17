from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table


app = typer.Typer(add_completion=False, help="SROS skill-first CLI (V3).")
console = Console()


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump") and callable(getattr(value, "model_dump")):
        return value.model_dump()
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    return value


def _emit(value: Any, raw: bool) -> None:
    if raw:
        typer.echo(json.dumps(_to_jsonable(value), ensure_ascii=False))
        return

    # Minimal human-friendly output (avoid huge prints)
    if isinstance(value, list) and value and isinstance(_to_jsonable(value[0]), dict):
        rows = [_to_jsonable(v) for v in value]
        table = Table(show_header=True, header_style="bold")
        keys = list(rows[0].keys())
        for k in keys:
            table.add_column(str(k))
        for r in rows:
            table.add_row(*[str(r.get(k, "")) for k in keys])
        console.print(table)
    else:
        console.print(_to_jsonable(value))


def _read_json_args(args_json: Optional[str]) -> Dict[str, Any]:
    if args_json is not None:
        return json.loads(args_json) if args_json.strip() else {}

    # If invoked via gateway reflection, args come from stdin.
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}

    return {}


def _raw_fail(message: str, *, details: Optional[Dict[str, Any]] = None) -> None:
    payload: Dict[str, Any] = {"ok": False, "error": message}
    if details:
        payload.update(details)
    typer.echo(json.dumps(payload, ensure_ascii=False))
    raise typer.Exit(code=1)


def _fail(message: str, *, raw: bool, details: Optional[Dict[str, Any]] = None) -> None:
    if raw:
        _raw_fail(message, details=details)
    if details:
        console.print({"ok": False, "error": message, **details})
    else:
        console.print({"ok": False, "error": message})
    raise typer.Exit(code=1)


@app.callback()
def _global(
    ctx: typer.Context,
    raw: bool = typer.Option(False, "--raw", help="Output pure JSON to stdout"),
):
    ctx.ensure_object(dict)
    ctx.obj["raw"] = raw


manuscript_app = typer.Typer(add_completion=False, help="Manuscript skills")
app.add_typer(manuscript_app, name="manuscript")


@manuscript_app.command("find-gaps")
def manuscript_find_gaps(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().find_gaps(file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.find-gaps"})
    _emit(res, raw=raw)


@manuscript_app.command("outline")
def manuscript_outline(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().get_outline_tree(file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.outline"})
    _emit(res, raw=raw)


@manuscript_app.command("get-outline-tree")
def manuscript_get_outline_tree_compat(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    """Compatibility alias for older prompts (use `outline`)."""
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().get_outline_tree(file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.get-outline-tree"})
    _emit(res, raw=raw)


@manuscript_app.command("sha256")
def manuscript_sha256(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().get_file_sha256(file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.sha256"})
    _emit({"file_path": file_path, "sha256": res}, raw=raw)


@manuscript_app.command("get-file-sha256")
def manuscript_get_file_sha256_compat(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    """Compatibility alias for older prompts (use `sha256`)."""
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().get_file_sha256(file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.get-file-sha256"})
    _emit({"file_path": file_path, "sha256": res}, raw=raw)


@manuscript_app.command("index-figures")
def manuscript_index_figures(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().index_figure_references(file_path=file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.index-figures"})
    _emit(res, raw=raw)
    if isinstance(res, dict) and res.get("ok") is False:
        raise typer.Exit(code=1)


@manuscript_app.command("insert")
def manuscript_insert(
    ctx: typer.Context,
    target: str = typer.Option(
        ..., "--target", help="append/end/section:end/anchor:<hash>/heading:<Title>/heading-<n>/line:<n>"
    ),
    content: str = typer.Option(..., "--content", help="Markdown content to insert"),
    position: Optional[str] = typer.Option(
        None,
        "--position",
        help="DEPRECATED (compat): accepted for older prompts; ignored (insertion is controlled by --target)",
    ),
    citations: List[str] = typer.Option([], "--cite", help="Citation keys (repeatable)"),
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
    expected_sha256: Optional[str] = typer.Option(None, "--expected-sha256", help="Optimistic concurrency guard"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = ManuscriptHandler().insert_section(
            target=target,
            content=content,
            citations=citations,
            file_path=file_path,
            expected_sha256=expected_sha256,
        )
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "manuscript.insert"})
    _emit(res, raw=raw)
    if isinstance(res, dict) and res.get("ok") is False:
        raise typer.Exit(code=1)


scholar_app = typer.Typer(add_completion=False, help="Scholar skills")
app.add_typer(scholar_app, name="scholar")


@scholar_app.command("federated-search")
def scholar_federated_search(
    ctx: typer.Context,
    query: str = typer.Option(..., "--query", help="Search query"),
    max_results: int = typer.Option(10, "--max-results", help="Max results"),
    filters_json: str = typer.Option("{}", "--filters", help="JSON object string for filters"),
):
    from sros.domain.schemas import SearchQuery
    from sros.servers.scholar.handler import ScholarHandler

    raw = bool((ctx.obj or {}).get("raw"))
    filters = json.loads(filters_json) if filters_json.strip() else {}
    q = SearchQuery(query=query, max_results=max_results, filters=filters)
    try:
        res = ScholarHandler().federated_search(q)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "scholar.federated-search"})
    _emit(res, raw=raw)


memory_app = typer.Typer(add_completion=False, help="Memory skills")
app.add_typer(memory_app, name="memory")


@memory_app.command("query")
def memory_query(
    ctx: typer.Context,
    query: str = typer.Option(..., "--query", help="Query string"),
    limit: int = typer.Option(10, "--limit", help="Max rows"),
):
    from sros.servers.memory.handler import MemoryHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = MemoryHandler().query_knowledge(query=query, limit=limit)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "memory.query"})
    _emit(res, raw=raw)


@memory_app.command("citation-map")
def memory_citation_map(
    ctx: typer.Context,
    section_id: str = typer.Option(..., "--section-id", help="Section id"),
):
    from sros.servers.memory.handler import MemoryHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = MemoryHandler().get_citation_map(section_id=section_id)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "memory.citation-map"})
    _emit(res, raw=raw)


@memory_app.command("store")
def memory_store(
    ctx: typer.Context,
    nodes_json: str = typer.Option("[]", "--nodes", help="JSON array of node dicts"),
    edges_json: str = typer.Option("[]", "--edges", help="JSON array of edge dicts"),
):
    from sros.domain.schemas import KnowledgeEdge
    from sros.servers.memory.handler import MemoryHandler

    raw = bool((ctx.obj or {}).get("raw"))
    nodes = json.loads(nodes_json) if nodes_json.strip() else []
    edges_in = json.loads(edges_json) if edges_json.strip() else []
    edges = [KnowledgeEdge(**e) if isinstance(e, dict) else e for e in edges_in]
    try:
        ok = MemoryHandler().store_knowledge(nodes=nodes, edges=edges)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "memory.store"})
    _emit({"ok": bool(ok)}, raw=raw)
    if not ok:
        raise typer.Exit(code=1)


rpc_app = typer.Typer(add_completion=False, help="RPC adapter for gateway reflection")
app.add_typer(rpc_app, name="rpc")


@rpc_app.command("call")
def rpc_call(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Tool name, e.g. manuscript.find_gaps"),
    args_json: Optional[str] = typer.Option(None, "--args-json", help="JSON args (otherwise read from stdin)"),
):
    raw = bool((ctx.obj or {}).get("raw"))
    args = _read_json_args(args_json)

    from sros.skills.rpc import dispatch_tool

    try:
        res = dispatch_tool(name, args)
        _emit(res, raw=raw)
    except typer.Exit:
        raise
    except Exception as e:
        _raw_fail(str(e), details={"tool": name})


data_app = typer.Typer(add_completion=False, help="Data skills")
app.add_typer(data_app, name="data")


@data_app.command("preview")
def data_preview(
    ctx: typer.Context,
    file_path: str = typer.Option(..., "--file", "-f", help="Path to CSV file"),
):
    from sros.servers.data.handler import DataHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = DataHandler().preview_csv(file_path)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "data.preview"})
    _emit(res, raw=raw)
    if isinstance(res, dict) and res.get("ok") is False:
        raise typer.Exit(code=1)


@data_app.command("run-script")
def data_run_script(
    ctx: typer.Context,
    script_path: str = typer.Option(..., "--script", "-s", help="Path to Python script"),
    dataset_paths: List[str] = typer.Option(
        [],
        "--dataset",
        "-d",
        help="Dataset path(s) used by the script (repeatable). Relative paths are resolved from SROS_WORKSPACE_DIR",
    ),
):
    from sros.servers.data.handler import DataHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = DataHandler().run_script(script_path, dataset_paths=dataset_paths)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "data.run-script"})
    _emit(res, raw=raw)
    if isinstance(res, dict) and res.get("ok") is False:
        raise typer.Exit(code=1)


plugins_app = typer.Typer(add_completion=False, help="Workspace plugins (.sros/plugins)")
app.add_typer(plugins_app, name="plugins")


@plugins_app.command("list")
def plugins_list(ctx: typer.Context):
    from sros.utils.plugin_loader import discover_plugins

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        found = discover_plugins()
        plugins: List[Dict[str, Any]] = []
        for p in found:
            plugins.append(
                {
                    "name": p.name,
                    "display_name": p.display_name or p.name,
                    "description": p.description,
                    "path": str(p.path),
                    "input_schema": p.input_schema,
                }
            )
        _emit({"ok": True, "plugins": plugins, "count": len(plugins)}, raw=raw)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "plugins.list"})


@plugins_app.command("run")
def plugins_run(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Plugin name (filename stem under .sros/plugins)") ,
    args_json: str = typer.Option("{}", "--args-json", help="JSON object passed to plugin run(args)") ,
):
    from sros.utils.plugin_loader import run_plugin

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        args = json.loads(args_json) if args_json.strip() else {}
        if not isinstance(args, dict):
            raise ValueError("--args-json must be a JSON object")
        value = run_plugin(name, args)
        _emit({"ok": True, "plugin": name, "result": value}, raw=raw)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "plugins.run", "plugin": name})


tasks_app = typer.Typer(add_completion=False, help="Long-running tasks (in-process)")
app.add_typer(tasks_app, name="tasks")


@tasks_app.command("run-plugin")
def tasks_run_plugin(
    ctx: typer.Context,
    plugin: str = typer.Option(..., "--plugin", help="Plugin id (filename stem under .sros/plugins)"),
    args_json: str = typer.Option("{}", "--args-json", help="JSON object passed to plugin run(args)"),
):
    from sros.servers.tasks.handler import TasksHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        args = json.loads(args_json) if args_json.strip() else {}
        if not isinstance(args, dict):
            raise ValueError("--args-json must be a JSON object")
        res = TasksHandler().run_plugin_async(plugin=plugin, args=args)
        _emit(res, raw=raw)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "tasks.run-plugin", "plugin": plugin})


@tasks_app.command("get")
def tasks_get(
    ctx: typer.Context,
    task_id: str = typer.Option(..., "--task-id", help="Task id"),
):
    from sros.servers.tasks.handler import TasksHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = TasksHandler().get_task(task_id)
        _emit(res, raw=raw)
        if isinstance(res, dict) and res.get("ok") is False:
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "tasks.get", "task_id": task_id})


@tasks_app.command("list")
def tasks_list(ctx: typer.Context):
    from sros.servers.tasks.handler import TasksHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = TasksHandler().list_tasks()
        _emit(res, raw=raw)
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "tasks.list"})


@tasks_app.command("wait")
def tasks_wait(
    ctx: typer.Context,
    task_id: str = typer.Option(..., "--task-id", help="Task id"),
    timeout_s: float = typer.Option(30.0, "--timeout", help="Timeout seconds"),
):
    from sros.servers.tasks.handler import TasksHandler

    raw = bool((ctx.obj or {}).get("raw"))
    try:
        res = TasksHandler().wait_task(task_id, timeout_s=timeout_s)
        _emit(res, raw=raw)
        if isinstance(res, dict) and res.get("ok") is False:
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        _fail(str(e), raw=raw, details={"tool": "tasks.wait", "task_id": task_id})


if __name__ == "__main__":
    app()
