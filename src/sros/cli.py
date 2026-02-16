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
from sros.gateway.config import GatewayConfig

app = typer.Typer()
console = Console()

def validate_workspace_dir(workspace_dir: str) -> str:
    """验证工作区目录"""
    if not os.path.exists(workspace_dir):
        raise typer.BadParameter(f"Workspace directory '{workspace_dir}' does not exist")
    return workspace_dir

@app.command()
def init(project_name: str = typer.Argument(..., help="项目名称")):
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
                "sros-gateway": {
                    "name": "SROS Gateway",
                    "url": "http://localhost:8000/sse",
                    "type": "sse",
                    "description": "SROS V2.3.2 Gateway (Local)",
                    "disabled": False,
                    "alwaysAllow": []
                }
            }
        }
        (project_path / ".roo" / "mcp.json").write_text(json.dumps(mcp_config, indent=2), encoding="utf-8")
        
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
        
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to initialize project: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def start(
    workspace_dir: Optional[str] = typer.Option(None, "--workspace", "-w", help="工作区目录"),
    port: int = typer.Option(8000, "--port", "-p", help="监听端口")
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
        
        # 检查端口是否被占用
        if is_port_in_use(port):
            console.print(f"[red]Error:[/red] Port {port} is already in use")
            raise typer.Exit(code=1)
        
        # 设置环境变量
        os.environ["SROS_WORKSPACE_DIR"] = str(workspace_path.absolute())
        os.environ["SROS_PORT"] = str(port)
        
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

if __name__ == "__main__":
    app()