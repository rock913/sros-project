# SROS CLI Commands Specification

## 1. Overview

This document provides detailed specifications for the three core SROS CLI commands: `sros init`, `sros start`, and `sros status`. Each command is designed to provide a seamless user experience while maintaining the powerful functionality of the SROS research automation system.

## 2. Command: sros init

### 2.1 Purpose
Initialize a new SROS research workspace with all necessary files and configurations.

### 2.2 Usage
```
sros init [OPTIONS] PROJECT_NAME
```

### 2.3 Arguments
- `PROJECT_NAME` (required): Name of the research project/directory to create

### 2.4 Options
- `--template TEXT`: Use a specific project template (default: "default")
- `--force`: Overwrite existing directory if it exists
- `--quiet`: Suppress non-error output
- `--verbose`: Show detailed output

### 2.5 Implementation Details

#### 2.5.1 Directory Structure Creation
```
PROJECT_NAME/
├── draft.md              # Main research document
├── ideas.md              # Initial hypotheses and concepts
├── .env                  # Environment variables
├── .roomodes             # Roo Code behavior configuration
├── .gitignore            # Git ignore patterns
├── materials/            # Supporting materials
│   ├── notes.md
│   └── references/
├── references/           # Formal citations
└── .sros/                # Hidden SROS state directory
    ├── graph.db          # Local knowledge graph (DuckDB)
    ├── research_log.jsonl # Research activity log
    └── config.json       # Project-specific SROS config
```

#### 2.5.2 Configuration Generation
- Generate `.roo/mcp.json` with Gateway SSE endpoint
- Create `.roomodes` with SROS-Writer and SROS-Researcher prompts
- Initialize `.env` with example API keys
- Set up `.gitignore` for SROS-specific files

#### 2.5.3 Implementation Pseudocode
```python
@app.command()
def init(
    name: str = typer.Argument(..., help="Name of your research project"),
    template: str = typer.Option("default", help="Project template to use"),
    force: bool = typer.Option(False, help="Overwrite existing directory"),
    quiet: bool = typer.Option(False, help="Suppress non-error output"),
    verbose: bool = typer.Option(False, help="Show detailed output")
):
    """Initialize a new SROS research workspace."""
    
    # 1. Validate project name and check existence
    target_dir = Path.cwd() / name
    if target_dir.exists() and not force:
        console.print(f"[red]Error: Directory '{name}' already exists.[/red]")
        raise typer.Exit(code=1)
    
    # 2. Create directory structure
    dirs_to_create = [
        target_dir / "materials",
        target_dir / "references", 
        target_dir / ".sros",
        target_dir / ".roo"
    ]
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # 3. Create initial content files
    create_draft_md(target_dir)
    create_ideas_md(target_dir)
    create_env_file(target_dir)
    create_gitignore(target_dir)
    
    # 4. Generate SROS-specific configurations
    generate_mcp_config(target_dir)  # .roo/mcp.json
    generate_roomodes(target_dir)    # .roomodes
    initialize_duckdb(target_dir)    # .sros/graph.db
    
    # 5. Success message and next steps
    console.print(f"[green]✅ Project '{name}' initialized successfully![/green]")
    console.print(f"👉 cd {name}")
    console.print(f"👉 sros start (in a separate terminal)")
    console.print(f"👉 Open VS Code in this folder")
```

### 2.6 Error Handling
- Directory already exists (without --force)
- Insufficient disk space
- Permission denied
- Invalid project name

## 3. Command: sros start

### 3.1 Purpose
Start the SROS Gateway and all sub-services for research automation.

### 3.2 Usage
```
sros start [OPTIONS]
```

### 3.3 Options
- `--port INTEGER`: Port for Gateway (default: 8000)
- `--auto-port`: Automatically find available port
- `--no-health-check`: Skip health check after startup
- `--background`: Run in background (future enhancement)
- `--timeout INTEGER`: Health check timeout in seconds (default: 60)

### 3.4 Implementation Details

#### 3.4.1 Startup Sequence
1. Validate environment and dependencies
2. Check port availability
3. Start Gateway server with embedded sub-servers
4. Wait for health check readiness
5. Report system status

#### 3.4.2 Process Management
- Manage Gateway subprocess lifecycle
- Handle graceful shutdown on SIGINT/SIGTERM
- Monitor sub-server health
- Provide detailed error reporting

#### 3.4.3 Implementation Pseudocode
```python
@app.command()
def start(
    port: int = typer.Option(8000, help="Port for Gateway"),
    auto_port: bool = typer.Option(False, help="Auto-find available port"),
    no_health_check: bool = typer.Option(False, help="Skip health check"),
    timeout: int = typer.Option(60, help="Health check timeout")
):
    """Start the SROS Gateway and all sub-services."""
    
    console.print("[bold blue]🚀 Starting SROS System...[/bold blue]")
    
    # 1. Validate environment
    if not validate_environment():
        console.print("[red]❌ Environment validation failed[/red]")
        raise typer.Exit(code=1)
    
    # 2. Determine port
    actual_port = port
    if auto_port:
        actual_port = find_available_port(port)
    
    # 3. Start Gateway
    gateway_process = start_gateway(actual_port)
    
    # 4. Wait for health check
    if not no_health_check:
        if not wait_for_health_check(actual_port, timeout):
            console.print("[red]❌ Gateway health check failed[/red]")
            gateway_process.terminate()
            raise typer.Exit(code=1)
    
    # 5. Success
    console.print(f"[green]✅ SYSTEM READY![/green]")
    console.print(f"📡 Gateway listening on http://localhost:{actual_port}")
    console.print(f"🔗 SSE endpoint: http://localhost:{actual_port}/sse")
    
    # 6. Wait for process or handle signals
    try:
        gateway_process.wait()
    except KeyboardInterrupt:
        console.print("\n[blue]🛑 Shutting down Gateway...[/blue]")
        gateway_process.terminate()
        gateway_process.wait()
```

### 3.5 Error Handling
- Port already in use
- Missing dependencies
- Gateway startup failure
- Health check timeout
- Signal interruption

## 4. Command: sros status / sros doctor

### 4.1 Purpose
Check system health and diagnose potential issues.

### 4.2 Usage
```
sros status [OPTIONS]
sros doctor [OPTIONS]
```

### 4.3 Options
- `--format TEXT`: Output format (json, yaml, table) (default: table)
- `--verbose`: Show detailed diagnostic information
- `--checks TEXT`: Specific checks to run (comma-separated)

### 4.4 Implementation Details

#### 4.4.1 Status Checks
- **Environment**: Python version, required packages
- **Dependencies**: MCP, Starlette, Uvicorn, DuckDB
- **Ports**: Gateway port availability
- **Processes**: Running Gateway instances
- **Files**: Configuration file integrity
- **Permissions**: Write access to necessary directories

#### 4.4.2 Doctor Checks (Extended Diagnostics)
- **Network**: Connectivity to external services
- **Performance**: System resource usage
- **Logs**: Recent error messages
- **Config**: Configuration consistency
- **Storage**: Disk space and database integrity

#### 4.4.3 Implementation Pseudocode
```python
@app.command()
def status(
    format: str = typer.Option("table", help="Output format"),
    verbose: bool = typer.Option(False, help="Show detailed info"),
    checks: str = typer.Option(None, help="Specific checks to run")
):
    """Check SROS system status."""
    
    status_report = collect_status_info(checks)
    
    if format == "json":
        console.print_json(data=status_report)
    elif format == "yaml":
        import yaml
        console.print(yaml.dump(status_report))
    else:  # table
        display_status_table(status_report)

@app.command()
def doctor(
    format: str = typer.Option("table", help="Output format"),
    verbose: bool = typer.Option(False, help="Show detailed diagnostics"),
    checks: str = typer.Option(None, help="Specific checks to run")
):
    """Run comprehensive system diagnostics."""
    
    diagnostic_report = run_comprehensive_diagnostics(checks, verbose)
    
    if format == "json":
        console.print_json(data=diagnostic_report)
    else:
        display_diagnostic_results(diagnostic_report)

def collect_status_info(checks=None):
    """Collect basic system status information."""
    report = {}
    
    # Environment check
    report['environment'] = check_environment()
    
    # Dependencies check
    report['dependencies'] = check_dependencies()
    
    # Gateway status
    report['gateway'] = check_gateway_status()
    
    # Project context
    report['project'] = check_current_project()
    
    return report

def run_comprehensive_diagnostics(checks=None, verbose=False):
    """Run extended diagnostic checks."""
    report = {}
    
    # Include basic status
    report.update(collect_status_info())
    
    # Extended checks
    report['network'] = check_network_connectivity()
    report['storage'] = check_storage_health()
    report['performance'] = check_performance_metrics()
    report['logs'] = analyze_recent_logs()
    
    return report
```

### 4.5 Output Formats
- **Table**: Human-readable summary
- **JSON**: Machine-readable format for automation
- **YAML**: Configurable format for documentation

## 5. Common Features

### 5.1 Help System
All commands provide comprehensive help with:
- Usage examples
- Option descriptions
- Default values
- Related commands

### 5.2 Color Output
- Green: Success messages
- Red: Error messages
- Blue: Informational messages
- Yellow: Warning messages

### 5.3 Progress Indicators
- Spinner animations for long operations
- Progress bars for multi-step processes
- Estimated time remaining

### 5.4 Configuration Override
Commands can accept configuration overrides via:
- Environment variables
- Command-line options
- Project-specific config files

## 6. Integration Points

### 6.1 Roo Code Integration
- Automatic `.roo/mcp.json` generation
- SSE endpoint configuration
- Tool namespace mapping

### 6.2 External Services
- API key validation
- Service connectivity checks
- Rate limit awareness

### 6.3 Version Management
- Version checking against remote
- Upgrade notifications
- Compatibility verification

This specification ensures consistent, user-friendly command interfaces while maintaining the powerful functionality of the SROS research automation system.