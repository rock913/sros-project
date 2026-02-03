# Semantic Scholar MCP Server

## Purpose
Provides academic search capabilities through the Semantic Scholar API.

## Features
- Paper search by keywords, authors, titles
- Citation context retrieval
- Paper metadata extraction
- PDF download capabilities

## Integration
This server integrates with the official Semantic Scholar API to provide scholarly research capabilities to the SROS system.

## Usage
The server will be called by the control plane (Roo Code) when academic gaps are detected in the manuscript.

## Development Status
This server is under development.

### Week 1: Foundation Setup ✅
- ✅ Create server directory structure
- ✅ Set up project dependencies (requests, asyncio, etc.)
- ✅ Implement basic MCP handler framework
- ✅ Configure API key management and rate limiting

### Week 2: Core Functionality ✅
- ✅ Implement paper search by keywords, authors, titles
- ✅ Add citation context retrieval capabilities
- ✅ Implement paper metadata extraction
- ✅ Add PDF download functionality

### Week 3: Advanced Features & Testing ✅
- ✅ Implement caching mechanism for API responses
- ✅ Add error handling and retry logic
- ✅ Write comprehensive unit tests
- ✅ Performance optimization

See `SROS_PROGRESS_TRACKING.md` for detailed development plan and timeline.