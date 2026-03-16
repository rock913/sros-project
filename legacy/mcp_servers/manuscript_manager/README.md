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

## API Methods

### Structure Retrieval
- `get_structure`: Get the current manuscript structure tree

### Gap Detection
- `detect_gaps`: Identify explicit (TODO) and implicit (short sections, lack of citations) gaps

### Section Editing
- `edit_section`: Atomically edit a section with modes (append, prepend, replace)
- `insert_content`: Insert cited content at a specified location

### Content Retrieval
- `get_section_content`: Get the content of a specific section

## Installation
```bash
pip install -r requirements.txt
```

## Configuration

The system now supports `.env` file configuration. Copy the root `.env.example` file to `.env` and fill in your actual values, or set environment variables directly.

### Manuscript configuration
```bash
SROS_MANUSCRIPT_PATH=draft.md
```

## Development
Run tests:
```bash
python -m unittest tests.py
```

## Status
✅ Implementation completed. See `SROS_PROGRESS_TRACKING.md` for integration testing schedule.