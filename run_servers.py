#!/usr/bin/env python3
"""
Unified entry point for running all SROS MCP servers.
This script provides a convenient way to start individual or all MCP servers.
"""

import argparse
import sys
import os
import logging
from pathlib import Path
import socket

def check_port(port, host='127.0.0.1'):
    """Check if a port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

# Add the mcp_servers directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "mcp_servers"))

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

def setup_logging():
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def run_federal_academic_search_server(port=8001, auto_port=False):
    """Run the Federal Academic Search MCP server."""
    original_port = port
    if auto_port:
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        from federal_academic_search.main import main as federal_academic_search_main
        print(f"Starting Federal Academic Search server on port {port}...")
        # Note: Federal Academic Search server doesn't currently use port parameter
        federal_academic_search_main()
    except ImportError as e:
        print(f"Error importing Federal Academic Search server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/federal_academic_search/requirements.txt")
    except Exception as e:
        print(f"Error running Federal Academic Search server: {e}")

def run_semantic_scholar_server(port=8002, auto_port=False):
    """Run the Federal Academic Search MCP server (replaces legacy Semantic Scholar server)."""
    original_port = port
    if auto_port:
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        from federal_academic_search.main import main as federal_academic_search_main
        print(f"Starting Federal Academic Search server on port {port}...")
        # Note: Federal Academic Search server doesn't currently use port parameter
        federal_academic_search_main()
    except ImportError as e:
        print(f"Error importing Federal Academic Search server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/federal_academic_search/requirements.txt")
    except Exception as e:
        print(f"Error running Federal Academic Search server: {e}")

def run_zotero_expert_server(port=8003, auto_port=False):
    """Run the Zotero Expert MCP server."""
    original_port = port
    if auto_port:
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        from zotero_expert.main import main as zotero_expert_main
        print(f"Starting Zotero Expert server on port {port}...")
        zotero_expert_main(port=port)
    except ImportError as e:
        print(f"Error importing Zotero Expert server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/zotero_expert/requirements.txt")
    except Exception as e:
        print(f"Error running Zotero Expert server: {e}")

def run_manuscript_manager_server(port=8004, auto_port=False):
    """Run the Manuscript Manager MCP server."""
    original_port = port
    if auto_port:
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        from manuscript_manager.main import main as manuscript_manager_main
        print(f"Starting Manuscript Manager server on port {port}...")
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create a new task
            loop.create_task(manuscript_manager_main(port=port))
        else:
            # If loop is not running, run until complete
            loop.run_until_complete(manuscript_manager_main(port=port))
    except ImportError as e:
        print(f"Error importing Manuscript Manager server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/manuscript_manager/requirements.txt")
    except Exception as e:
        print(f"Error running Manuscript Manager server: {e}")

def run_duckdb_memory_server(port=8005, auto_port=False):
    """Run the DuckDB Memory MCP server."""
    original_port = port
    if auto_port:
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        from duckdb_memory.main import main as duckdb_memory_main
        print(f"Starting DuckDB Memory server on port {port}...")
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create a new task
            loop.create_task(duckdb_memory_main(port=port))
        else:
            # If loop is not running, run until complete
            loop.run_until_complete(duckdb_memory_main(port=port))
    except ImportError as e:
        print(f"Error importing DuckDB Memory server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/duckdb_memory/requirements.txt")
        print("Note: DuckDB is required for this server.")
    except Exception as e:
        print(f"Error running DuckDB Memory server: {e}")

def run_sros_logic_server(port=8006, auto_port=False):
    """Run the SROS Logic MCP server."""
    original_port = port
    if auto_port:
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        from mcp_sros_logic.main import main as sros_logic_main
        print(f"Starting SROS Logic server on port {port}...")
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create a new task
            loop.create_task(sros_logic_main(port=port))
        else:
            # If loop is not running, run until complete
            loop.run_until_complete(sros_logic_main(port=port))
    except ImportError as e:
        print(f"Error importing SROS Logic server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/mcp_sros_logic/requirements.txt")
    except Exception as e:
        print(f"Error running SROS Logic server: {e}")
def run_all_servers(auto_port=False):
    """Run all MCP servers simultaneously."""
    print("Starting all SROS MCP servers...")
    
    # Import and run all servers
    servers = [
        ("Federal Academic Search", run_federal_academic_search_server, 8001),
        ("Legacy Semantic Scholar (Federal Backend)", run_semantic_scholar_server, 8002),
        ("Zotero Expert", run_zotero_expert_server, 8003),
        ("Manuscript Manager", run_manuscript_manager_server, 8004),
        ("DuckDB Memory", run_duckdb_memory_server, 8005),
        ("SROS Logic", run_sros_logic_server, 8006)
    ]
    
    for name, runner, port in servers:
        try:
            runner(port, auto_port=auto_port)
        except Exception as e:
            print(f"Failed to start {name} server: {e}")


def main():
    """Main entry point."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Run SROS MCP servers")
    parser.add_argument(
        "server",
        nargs="?",
        choices=["federal-academic-search", "legacy-semantic-scholar", "zotero-expert", "manuscript-manager", "duckdb-memory", "sros-logic", "all"],
        help="Which server to run (legacy-semantic-scholar now runs the federal academic search backend)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )
    parser.add_argument(
        "--auto-port",
        action="store_true",
        help="Automatically find available port if default is occupied"
    )

    args = parser.parse_args()
    
    if not args.server:
        parser.print_help()
        return
    if args.server == "federal-academic-search":
        run_federal_academic_search_server(args.port, auto_port=args.auto_port)
    elif args.server == "legacy-semantic-scholar":
        run_semantic_scholar_server(args.port, auto_port=args.auto_port)
    elif args.server == "zotero-expert":
        run_zotero_expert_server(args.port, auto_port=args.auto_port)
    elif args.server == "manuscript-manager":
        run_manuscript_manager_server(args.port, auto_port=args.auto_port)
    elif args.server == "duckdb-memory":
        run_duckdb_memory_server(args.port, auto_port=args.auto_port)
    elif args.server == "sros-logic":
        run_sros_logic_server(args.port, auto_port=args.auto_port)
    elif args.server == "all":
        run_all_servers(auto_port=args.auto_port)


if __name__ == "__main__":
    main()