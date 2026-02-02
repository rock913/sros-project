"""
MCP Tools for VS Code Editor Integration.

Provides Real-time draft context synchronization and editing suggestions
for the Agentic Editor system.
"""

import logging
from typing import List, Dict, Any, Optional, AsyncIterable
from datetime import datetime
from agent.domain.schemas.draft import DraftContext, EvidenceGap, DraftImprovement
from agent.domain.schemas.mcp import McpTool
from agent.domain.schemas.mcp_protocol import ResearchUpdate
from pydantic import BaseModel, Field
from agent.infrastructure.nodes.gap_analyzer import GapAnalyzerAdapter
from agent.application.nodes.writer import WriterNode


logger = logging.getLogger(__name__)


class SyncDraftContextInput(BaseModel):
    """Input schema for sync_draft_context MCP tool."""
    content: str = Field(..., description="Full markdown content of the research draft")
    cursor_line: Optional[int] = Field(None, description="Optional cursor line for focused analysis", ge=0)
    cursor_column: Optional[int] = Field(None, description="Optional cursor column", ge=0)


class ProposeEditsInput(BaseModel):
    """Input schema for propose_edits MCP tool."""
    gaps: List[Dict[str, Any]] = Field(..., description="List of evidence gaps to address")
    file_path: str = Field("draft.md", description="VS Code file path for context")


class ApplyEditInput(BaseModel):
    """Input schema for apply_edit MCP tool."""
    file_path: str = Field(..., description="Target file path")
    original_text: str = Field(..., description="Original text to replace")
    new_text: str = Field(..., description="Improved text to insert")
    line_start: int = Field(..., description="Starting line number (0-based)", ge=0)
    line_end: int = Field(..., description="Ending line number (0-based)", ge=0)


async def sync_draft_context(ctx: Any, input_data: dict) -> Dict[str, Any]:
    """
    MCP Tool: sync_draft_context

    Synchronizes VS Code document content with backend for gap analysis.
    Called when user edits manuscript to enable real-time critique.

    @TestScenarios
    - Convert input dict to DraftContext and analyze for gaps
    - Return properly formatted gap objects with MCP-compatible structure
    - Handle analysis errors gracefully with appropriate error responses
    - Support optional cursor positioning for focused analysis
    """
    # Global gap analyzer instance (injected via MCP server context)
    gap_analyzer = ctx.get('gap_analyzer')
    if not gap_analyzer:
        raise ValueError("Gap analyzer not available in MCP context")

    # Convert input data to Pydantic model if needed
    if isinstance(input_data, dict):
        input_model = SyncDraftContextInput(**input_data)
    else:
        input_model = input_data

    try:
        logger.info(f"Analyzing draft content: {len(input_model.content)} characters")

        # Convert coordinates if provided
        cursor_pos = None
        if input_model.cursor_line is not None and input_model.cursor_column is not None:
            cursor_pos = (input_model.cursor_line, input_model.cursor_column)

        # Create draft context
        draft_context = DraftContext(
            content=input_model.content,
            cursor_position=cursor_pos
        )

        # Analyze for gaps
        gaps = await gap_analyzer.analyze(draft_context)

        # Convert to MCP-compatible format
        gap_dicts = []
        for gap in gaps:
            gap_dicts.append({
                "id": str(gap.id),
                "context_snippet": gap.context_snippet,
                "missing_information": gap.missing_information,
                "search_queries": gap.search_queries,
                "confidence": gap.confidence,
                "is_high_confidence": gap.is_high_confidence
            })

        logger.info(f"Found {len(gaps)} evidence gaps")

        return {
            "success": True,
            "gaps_found": len(gaps),
            "gaps": gap_dicts,
            "message": f"Analysis complete: {len(gaps)} evidence gaps identified"
        }

    except Exception as e:
        logger.error(f"Draft sync failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "gaps": [],
            "gaps_found": 0
        }


async def propose_edits(ctx: Any, input_data: dict) -> Dict[str, Any]:
    """
    MCP Tool: propose_edits

    Generates and proposes specific text improvements to fill evidence gaps.
    Called after gap analysis to provide concrete editing suggestions.

    @TestScenarios
    - Convert gap dicts to EvidenceGap objects for processing
    - Generate improvements using nested Co-STORM research
    - Return structured improvements with citations
    - Handle writer errors with fallback responses
    """
    writer_node = ctx.get('writer_node')
    if not writer_node:
        raise ValueError("Writer node not available in MCP context")

    # Convert input data to Pydantic model if needed
    if isinstance(input_data, dict):
        input_model = ProposeEditsInput(**input_data)
    else:
        input_model = input_data

    try:
        logger.info(f"Generating edits for {len(input_model.gaps)} gaps")

        # Convert MCP gap format to EvidenceGap objects
        evidence_gaps = []
        for gap_data in input_model.gaps:
            evidence_gaps.append(EvidenceGap(**gap_data))

        if not evidence_gaps:
            return {
                "success": True,
                "improvements": [],
                "message": "No gaps to address"
            }

        # Generate improvements using nested Co-STORM
        improvements = await writer_node.fill_gaps_with_research(evidence_gaps)

        # Convert to MCP-compatible format
        improvement_dicts = []
        for imp in improvements:
            improvement_dicts.append({
                "gap_id": str(imp.gap_id),
                "original_snippet": imp.original_snippet,
                "suggested_insertion": imp.suggested_insertion,
                "citations": imp.citations,
                "rationale": imp.rationale,
                "has_citations": imp.has_citations
            })

        logger.info(f"Generated {len(improvements)} improvement suggestions")

        return {
            "success": True,
            "improvements": improvement_dicts,
            "file_path": input_model.file_path,
            "message": f"Generated {len(improvements)} improvement suggestions"
        }

    except Exception as e:
        logger.error(f"Edit proposal failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "improvements": []
        }


async def apply_edit(ctx: Any, input_data: dict) -> Dict[str, Any]:
    """
    MCP Tool: apply_edit

    Directly applies an approved improvement to the VS Code document.
    Optionally called when user accepts a suggestion.

    @TestScenarios
    - Generate edit specification for VS Code workspace integration
    - Handle line number validation and text replacement logic
    - Return structured edit spec for frontend processing
    - Log edit operations for debugging
    """
    # Convert input data to Pydantic model if needed
    if isinstance(input_data, dict):
        input_model = ApplyEditInput(**input_data)
    else:
        input_model = input_data

    try:
        logger.info(f"Applying edit to {input_model.file_path} lines {input_model.line_start}-{input_model.line_end}")

        # Validate edit parameters
        if input_model.line_end <= input_model.line_start:
            raise ValueError("line_end must be greater than line_start")

        # Return edit specification for frontend to handle
        return {
            "success": True,
            "file_path": input_model.file_path,
            "edit_spec": {
                "original_text": input_model.original_text,
                "new_text": input_model.new_text,
                "line_start": input_model.line_start,
                "line_end": input_model.line_end
            },
            "message": "Edit specification generated for VS Code"
        }

    except Exception as e:
        logger.error(f"Edit application failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_sync_draft_context_tool() -> McpTool:
    """Create and return MCP tool for draft context synchronization."""
    return McpTool(
        name="sync_draft_context",
        description="Sync VS Code draft content and analyze for evidence gaps",
        input_schema=SyncDraftContextInput.model_json_schema(),
        handler=sync_draft_context
    )


def get_propose_edits_tool() -> McpTool:
    """Create and return MCP tool for proposing edits."""
    return McpTool(
        name="propose_edits",
        description="Generate editing suggestions to fill identified evidence gaps",
        input_schema=ProposeEditsInput.model_json_schema(),
        handler=propose_edits
    )


def get_apply_edit_tool() -> McpTool:
    """Create and return MCP tool for applying edits."""
    return McpTool(
        name="apply_edit",
        description="Apply an approved text improvement to the VS Code document",
        input_schema=ApplyEditInput.model_json_schema(),
        handler=apply_edit
    )
