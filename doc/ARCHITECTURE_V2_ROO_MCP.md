# SROS V2.0 Architecture: Roo Code x MCP

## Overview
SROS V2.0 (Scientific Research Operating System) is an AI-Native research platform built on **VS Code**, **Roo Code**, and **MCP (Model Context Protocol)**. It replaces traditional rigid workflow engines with a flexible, agentic architecture driven by context-aware Large Language Models.

## Core Components

### 1. The Orchestrator: Roo Code
Instead of a backend Python script managing state, **Roo Code** (VS Code Extension) serves as the primary runtime environment. It manages:
- **Context Window**: 1M+ token context (via Gemini 1.5 Pro or Qwen2.5-Coder).
- **Tool Access**: Dynamic loading of MCP servers.
- **File System**: Direct manipulation of the user's workspace.

### 2. The Capabilities: MCP Servers
Tools are no longer imported Python functions but independent local servers speaking JSON-RPC.

| Server Name | Tech Stack | Responsibilities |
| :--- | :--- | :--- |
| **`zotero-expert`** | Node.js TS | Interfaces with local Zotero SQLite. Provides citation keys and PDF paths. |
| **`academic-fetch`** | Python | Fetches data from ArXiv, Semantic Scholar, and unpaywall.org. |
| **`neo4j-rag`** | Node.js | Stores "Claims" and "Evidence" as a knowledge graph. |

### 3. The Roles: Custom Modes
We utilize Roo Code's custom mode feature to switch "Persona" and "Tool Sets".

#### 📚 Librarian (Researcher)
- **Goal**: Broad search and filtration.
- **Prompts**: Optimized for keyword expansion and relevance scoring.
- **Tools**: `academic-fetch/*`, `zotero-expert/search`.

#### 🧠 Analyst (Reader)
- **Goal**: Deep reading and knowledge extraction.
- **Prompts**: Optimized for logic extraction and triple extraction (Subject-Predicate-Object).
- **Tools**: `pdf_extract`, `neo4j-rag/write`.

#### ✍️ Scribe (Writer)
- **Goal**: Synthesis and production.
- **Prompts**: Optimized for LaTeX/Markdown generation and hallucination checking.
- **Tools**: `fs/*`, `zotero-expert/verify`.

## Workflow: The "Reflexion" Loop

Because we lack a rigid state machine, we use **System Instructions** to enforce quality control loops:

1.  **Drafting**: Scribe generates a paragraph with citations `(Author, Year)`.
2.  **Verification Trigger**: System prompt rules dictate: "After writing, you MUST run `check_citation_key`".
3.  **Correction**: If the tool returns "Key Check Failed", the Agent self-corrects based on tool output.

## Directory Structure
```
.
├── .vscode/
│   └── roocode_config/      # Shared Mode Definitions
├── mcp_servers/             # Independent Server Code
│   ├── zotero-expert/
│   ├── academic-fetch/
│   └── neo4j-rag/
├── docs/                    # Architecture Documentation
└── workspace/               # User Research Data
```

## Future Roadmap
- **Server-Side LangGraph**: For massive batch jobs (e.g., "Analyze 5000 papers"), we will re-introduce LangGraph as a hidden backend service that exposes a simple status API to Roo Code.
