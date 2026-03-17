# SROS V2.3 CLI Implementation Plan

## 1. Executive Summary

The SROS V2.3 upgrade transforms the current coupled architecture into a decoupled CLI-based system. This plan outlines the implementation of a Python package that provides the `sros` command-line interface, enabling users to initialize research projects independently of the source code repository.

## 2. Current Architecture Analysis

### 2.1 Pain Points Identified
- **Coupling Issue**: Tool source code (`mcp_servers/`) mixed with user data (`workspace/`)
- **Installation Complexity**: Users must clone entire repo and configure Python environment
- **Directory Confusion**: User papers buried in source code structure
- **Environment Dependencies**: Manual pip installation prone to conflicts
- **Startup Complexity**: Must run from source root directory
- **Context Interference**: Roo Code indexes all Python code, causing token waste and hallucinations

### 2.2 Current Components
- **Gateway**: Central hub managing sub-servers via stdio
- **Sub-servers**: Federal Academic Search, Manuscript Manager, DuckDB Memory, Context Ingester, Zotero Expert
- **Configuration**: `.roo/mcp.json` for Roo Code integration
- **Runtime**: `run_servers.py` for launching services

## 3. Target Architecture

### 3.1 Decoupled Design
```
User Space: Independent research projects with sros CLI
     ↓ (pip install sros)
Package Space: Installed sros package with embedded servers
```

### 3.2 New User Flow
1. `pip install sros` - Install CLI tool
2. `sros init my-paper` - Initialize project anywhere
3. `cd my-paper && sros start` - Start services locally
4. Open VS Code - Auto-configured for SROS

## 4. Package Structure Design

### 4.1 Proposed Directory Structure
```
/sros-package/
├── pyproject.toml              # [CORE] Package definition and CLI entry
├── src/
│   └── sros/                   # Main package
│       ├── __init__.py
│       ├── cli.py              # [NEW] CLI entry logic (Typer/Click)
│       ├── gateway/            # Gateway server code
│       │   ├── __init__.py
│       │   ├── main.py         # Gateway implementation
│       │   └── config.json     # Server configuration
│       ├── servers/            # Sub-server implementations
│       │   ├── federal_academic_search/
│       │   ├── manuscript_manager/
│       │   ├── duckdb_memory/
│       │   ├── context_ingester/
│       │   └── zotero_expert/
│       ├── templates/          # Project templates
│       │   ├── .roomodes
│       │   └── prompts/
│       └── utils/              # Utilities and runner
│           ├── __init__.py
│           ├── runner.py       # System startup logic
│           └── project_init.py # Project initialization
└── README.md
```

### 4.2 Package Metadata (pyproject.toml)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sros"
version = "2.3.0"
description = "Scientific Research Operating System - CLI Edition"
authors = [{name = "SROS Team", email = "team@sros.org"}]
license = {text = "MIT"}
dependencies = [
    "mcp>=1.0.0",
    "starlette>=0.30.0",
    "uvicorn>=0.20.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "duckdb>=0.10.0",
    "pandas>=2.0.0",
    "requests>=2.30.0"
]

[project.scripts]
sros = "sros.cli:app"  # Register 'sros' command
```

## 5. CLI Command Specifications

### 5.1 sros init [project_name]
**Purpose**: Initialize a new SROS research workspace

**Behavior**:
- Creates directory `project_name`
- Creates standard structure: `draft.md`, `materials/`, `references/`, `ideas.md`
- Generates `.roo/mcp.json` pointing to `http://localhost:8000/sse`
- Copies `.roomodes` template with SROS-Writer and SROS-Researcher prompts
- Initializes `.sros/` hidden directory and DuckDB database

**Implementation**:
```python
@app.command()
def init(name: str = typer.Argument(..., help="Name of your research project")):
    """Initialize a new SROS research workspace."""
    # Implementation details...
```

### 5.2 sros start [--port PORT]
**Purpose**: Start the SROS Gateway and all sub-services

**Behavior**:
- Starts Gateway server from installed package
- Waits for health check to pass
- Prints "SYSTEM READY" when operational
- Handles port conflicts with auto-assignment

**Implementation**:
```python
@app.command()
def start(port: int = typer.Option(8000, help="Port for Gateway")):
    """Start the SROS Gateway and all sub-services."""
    # Implementation details...
```

### 5.3 sros status / sros doctor
**Purpose**: Environment self-check and diagnostics

**Behavior**:
- Checks dependency completeness
- Verifies Gateway port availability
- Validates DuckDB file integrity
- Reports system health status

**Implementation**:
```python
@app.command()
def status():
    """Check SROS system status."""
    # Implementation details...

@app.command()
def doctor():
    """Run comprehensive system diagnostics."""
    # Implementation details...
```

## 6. Implementation Phases

### Phase 1: Package Structure Setup
- [ ] Restructure current codebase to package format
- [ ] Create pyproject.toml with proper dependencies
- [ ] Move gateway and server code to src/sros/
- [ ] Set up proper imports and namespace packages

### Phase 2: CLI Development
- [ ] Implement sros init command
- [ ] Implement sros start command
- [ ] Implement sros status/doctor commands
- [ ] Add proper error handling and user feedback

### Phase 3: Integration and Testing
- [ ] Test package installation and distribution
- [ ] Verify all sub-servers work from installed package
- [ ] Test cross-platform compatibility
- [ ] Validate Roo Code integration

### Phase 4: Migration Support
- [ ] Create migration guide for existing users
- [ ] Provide backward compatibility for current workflow
- [ ] Update documentation for new workflow

## 7. Technical Considerations

### 7.1 Resource Access
- Embed server configurations as package data
- Use pkg_resources or importlib.resources for template access
- Handle file paths correctly in installed environment

### 7.2 Process Management
- Properly manage subprocess lifecycle for sub-servers
- Implement graceful shutdown handling
- Add health check integration with startup process

### 7.3 Configuration Management
- Generate project-specific configs during init
- Maintain backward compatibility with existing setups
- Handle environment variable propagation to sub-servers

## 8. Migration Strategy

### 8.1 From Coupled to Decoupled
1. **Existing Users**: Continue supporting current workflow during transition
2. **New Users**: Default to CLI-based workflow
3. **Documentation**: Update all guides to reflect new approach
4. **Tools**: Provide migration utilities for existing projects

### 8.2 Backward Compatibility
- Maintain `run_servers.py` for development/testing
- Support both configuration formats during transition period
- Provide clear deprecation timeline

## 9. Success Metrics

### 9.1 Usability Improvements
- Installation time reduced from minutes to seconds
- New user onboarding simplified from 5 steps to 3 steps
- Zero configuration required for basic usage

### 9.2 Technical Improvements
- Complete separation of user data and tool code
- Elimination of context interference issues
- Improved dependency isolation

## 10. Risk Mitigation

### 10.1 Potential Issues
- Packaging complexity with multiple server dependencies
- Cross-platform compatibility challenges
- Performance overhead from package distribution

### 10.2 Mitigation Strategies
- Thorough testing across platforms
- Incremental rollout with fallback options
- Comprehensive documentation and support