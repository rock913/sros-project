"""Unified Langfuse initialization module.

This module provides a centralized way to initialize Langfuse observability,
handling cases where Langfuse is not configured (e.g., missing API keys).
"""

import os

from langfuse import Langfuse


class LangfuseManager:
    """Manages Langfuse instance with safe initialization."""

    _instance: Langfuse | None = None
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
    def get_instance(cls) -> Langfuse | None:
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
    def trace(cls, name: str = None, **kwargs):
        """Create a trace/span if Langfuse is enabled, otherwise return a no-op context.
        
        Handles compatibility between Langfuse SDK v2 (trace) and v3 (start_span).
        
        Returns:
            Langfuse trace object or NoOpTrace.
        """
        if cls.is_enabled() and cls._instance:
            # Check if trace method exists (SDK v2)
            if hasattr(cls._instance, 'trace'):
                return cls._instance.trace(name=name, **kwargs)
            
            # SDK v3 Compatibility: use start_span as root trace
            # Filter arguments supported by start_span
            # start_span usually supports: name, metadata, input, start_time
            # user_id, session_id etc must be passed via update()
            
            start_span_args = {}
            if name:
                start_span_args['name'] = name
            
            if 'metadata' in kwargs:
                start_span_args['metadata'] = kwargs.pop('metadata')
                
            # Create the span/trace
            try:
                # Assuming start_span exists in v3
                trace = cls._instance.start_span(**start_span_args)
                
                # Apply remaining kwargs (user_id, session_id, etc) via update if any
                if kwargs:
                    try:
                        trace.update(**kwargs)
                    except Exception as e:
                        print(f"⚠️ Failed to update trace attributes: {e}")
                
                return trace
            except Exception as e:
                print(f"⚠️ Failed to create Langfuse trace: {e}")
                return NoOpTrace()
                
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
