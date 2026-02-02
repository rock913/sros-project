# Scientific Research Operating System (SROS) V2.1.5

**Version**: V2.1.5 (Agentic & Serverless)
**Core Philosophy**: Manuscript-Centric, MCP-Powered, Roo Code Brained.

## Overview

SROS V2.1.5 represents a fundamental shift from traditional backend applications to a Serverless Agent configuration architecture. This version embraces a "Dual-Plane Model":

### Control Plane (The Brain)
- **Carrier**: Roo Code / Cline (VS Code Extension)
- **Responsibility**: Task planning, CoT reasoning, decision making, and human interaction
- **Logic Storage**: All orchestration logic is stored in `.roomodes` and `.clinerules`

### Capability Plane (The Tools)
- **Carrier**: Model Context Protocol (MCP) compliant servers
- **Responsibility**: Execute specific I/O operations (academic search, file operations, database access)
- **Principle**: Leverage mature community servers, only develop core research logic internally

## Project Structure

```
.
├── .roomodes                  # Roo Code role definitions (Brain)
├── .clinerules                # Global behavioral guidelines
├── mcp_servers/               # Capability plane (Tools)
│   ├── zotero-expert/
│   ├── semantic-scholar/
│   └── manuscript-manager/    # Core self-developed
├── doc/                       # Core documentation
└── workspace/                 # User research workspace example
    ├── .sros/                 # Hidden state directory
    │   ├── graph.db           # Local knowledge graph (DuckDB)
    │   └── research_log.jsonl # Research history (avoid token waste)
    ├── .roomodes              # Project-specific Roo Code behavior
    ├── draft.md               # Single source of truth
    └── references/            # Downloaded PDF clips
```

## Core Workflow: Draft-Driven Discovery

The system operates on a "write-as-you-go" principle rather than "search-then-write":

1. **Observe**: Roo Code calls `manuscript-mcp` to get the current Markdown structure tree
2. **Detect**: Identify gaps in the manuscript (explicit `[TODO:]` or implicit weak sections)
3. **Retrieve**: Call `scholar-mcp` (Semantic Scholar) to find evidence for specific gaps
4. **Build**: Store literature relationships (CiTO ontology) in local `.sros/graph.db`
5. **Expand**: Use `manuscript-mcp` atomic editing tools to insert cited content in specified sections
6. **Iterate**: Rescan the manuscript to check if gaps are resolved

## Getting Started

1. Configure MCP servers in the `mcp_servers/` directory
2. Initialize a research workspace with `sros init`
3. Start writing in `draft.md` - the system will assist with research and expansion

## Development Roadmap

See `doc/SROS_V2.1_PURE_ROO_MCP_PLAN.md` for detailed implementation phases.

## Current Status

✅ Phase 1: Infrastructure Refactoring Complete
✅ Phase 2: MCP Ecosystem Integration Complete  
✅ Phase 3: Knowledge Management & Closed Loop Complete
✅ Phase 4: Experience Optimization Complete
