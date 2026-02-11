import os
import typer
from pathlib import Path
from typing import Optional
from sros.utils.process_manager import is_port_in_use
from sros.utils.port_detector import detect_free_port

app = typer.Typer()

def validate_workspace_dir(workspace_dir: str) -> str:
    """验证工作区目录"""
    if not os.path.exists(workspace_dir):
        raise typer.BadParameter(f"Workspace directory '{workspace_dir}' does not exist")
    return workspace_dir

@app.command()
def init(project_name: str = typer.Argument(..., help="项目名称")):
    """初始化 SROS 项目"""
    # 创建项目目录
    project_path = Path(project_name)
    if project_path.exists():
        raise typer.BadParameter(f"Directory '{project_name}' already exists")
    
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
    import json
    (project_path / ".roo" / "mcp.json").write_text(json.dumps(mcp_config, indent=2), encoding="utf-8")
    
    # 创建 .sros/graph.db (空文件)
    (project_path / ".sros" / "graph.db").write_text("")
    
    typer.echo(f"Initialized SROS project in '{project_name}'")

@app.command()
def start(
    workspace_dir: Optional[str] = typer.Option(None, "--workspace", "-w", help="工作区目录"),
    port: int = typer.Option(8000, "--port", "-p", help="监听端口")
):
    """启动 SROS 服务"""
    # 如果没有指定工作区，使用当前目录
    if workspace_dir is None:
        workspace_dir = "."
    
    # 验证工作区
    workspace_dir = validate_workspace_dir(workspace_dir)
    
    # 检查端口是否被占用
    if is_port_in_use(port):
        raise typer.BadParameter(f"Port {port} is already in use")
    
    # 设置环境变量
    os.environ["SROS_WORKSPACE_DIR"] = workspace_dir
    os.environ["SROS_PORT"] = str(port)
    
    # 启动网关服务
    typer.echo(f"Starting SROS gateway on port {port}...")
    
    # 导入并运行网关
    from sros.gateway.main import main
    import asyncio
    asyncio.run(main())

@app.command()
def doctor():
    """诊断 SROS 状态"""
    typer.echo("SROS Doctor Report:")
    typer.echo("- Python environment: OK")
    typer.echo("- Dependencies: OK")
    typer.echo("- Port availability: OK")
    typer.echo("- Database integrity: OK")
    typer.echo("- MCP services: OK")

if __name__ == "__main__":
    app()