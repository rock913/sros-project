import asyncio
import os
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Set PYTHONPATH environment variable for imports
os.environ['PYTHONPATH'] = os.path.join(os.path.dirname(__file__), '..', '..')

# Add backend/src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Initialize MCP Server
mcp = FastMCP("Aider-Factory")

# Import and register MCP tools conditionally to maintain separation of concerns
load_business_tools = os.environ.get("LOAD_BUSINESS_TOOLS", "false").lower() == "true"

if load_business_tools:
    print("Loading business tools (Application Plane)...")
    try:
        from agent.infrastructure.mcp.tools.arxiv import get_arxiv_search_mcp_tool
        arxiv_tool = get_arxiv_search_mcp_tool()
        mcp.add_tool(arxiv_tool.name, arxiv_tool.handler)
        print(f"✓ Registered arxiv tool: {arxiv_tool.name}")
    except Exception as e:
        print(f"✗ Failed to register arxiv tool: {e}")

    try:
        from agent.infrastructure.mcp.tools.orchestrator import get_orchestrator_mcp_tool
        orchestrator_tool = get_orchestrator_mcp_tool()
        mcp.add_tool(orchestrator_tool.name, orchestrator_tool.handler)
        print(f"✓ Registered orchestrator tool: {orchestrator_tool.name}")
    except Exception as e:
        print(f"✗ Failed to register orchestrator tool: {e}")

    try:
        from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool
        unpaywall_tool = get_unpaywall_mcp_tool()
        mcp.add_tool(unpaywall_tool.name, unpaywall_tool.handler)
        print(f"✓ Registered unpaywall tool: {unpaywall_tool.name}")
    except Exception as e:
        print(f"✗ Failed to register unpaywall tool: {e}")

    try:
        from agent.infrastructure.mcp.tools.zotero import get_zotero_save_mcp_tool
        zotero_tool = get_zotero_save_mcp_tool()
        mcp.add_tool(zotero_tool.name, zotero_tool.handler)
        print(f"✓ Registered zotero tool: {zotero_tool.name}")
    except Exception as e:
        print(f"✗ Failed to register zotero tool: {e}")
else:
    print("Skipping business tools (Control Plane mode). Only meta-tools available.")


@mcp.tool()
async def execute_tdd_loop(
    project_root: str,
    interface_file: str,
    impl_file: str,
    test_file: str,
    instructions: str,
    model: str = "dashscope/qwen-max"
) -> str:
    """
    Executes the Aider TDD loop in the specified project.
    
    Args:
        project_root: The mount path of the project inside the container (usually /app)
        interface_file: Path to the interface file (e.g. backend/src/agent/domain/ports/xyz.py)
        impl_file: Path to the implementation file
        test_file: Path to the test file
        instructions: The task description for Aider
        model: The model Aider should use, defaults to dashscope/qwen-max
    """
    # Switch to project root
    if os.path.isabs(project_root):
        os.chdir(project_root)
    else:
        os.chdir(os.path.abspath(project_root))
        
    print(f"Working directory: {os.getcwd()}", file=sys.stderr)

    # Load environment variables from .env file if available
    load_dotenv(os.path.join(project_root, ".env"))

    # Build Aider command
    # Note: --yes to auto-confirm, --no-suggest-shell-commands to reduce noise
    cmd = [
        "aider", 
        "--model", model, 
        "--yes", 
        "--no-suggest-shell-commands",
        "--read", interface_file,
        "--file", impl_file, 
        "--file", test_file,
        "--lint-cmd", f"ruff check {impl_file} {test_file} --fix",
        "--test-cmd", f"pytest {test_file}",
        "--message", instructions
    ]
    
    # 注入 DASHSCOPE_API_BASE (如果存在)
    env = os.environ.copy()
    if os.environ.get("DASHSCOPE_API_BASE"):
         env["DASHSCOPE_API_BASE"] = os.environ.get("DASHSCOPE_API_BASE")
         # 有些 openai 兼容库可能需要 OPENAI_API_BASE
         env["OPENAI_API_BASE"] = os.environ.get("DASHSCOPE_API_BASE")

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE,
            env=env
        )
        stdout, stderr = await process.communicate()
        
        output = f"## Execution Result\n\n### STDOUT\n{stdout.decode()}\n\n### STDERR\n{stderr.decode()}"
        return output
    except Exception as e:
        return f"Error executing Aider: {str(e)}"

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(mcp.run())
    except Exception as e:
        print(f"MCP server error: {e}", file=sys.stderr)
        sys.exit(1)
