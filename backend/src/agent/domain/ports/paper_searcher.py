"""
Paper Searcher Port for Co-STORM Librarian Node

This module defines the contract for paper searching functionality used by the Librarian node
in the Co-STORM discourse loop. Following hexagonal architecture, this is a pure domain port
that allows for multiple implementations (Arxiv, PubMed, Semantic Scholar, etc.).

@Hexagonal Architecture:
- Domain layer: Pure contract, no I/O dependencies
- Application layer: Orchestrates port usage in Librarian node
- Infrastructure layer: Implements adapters (e.g., ArxivSearcher)

@TestScenarios
- search_papers(["keyword1", "keyword2"]): Returns List[Paper] with valid domain models
- Empty keywords: Returns empty list gracefully
- Invalid keywords: Raises ValueError
- Network/Rate limit errors: Handles with logging/fallbacks
"""

from typing import List, Protocol, runtime_checkable

from agent.domain.schemas.paper import Paper


@runtime_checkable
class PaperSearcherPort(Protocol):
    """Contract for searching academic papers by keywords.

    This port enables the Librarian node to search for papers without knowing
    the specific search provider (Arxiv, PubMed, etc.).

    @TestScenarios
    - search_papers(["quantum", "computing", "methods"]): Returns 3-5 papers about quantum computing methods
    - search_papers(["nonexistent_keyword"]): Returns empty list without errors
    - search_papers([]): Raises ValueError for empty keyword list
    - Consecutive calls: Rate limited gracefully with backoff
    """

    async def search_papers(self, keywords: List[str]) -> List[Paper]:
        """Search for papers using the provided keywords.

        Args:
            keywords: Search keywords (e.g., ["quantum", "computing", "algorithms"])

        Returns:
            List of Paper domain models with populated metadata

        Raises:
            ValueError: If keywords list is empty
        """
        ...


def get_paper_searcher() -> PaperSearcherPort:
    """Factory function to get the configured PaperSearcher adapter.

    This allows the application layer to be configured with different
    search implementations (Arxiv, mock for testing, etc.).

    Returns:
        Configured PaperSearcherPort implementation
    """
    # Import here to avoid circular dependencies
    from agent.infrastructure.mcp.tools.arxiv import ArxivSearcher

    # For now, use Arxiv as the primary implementation
    # Future: Read from configuration for multi-provider setup
    return ArxivSearcher()