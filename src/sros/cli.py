import os
import typer
import json
import asyncio
from pathlib import Path
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from sros.utils.process_manager import is_port_in_use
from sros.utils.health_checker import HealthChecker
from sros.utils.port_detector import detect_free_port
from sros.gateway.config import GatewayConfig

app = typer.Typer()
console = Console()


DEFAULT_ROOMODES_YAML = """customModes:
    - slug: sros-writer
        name: SROS Writer
        description: Draft-driven academic writing mode (SROS)
        roleDefinition: >
            You are a professional academic writer. Your goal is to eliminate TODO markers in draft.md by using SROS tools.
            Prefer local knowledge (memory) before external searching.
        whenToUse: When you want to write/expand sections in draft.md.
        groups:
            - read
            - edit
            - browser
            - mcp
        customInstructions: |
            - Prefer calling memory.query_knowledge before any web search.
            - Do incremental edits; avoid rewriting the entire draft.
            - Every new claim should have a citation key like [@citekey] if possible.

    - slug: sros-researcher
        name: SROS Researcher
        description: Literature search & knowledge graph mode (SROS)
        roleDefinition: >
            You are a professional academic researcher. Your goal is to find evidence/citations and store them into local memory.
        whenToUse: When you need to research sources to fill gaps.
        groups:
            - read
            - browser
            - mcp
            - command
        customInstructions: |
            - Start with manuscript.find_gaps to identify TODOs.
            - Store useful findings via memory.store_knowledge.
"""


def _load_dotenv(dotenv_path: Path) -> None:
    """Load a simple .env file into os.environ.

    - No external dependency (python-dotenv).
    - Does not override already-set environment variables.
    """
    try:
        if not dotenv_path.exists() or not dotenv_path.is_file():
            return

        for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].lstrip()

            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                continue

            # Strip optional quotes
            if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
                value = value[1:-1]

            if key not in os.environ:
                os.environ[key] = value
    except Exception:
        # dotenv loading should be best-effort and never block startup
        return


def _update_roo_mcp_json(workspace_path: Path, url: str, server_key: str = "sros-gateway") -> None:
    mcp_path = workspace_path / ".roo" / "mcp.json"
    if not mcp_path.exists():
        return

    try:
        data = json.loads(mcp_path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers", {})
        if isinstance(servers, dict) and server_key in servers and isinstance(servers[server_key], dict):
            servers[server_key]["url"] = url
        elif isinstance(servers, dict) and len(servers) >= 1:
            # Fallback: update the first server entry
            first_key = next(iter(servers.keys()))
            if isinstance(servers[first_key], dict):
                servers[first_key]["url"] = url
        else:
            return

        mcp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        # Don't block startup on config update errors
        return


DEFAULT_CLAUDE_INSTRUCTIONS = """You are a senior academic researcher/writer.

Goal: enrich the manuscript in draft.md by eliminating TODO markers.

Hard rules:
- Do NOT directly edit draft.md with raw file edits. Use MCP tools only.
- First call manuscript.get_outline_tree(file_path=\"draft.md\") and locate an anchor for the target heading.
- Prefer target=\"anchor:<hash>\" for insert_section.
- Use optimistic concurrency: call manuscript.get_file_sha256(file_path=\"draft.md\") and pass expected_sha256=... into insert_section/patch_draft.

Suggested loop:
1) manuscript.find_gaps(file_path=\"draft.md\")
2) manuscript.get_outline_tree(file_path=\"draft.md\")
3) scholar.federated_search(query=..., max_results=..., filters={...})
4) manuscript.insert_section(target=\"anchor:<hash>\", content=..., citations=[...], file_path=\"draft.md\", expected_sha256=...)
5) memory.store_knowledge(...) when useful
"""


def _write_claude_rc(workspace_path: Path, url: str, server_key: str = "sros-gateway") -> None:
    config = {
        "custom_instructions": DEFAULT_CLAUDE_INSTRUCTIONS,
        "mcp_servers": {server_key: {"url": url}},
    }
    (workspace_path / ".clauderc").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def _update_claude_rc(workspace_path: Path, url: str, server_key: str = "sros-gateway") -> None:
    rc_path = workspace_path / ".clauderc"
    if not rc_path.exists():
        return

    try:
        data = json.loads(rc_path.read_text(encoding="utf-8"))
        servers = data.get("mcp_servers")
        if not isinstance(servers, dict):
            servers = {}
            data["mcp_servers"] = servers
        entry = servers.get(server_key)
        if not isinstance(entry, dict):
            entry = {}
            servers[server_key] = entry
        entry["url"] = url
        rc_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        return


def _write_claude_md(workspace_path: Path, url: str) -> None:
    content = f"""# Claude Code + SROS (MVP)

MCP Gateway SSE URL:

- {url}

Recommended workflow:

1) `manuscript.find_gaps(file_path=\"draft.md\")`
2) `manuscript.get_outline_tree(file_path=\"draft.md\")` → copy the target heading's `anchor`
3) `manuscript.get_file_sha256(file_path=\"draft.md\")`
4) `manuscript.insert_section(target=\"anchor:<hash>\", ..., expected_sha256=<sha>)`

Rules:

- Prefer `target=\"anchor:<hash>\"` (stable).
- Always pass `expected_sha256` on write operations to avoid clobbering user edits.
"""
    (workspace_path / "CLAUDE.md").write_text(content, encoding="utf-8")

def validate_workspace_dir(workspace_dir: str) -> str:
    """验证工作区目录"""
    if not os.path.exists(workspace_dir):
        raise typer.BadParameter(f"Workspace directory '{workspace_dir}' does not exist")
    return workspace_dir

@app.command()
def init(
    project_name: str = typer.Argument(..., help="项目名称"),
    target: str = typer.Option(
        "roo",
        "--target",
        help="对接目标：roo | claude-code | both（默认 roo）",
    ),
    gateway_url: str = typer.Option(
        "http://localhost:8000/sse",
        "--gateway-url",
        help="写入 .roo/mcp.json 的 Gateway SSE URL（Remote-SSH/端口转发场景很有用）",
    ),
    server_key: str = typer.Option(
        "sros-gateway",
        "--server-key",
        help=".roo/mcp.json 中 mcpServers 的 key（显示名称/区分多个 server）",
    ),
    with_roomodes: bool = typer.Option(
        False,
        "--with-roomodes",
        help="同时生成项目级 .roomodes（Roo Code 自定义模式，可选）",
    ),
):
    """初始化 SROS 项目"""
    try:
        target_norm = (target or "roo").strip().lower()
        if target_norm not in {"roo", "claude-code", "both"}:
            raise typer.BadParameter("--target must be one of: roo, claude-code, both")

        # 创建项目目录
        project_path = Path(project_name)
        if project_path.exists():
            typer.echo(f"Error: Directory '{project_name}' already exists", err=True)
            raise typer.Exit(code=1)
        
        project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建工作区结构
        workspace_dirs = [
            project_path / ".sros",
            project_path / "materials",
            project_path / "references"
        ]

        if target_norm in {"roo", "both"}:
            workspace_dirs.append(project_path / ".roo")
        
        for dir_path in workspace_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建初始文件
        (project_path / "draft.md").write_text("# My Paper\n\n")
        (project_path / "ideas.md").write_text("# Ideas\n\n")
        
        if target_norm in {"roo", "both"}:
            # 创建 .roo/mcp.json (Roo Code expected schema)
            mcp_config = {
                "mcpServers": {
                    server_key: {
                        "name": "SROS Gateway",
                        "url": gateway_url,
                        "type": "sse",
                        "description": "SROS V2.3.x Gateway (Local)",
                        "disabled": False,
                        "alwaysAllow": [],
                    }
                }
            }
            (project_path / ".roo" / "mcp.json").write_text(
                json.dumps(mcp_config, indent=2, ensure_ascii=False), encoding="utf-8"
            )

        if target_norm in {"claude-code", "both"}:
            _write_claude_rc(project_path, gateway_url, server_key=server_key)
            _write_claude_md(project_path, gateway_url)

        if with_roomodes:
            (project_path / ".roomodes").write_text(DEFAULT_ROOMODES_YAML, encoding="utf-8")
        
        # 创建 .sros/graph.db (有效 DuckDB 文件)
        # NOTE: 必须是可连接的 DB 文件，不能是空文本，否则会导致运行期错误。
        try:
            import duckdb  # lazy import

            db_path = project_path / ".sros" / "graph.db"
            duckdb.connect(str(db_path)).close()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DuckDB at {project_path / '.sros' / 'graph.db'}: {e}") from e
        
        console.print(f"[green]✓[/green] Initialized SROS project in '{project_name}'")
        console.print(f"\n[bold]Next steps:[/bold]")
        console.print(f"1. cd {project_name}")
        console.print(f"2. sros start")
        if target_norm in {"roo", "both"}:
            console.print(f"3. Open this directory in VS Code with Roo Code extension")
            console.print(
                f"\nTip: if Roo Code shows 'Retrying...' under Remote-SSH, forward port 8000 and re-run init with --gateway-url"
            )
        if target_norm in {"claude-code", "both"}:
            console.print("3. Run Claude Code in this workspace (see CLAUDE.md)")
            console.print("4. (Recommended) Run: sros verify --port 8000")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to initialize project: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def start(
    workspace_dir: Optional[str] = typer.Option(None, "--workspace", "-w", help="工作区目录"),
    port: int = typer.Option(8000, "--port", "-p", help="监听端口"),
    auto_port: bool = typer.Option(False, "--auto-port", help="端口占用时自动寻找可用端口"),
    update_mcp_json: Optional[bool] = typer.Option(
        None,
        "--update-mcp-json/--no-update-mcp-json",
        help="自动更新工作区 .roo/mcp.json 的 url 为实际启动端口（默认：仅在 --auto-port 时启用）",
    ),
    mcp_host: str = typer.Option(
        "127.0.0.1",
        "--mcp-host",
        help="写回 .roo/mcp.json 的 host（Remote-SSH 本地端口转发通常用 127.0.0.1）",
    ),
    server_key: str = typer.Option(
        "sros-gateway",
        "--server-key",
        help="更新 .roo/mcp.json 时使用的 mcpServers key",
    ),
    update_clauderc: Optional[bool] = typer.Option(
        None,
        "--update-clauderc/--no-update-clauderc",
        help="自动更新工作区 .clauderc 的 Gateway SSE URL（默认：仅在 --auto-port 时启用）",
    ),
):
    """启动 SROS 服务"""
    try:
        # 如果没有指定工作区，使用当前目录
        if workspace_dir is None:
            workspace_dir = "."
        
        # 验证工作区
        workspace_path = Path(workspace_dir)
        if not workspace_path.exists():
            console.print(f"[red]Error:[/red] Workspace directory '{workspace_dir}' does not exist")
            raise typer.Exit(code=1)

        # Best-effort: load workspace .env for provider config (OpenAlex/Zotero/etc)
        _load_dotenv(workspace_path / ".env")
        
        # 检查端口是否被占用
        if is_port_in_use(port):
            if not auto_port:
                console.print(f"[red]Error:[/red] Port {port} is already in use")
                console.print("Tip: use --auto-port or -p <port>, or stop the existing process.")
                raise typer.Exit(code=1)
            free_port = detect_free_port(start_port=port)
            if free_port is None:
                console.print(f"[red]Error:[/red] No free port found near {port}")
                raise typer.Exit(code=1)
            console.print(f"[yellow]Port {port} in use; switching to {free_port}[/yellow]")
            port = free_port

        if update_mcp_json is None:
            update_mcp_json = bool(auto_port)

        if update_clauderc is None:
            update_clauderc = bool(auto_port)
        
        # 设置环境变量
        os.environ["SROS_WORKSPACE_DIR"] = str(workspace_path.absolute())
        os.environ["SROS_PORT"] = str(port)

        if update_mcp_json:
            gateway_url = f"http://{mcp_host}:{port}/sse"
            _update_roo_mcp_json(workspace_path, gateway_url, server_key=server_key)
            console.print(f"[green]Updated .roo/mcp.json url ->[/green] {gateway_url}")

        if update_clauderc:
            gateway_url = f"http://{mcp_host}:{port}/sse"
            _update_claude_rc(workspace_path, gateway_url, server_key=server_key)
            if (workspace_path / ".clauderc").exists():
                console.print(f"[green]Updated .clauderc url ->[/green] {gateway_url}")
        
        console.print(f"[blue]Starting SROS gateway on port {port}...[/blue]")
        
        # 创建配置对象并传递给网关
        config = GatewayConfig()
        config.port = port
        config.workspace_dir = str(workspace_path.absolute())
        
        # 导入并运行网关
        from sros.gateway.main import main
        asyncio.run(main(config))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]SROS gateway stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to start gateway: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def doctor():
    """诊断 SROS 状态"""
    try:
        checker = HealthChecker()
        report = checker.generate_report()
        
        table = Table(title="SROS Health Report")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Details", style="green")
        
        for component, status in report.items():
            if isinstance(status, dict):
                status_str = status.get('status', 'unknown')
                details = status.get('details', '')
            else:
                status_str = str(status)
                details = ''
            table.add_row(component, status_str, details)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to run health check: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def status():
    """显示 SROS 状态"""
    try:
        # 检查当前工作区状态
        current_dir = Path.cwd()
        workspace_dir = Path(os.getenv("SROS_WORKSPACE_DIR") or current_dir).expanduser().resolve()
        workspace_files = {
            "draft.md": (workspace_dir / "draft.md").exists(),
            ".roo/mcp.json": (workspace_dir / ".roo" / "mcp.json").exists(),
            ".clauderc": (workspace_dir / ".clauderc").exists(),
            "CLAUDE.md": (workspace_dir / "CLAUDE.md").exists(),
            ".sros/graph.db": (workspace_dir / ".sros" / "graph.db").exists(),
        }
        
        table = Table(title="Current Workspace Status")
        table.add_column("File", style="cyan")
        table.add_column("Exists", style="magenta")
        
        for file_path, exists in workspace_files.items():
            status = "[green]✓[/green]" if exists else "[red]✗[/red]"
            table.add_row(file_path, status)
        
        console.print(table)

        console.print(f"\nWorkspace: [bold]{workspace_dir}[/bold]")

        backend = (os.getenv("SROS_SCHOLAR_BACKEND") or "mock").strip().lower()
        openalex_mailto = (
            os.getenv("SROS_OPENALEX_MAILTO")
            or os.getenv("SROS_OPENALEX_EMAIL")
            or os.getenv("OPENALEX_EMAIL")
        )
        if backend == "openalex":
            console.print(
                f"Scholar backend: [bold]openalex[/bold] ({'mailto ok' if openalex_mailto else 'missing OPENALEX_EMAIL'})"
            )
        else:
            console.print(f"Scholar backend: [bold]{backend}[/bold]")
        
        # 检查端口状态
        port_in_use = is_port_in_use(8000)
        console.print(f"\nPort 8000: {'[red]In Use[/red]' if port_in_use else '[green]Available[/green]'}")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to check status: {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def roomodes(
    workspace_dir: Optional[str] = typer.Option(None, "--workspace", "-w", help="工作区目录（默认当前目录）"),
    force: bool = typer.Option(False, "--force", help="若已存在则覆盖 .roomodes"),
):
    """生成项目级 .roomodes（Roo Code 自定义模式，可选）"""
    try:
        if workspace_dir is None:
            workspace_dir = "."

        workspace_path = Path(workspace_dir)
        if not workspace_path.exists():
            console.print(f"[red]Error:[/red] Workspace directory '{workspace_dir}' does not exist")
            raise typer.Exit(code=1)

        target_path = workspace_path / ".roomodes"
        if target_path.exists() and not force:
            console.print("[yellow].roomodes already exists. Use --force to overwrite.[/yellow]")
            raise typer.Exit(code=1)

        target_path.write_text(DEFAULT_ROOMODES_YAML, encoding="utf-8")
        console.print(f"[green]✓[/green] Wrote {target_path}")
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to write .roomodes: {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def verify(
    port: int = typer.Option(8000, "--port", "-p", help="Gateway 端口（默认 8000）"),
    query: str = typer.Option("neuro ai", "--query", help="用于 scholar.federated_search 的测试 query"),
    output: str = typer.Option(
        "logs/claude_mvp_verification.json",
        "--output",
        help="输出报告路径（相对当前目录）",
    ),
):
    """MVP 验证：不运行 Claude，也能确认 MCP SSE 网关可用（initialize/tools/list/tools/call）。"""
    try:
        from time import perf_counter
        from mcp import ClientSession
        from mcp.client.sse import sse_client

        sse_url = f"http://localhost:{port}/sse"

        async def _run():
            report = {
                "started_at": datetime.now().isoformat(),
                "sse_url": sse_url,
                "query": query,
                "checks": [],
                "ok": False,
            }
            async with sse_client(sse_url) as (read, write):
                async with ClientSession(read, write) as session:
                    t0 = perf_counter()
                    await session.initialize()
                    report["checks"].append({"name": "initialize", "ok": True, "duration_s": perf_counter() - t0})

                    t0 = perf_counter()
                    tools = await session.list_tools()
                    report["checks"].append({"name": "tools/list", "ok": True, "duration_s": perf_counter() - t0})
                    tool_names = [t.name for t in tools.tools]

                    required = [
                        "manuscript.find_gaps",
                        "manuscript.get_outline_tree",
                        "manuscript.insert_section",
                    ]
                    missing = [t for t in required if t not in tool_names]
                    report["checks"].append({"name": "tools/required", "ok": not missing, "missing": missing})
                    if missing:
                        report["ok"] = False
                        report["finished_at"] = datetime.now().isoformat()
                        return report

                    t0 = perf_counter()
                    res = await session.call_tool("manuscript.find_gaps", {"file_path": "draft.md"})
                    report["checks"].append({"name": "tool:manuscript.find_gaps", "ok": True, "duration_s": perf_counter() - t0})
                    report["sample"] = (res.content[0].text[:200] if res.content else "")

                    # Optional: exercise scholar if present (can be mock/offline)
                    if "scholar.federated_search" in tool_names:
                        t0 = perf_counter()
                        await session.call_tool("scholar.federated_search", {"query": query, "max_results": 1, "filters": {}})
                        report["checks"].append(
                            {"name": "tool:scholar.federated_search", "ok": True, "duration_s": perf_counter() - t0}
                        )

            report["ok"] = all(c.get("ok") for c in report["checks"])
            report["finished_at"] = datetime.now().isoformat()
            return report

        report = asyncio.run(_run())
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        if report.get("ok"):
            console.print(f"[green]✓[/green] MCP verify ok. Report -> {out_path}")
        else:
            console.print(f"[red]✗[/red] MCP verify failed. Report -> {out_path}")
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] verify failed: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()