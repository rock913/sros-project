# SROS - Scientific Research Operating System

**Version 3.0 (WIP)** - *Skill-First Headless Lab for AI4S*

This branch is the start of the V3.0 line: **IDE-as-UI + CLI Skills + Thin MCP Gateway**.

Authoritative V3.0 docs:

- `doc/SROS_V3.0.md` (single source of truth)
- `plans/sros_v30_implementation_plan.md` (Golden Thread + TDD)

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

Optional (V3 direction): use the skill-first CLI directly:

```bash
sros-skill --help
sros-skill manuscript find-gaps --file draft.md --raw
```

### Start Services
```bash
sros start -w . -p 8000
```

If port 8000 is occupied, use:
```bash
sros start -w . --auto-port
```

### Begin Writing
Open the project directory in VS Code with Roo Code extension — the MCP connection is auto-configured via `.roo/mcp.json`.

V3 recommended “visualization”: open `draft.md` in VS Code and keep Markdown preview visible; treat file growth + figures/ outputs as the UI.

### Verify Locally

- Health: `curl -s http://localhost:8000/health`
- SSE stream (MCP transport; should start with an `event: endpoint` frame): `curl -N http://localhost:8000/sse`

Production verification (end-to-end MCP initialize → tools/list → tools/call):

```bash
python scripts/verify_production.py --port 8000 --query "transformer attention"
```

This writes a machine-readable report to `logs/production_verification.json`.

For the authoritative V3 execution contract and milestones, see:

- `doc/SROS_V3.0.md`
- `plans/sros_v30_implementation_plan.md`

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

V3 adds a second CLI surface:

- `sros` stays as the **workspace + gateway** CLI.
- `sros-skill` is the **skill-first** CLI for agents/pipes.

### `sros-skill` (V3)

Rules:

- Default output is human-friendly.
- `--raw` prints pure JSON to stdout (for Claude Code / jq / pipes).

Examples:

```bash
# list gaps as JSON
sros-skill --raw manuscript find-gaps --file draft.md

# get outline
sros-skill --raw manuscript outline --file draft.md

# insert markdown (repeat --cite as needed)
sros-skill --raw manuscript insert --target "heading:Introduction" --content "..." --cite doe2021 --file draft.md
```

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

Roo Code compatible mode:
- `GET /sse` for the event-stream
- `POST /messages` for JSON-RPC (reference MCP SSE transport posts to the endpoint returned by the initial `event: endpoint` frame)
- Also accepts `POST /sse` for backward compatibility

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

`insert_section.target` (deterministic minimal contract):

- `"append"` / `"end"` / `""`: append to end of file
- `"heading:<Title>"`: insert right after the first matching markdown heading line
- `"heading-<line_no>"`: insert after a specific heading line number (matches ids from `get_outline_tree`, e.g. `heading-12`)
- `"line:<n>"` or `"Line <n>"`: insert after line *n*

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

Query citation map (section ids are created by `insert_section` when citations are provided):

- Convention: `draft_section:<file_path>#heading-<line_no>` (example: `draft_section:draft.md#heading-12`)

```bash
curl -s http://localhost:8000/sse \
	-H 'Content-Type: application/json' \
	-d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"memory.get_citation_map","arguments":{"section_id":"draft_section:draft.md#heading-12"}}}'
```

### Scholar Tools (`mcp-scholar`)
- `brainstorm_perspectives(query)` - Multi-perspective research generation
- `find_critiques(paper_id)` - Critical analysis and counter-arguments
- `federated_search(query, max_results, filters)` - Cross-database search

Scholar backends:

- Default (offline + deterministic): `SROS_SCHOLAR_BACKEND=mock`
- Real OpenAlex backend (network): `SROS_SCHOLAR_BACKEND=openalex` and set `OPENALEX_EMAIL`
- Optional fallback when OpenAlex errors: `SROS_SCHOLAR_FALLBACK=mock`

### Memory Tools (`mcp-memory`)
- `store_knowledge(nodes, edges)` - Persist research relationships
- `query_knowledge(query, limit)` - Search knowledge graph
- `get_citation_map(section_id)` - Query citation edges for a draft section

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

## 🧭 Development (V3 Golden Thread)

The fastest local loop is: **edit workspace files → run a skill → observe draft/figures changes → repeat**.

### Workspace env

Most skills/tools operate on workspace-relative paths and rely on:

```bash
export SROS_WORKSPACE_DIR="$PWD"
```

### Skill-first loop (no gateway)

```bash
sros-skill --raw manuscript find-gaps --file draft.md
sros-skill --raw manuscript outline --file draft.md
sros-skill --raw manuscript insert --target "append" --content "Hello" --file draft.md
```

### Gateway loop (for Roo / MCP clients)

```bash
sros start -w . -p 8000
curl -s http://localhost:8000/health
```

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