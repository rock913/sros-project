"""Unified Langfuse initialization module.

This module provides a centralized way to initialize Langfuse observability,
handling cases where Langfuse is not configured (e.g., missing API keys).
"""

import os
from typing import Optional
from langfuse import Langfuse


class LangfuseManager:
    """Manages Langfuse instance with safe initialization."""

    _instance: Optional[Langfuse] = None
    _enabled: bool = False

    @classmethod
    def initialize(cls) -> None:
        """Initialize Langfuse with environment variables.
        
        If LANGFUSE_PUBLIC_KEY is not set, Langfuse will be disabled.
        """
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
        host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

        if public_key and secret_key:
            try:
                cls._instance = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=host
                )
                cls._enabled = True
                print(f"✅ Langfuse initialized successfully (host: {host})")
            except Exception as e:
                print(f"⚠️ Failed to initialize Langfuse: {e}")
                print("   Continuing without Langfuse observability...")
                cls._instance = None
                cls._enabled = False
        else:
            print("ℹ️ Langfuse not configured (missing API keys). Running without observability.")
            cls._instance = None
            cls._enabled = False

    @classmethod
    def get_instance(cls) -> Optional[Langfuse]:
        """Get the Langfuse instance.
        
        Returns:
            Langfuse instance if enabled, None otherwise.
        """
        if cls._instance is None and not hasattr(cls, '_initialized'):
            cls._initialized = True
            cls.initialize()
        return cls._instance

    @classmethod
    def is_enabled(cls) -> bool:
        """Check if Langfuse is enabled.
        
        Returns:
            True if Langfuse is properly initialized, False otherwise.
        """
        if not hasattr(cls, '_initialized'):
            cls.initialize()
        return cls._enabled

    @classmethod
    def trace(cls, *args, **kwargs):
        """Create a trace if Langfuse is enabled, otherwise return a no-op context.
        
        Note: Always returns NoOpTrace for now due to API compatibility issues.
        Future: Implement proper Langfuse integration when observability is prioritized.
        
        Returns:
            A no-op context manager that safely handles trace.span() calls.
        """
        # TODO: Implement proper Langfuse tracing when observability becomes priority
        # For now, return no-op to avoid AttributeError issues
        return NoOpTrace()


class NoOpTrace:
    """No-operation trace context manager for when Langfuse is disabled."""

    def __enter__(self):
        """Enter context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        return False

    def span(self, *args, **kwargs):
        """No-op span method."""
        return NoOpSpan()

    def update(self, *args, **kwargs):
        """No-op update method."""
        pass
    
    def end(self, *args, **kwargs):
        """No-op end method (for Langfuse observation compatibility)."""
        pass


class NoOpSpan:
    """No-operation span context manager."""

    def __enter__(self):
        """Enter context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        return False

    def update(self, *args, **kwargs):
        """No-op update method."""
        pass
    
    def end(self, *args, **kwargs):
        """No-op end method (for Langfuse observation compatibility)."""
        pass


# Initialize on module load
langfuse = LangfuseManager.get_instance()
