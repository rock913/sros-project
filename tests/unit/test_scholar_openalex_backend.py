from __future__ import annotations

from typing import Any, Dict

import pytest

from sros.domain.schemas import SearchQuery
from sros.servers.scholar.federated.openalex_backend import OpenAlexBackend


class _DummyResp:
    def __init__(self, status_code: int, payload: Dict[str, Any]):
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self) -> Dict[str, Any]:
        return self._payload


def test_openalex_backend_transforms_results(monkeypatch: pytest.MonkeyPatch):
    payload = {
        "results": [
            {
                "id": "https://openalex.org/W123",
                "doi": "https://doi.org/10.1000/xyz123",
                "display_name": "A Test Paper",
                "publication_year": 2024,
                "abstract_inverted_index": {"hello": [0], "world": [1]},
                "host_venue": {"display_name": "Test Journal"},
                "primary_location": {"landing_page_url": "https://example.org/paper"},
                "authorships": [
                    {"author": {"display_name": "Alice"}},
                    {"author": {"display_name": "Bob"}},
                ],
            }
        ]
    }

    backend = OpenAlexBackend(session=None)

    def _fake_get(url: str, params=None, timeout=None):
        assert url.endswith("/works")
        assert params["search"] == "transformer"
        return _DummyResp(200, payload)

    monkeypatch.setattr(backend.session, "get", _fake_get)

    results = backend.search(SearchQuery(query="transformer", max_results=1, filters={}))
    assert len(results) == 1
    r0 = results[0]
    assert r0["title"] == "A Test Paper"
    assert r0["authors"] == ["Alice", "Bob"]
    assert r0["year"] == 2024
    assert r0["journal"] == "Test Journal"
    assert r0["abstract"] == "hello world"
    assert r0["url"] == "https://example.org/paper"
    assert r0["source"] == "openalex"
