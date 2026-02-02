# MCP Servers Directory

This directory contains all the Model Context Protocol (MCP) servers that provide capabilities to the SROS system.

## Server Structure

Each subdirectory represents a specific MCP server:

1. **semantic-scholar/** - Academic search and paper retrieval
2. **zotero-expert/** - Local citation management
3. **manuscript-manager/** - Core manuscript operations (most critical)
4. **duckdb-memory/** - Local knowledge graph storage
5. **mcp-sros-logic/** - Custom SROS logic and workflow management

## Integration Guidelines

- All servers must comply with the MCP specification
- Servers should be lightweight and focused on single responsibilities
- Prefer using existing community servers when available
- Only develop custom servers for core research logic

## Configuration

Each server should have its own configuration file and documentation in its respective directory.
