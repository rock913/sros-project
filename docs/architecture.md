# SROS Architecture — Module Topology

> 地方解剖图：模块 Fan-in / Fan-out 拓扑关系
> 更详细的实现级架构见 Code-Wiki 自动生成图谱：`docs/code_wiki/index.md`

## 分层架构

```
┌─────────────────────────────────────────────────┐
│  Layer 0: CLI Entry                              │
│  src/sros/cli.py — sros CLI: init/start/stop/    │
│  status/doctor                                   │
│  src/sros/skills/cli.py — sros-skill CLI         │
├─────────────────────────────────────────────────┤
│  Layer 1: MCP Gateway (Thin — no business logic) │
│  src/sros/gateway/ — FastAPI + JSON-RPC SSE Hub  │
│  Fan-out: 1 → N handlers via dispatch_tool()     │
├─────────────────────────────────────────────────┤
│  Layer 2: Tool Dispatch                          │
│  src/sros/skills/rpc.py — TOOL_TABLE             │
│  ~50 tool names → handler functions              │
├─────────────────────────────────────────────────┤
│  Layer 3: Domain Servers (Fan-out by domain)     │
│  src/sros/servers/                               │
│  ├── manuscript/  — gap/outline/insert/patch     │
│  ├── scholar/     — federated_search + OpenAlex  │
│  ├── memory/      — DuckDB knowledge graph       │
│  ├── data/        — CSV preview + Python exec    │
│  ├── db/          — BIDS/TSV/Excel ingest + SQL  │
│  ├── hpc/         — Slurm job management + OOM   │
│  ├── rag/         — Lexical chunking + URL fetch │
│  ├── ext/         — Web scraping                 │
│  ├── tasks/       — Async task management        │
│  └── zotero/      — Zotero citation management   │
├─────────────────────────────────────────────────┤
│  Layer 4: Domain Models & Contracts              │
│  src/sros/domain/ports/    — Protocol interfaces │
│  src/sros/domain/schemas/  — Pydantic models     │
│  contracts/                — Cross-system specs  │
├─────────────────────────────────────────────────┤
│  Layer 5: Infrastructure                         │
│  config/duckdb/schema.sql  — 8-table DDL         │
│  config/slurm/*.slurm      — Slurm templates     │
└─────────────────────────────────────────────────┘
```

## Module Fan-in / Fan-out

| Module | Fan-in (callers) | Fan-out (callees) | Criticality |
|--------|:---:|:---:|:---:|
| `rpc.py::dispatch_tool()` | Gateway (1) | ~50 handlers | 🔴 HIGH |
| `gateway/main.py` | External MCP clients | `rpc.py` | 🔴 HIGH |
| `servers/db/` | `rpc.py`, CLI | `config/duckdb/` | 🟡 MEDIUM |
| `servers/hpc/` | `rpc.py`, CLI | `config/slurm/` | 🟡 MEDIUM |
| `servers/manuscript/` | `rpc.py`, CLI | `utils/` | 🟢 LOW |
| `domain/schemas/` | All servers | None (leaf) | 🔴 HIGH |

## Data Flow

```
MCP Client → Gateway (SSE) → dispatch_tool() → Domain Handler
                                                    ↓
CLI --raw JSON ← stdout ← emit_ok/emit_error ←──────┘
```

## Key Contracts

- **Interface**: JSON-RPC 2.0 `{jsonrpc, method, params, id}` via SSE
- **CLI**: `sros-skill --raw` → stdout=JSON, stderr=logs
- **Cross-system**: ARC `arc_wiki.json` + DuckDB `schema.sql` (versioned)
- **External**: SROS → GraphMRI-Lite via CLI `--raw` JSON (never `import`)
