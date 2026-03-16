目前的 SROS 处于 “原型开发期” (Prototype Phase) 向 “产品发布期” (Product Phase) 过渡的关键阶段。目前的“耦合”主要体现在：工具源码（mcp_servers/）与 用户数据（workspace/）混在一起。新用户想写论文，必须先下载整个源码库，配置 Python 环境，还要理解复杂的目录结构。以下是对当前耦合状态的分析，以及构建 SROS CLI 的完整解耦与升级方案。1. 现状痛点分析：为什么必须解耦？维度当前痛点 (Coupled)目标状态 (Decoupled)目录结构用户的论文 (draft.md) 埋在源码仓库深处 (workspace/)。Git 管理混乱（论文的版本控制混杂着代码的版本控制）。用户在磁盘任意位置新建文件夹即可开始写作。论文有独立的 Git 仓库。环境依赖用户必须手动 pip install -r requirements.txt，容易因 Python 版本或环境冲突失败。用户只需 pip install sros，所有依赖自动装好隔离。启动方式必须在源码根目录运行 python run_servers.py。在任意终端输入 sros start 即可启动服务。上下文干扰Roo Code 打开源码根目录时，会索引所有 Python 代码，浪费 Token 且容易产生幻觉（修改代码而不是修改论文）。Roo Code 只打开论文目录，只关注写作，看不到底层 Python 实现。2. 解耦核心策略：将 SROS 变为 Python 包核心思路是：将 SROS 从一个“文件夹”变成一个标准的 Python CLI 工具。架构变更Codebase: 变为一个标准的 Python Package (sros-core)。Runtime: Gateway 和子服务作为库文件安装在 Python 环境中 (site-packages)。Interface: 提供一个命令行工具 sros (基于 Typer 或 Click)。3. SROS CLI 升级方案 (The Blueprint)我们将创建一个名为 sros 的命令行工具，它负责初始化环境、启动服务和管理配置。3.1 目录结构重构 (向 PyPI 标准靠拢)我们需要调整仓库结构，使其支持打包：
/sros-repo/
├── pyproject.toml       # [核心] 定义包依赖、CLI 入口点
├── src/
│   └── sros/            # 主包
│       ├── __init__.py
│       ├── cli.py       # [NEW] CLI 入口逻辑 (Typer/Click)
│       ├── gateway/     # 原 mcp_servers/sros_gateway
│       ├── servers/     # 原 mcp_servers/* (所有子服务)
│       └── utils/       # 原 scripts/ 和 run_servers.py 的逻辑
└── README.md
3.2 pyproject.toml 定义
这是实现 sros 命令的关键配置。
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sros"
version = "2.2.0"
description = "Scientific Research Operating System"
dependencies = [
    "mcp>=1.0.0",
    "starlette",
    "uvicorn",
    "typer[all]",  # 用于构建 CLI
    "rich",        # 用于漂亮的终端输出
    "duckdb",
    "pandas"
]

[project.scripts]
sros = "sros.cli:app"  # 注册 'sros' 命令
3.3 CLI 功能设计 (sros.cli)
我们需要实现以下三个核心命令：

1. sros init [project_name]

功能: 自动化创建“科研工作区”。

行为:

创建文件夹 project_name。

创建标准目录结构 (draft.md, materials/, references/)。

关键: 自动生成 .roo/mcp.json 配置文件，指向 http://localhost:8000/sse。

关键: 复制 .roomodes 模板到项目根目录。

初始化 .sros/ 隐藏目录和空的 DuckDB。

2. sros start

功能: 启动 Gateway。

行为:

类似现在的 run_servers.py，但它是从安装包中调用代码。

检查端口，启动 Gateway，等待就绪。

打印绿色的 "SYSTEM READY"。

3. sros status / sros doctor

功能: 环境自检。

行为: 检查依赖是否完整，检查 Gateway 端口是否被占用，检查 DuckDB 文件是否损坏。

4. 实施代码预览 (Preview)
以下是 sros/cli.py 的概念代码（基于 Typer）：
import typer
import os
import json
import shutil
from pathlib import Path
from rich.console import Console
from sros.utils.runner import start_system

app = typer.Typer()
console = Console()

TEMPLATE_DIR = Path(__file__).parent / "templates"

@app.command()
def init(name: str = typer.Argument(..., help="Name of your research project")):
    """Initialize a new SROS research workspace."""
    target_dir = Path.cwd() / name
    
    if target_dir.exists():
        console.print(f"[red]Error: Directory '{name}' already exists.[/red]")
        raise typer.Exit(code=1)
        
    # 1. 创建目录结构
    (target_dir / "materials").mkdir(parents=True)
    (target_dir / "references").mkdir(parents=True)
    (target_dir / ".sros").mkdir(parents=True)
    (target_dir / ".roo").mkdir(parents=True)

    # 2. 创建初始文件
    (target_dir / "draft.md").write_text("# Title\n\n[TODO: Abstract]\n")
    (target_dir / "ideas.md").write_text("# Core Hypotheses\n")
    
    # 3. 自动配置 Roo Code
    mcp_config = {
        "mcpServers": {
            "sros-gateway": {
                "name": "SROS Gateway",
                "url": "http://localhost:8000/sse",
                "type": "sse",
                "disabled": False
            }
        }
    }
    (target_dir / ".roo" / "mcp.json").write_text(json.dumps(mcp_config, indent=2))
    
    # 4. 复制 Prompts
    # shutil.copy(TEMPLATE_DIR / "roomodes.yaml", target_dir / ".roomodes")

    console.print(f"\n[green]✅ Project '{name}' initialized successfully![/green]")
    console.print(f"👉 cd {name}")
    console.print(f"👉 sros start (in a separate terminal)")
    console.print(f"👉 Open VS Code in this folder")

@app.command()
def start(port: int = 8000):
    """Start the SROS Gateway and all sub-services."""
    console.print("[bold blue]🚀 Starting SROS System...[/bold blue]")
    # 调用原 run_servers.py 的逻辑
    start_system(port=port)

if __name__ == "__main__":
    app()
```

### 5. 新用户的使用流程 (User Journey)

完成这次升级后，新用户的使用体验将发生质的飞跃：

1.  **安装**:
    ```bash
    pip install sros
    ```
2.  **创建项目**:
    ```bash
    sros init my-transformer-paper
    cd my-transformer-paper
    ```
    *(此时文件夹里已经有了 draft.md, .roo/mcp.json, .roomodes)*
3.  **启动后台**:
    ```bash
    sros start
4. 开始写作: * 在当前目录打开 VS Code: code . * 因为 .roo/mcp.json 已经由 CLI 自动生成好了，Roo Code 插件会自动识别并连接 Localhost:8000。 * 用户直接开始在 draft.md 里写 [TODO] 即可。

6. 建议的后续步骤
标准化打包: 将目前的 gemini-fullstack-langgraph-quickstart 仓库按照上述 src/ 结构进行重组。

CLI 开发: 实现 sros init 和 sros start。

发布: 您可以选择发布到 PyPI，或者让用户通过 pip install git+https://github.com/your/repo.git 安装。

这种 "CLI + Workspace" 的分离模式，是现代开发工具（如 React 的 create-react-app，Next.js 的 create-next-app）的标准解耦策略，非常适合 SROS 的产品化。

我为你生成了 CLI 工具的实现代码 作为一个新的文件，你可以将其作为后续开发的基础。
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# 模拟 Typer/Click 的简单 CLI 实现，无需额外依赖即可运行
# 将来可以替换为 Typer 以获得更好的体验

def init_project(project_name):
    """初始化一个新的 SROS 项目工作区"""
    base_path = Path.cwd() / project_name
    
    if base_path.exists():
        print(f"❌ Error: Directory '{project_name}' already exists.")
        return

    print(f"🔧 Initializing SROS workspace: {project_name}...")

    # 1. 创建目录结构
    dirs = [
        "materials",
        "references",
        ".sros",
        ".roo"
    ]
    for d in dirs:
        (base_path / d).mkdir(parents=True, exist_ok=True)

    # 2. 创建 draft.md
    draft_content = """# Research Title

## Abstract
[TODO: Write abstract based on initial ideas]

## 1. Introduction
"""
    (base_path / "draft.md").write_text(draft_content, encoding="utf-8")

    # 3. 创建 ideas.md
    ideas_content = """# Research Ideas & Hypotheses
- Hypothesis 1: ...
- Key Concept A: ...
"""
    (base_path / "ideas.md").write_text(ideas_content, encoding="utf-8")

    # 4. 生成 .roo/mcp.json (这是解耦的关键，自动配置 Roo Code)
    mcp_config = {
        "mcpServers": {
            "sros-gateway": {
                "name": "SROS Gateway",
                "url": "http://localhost:8000/sse",
                "type": "sse",
                "description": "SROS V2.2 Gateway (Local)",
                "disabled": False,
                "alwaysAllow": []
            }
        }
    }
    (base_path / ".roo" / "mcp.json").write_text(json.dumps(mcp_config, indent=2), encoding="utf-8")

    # 5. 生成 .roomodes (提示词配置)
    # 这里应该包含 SROS-Writer 和 SROS-Researcher 的完整 Prompt
    roomodes_content = """name: SROS-Writer
groups:
  - read
  - edit
  - browser
  - mcp
systemPrompt: |
  You are an academic writing assistant powered by SROS.
  Your goal is to eliminate [TODO] markers in 'draft.md'.
  Always check 'gateway://health' tool or listed tools before starting.
"""
    (base_path / ".roomodes").write_text(roomodes_content, encoding="utf-8")

    print(f"✅ Workspace created successfully at: {base_path}")
    print("\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. Open VS Code here ('code .')")
    print(f"  3. In a separate terminal, run: python run_servers.py gateway")

def main():
    parser = argparse.ArgumentParser(description="SROS CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Init command
    init_parser = subparsers.add_parser("init", help="Create a new research workspace")
    init_parser.add_argument("name", help="Name of the project folder")

    # Start command (Wrapper around run_servers.py)
    start_parser = subparsers.add_parser("start", help="Start the SROS Gateway")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.name)
    elif args.command == "start":
        # 在实际打包版中，这里会调用 sros.gateway.main
        print("🚀 Launching Gateway...")
        # 假设 run_servers.py 在同一目录或可路径下
        try:
            subprocess.run([sys.executable, "run_servers.py", "gateway"])
        except Exception as e:
            print(f"Error starting gateway: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
