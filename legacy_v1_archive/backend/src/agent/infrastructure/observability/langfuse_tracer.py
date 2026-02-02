"""
LangFuse Tracer for Co-STORM Observability

This module implements deep tracing for the Co-STORM workflow using LangFuse.
Provides end-to-end observability for research agent execution with nested spans.

@Hexagonal Architecture:
- Infrastructure layer: External service integration (LangFuse API)
- Application layer: Uses tracer for span creation and metadata enrichment
- Domain layer: Trace IDs propagated to UI for user debugging

@Tracing Strategy:
- Parent Trace: "Co-STORM Execution" (full research session)
- Child Spans: Librarian Node, Analyst Node, Writer Node
- Metadata: Research topic, perspective count, paper counts
- Links: Trace IDs included in mindmap_generated events for frontend linking

@LangFuse Integration:
- Automatic span timing and performance metrics
- Error tracking with stack traces
- User tagging for multi-researcher analytics
- Frontend links back to detailed traces
"""

import contextlib
import os
from typing import Any, Dict, Optional

import langfuse
from langfusecore import Langfuse
from agent.configuration import Configuration


class LangFuseTracer:
    """Manages LangFuse tracing for Co-STORM research workflows.

    @Hexagonal Architecture:
    - Infrastructure layer: Manages LangFuse SDK integration
    - Configurable: Enables/disables tracing based on environment
    - Thread-safe: Uses LangFuse's built-in context management

    @Usage Pattern:
    with tracer.start_trace("Co-STORM Execution", {"topic": "RL"}) as trace:
        with tracer.start_span(trace, "Librarian Node", {}) as span:
            # Search for papers
            span.update(metadata={"papers_found": 15})
    """

    def __init__(self):
        """Initialize LangFuse tracer with configuration."""
        self._enabled = self._should_enable_tracing()
        if not self._enabled:
            print("[LangFuse] Tracing disabled - set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY to enable")
            self._langfuse = None
        else:
            try:
                self._langfuse = Langfuse(
                    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                    host=os.getenv("LANGFUSE_HOST"),
                )
                print("[LangFuse] Tracing enabled and initialized")
            except Exception as e:
                print(f"[LangFuse] Failed to initialize: {e}")
                self._langfuse = None
                self._enabled = False

    def _should_enable_tracing(self) -> bool:
        """Determine if tracing should be enabled based on configuration."""
        config = Configuration.from_runnable_config({})
        return bool(
            config.langfuse_public_key
            and config.langfuse_secret_key
        )

    @property
    def enabled(self) -> bool:
        """Check if tracing is currently enabled."""
        return self._enabled and self._langfuse is not None

    @contextlib.contextmanager
    def start_trace(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        session_id: Optional[str] = None
    ):
        """Create a new trace for a research session.

        Args:
            name: Trace name (e.g., "Co-STORM Execution")
            metadata: Extra metadata (topic, perspective count, etc.)
            tags: Tags for filtering/grouping
            session_id: Research session ID for correlation

        Returns:
            Context manager yielding the trace object
        """
        trace = None

        if not self.enabled:
            # Yield a dummy object for compatibility
            yield DummyTrace()
            return

        try:
            trace = self._langfuse.trace(
                name=name,
                metadata=metadata or {},
                tags=tags or [],
                session_id=session_id
            )
            yield trace
        except Exception as e:
            print(f"[LangFuse] Failed to start trace '{name}': {e}")
            yield DummyTrace()
        finally:
            # LangFuse handles auto-flushing on context exit
            pass

    @contextlib.contextmanager
    def start_span(
        self,
        parent: Any,  # LangFuse trace or span
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        span_type: str = "generic"
    ):
        """Create a child span within a trace.

        Args:
            parent: Parent trace or span object
            name: Span name (e.g., "Librarian Node", "Analyst Node")
            metadata: Span-specific metadata
            span_type: Type of span for categorization

        Returns:
            Context manager yielding the span object
        """
        span = None

        if not self.enabled:
            # Yield a dummy object for compatibility
            yield DummySpan()
            return

        try:
            # Use span creation based on parent type
            if hasattr(parent, 'span'):
                # Parent is a trace, create child span
                span = parent.span(
                    name=name,
                    metadata=metadata or {},
                    span_type=span_type
                )
            else:
                # Parent might be another span, create nested span
                span = parent.span(
                    name=name,
                    metadata=metadata or {},
                    span_type=span_type
                )
            yield span
        except Exception as e:
            print(f"[LangFuse] Failed to start span '{name}': {e}")
            yield DummySpan()
        finally:
            # LangFuse handles auto-flushing
            pass

    def update_metadata(self, span: Any, metadata: Dict[str, Any]) -> None:
        """Update metadata on an active span.

        Args:
            span: Active span object
            metadata: New metadata to add/update
        """
        if not self.enabled:
            return

        try:
            span.update(metadata=metadata)
        except Exception as e:
            print(f"[LangFuse] Failed to update span metadata: {e}")

    def record_error(self, span: Any, error: Exception) -> None:
        """Record an error on an active span.

        Args:
            span: Active span object
            error: Exception to record
        """
        if not self.enabled:
            return

        try:
            span.update(level="ERROR", status_message=str(error))
        except Exception as e:
            print(f"[LangFuse] Failed to record error: {e}")

    def get_trace_url(self, trace: Any) -> Optional[str]:
        """Get the URL to view the trace in LangFuse UI.

        Args:
            trace: Completed trace object

        Returns:
            URL string or None if unavailable
        """
        if not self.enabled or not hasattr(trace, 'get_trace_url'):
            return None

        try:
            return trace.get_trace_url()
        except Exception as e:
            print(f"[LangFuse] Failed to get trace URL: {e}")
            return None


class DummyTrace:
    """Dummy trace object for when tracing is disabled."""

    def __init__(self):
        self.id = "dummy-trace-id"

    def span(self, *args, **kwargs):
        return DummySpan()


class DummySpan:
    """Dummy span object for when tracing is disabled."""

    def __init__(self):
        self.id = "dummy-span-id"

    def update(self, **kwargs):
        pass


# Global tracer instance (singleton pattern)
_langfuse_tracer = None


def get_langfuse_tracer() -> LangFuseTracer:
    """Factory function for LangFuse tracer instance.

    Implements singleton pattern for consistent tracing across the application.

    Returns:
        Configured LangFuse tracer instance
    """
    global _langfuse_tracer

    if _langfuse_tracer is None:
        _langfuse_tracer = LangFuseTracer()

    return _langfuse_tracer