SROS Architecture Refactoring Plan: From "Import Hell" to "Modular Harmony"

1. The Diagnosis: Identity Crisis

SROS is currently suffering from a conflict between File Structure (Hyphenated, Microservice-style) and Runtime Behavior (Python Monolith, Import-heavy).

Symptom: ImportError and sys.path hacks.

Root Cause: Treating distinct MCP microservices as a single cohesive Python package without a shared kernel.

The Fix: Transition to a "Modular Monolith" architecture with a standardized naming convention and a shared core library.

2. Immediate Tactical Fixes (The "Great Rename")

We must align directory names with Python's PEP 8 standards (snake_case). This is non-negotiable for a healthy Python codebase.

Action Item 1: Standardize Directory Names

Execute the following moves to make the codebase import-friendly immediately:

# Rename directories to snake_case
mv mcp_servers/duckdb-memory/       mcp_servers/duckdb_memory/
mv mcp_servers/manuscript-manager/  mcp_servers/manuscript_manager/
mv mcp_servers/mcp-sros-logic/      mcp_servers/mcp_sros_logic/
mv mcp_servers/semantic-scholar/    mcp_servers/semantic_scholar/
mv mcp_servers/zotero-expert/       mcp_servers/zotero_expert/


Action Item 2: Establish Package Roots

Ensure every directory has an __init__.py to be treated as a proper package.

touch mcp_servers/__init__.py
touch mcp_servers/duckdb_memory/__init__.py
# ... ensure for all subfolders


3. Strategic Architectural Fixes (The "Elegant Solution")

Instead of just fixing imports, we fix the coupling.

Strategy A: The "Shared Core" Pattern (To kill Circular Imports)

Create a lightweight common or core module. This breaks the dependency chain where Server A imports Server B.

New Structure:

mcp_servers/
├── __init__.py
├── common/                 <-- NEW: The Shared Kernel
│   ├── __init__.py
│   ├── models.py           # Shared Pydantic models (Gap, Manuscript, etc.)
│   ├── interfaces.py       # Abstract Base Classes (MemoryStore, ResearchTool)
│   └── utils.py            # Shared logging, config logic
├── duckdb_memory/          # Implements MemoryStore interface
├── mcp_sros_logic/         # Depends on interfaces, not implementations
└── ...


Implementation Example (mcp_servers/common/interfaces.py):

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class MemoryStore(ABC):
    """Abstract interface for memory storage (DuckDB, SQLite, InMemory)."""
    @abstractmethod
    def add_knowledge(self, subject: str, predicate: str, object: str):
        pass

    @abstractmethod
    def query(self, sql: str) -> List[Dict[str, Any]]:
        pass


Strategy B: Dependency Injection for DuckDB (To Fix The Missing Dependency)

Isolate the heavy dependency so unit tests can run without it.

Refactored mcp_servers/duckdb_memory/server.py:

from mcp_servers.common.interfaces import MemoryStore
import logging

class DuckDBMemoryServer(MemoryStore):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None

    @property
    def conn(self):
        # Lazy Loading: Only import duckdb when actually needed, not at module level
        if self._conn is None:
            try:
                import duckdb
                self._conn = duckdb.connect(self.db_path)
            except ImportError:
                logging.error("DuckDB not installed. Feature unavailable.")
                raise RuntimeError("DuckDB dependency missing")
        return self._conn

    def query(self, sql: str):
        return self.conn.sql(sql).fetchall()


The Test-Friendly Mock (tests/mocks.py):

class InMemoryStore(MemoryStore):
    """A pure Python dictionary implementation for testing."""
    def __init__(self):
        self.triples = []

    def add_knowledge(self, s, p, o):
        self.triples.append((s, p, o))

    def query(self, sql: str):
        # Return mock data based on simple checks
        return [{"mock": "data"}]


4. The Unified Entry Point (fixing sys.path)

Stop running scripts from inside subdirectories. Treat mcp_servers as the project root.

Create run_server.py at the root

import sys
import os
import argparse
from mcp_servers.mcp_sros_logic.server import SROSLogicServer
# Now imports work cleanly because we run from root

if __name__ == "__main__":
    # Logic to start specific servers based on args
    pass


5. Execution Roadmap

Refactor Names (Today): Rename all folders to snake_case. This stops the bleeding.

Fix Imports (Today): Use global search/replace to update from mcp_servers.manuscript-manager to from mcp_servers.manuscript_manager.

Implement Lazy Loading (Tomorrow): Modify DuckDBMemoryServer to import duckdb only inside methods, wrapping it in try/except.

Extract Common Models (Next Week): Move ResearchGap, ManuscriptStructure pydantic models to mcp_servers.common.models to clean up the architecture.

6. Summary of Benefits

Feature

Old Approach

New "Insightful" Approach

Directory Names

kebab-case (Python hostile)

snake_case (Python native)

Dependencies

Hard imports at top of file

Lazy imports + Abstractions

Coupling

Direct Logic -> DB coupling

Logic -> Interface <- DB Adapter

Testing

Fails if DB missing

Passes using InMemory Mock