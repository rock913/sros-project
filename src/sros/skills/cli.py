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
    res = ManuscriptHandler().find_gaps(file_path)
    _emit(res, raw=raw)


@manuscript_app.command("outline")
def manuscript_outline(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    res = ManuscriptHandler().get_outline_tree(file_path)
    _emit(res, raw=raw)


@manuscript_app.command("sha256")
def manuscript_sha256(
    ctx: typer.Context,
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    res = ManuscriptHandler().get_file_sha256(file_path)
    _emit({"file_path": file_path, "sha256": res}, raw=raw)


@manuscript_app.command("insert")
def manuscript_insert(
    ctx: typer.Context,
    target: str = typer.Option(..., "--target", help="append/end/anchor:<hash>/heading:<Title>/heading-<n>/line:<n>"),
    content: str = typer.Option(..., "--content", help="Markdown content to insert"),
    citations: List[str] = typer.Option([], "--cite", help="Citation keys (repeatable)"),
    file_path: str = typer.Option("draft.md", "--file", "-f", help="Workspace-relative markdown path"),
    expected_sha256: Optional[str] = typer.Option(None, "--expected-sha256", help="Optimistic concurrency guard"),
):
    from sros.servers.manuscript.handler import ManuscriptHandler

    raw = bool((ctx.obj or {}).get("raw"))
    res = ManuscriptHandler().insert_section(
        target=target,
        content=content,
        citations=citations,
        file_path=file_path,
        expected_sha256=expected_sha256,
    )
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
    res = ScholarHandler().federated_search(q)
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
    res = MemoryHandler().query_knowledge(query=query, limit=limit)
    _emit(res, raw=raw)


@memory_app.command("citation-map")
def memory_citation_map(
    ctx: typer.Context,
    section_id: str = typer.Option(..., "--section-id", help="Section id"),
):
    from sros.servers.memory.handler import MemoryHandler

    raw = bool((ctx.obj or {}).get("raw"))
    res = MemoryHandler().get_citation_map(section_id=section_id)
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
    ok = MemoryHandler().store_knowledge(nodes=nodes, edges=edges)
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
    res = DataHandler().preview_csv(file_path)
    _emit(res, raw=raw)
    if isinstance(res, dict) and res.get("ok") is False:
        raise typer.Exit(code=1)


@data_app.command("run-script")
def data_run_script(
    ctx: typer.Context,
    script_path: str = typer.Option(..., "--script", "-s", help="Path to Python script"),
):
    from sros.servers.data.handler import DataHandler

    raw = bool((ctx.obj or {}).get("raw"))
    res = DataHandler().run_script(script_path)
    _emit(res, raw=raw)
    if isinstance(res, dict) and res.get("ok") is False:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
