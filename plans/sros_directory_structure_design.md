# SROS V2.3 Directory Structure Design

## 1. Overview

This document outlines the complete directory structure transformation from the current coupled architecture to the decoupled CLI-based system. The design separates user research projects from the SROS tooling, enabling independent evolution and maintenance.

## 2. Current vs. Target Architecture

### 2.1 Current Coupled Structure
```
gemini-fullstack-langgraph-quickstart/ (Source Code Repo)
├── mcp_servers/                 # Tool source code
│   ├── sros_gateway/
│   ├── federal_academic_search/
│   ├── manuscript_manager/
│   ├── duckdb_memory/
│   ├── context_ingester/
│   └── zotero_expert/
├── workspace/                   # User data mixed with source
│   ├── sample-project/
│   │   ├── draft.md
│   │   ├── ideas.md
│   │   └── materials/
│   └── research-playground/
│       └── draft.md
├── run_servers.py              # Runtime entry point
├── requirements.txt            # Dependencies
└── README.md
```

### 2.2 Target Decoupled Structure
```
User's Computer:
├── My_Research_Project/         # Independent research project
│   ├── draft.md               # Main research document
│   ├── ideas.md               # Initial hypotheses
│   ├── .env                   # API keys
│   ├── .roomodes              # Roo Code behavior
│   ├── .gitignore
│   ├── materials/             # Supporting materials
│   │   ├── notes.md
│   │   └── papers/
│   ├── references/            # Citations
│   └── .sros/                 # SROS state
│       ├── graph.db           # Knowledge graph
│       ├── research_log.jsonl # Activity log
│       └── config.json        # Project config
│
Installed Package:
/usr/local/lib/python3.x/site-packages/sros/  # Installed SROS package
├── __init__.py
├── cli.py                    # CLI entry point
├── gateway/                  # Gateway server
│   ├── __init__.py
│   ├── main.py
│   └── config.json
├── servers/                  # Sub-servers
│   ├── federal_academic_search/
│   ├── manuscript_manager/
│   ├── duckdb_memory/
│   ├── context_ingester/
│   └── zotero_expert/
├── templates/                # Project templates
│   ├── project/
│   │   ├── draft.md.j2
│   │   ├── ideas.md.j2
│   │   └── .roomodes.j2
│   └── prompts/
├── utils/                    # Utilities
│   ├── __init__.py
│   ├── filesystem.py
│   ├── process.py
│   └── validation.py
└── core/                     # Core logic
    ├── __init__.py
    ├── project.py
    ├── gateway.py
    └── system.py
```

## 3. Detailed Package Structure

### 3.1 Source Package Layout
```
sros-source/
├── pyproject.toml              # Build configuration
├── README.md                   # Package description
├── LICENSE                     # License terms
├── CHANGELOG.md                # Version history
├── docs/
│   ├── installation.md
│   ├── usage.md
│   └── api-reference.md
├── src/
│   └── sros/                   # Main package
│       ├── __init__.py         # Package metadata
│       ├── __about__.py        # Version and author info
│       ├── cli.py              # CLI application
│       ├── constants.py        # Shared constants
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py     # Configuration management
│       │   └── defaults.py     # Default values
│       ├── core/
│       │   ├── __init__.py
│       │   ├── project.py      # Project management
│       │   ├── gateway.py      # Gateway operations
│       │   ├── system.py       # System utilities
│       │   └── validation.py   # Input validation
│       ├── gateway/
│       │   ├── __init__.py
│       │   ├── main.py         # Gateway entry point
│       │   ├── server.py       # Gateway implementation
│       │   └── config.json     # Gateway configuration
│       ├── servers/            # Sub-server modules
│       │   ├── __init__.py
│       │   ├── federal_academic_search/
│       │   │   ├── __init__.py
│       │   │   ├── main.py     # Server implementation
│       │   │   ├── mcp_handler.py # MCP interface
│       │   │   └── config.py   # Server config
│       │   ├── manuscript_manager/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   ├── mcp_handler.py
│       │   │   └── config.py
│       │   ├── duckdb_memory/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   ├── mcp_handler.py
│       │   │   └── config.py
│       │   ├── context_ingester/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   ├── mcp_handler.py
│       │   │   └── config.py
│       │   └── zotero_expert/
│       │       ├── __init__.py
│       │       ├── main.py
│       │       ├── mcp_handler.py
│       │       └── config.py
│       ├── templates/          # Project templates
│       │   ├── __init__.py
│       │   ├── project/
│       │   │   ├── draft.md.j2
│       │   │   ├── ideas.md.j2
│       │   │   ├── .roomodes.j2
│       │   │   ├── .env.j2
│       │   │   └── .gitignore.j2
│       │   └── prompts/
│       │       ├── writer.yaml.j2
│       │       └── researcher.yaml.j2
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── filesystem.py   # File operations
│       │   ├── process.py      # Process management
│       │   ├── network.py      # Network utilities
│       │   ├── validation.py   # Validation helpers
│       │   └── formatting.py   # Output formatting
│       └── exceptions.py       # Custom exceptions
└── tests/                      # Test suite
    ├── __init__.py
    ├── conftest.py             # Test configuration
    ├── unit/
    │   ├── __init__.py
    │   ├── test_cli.py
    │   ├── test_project.py
    │   ├── test_gateway.py
    │   └── test_servers/
    ├── integration/
    │   ├── __init__.py
    │   └── test_full_workflow.py
    └── fixtures/
        ├── __init__.py
        └── sample_configs/
```

## 4. User Project Structure

### 4.1 Standard Project Layout
```
My_Research_Project/
├── draft.md                   # Main research document (single source of truth)
├── ideas.md                   # Initial hypotheses and core concepts
├── .env                       # Environment variables (API keys, etc.)
├── .roomodes                  # Roo Code behavior configuration
├── .gitignore                 # Git ignore patterns
├── materials/                 # Supporting research materials
│   ├── notes.md               # General notes
│   ├── papers/                # Paper PDFs and summaries
│   ├── web_clips.txt          # Web content clips
│   └── deep_research.md       # Detailed research findings
├── references/                # Formal citations and bibliography
│   ├── citations.bib
│   └── pdfs/                  # PDF attachments
├── figures/                   # Visual content
│   ├── charts/
│   └── diagrams/
└── .sros/                     # SROS-specific hidden directory
    ├── graph.db               # Local knowledge graph (DuckDB)
    ├── research_log.jsonl     # Research activity log
    ├── cache/                 # Temporary cache files
    ├── logs/                  # System logs
    └── config.json            # Project-specific SROS config
```

### 4.2 Generated Configuration Files

#### 4.2.1 .roo/mcp.json (Auto-generated)
```json
{
  "mcpServers": {
    "sros-gateway": {
      "name": "SROS Gateway",
      "url": "http://localhost:8000/sse",
      "type": "sse",
      "description": "SROS V2.3 Gateway - Unified MCP Server Aggregator",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

#### 4.2.2 .roomodes (Auto-generated)
```yaml
name: SROS-Writer-V2.3
groups:
  - read
  - edit
  - browser
  - mcp
systemPrompt: |
  You are an academic writing assistant powered by SROS V2.3.
  Your goal is to eliminate [TODO] markers in 'draft.md'.

  Core Rules:
  1. **Context Priority**: Always check local knowledge graph before external search
  2. **Atomic Edits**: Use ms_edit_section for all modifications
  3. **Evidence-Based**: Support all claims with citations

  Available Tools:
  - federal_search_paper: Search academic databases
  - ms_parse_structure: Analyze document structure
  - ms_edit_section: Edit document sections
  - mem_query_graph: Query local knowledge graph
  - mem_store_knowledge: Store new knowledge
  - ctx_ingest_materials: Process materials/
  - ctx_search_soft_knowledge: Search soft knowledge
  - zot_manage_references: Manage citations

  Workflow:
  1. Preheat: ctx_ingest_materials
  2. Observe: ms_parse_structure
  3. Detect: Identify [TODO] and gaps
  4. Query: mem_query_graph first
  5. Search: federal_search_paper if needed
  6. Store: mem_store_knowledge
  7. Write: ms_edit_section
```

## 5. Migration Path

### 5.1 From Old to New Structure
```
Old: gemini-fullstack-langgraph-quickstart/workspace/my-project/
     ↓ Migration Tool
New: ~/Documents/my-research-project/

Migration Steps:
1. Copy draft.md, ideas.md, materials/ to new location
2. Convert old .roo/config.json to new .roo/mcp.json
3. Update .roomodes for new tool namespaces
4. Initialize .sros/ directory and graph.db
5. Preserve research history and logs
```

### 5.2 Backward Compatibility
- Maintain run_servers.py for development
- Support old configuration formats during transition
- Provide migration utilities

## 6. Security and Permissions

### 6.1 File Permissions
- User project files: Read/write for user only
- SROS state files: Read/write for user only
- Configuration files: Secure permissions for sensitive data

### 6.2 Isolation
- Each project maintains independent state
- No cross-project data leakage
- Secure API key handling

## 7. Performance Considerations

### 7.1 Resource Management
- Efficient file I/O operations
- Proper process cleanup
- Memory-efficient data structures

### 7.2 Caching Strategy
- Intelligent caching in .sros/cache/
- Cache invalidation mechanisms
- Performance optimization for repeated operations

## 8. Cross-Platform Support

### 8.1 Directory Paths
- Use pathlib for cross-platform compatibility
- Handle Windows/Unix path differences
- Support various Python environments

### 8.2 Process Management
- Cross-platform process spawning
- Signal handling for graceful shutdown
- Environment variable management

This directory structure design enables the complete decoupling of user research projects from the SROS tooling while maintaining all functionality and improving usability.