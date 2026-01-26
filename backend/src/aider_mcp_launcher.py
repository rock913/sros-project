import asyncio
import os
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Initialize MCP Server
mcp = FastMCP("Aider-Factory")

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
    mcp.run()
