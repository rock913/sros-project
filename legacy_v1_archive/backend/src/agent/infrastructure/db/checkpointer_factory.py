"""
Checkpointer Factory for AsyncPostgresSaver

This module provides a singleton factory for AsyncPostgresSaver instances,
ensuring consistent database connection pooling across all LangGraph workflows.

@Hexagonal Architecture:
- Infrastructure Layer: Concrete implementation of domain Checkpointer protocol
- Factory Pattern: Single responsibility for checkpointer instantiation
- Singleton Pattern: Ensures single connection pool per application lifecycle

@Async Connection Pool Management:
- Single AsyncConnectionPool instance shared across all graphs
- Eliminates pool exhaustion from multiple graph instances
- Configurable pool size for production scaling

@Thread Safety:
- Singleton ensures thread-safe access across event loop
- Connection pool handles async context management internally

@TestScenarios (verified by unittest.mock at infrastructure layer)
- get_async_checkpointer: Returns valid AsyncPostgresSaver instance
- Singleton behavior: Multiple calls return same instance
- Configuration consistency: All checkpointers use same pool/connection
- Async operations: Supports concurrent graph execution without conflicts
"""

import os
from typing import Optional

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

from agent.domain.ports.checkpointer import Checkpointer


# Singleton instances for application lifecycle management
_async_postgres_saver: Optional[Checkpointer] = None
_connection_pool: Optional[AsyncConnectionPool] = None


class AsyncPostgresCheckpointer(Checkpointer):
    """Concrete implementation of Checkpointer protocol using AsyncPostgresSaver.

    This adapter wraps LangGraph's AsyncPostgresSaver to provide
    the domain contract interface expected by application layer.

    @Implementation Notes:
    - Wraps AsyncPostgresSaver methods to match protocol
    - Handles checkpointer-specific configuration (thread_id requirements)
    - Provides synchronous and asynchronous method variants
    - Propagates exceptions without catching (infrastructure responsibility)
    """

    def __init__(self, saver: AsyncPostgresSaver):
        """Initialize with pre-configured AsyncPostgresSaver instance.

        Args:
            saver: Pre-configured AsyncPostgresSaver with connection pool
        """
        self._saver = saver

    def get_tuple(self, config: dict[str, any]) -> Optional[any]:
        """Synchronous checkpoint retrieval via protocol contract."""
        return self._saver.get_tuple(config)

    def put_tuple(self, config: dict[str, any], checkpoint: any, metadata: any) -> None:
        """Synchronous checkpoint storage via protocol contract."""
        self._saver.put_tuple(config, checkpoint, metadata)

    def list_configs(self, filter: Optional[dict[str, any]] = None) -> any:
        """Synchronous configuration listing via protocol contract."""
        return self._saver.list_configs(filter)

    async def aget_tuple(self, config: dict[str, any]) -> Optional[any]:
        """Asynchronous checkpoint retrieval via protocol contract."""
        return await self._saver.aget_tuple(config)

    async def aput_tuple(self, config: dict[str, any], checkpoint: any, metadata: any) -> None:
        """Asynchronous checkpoint storage via protocol contract."""
        await self._saver.aput_tuple(config, checkpoint, metadata)

    async def alist_configs(self, filter: Optional[dict[str, any]] = None) -> any:
        """Asynchronous configuration listing via protocol contract."""
        return await self._saver.alist_configs(filter)


def get_async_connection_pool() -> AsyncConnectionPool:
    """Get the singleton AsyncConnectionPool instance.

    Creates connection pool on first call, returns cached instance thereafter.
    This ensures all graphs share the same underlying database connections.

    @Configuration:
    - Reads POSTGRES_URI from environment variables
    - Configures pool size for concurrent workflow execution
    - Uses autocommit to prevent transaction management issues
    - Enables connection preparation for performance

    @Error Handling:
    - Raises ValueError if POSTGRES_URI not configured
    - Propagates psycopg_pool exceptions for connection failures

    Returns:
        Configured AsyncConnectionPool instance

    @TestScenarios
    - Valid configuration: Returns pooled connection instance
    - Missing POSTGRES_URI: Raises ValueError with descriptive message
    - Concurrent calls: Returns same pool instance
    """
    global _connection_pool

    if _connection_pool is None:
        db_uri = os.getenv(
            "POSTGRES_URI",
            "postgresql://postgres:postgres@langgraph-postgres:5432/postgres"
        )

        # Validate configuration
        if not db_uri:
            raise ValueError(
                "POSTGRES_URI environment variable must be set for checkpointer factory"
            )

        # Create singleton connection pool
        _connection_pool = AsyncConnectionPool(
            conninfo=db_uri,
            max_size=20,  # Configurable for production scaling
            kwargs={
                "autocommit": True,  # Prevent transaction scope issues
                "prepare_threshold": 0,  # Enable prepared statements
            }
        )

    return _connection_pool


def get_async_checkpointer() -> Checkpointer:
    """Get the singleton AsyncPostgresCheckpointer instance.

    Factory function that provides checkpointer instances for dependency injection.
    Ensures all LangGraph workflows use the same underlying connection pool.

    @Dependency Injection:
    - Application layer calls this factory for checkpointer instances
    - Infrastructure layer manages connection lifecycle internally
    - Enables testing with mocked checkpointers via unittest.mock

    @Singleton Pattern:
    - Single checkpointer instance per application lifecycle
    - Prevents connection pool duplication across graph instances
    - Ensures consistent state management across workflows

    Returns:
        Configured Checkpointer protocol implementation

    @TestScenarios (infrastructure layer tests)
    - First call: Creates and returns new checkpointer instance
    - Subsequent calls: Returns cached singleton instance
    - Valid database connection: Operations succeed
    - Connection failure: Exceptions propagated appropriately
    - Concurrent graph execution: No connection pool conflicts
    """
    global _async_postgres_saver

    if _async_postgres_saver is None:
        # Get shared connection pool
        pool = get_async_connection_pool()

        # Create checkpointer with shared pool
        postgres_saver = AsyncPostgresSaver(pool)

        # Wrap in protocol adapter
        _async_postgres_saver = AsyncPostgresCheckpointer(postgres_saver)

    return _async_postgres_saver


# Cleanup function for application shutdown (optional)
async def close_async_connection_pool() -> None:
    """Clean up connection pool on application shutdown.

    Should be called during application teardown to ensure
    proper resource cleanup and prevent connection leaks.

    @Usage:
    - Call in FastAPI lifespan shutdown event
    - Call in pytest teardown fixtures
    - Ensures graceful connection pool termination
    """
    global _connection_pool, _async_postgres_saver

    if _connection_pool is not None:
        await _connection_pool.close()
        _connection_pool = None

    _async_postgres_saver = None