# DuckDB Memory MCP Server

## Purpose
Provides local knowledge graph storage using DuckDB for the SROS system.

## Features
- Local triple store for literature relationships
- CiTO (Citation Typing Ontology) table structure
- Fast querying of research connections
- Persistent storage in `.sros/graph.db`

## Integration
This server manages the local memory layer of the SROS system, storing all research relationships and findings.

## Usage
The server is automatically initialized when a new workspace is created and maintains the research knowledge graph throughout the project lifecycle.

## API Methods

### Paper Management
- `create_paper`: Create a new paper record
- `get_paper`: Retrieve a paper by ID, DOI, or citation key
- `update_paper`: Update paper information
- `delete_paper`: Delete a paper record

### Citation Tracking
- `create_citation`: Record a citation between two papers
- `get_citations`: Retrieve citations for a paper

### Relationship Mapping
- `create_relationship`: Create a relationship between papers (critiques, extends, etc.)
- `get_relationships`: Retrieve relationships for a paper or by type

### Research Gap Tracking
- `create_research_gap`: Record a research gap identified in the manuscript
- `get_research_gaps`: Retrieve research gaps
- `update_research_gap`: Update gap status or priority

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
The server can be configured using environment variables:
- `SROS_DUCKDB_PATH`: Path to the DuckDB database file (default: `.sros/graph.db`)
- `SROS_LOG_LEVEL`: Logging level (default: `INFO`)
- `SROS_DUCKDB_LOG_FILE`: Log file path (default: `.sros/logs/duckdb.log`)

## Development
Run tests:
```bash
python -m unittest tests.py
```

## Status
✅ Implementation completed. See `SROS_PROGRESS_TRACKING.md` for integration testing schedule.