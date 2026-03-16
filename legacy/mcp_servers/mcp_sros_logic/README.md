# SROS Logic MCP Server

## Purpose
Custom SROS logic implementation for core research workflows.

## Features
- `init_workspace()`: Initialize `.sros` directory structure with enhanced configuration
- `detect_academic_gaps()`: Detect weak sections in manuscripts using comprehensive academic rules and quality metrics
- `research_coordination()`: Coordinate between different MCP servers with task planning and execution
- `workflow_management()`: Manage the draft-driven discovery loop with progress tracking and quality assessment

## Integration
This server provides the core intelligence for the SROS system, implementing the unique research methodologies.

## Usage
This is the central coordination point for all SROS-specific logic and workflows.

## API Methods

### Workspace Management
- `init_workspace`: Initialize a new SROS workspace with required directories and files

### Academic Analysis
- `detect_academic_gaps`: Analyze manuscript and detect academic weaknesses with comprehensive quality metrics
- `research_coordination`: Coordinate research activities between MCP servers with task planning and execution
- `workflow_management`: Manage the draft-driven discovery workflow with progress tracking and quality assessment

## Installation
```bash
pip install -r requirements.txt
```

## Development
Run tests:
```bash
python -m unittest tests.py
```

## Status
🔄 Core logic enhancement in progress. Week 1 implementation completed. See `SROS_PROGRESS_TRACKING.md` for detailed implementation plan.