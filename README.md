# SROS — Scientific Research Operating System

**V4.0-dev** | Python 3.8+ | MIT | 138 tests

> AI-native research OS: an MCP server fleet that gives LLM agents the ability to write manuscripts, search literature, ingest data, and schedule HPC jobs — as naturally as an OS provides system calls.

---

## Quick Start

```bash
pip install -e ".[test]"
sros init my-paper && cd my-paper
export SROS_WORKSPACE_DIR="$PWD"
sros start -w . -p 8000
curl http://localhost:8000/health
```

Open in VS Code with Roo Code — MCP auto-configured via `.roo/mcp.json`.

---

## What is SROS?

SROS turns research infrastructure into MCP tools. It doesn't replace domain tools (fMRIPrep, graphmri, Zotero) — it orchestrates them through a unified protocol.

| Your agent wants to... | SROS tool |
|---|---|
| Write a paper section | `manuscript.insert_section` |
| Search literature | `scholar.federated_search` |
| Ingest neuroimaging data | `db.ingest` |
| Query subject demographics | `db.query` |
| Submit an fMRIPrep job | `hpc.submit` |
| Store facts as a graph | `memory.store_knowledge` |
| Check system health | `sros doctor` |

**Core philosophy**: IDE-as-UI, Skill-First CLI, Thin Gateway (zero business logic in gateway).

---

## CLI

Two surfaces: `sros` (workspace ops) and `sros-skill` (tool execution). All accept `--raw` for JSON output.

```bash
# Workspace
sros init <name>            # Bootstrap workspace
sros start [-w .] [-p 8000]  # Launch MCP gateway
sros stop [-w .]             # Graceful shutdown
sros doctor                  # Full health check
sros verify [--port 8000]    # E2E MCP smoke test

# Tools (sample)
sros-skill manuscript find-gaps --file draft.md
sros-skill --raw db ingest --source /data/SXMU --bids-dir Bids_data
sros-skill --raw db query --sql "SELECT * FROM subjects WHERE group='dTMS'"
sros-skill hpc submit --script jobs/fmriprep.slurm
```

Run `sros-skill --help` for the full module tree.

---

## MCP Tools

All callable via JSON-RPC at `http://localhost:8000/sse`.

### Manuscript & Scholar
`find_gaps` · `get_outline_tree` · `insert_section` · `refactor_section` · `patch_draft` · `get_file_sha256` · `federated_search` · `search` · `zotero_sync` · `brainstorm_perspectives` · `find_critiques`

### Memory, Data & HPC
`store_knowledge` · `query_knowledge` · `get_citation_map` · `db.ingest` · `db.query` · `hpc.submit` · `hpc.status` · `hpc.cancel` · `hpc.list` · `hpc.logs` · `hpc.generate`

### Neuro, Plugins & Tasks
`neuro.validate` · `neuro.generate_graphmri` · `neuro.generate_fmriprep` · `plugins.list` · `plugins.run` · `tasks.run_plugin_async` · `tasks.get` · `tasks.list` · `tasks.wait`

Full tool schemas (inputSchema + descriptions): see `doc/PRD_SXMU_Data_Ingestion_HPC.md`.

---

## Architecture

```
AI Agent (Claude Code / Roo Code)
       │ MCP over SSE
       ▼
SROS Gateway (Thin: FastAPI + SSE, no business logic)
       │ dispatch_tool()
       ▼
Skill RPC (~50 tools → handlers)
       │
  ┌────┼────┬─────┬─────┬─────┬─────┐
  ▼    ▼     ▼     ▼     ▼     ▼     ▼
Manu  Sch   Mem   Data  HPC   Neuro Plugins
script olar  ory   +DB               +Tasks
       │
       ▼
  DuckDB · Subprocess · Slurm · SSH
```

**Rules**: Thin Gateway, Skill-First CLI, workspace-relative paths, TDD mandatory.

---

## ARC Code-Wiki

Auto-generated architecture graph that AI agents read before modifying code:

```bash
make update-wiki    # Compile src/sros/ → docs/code_wiki/
make check-wiki     # CI guard: exits 1 if wiki is stale
make lint           # flake8 + mypy + check-wiki
sros doctor         # Health check: wiki freshness, contract validity
```

Contract: `arc_wiki.json` + `docs/code_schema.md` → `claw-code-ingest` → `docs/code_wiki/`.

---

## Development

```bash
pip install -e ".[dev]"
make test            # 138 tests
make lint            # flake8 + mypy + check-wiki
make update-wiki     # Refresh Code-Wiki after source changes
```

TDD: failing test → implementation → green bar → `make lint` → PR.

---

## Docs Index

| Document | Purpose |
|---|---|
| `doc/SROS_V4.0.md` | Strategic PRD (WHY + WHAT) |
| `doc/PRD_SXMU_Data_Ingestion_HPC.md` | Feature PRD (HOW: CLI + MCP schemas) |
| `ROADMAP.md` | Progress (WHEN + STATUS) |
| `CLAUDE.md` | Agent instructions |

---

**SROS V4.0-dev** — *Skill-First OS for AI4S | Data OS + HPC + DSL + Feishu Control Plane*
