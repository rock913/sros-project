# SROS Project Progress - Consolidated Status

## Snapshot (Feb 5, 2026)
- **Architecture**: Gateway + stdio sub-servers is operational.
- **Core servers**: Gateway, search, manuscript, memory, and zotero are integrated.
- **Context ingester**: MVP exists; parsing works but graph storage/search is still a stub.
- **Testing**: Consolidated into [tests](tests) with unit/integration/performance.

## Reality Check (Resolved Inconsistencies)
- Prior docs conflicted on whether the context ingester exists. It does exist in [mcp_servers/context_ingester](mcp_servers/context_ingester), but uses placeholder graph storage and search.
- “All tests passing” claims are not uniformly traceable because tests are spread across root scripts and per-server folders without a single canonical entrypoint.

## Core Components (Current Status)
- [mcp_servers/sros_gateway](mcp_servers/sros_gateway): Gateway SSE server (Port 8000).
- [mcp_servers/federal_academic_search](mcp_servers/federal_academic_search): OpenAlex + Unpaywall + S2.
- [mcp_servers/manuscript_manager](mcp_servers/manuscript_manager): Manuscript operations.
- [mcp_servers/duckdb_memory](mcp_servers/duckdb_memory): Local graph storage (DuckDB).
- [mcp_servers/zotero_expert](mcp_servers/zotero_expert): Citation management.
- [mcp_servers/context_ingester](mcp_servers/context_ingester): MVP parser; graph integration pending.

## Testing Structure (Current)
- Consolidated to [tests](tests) with:
	- [tests/unit](tests/unit)
	- [tests/integration](tests/integration)
	- [tests/performance](tests/performance)
- Root test scripts are thin wrappers for backward compatibility.
- [run_all_tests.py](run_all_tests.py) uses the new paths.

## Documentation Structure (Current)
The [doc](doc) folder is now normalized:
- [doc/SROS V2.2 架构实施总蓝图.md](doc/SROS%20V2.2%20%E6%9E%B6%E6%9E%84%E5%AE%9E%E6%96%BD%E6%80%BB%E8%93%9D%E5%9B%BE.md)
- [doc/SROS_V2.2_DEPLOYMENT_GUIDE.md](doc/SROS_V2.2_DEPLOYMENT_GUIDE.md) (includes stability fixes)
- [doc/SROS_V2.2_STABILITY_FIX.md](doc/SROS_V2.2_STABILITY_FIX.md) (redirect only)
- [doc/SROS_DEVELOPMENT_GUIDELINES.md](doc/SROS_DEVELOPMENT_GUIDELINES.md)

Notes:
- Stability fixes merged into deployment guide to reduce duplication.

## Cleanup & Consolidation Plan (Completed)
### 1) Tests
- Created [tests](tests) with unit/integration/performance.
- Moved root test scripts into subfolders.
- Kept [run_all_tests.py](run_all_tests.py) as the orchestrator.
- Root scripts are thin wrappers for compatibility.

### 2) Documentation
- Merged stability fixes into [doc/SROS_V2.2_DEPLOYMENT_GUIDE.md](doc/SROS_V2.2_DEPLOYMENT_GUIDE.md).
- [doc/SROS_V2.2_STABILITY_FIX.md](doc/SROS_V2.2_STABILITY_FIX.md) now redirects.
- Kept architecture and contribution docs as single sources.

### 3) Root Cleanliness
- Moved diagnostic utilities into [scripts](scripts).
- Root keeps entrypoints; wrappers remain for compatibility.

## Next Steps (Small, Concrete)
1. Optionally delete root wrappers once downstream users update paths.
2. Keep consolidating per-server tests under [tests](tests) as needed.
3. Maintain ingester MVP notes in [README.md](README.md).

---
Last Updated: February 5, 2026
