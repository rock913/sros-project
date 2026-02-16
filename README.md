# SROS - Scientific Research Operating System

**Version 2.3.2** - *Draft-Driven Academic Writing Assistant*

SROS is an AI-native research operating system that transforms academic writing through intelligent gap detection, multi-perspective analysis, and seamless citation management.

## 🚀 Quick Start

### Installation
```bash
pip install -e .
```

> Tip: If you prefer a regular install, build/publish the package and then use `pip install sros`.

### Initialize Project
```bash
sros init my-research-paper
cd my-research-paper
```

### Start Services
```bash
sros start -w . -p 8000
```

### Begin Writing
Open the project directory in VS Code with Roo Code extension — the MCP connection is auto-configured via `.roo/mcp.json`.

### Verify Locally

- Health: `curl -s http://localhost:8000/health`
- SSE stream (should print `data:` lines): `curl -N http://localhost:8000/sse`

For the authoritative execution contract and acceptance tests, see:
- `docs/specs/sros_roo_playbooks.md`
- `docs/specs/sros_v232_implementation_spec.md`

## ✨ Key Features

### 1. **Draft-Driven Discovery**
- Gap analysis identifies evidence needs, elaboration opportunities, and citation gaps
- Real-time outline generation and structure validation
- Incremental writing with intelligent content insertion

### 2. **Multi-Perspective Analysis (Co-STORM)**
- Generate diverse research perspectives on any topic
- Critical analysis and counter-argument identification (CiTO logic)
- Federated search across multiple academic databases

### 3. **Knowledge Graph Management**
- Persistent DuckDB storage for research relationships
- Citation mapping and reference tracking
- Live knowledge graph visualization

### 4. **Seamless Integration**
- MCP (Model Context Protocol) compliant
- Roo Code integration ready
- Cross-platform compatibility

## 🛠️ Command Line Interface

### `sros init <project_name>`
Creates a new research project with proper directory structure:
```
my-paper/
├── .roo/mcp.json          # Auto-configured for Roo Code
├── .sros/graph.db         # Knowledge graph database
├── draft.md              # Main manuscript (single source of truth)
├── ideas.md              # Research notes
├── materials/            # Research documents
└── references/           # Citations
```

### `sros start`
Launches the MCP gateway and all services on port 8000:
- **SSE Endpoint**: `http://localhost:8000/sse`
- **Health Check**: `http://localhost:8000/health`
- **Tools List**: `http://localhost:8000/tools`

The gateway supports MCP JSON-RPC over HTTP POST on the same `/sse` endpoint:
- `initialize`
- `tools/list`
- `tools/call`

### `sros doctor`
Comprehensive system health check covering:
- Python environment and dependencies
- Port availability
- Database integrity
- Service connectivity

### `sros status`
Quick project status overview showing workspace files and service status.

## 🔧 Available MCP Tools

### Manuscript Tools (`mcp-manuscript`)
- `find_gaps(file_path)` - Identify research gaps and TODOs
- `get_outline_tree(file_path)` - Generate document structure
- `insert_section(target, content, citations, file_path)` - Add content with citations
- `patch_draft(patches, file_path)` - Batch content updates

Important: `file_path` is **workspace-relative** (e.g. `draft.md`, `notes/draft.md`).
Absolute paths and path traversal (like `../x`) are rejected for safety.

### MCP JSON-RPC Examples

List tools:
```bash
curl -s http://localhost:8000/sse \
	-H 'Content-Type: application/json' \
	-d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Call a tool (workspace-relative path):
```bash
curl -s http://localhost:8000/sse \
	-H 'Content-Type: application/json' \
	-d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"manuscript.find_gaps","arguments":{"file_path":"draft.md"}}}'
```

### Scholar Tools (`mcp-scholar`)
- `brainstorm_perspectives(query)` - Multi-perspective research generation
- `find_critiques(paper_id)` - Critical analysis and counter-arguments
- `federated_search(query, max_results, filters)` - Cross-database search

### Memory Tools (`mcp-memory`)
- `store_knowledge(nodes, edges)` - Persist research relationships
- `query_knowledge(query, limit)` - Search knowledge graph
- `get_citation_map(section_id)` - Visualize citation networks

### Zotero Tools (`mcp-zotero`)
- `add_citation(citekey, title, authors, year, journal, url, bibtex)` - Add reference
- `get_citation(citekey)` - Retrieve citation details
- `search_citations(query)` - Find references

## 🏗️ Architecture

SROS follows a clean architecture pattern:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Domain        │    │   Application   │    │   Infrastructure│
│   Layer         │◄──►│   Layer         │◄──►│   Layer         │
│                 │    │                 │    │                 │
│ • Protocols     │    │ • MCP Servers   │    │ • FastAPI       │
│ • Pydantic      │    │ • CLI Commands  │    │ • DuckDB        │
│ • Models        │    │ • Gateways      │    │ • Typer         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

- **Domain**: Pure contracts and data structures (no I/O)
- **Application**: Business logic and MCP service implementations
- **Infrastructure**: External interfaces and persistence

## 🧪 Testing

Run the test suite:
```bash
python -m pytest -q
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions, please open an issue on GitHub.

---

**SROS V2.3.2** - *Draft is State, CLI is Interface*