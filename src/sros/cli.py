import os
import typer
import json
import asyncio
from pathlib import Path
from typing import Optional
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

                mcp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
                # Don't block startup on config update errors
                return

def validate_workspace_dir(workspace_dir: str) -> str:
    """验证工作区目录"""
    if not os.path.exists(workspace_dir):
        raise typer.BadParameter(f"Workspace directory '{workspace_dir}' does not exist")
    return workspace_dir

@app.command()
def init(
    project_name: str = typer.Argument(..., help="项目名称"),
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
        # 创建项目目录
        project_path = Path(project_name)
        if project_path.exists():
            typer.echo(f"Error: Directory '{project_name}' already exists", err=True)
            raise typer.Exit(code=1)
        
        project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建工作区结构
        workspace_dirs = [
            project_path / ".roo",
            project_path / ".sros",
            project_path / "materials",
            project_path / "references"
        ]
        
        for dir_path in workspace_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建初始文件
        (project_path / "draft.md").write_text("# My Paper\n\n")
        (project_path / "ideas.md").write_text("# Ideas\n\n")
        
        # 创建 .roo/mcp.json (Roo Code expected schema)
        mcp_config = {
            "mcpServers": {
                server_key: {
                    "name": "SROS Gateway",
                    "url": gateway_url,
                    "type": "sse",
                    "description": "SROS V2.3.2 Gateway (Local)",
                    "disabled": False,
                    "alwaysAllow": []
                }
            }
        }
        (project_path / ".roo" / "mcp.json").write_text(json.dumps(mcp_config, indent=2), encoding="utf-8")

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
        console.print(f"3. Open this directory in VS Code with Roo Code extension")
        console.print(f"\nTip: if Roo Code shows 'Retrying...' under Remote-SSH, forward port 8000 and re-run init with --gateway-url")
        
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
        
        # 设置环境变量
        os.environ["SROS_WORKSPACE_DIR"] = str(workspace_path.absolute())
        os.environ["SROS_PORT"] = str(port)

        if update_mcp_json:
            gateway_url = f"http://{mcp_host}:{port}/sse"
            _update_roo_mcp_json(workspace_path, gateway_url, server_key=server_key)
            console.print(f"[green]Updated .roo/mcp.json url ->[/green] {gateway_url}")
        
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
        workspace_files = {
            "draft.md": (current_dir / "draft.md").exists(),
            ".roo/mcp.json": (current_dir / ".roo" / "mcp.json").exists(),
            ".sros/graph.db": (current_dir / ".sros" / "graph.db").exists()
        }
        
        table = Table(title="Current Workspace Status")
        table.add_column("File", style="cyan")
        table.add_column("Exists", style="magenta")
        
        for file_path, exists in workspace_files.items():
            status = "[green]✓[/green]" if exists else "[red]✗[/red]"
            table.add_row(file_path, status)
        
        console.print(table)
        
        # 检查端口状态
        from sros.utils.port_detector import detect_free_port
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

if __name__ == "__main__":
    app()