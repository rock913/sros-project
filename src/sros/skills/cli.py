from __future__ import annotations

import json
from typing import Any, List, Optional

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
