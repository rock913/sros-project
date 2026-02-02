# Manuscript Manager MCP Server

## Purpose
Core server for manuscript operations and atomic editing capabilities.

## Features
- `get_structure`: Retrieve current Markdown structure tree
- `edit_section`: Atomic section editing based on headers
- `detect_gaps`: Identify explicit and implicit gaps in the manuscript
- `insert_content`: Insert cited content at specified locations

## Integration
This is the most critical tool in the SROS ecosystem, ensuring safe and precise manuscript manipulation.

## Usage
All manuscript modifications must go through this server to maintain document integrity and prevent corruption.