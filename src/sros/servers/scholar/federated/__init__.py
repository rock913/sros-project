"""Federated search backends for Scholar.

Default behavior in SROS is to stay deterministic/offline-friendly.
Backends that perform network calls must be explicitly enabled.
"""

from .openalex_backend import OpenAlexBackend

__all__ = ["OpenAlexBackend"]
