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
import subprocess
import time
import requests
import threading
import signal

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

def _run_server_process(module_path, port, mode, name, extra_args=None):
    """Helper to run a server process."""
    if extra_args is None:
        extra_args = []
        
    cmd = [sys.executable, "-m", module_path]
    
    if mode == "sse":
        cmd.extend(["--mode", "sse", "--port", str(port)])
        cmd.extend(extra_args)
        print(f"Starting {name} server in SSE mode on port {port}...")
        try:
            process = subprocess.Popen(cmd)
            time.sleep(0.5) # Give it a moment to possibly fail
            if process.poll() is not None:
                print(f"Failed to start {name} server (exited with code {process.returncode})")
                return None
            print(f"{name} server started on port {port} (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"Error starting {name} server: {e}")
            return None
    else:
        print(f"Starting {name} server in stdio mode...")
        cmd.extend(extra_args)
        subprocess.run(cmd)
        return None

def run_federal_academic_search_server(port=8001, auto_port=False, mode="sse"):
    """Run the Federal Academic Search MCP server."""
    original_port = port
    if auto_port and mode == "sse":
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        # Check imports to ensure dependencies are met
        import mcp_servers.federal_academic_search.main
        return _run_server_process(
            "mcp_servers.federal_academic_search.main", 
            port, mode, "Federal Academic Search"
        )
    except ImportError as e:
        print(f"Error importing Federal Academic Search server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/federal_academic_search/requirements.txt")
    except Exception as e:
        print(f"Error running Federal Academic Search server: {e}")
    return None

def run_semantic_scholar_server(port=8002, auto_port=False, mode="sse"):
    """Run the Federal Academic Search MCP server (replaces legacy Semantic Scholar server)."""
    original_port = port
    if auto_port and mode == "sse":
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        # Check imports
        import mcp_servers.federal_academic_search.main
        return _run_server_process(
            "mcp_servers.federal_academic_search.main", 
            port, mode, "Legacy Semantic Scholar (Federal Backend)"
        )
    except ImportError as e:
        print(f"Error importing Semantic Scholar server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/federal_academic_search/requirements.txt")
    except Exception as e:
        print(f"Error running Semantic Scholar server: {e}")
    return None

def run_zotero_expert_server(port=8003, auto_port=False, mode="sse"):
    """Run the Zotero Expert MCP server."""
    original_port = port
    if auto_port and mode == "sse":
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        import mcp_servers.zotero_expert.main
        return _run_server_process(
            "mcp_servers.zotero_expert.main", 
            port, mode, "Zotero Expert"
        )
    except ImportError as e:
        print(f"Error importing Zotero Expert server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/zotero_expert/requirements.txt")
    except Exception as e:
        print(f"Error running Zotero Expert server: {e}")
    return None

def run_manuscript_manager_server(port=8004, auto_port=False, mode="sse"):
    """Run the Manuscript Manager MCP server."""
    original_port = port
    if auto_port and mode == "sse":
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        import mcp_servers.manuscript_manager.main
        return _run_server_process(
            "mcp_servers.manuscript_manager.main", 
            port, mode, "Manuscript Manager"
        )
    except ImportError as e:
        print(f"Error importing Manuscript Manager server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/manuscript_manager/requirements.txt")
    except Exception as e:
        print(f"Error running Manuscript Manager server: {e}")
    return None

def run_duckdb_memory_server(port=8005, auto_port=False, mode="sse"):
    """Run the DuckDB Memory MCP server."""
    original_port = port
    if auto_port and mode == "sse":
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        # Note: DuckDB requirement might fail import if not present, handle that
        import mcp_servers.duckdb_memory.main
        return _run_server_process(
            "mcp_servers.duckdb_memory.main", 
            port, mode, "DuckDB Memory"
        )
    except ImportError as e:
        print(f"Error importing DuckDB Memory server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/duckdb_memory/requirements.txt")
        print("Note: DuckDB is required for this server.")
    except Exception as e:
        print(f"Error running DuckDB Memory server: {e}")
    return None

def run_sros_logic_server(port=8006, auto_port=False, mode="sse"):
    """Run the SROS Logic MCP server."""
    original_port = port
    if auto_port and mode == "sse":
        while not check_port(port):
            port += 1
        if port != original_port:
            print(f"Port {original_port} unavailable. Using port {port} instead.")

    try:
        import mcp_servers.mcp_sros_logic.main
        return _run_server_process(
            "mcp_servers.mcp_sros_logic.main", 
            port, mode, "SROS Logic"
        )
    except ImportError as e:
        print(f"Error importing SROS Logic server: {e}")
        print("Please install required dependencies: pip install -r mcp_servers/mcp_sros_logic/requirements.txt")
    except Exception as e:
        print(f"Error running SROS Logic server: {e}")
    return None

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
    
    processes = []
    
    try:
        for name, runner, port in servers:
            try:
                p = runner(port, auto_port=auto_port)
                if p:
                    processes.append(p)
                else:
                    print(f"Warning: {name} did not start or returned no process handle.")
            except Exception as e:
                print(f"Failed to start {name} server: {e}")
        
        if not processes:
            print("No servers started.")
            return

        print("\nAll servers operational. Press Ctrl+C to stop.")
        
        # Keep the script running to maintain the processes
        while True:
            time.sleep(1)
            # Check if processes are still alive
            for p in processes:
                if p.poll() is not None:
                    print(f"Process {p.pid} exited unexpectedly with code {p.returncode}")
                    processes.remove(p)
            if not processes:
                print("All servers have exited.")
                break
                
    except KeyboardInterrupt:
        print("\nStopping all servers...")
    finally:
        for p in processes:
            if p.poll() is None:
                print(f"Terminating process {p.pid}...")
                p.terminate()
                try:
                    p.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    p.kill()
        print("Shutdown complete.")


def wait_for_gateway_health(port=8000, timeout=60):
    """Wait for gateway to become healthy by polling health endpoint."""
    print(f"⏳ Waiting for Gateway to warm up on port {port}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "healthy" and health_data.get("ready", False):
                    print("✅ SYSTEM READY!")
                    print(f"📊 Health check passed: {health_data}")
                    return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
    
    print("❌ Gateway health check timeout!")
    return False


def main():
    """Main entry point."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Run SROS MCP servers")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["gateway", "federal-academic-search", "legacy-semantic-scholar", "zotero-expert", "manuscript-manager", "duckdb-memory", "sros-logic", "all"],
        default="gateway",
        help="Mode to run (gateway for V2.2, or individual servers for legacy)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=0, # Changed default to 0 to indicate "use server default"
        help="Port to run the server on (default: server specific)"
    )
    parser.add_argument(
        "--auto-port",
        action="store_true",
        help="Automatically find available port if default is occupied"
    )
    parser.add_argument(
        "--no-health-check",
        action="store_true",
        help="Skip health check after gateway startup"
    )

    args = parser.parse_args()
    
    # If gateway mode is selected, run the gateway server
    if args.mode == "gateway":
        print("🚀 Starting SROS Gateway (V2.2 Hub-and-Spoke Mode)...")
        print("   - Port: 8000 (SSE)")
        print("   - Transport: Stdio for sub-services")
        print("   - SSE Endpoint: http://localhost:8000/sse")
        print("   - Health Endpoint: http://localhost:8000/health")
        
        # Check port availability
        port_to_use = 8000  # Default gateway port
        if args.port != 0:
            port_to_use = args.port
            
        if args.auto_port:
            # Find available port starting from 8000
            for p in range(8000, 8020):
                if check_port(p):
                    port_to_use = p
                    break
            else:
                print("❌ No available ports found!")
                return 1
        else:
            if not check_port(port_to_use):
                print(f"❌ Port {port_to_use} is already in use!")
                return 1
        
        # Start gateway server
        cmd = [sys.executable, "-m", "mcp_servers.sros_gateway.main", "--port", str(port_to_use)]
        
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        try:
            print(f"✅ Starting gateway on port {port_to_use}...")
            # Use Popen instead of run to handle signals properly
            process = subprocess.Popen(cmd, env=env)
            
            # Register signal handler to gracefully stop child process
            def signal_handler(sig, frame):
                print("\n🛑 Received stop signal. Terminating Gateway...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                sys.exit(0)
                
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Wait a bit for gateway to start accepting connections
            time.sleep(2)
            
            # Perform health check if not disabled
            if not args.no_health_check:
                if wait_for_gateway_health(port_to_use):
                    print("\n🎉 Gateway is fully operational!")
                    print("💡 You can now connect to Roo Code - Gateway is ready to handle requests")
                else:
                    print("\n⚠️  Gateway started but health check failed")
                    print("   Proceed with caution - some services may not be ready")
            
            # Wait for process
            process.wait()
            
        except KeyboardInterrupt:
            # This might be caught by signal handler first, but just in case
            print("\n🛑 Gateway stopped. All sub-processes cleaned up.")
            if 'process' in locals() and process.poll() is None:
                process.terminate()
                process.wait()
        except Exception as e:
            print(f"❌ Gateway failed: {e}")
            if 'process' in locals() and process.poll() is None:
                process.kill()
            return 1
    else:
        # Legacy server mode
        server = args.mode
        
        # Helper to handle single server run with keep-alive
        def run_wrapper(runner, default_port):
            port = args.port if args.port != 0 else default_port
            p = runner(port, auto_port=args.auto_port)
            if p:
                try:
                    print(f"Server running. Press Ctrl+C to stop.")
                    p.wait()
                except KeyboardInterrupt:
                    print("\nStopping server...")
                    p.terminate()
                    p.wait()

        if server == "federal-academic-search":
            run_wrapper(run_federal_academic_search_server, 8001)
        elif server == "legacy-semantic-scholar":
            run_wrapper(run_semantic_scholar_server, 8002)
        elif server == "zotero-expert":
            run_wrapper(run_zotero_expert_server, 8003)
        elif server == "manuscript-manager":
            run_wrapper(run_manuscript_manager_server, 8004)
        elif server == "duckdb-memory":
            run_wrapper(run_duckdb_memory_server, 8005)
        elif server == "sros-logic":
            run_wrapper(run_sros_logic_server, 8006)
        elif server == "all":
            run_all_servers(auto_port=args.auto_port)


if __name__ == "__main__":
    main()
