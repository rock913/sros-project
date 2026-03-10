from __future__ import annotations

import pytest

from sros.domain.schemas import SearchQuery
from sros.servers.scholar.handler import ScholarHandler


def test_scholar_openalex_failure_can_fallback_to_mock(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_SCHOLAR_BACKEND", "openalex")
    monkeypatch.setenv("SROS_SCHOLAR_FALLBACK", "mock")

    handler = ScholarHandler()
    assert handler._openalex is not None

    def _boom(_query: SearchQuery):
        raise RuntimeError("network down")

    monkeypatch.setattr(handler._openalex, "search", _boom)

    results = handler.federated_search(SearchQuery(query="x", max_results=3, filters={}))
    assert isinstance(results, list)
    assert results and results[0]["source"] == "mock"


def test_scholar_openalex_failure_raises_without_fallback(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_SCHOLAR_BACKEND", "openalex")
    monkeypatch.delenv("SROS_SCHOLAR_FALLBACK", raising=False)

    handler = ScholarHandler()
    assert handler._openalex is not None

    def _boom(_query: SearchQuery):
        raise RuntimeError("network down")

    monkeypatch.setattr(handler._openalex, "search", _boom)

    with pytest.raises(RuntimeError):
        handler.federated_search(SearchQuery(query="x", max_results=3, filters={}))
