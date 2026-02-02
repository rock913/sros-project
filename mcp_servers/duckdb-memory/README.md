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