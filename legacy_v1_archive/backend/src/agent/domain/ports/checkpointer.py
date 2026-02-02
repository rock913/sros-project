"""
Checkpointer Port (Protocol) for Hexagonal Architecture

This module defines the abstract interface for LangGraph checkpointers,
enabling infrastructure abstraction and dependency injection throughout the research platform.

@Hexagonal Architecture:
- Domain Layer: Pure abstract contracts (no I/O, no implementations)
- Application Layer: Uses checkpointer contracts for state management
- Infrastructure Layer: Provides concrete implementations (AsyncPostgresSaver, etc.)

@TestScenarios (verified by unittest.mock at infrastructure layer)
- get_tuple: Returns checkpoint data for session/thread resumption
- put_tuple: Stores checkpoint data with metadata
- list_configs: Enumerates available session/thread configurations
- aget_tuple: Async version of get_tuple for non-blocking operations
- aput_tuple: Async version of put_tuple for non-blocking operations
- alist_configs: Async version of list_configs
"""

from abc import ABC, abstractmethod
from typing import Any, Iterator, Optional

# Compatibility shim: LangGraph version compatibility layer
# Handles both langgraph v0.1.x (checkpoint.base) and v0.2+ (types)
try:
    # Try v0.2+ (newer langgraph versions)
    from langgraph.types import Checkpoint, CheckpointMetadata, CheckpointTuple
except ImportError:
    # Fallback to v0.1.x (older langgraph versions)
    from langgraph.checkpoint.base import Checkpoint, CheckpointMetadata, CheckpointTuple


class Checkpointer(ABC):
    """Abstract base class defining the checkpointer contract.

    This protocol ensures all checkpointer implementations provide
    consistent state persistence capabilities for LangGraph workflows.

    @Contract Requirements:
    - Must handle synchronous and asynchronous operations
    - Must support configurable metadata for organization
    - Must be thread-safe for concurrent graph execution
    - Must handle checkpointer-specific configuration (e.g., thread_id)

    @Implementation Notes:
    - Concrete implementations will wrap LangGraph checkpointers (AsyncPostgresSaver, MemorySaver, etc.)
    - Factory pattern enables runtime checkpointer selection (dev/prod environments)
    - Single-responsibility: Only checkpointer duties, no business logic
    """

    @abstractmethod
    def get_tuple(self, config: dict[str, Any]) -> Optional[CheckpointTuple]:
        """Synchronously retrieve checkpoint tuple by configuration.

        Args:
            config: Configuration dict containing identifiers (session_id, thread_id, etc.)

        Returns:
            CheckpointTuple if found, None otherwise

        @TestScenarios
        - Valid config returns existing checkpoint
        - Invalid config returns None without error
        - Corrupted data raises implementation-specific exception
        """
        pass

    @abstractmethod
    def put_tuple(self, config: dict[str, Any], checkpoint: Checkpoint, metadata: CheckpointMetadata) -> None:
        """Synchronously store checkpoint tuple with associated metadata.

        Args:
            config: Configuration dict containing identifiers
            checkpoint: The checkpoint state to persist
            metadata: Additional metadata for organization/filtering

        @TestScenarios
        - New checkpoint stored successfully
        - Overwrites existing checkpoint for same config
        - Invalid data raises implementation-specific exception
        """
        pass

    @abstractmethod
    def list_configs(self, filter: Optional[dict[str, Any]] = None) -> Iterator[dict[str, Any]]:
        """Synchronously list available checkpoint configurations.

        Args:
            filter: Optional filtering criteria for configurations

        Returns:
            Iterator of configuration dictionaries

        @TestScenarios
        - No filter returns all configurations
        - Filter narrows results appropriately
        - Empty result when no checkpoints exist
        """
        pass

    @abstractmethod
    async def aget_tuple(self, config: dict[str, Any]) -> Optional[CheckpointTuple]:
        """Asynchronously retrieve checkpoint tuple by configuration.

        This is the primary method used by LangGraph workflows for state management.

        Args:
            config: Configuration dict containing identifiers (session_id, thread_id, etc.)

        Returns:
            CheckpointTuple if found, None otherwise

        @TestScenarios
        - Valid config returns existing checkpoint
        - Invalid config returns None without error
        - Supports concurrent async operations without blocking
        """
        pass

    @abstractmethod
    async def aput_tuple(self, config: dict[str, Any], checkpoint: Checkpoint, metadata: CheckpointMetadata) -> None:
        """Asynchronously store checkpoint tuple with associated metadata.

        Args:
            config: Configuration dict containing identifiers
            checkpoint: The checkpoint state to persist
            metadata: Additional metadata for organization/filtering

        @TestScenarios
        - New checkpoint stored successfully
        - Overwrites existing checkpoint for same config
        - Invalid data raises implementation-specific exception
        """
        pass

    @abstractmethod
    async def alist_configs(self, filter: Optional[dict[str, Any]] = None) -> Iterator[dict[str, Any]]:
        """Asynchronously list available checkpoint configurations.

        Args:
            filter: Optional filtering criteria for configurations

        Returns:
            Iterator of configuration dictionaries

        @TestScenarios
        - No filter returns all configurations
        - Filter narrows results appropriately
        - Empty result when no checkpoints exist
        """
        pass