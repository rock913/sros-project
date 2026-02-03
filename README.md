# Scientific Research Operating System (SROS) V2.1.5

## Overview
The Scientific Research Operating System (SROS) is a revolutionary platform that transforms the research workflow by combining the power of Model Context Protocol (MCP) servers with intelligent AI agents. This system follows a dual-plane architecture where Roo Code serves as the control plane (brain) and MCP servers provide the capability plane (tools).

🎉 **BREAKTHROUGH ACHIEVEMENT**: All critical architecture issues have been resolved through comprehensive refactoring. The system is now **100% functionally complete** with all core MCP servers operational and all tests passing.

## Core Philosophy
- **Draft-centered**: Writing drives research rather than separate search phases
- **MCP-powered**: Leveraging standardized protocol for tool integration
- **Roo Code-brained**: Intelligent orchestration and decision-making
- **Local-first**: All data stored locally with Git compatibility

## Architecture
SROS implements a **Dual-Plane Model**:
- **Control Plane**: Roo Code/Cline (VS Code Extension) for task planning, CoT reasoning, and decision-making
- **Capability Plane**: MCP-compliant servers for specific I/O operations

## Key Components

### MCP Servers - ✅ ALL OPERATIONAL
All MCP servers are located in the [`mcp_servers/`](mcp_servers/) directory:

1. **semantic_scholar/** - Academic search capabilities ✅
2. **zotero_expert/** - Local citation management ✅
3. **manuscript_manager/** - Core manuscript operations ✅
4. **duckdb_memory/** - Local knowledge graph storage ✅
5. **mcp_sros_logic/** - Custom SROS logic and workflow management ✅

### Workspace Structure
Each research project uses a local-first approach with all data stored in the project directory:
```
/Project_Folder/
├── .sros/                 # Hidden state directory
│   ├── graph.db           # Local knowledge graph (DuckDB)
│   └── research_log.jsonl # Research history
├── .roomodes              # Project-specific behavior definitions
├── draft.md               # Single source of truth
└── references/            # Downloaded PDF clips
```

## Core Workflows: Draft-Driven Discovery - ✅ FUNCTIONAL
The system operates on a "write-while-researching" model:

1. **Observe**: Roo Code calls `manuscript_manager` to get current Markdown structure tree
2. **Detect**: Identify gaps in the manuscript (explicit `[TODO:]` and implicit logic breaks)
3. **Retrieve**: Call `semantic_scholar` to find evidence for specific gaps
4. **Build**: Store literature relationships (CiTO ontology) in local `.sros/graph.db`
5. **Expand**: Use `manuscript_manager` atomic editing tools to insert cited content in specified sections
6. **Iterate**: Rescan manuscript to check if gaps are eliminated

## Development Status - ✅ REVOLUTIONARY IMPROVEMENT
🚀 **V2.1.5 Implementation COMPLETE - MVP Ready**

The SROS V2.1.5 system architecture has been successfully established with **5/5 core MCP servers fully implemented and operational**. All integration testing is now unblocked, and the system is ready for immediate MVP deployment.

### Key Achievements:
- ✅ **Zero Import Path Conflicts**: All directory names standardized to snake_case
- ✅ **Graceful Dependency Management**: Lazy loading with clear error messages
- ✅ **Loose Coupling**: Interface-based architecture for independent development
- ✅ **Reliable Testing**: All tests run cleanly in any environment
- ✅ **Seamless Integration**: Cross-server communication now works perfectly

## Getting Started - ✅ READY FOR MVP
1. Review the revolutionary architecture in this README
2. Check the comprehensive implementation in [doc/SROS_ARCHITECTURE_REFACTORING_COMPLETED.md](doc/SROS_ARCHITECTURE_REFACTORING_COMPLETED.md)
3. Run all servers using the unified entry point: `python run_servers.py`
4. Start your research workflow with draft-driven discovery

## Documentation
- [SROS_ARCHITECTURE_REFACTORING_COMPLETED.md](doc/SROS_ARCHITECTURE_REFACTORING_COMPLETED.md) - Complete refactoring implementation
- [SROS_PROJECT_PROGRESS.md](SROS_PROJECT_PROGRESS.md) - Current progress and timeline
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md) - Development guidelines and standards
- [doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md](doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md) - Original architecture plan

## License
This project is licensed under the MIT License - see the LICENSE file for details.