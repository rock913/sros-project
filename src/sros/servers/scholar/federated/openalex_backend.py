from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional

import requests

from sros.domain.schemas import SearchQuery


class OpenAlexBackend:
    """Minimal OpenAlex-backed federated search.

    Notes:
    - Uses `requests` (sync) to keep integration simple.
    - Network usage should be gated by higher-level config (see ScholarHandler).
    - OpenAlex recommends providing a `mailto` query param.
    """

    def __init__(
        self,
        base_url: str | None = None,
        mailto: str | None = None,
        session: Optional[requests.Session] = None,
        timeout_s: float = 15.0,
        max_retries: int = 2,
        retry_backoff_s: float = 0.75,
    ) -> None:
        self.base_url = (base_url or os.getenv("SROS_OPENALEX_BASE_URL") or "https://api.openalex.org").rstrip("/")
        self.mailto = mailto or os.getenv("SROS_OPENALEX_MAILTO") or os.getenv("SROS_OPENALEX_EMAIL")
        self.session = session or requests.Session()
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.retry_backoff_s = retry_backoff_s

    def search(self, query: SearchQuery) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/works"
        params: Dict[str, Any] = {
            "search": query.query,
            "per-page": min(int(query.max_results or 10), 200),
            "select": "id,doi,display_name,publication_year,abstract_inverted_index,host_venue,primary_location,best_oa_location,authorships",
        }
        if self.mailto:
            params["mailto"] = self.mailto

        data = self._get_json_with_retry(url, params=params)
        results = []
        for work in (data or {}).get("results", []) or []:
            results.append(self._transform_work(work))
        return results

    def _get_json_with_retry(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    time.sleep(self.retry_backoff_s * (2 ** (attempt - 1)))
                resp = self.session.get(url, params=params, timeout=self.timeout_s)
                if resp.status_code in (429,) or 500 <= resp.status_code <= 599:
                    # Retryable
                    last_exc = RuntimeError(f"OpenAlex HTTP {resp.status_code}")
                    continue
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_exc = e
                continue
        raise RuntimeError(f"OpenAlex request failed after retries: {last_exc}")

    @staticmethod
    def _abstract_from_inverted_index(inverted_index: Any) -> str:
        if not isinstance(inverted_index, dict):
            return ""

        words_by_pos: Dict[int, str] = {}
        for word, positions in inverted_index.items():
            if isinstance(positions, list):
                for pos in positions:
                    if isinstance(pos, int):
                        words_by_pos[pos] = str(word)
            elif isinstance(positions, int):
                words_by_pos[positions] = str(word)

        if not words_by_pos:
            return ""
        return " ".join(words_by_pos[i] for i in sorted(words_by_pos.keys()))

    @staticmethod
    def _transform_work(work: Dict[str, Any]) -> Dict[str, Any]:
        authors: List[str] = []
        for a in work.get("authorships", []) or []:
            author = (a.get("author") or {}).get("display_name")
            if author:
                authors.append(author)

        venue = (work.get("host_venue") or {}).get("display_name")
        abstract = OpenAlexBackend._abstract_from_inverted_index(work.get("abstract_inverted_index"))

        primary_url = None
        primary_loc = work.get("primary_location") or {}
        if isinstance(primary_loc, dict):
            primary_url = primary_loc.get("landing_page_url") or primary_loc.get("pdf_url")

        if not primary_url:
            best_loc = work.get("best_oa_location") or {}
            if isinstance(best_loc, dict):
                primary_url = best_loc.get("landing_page_url") or best_loc.get("pdf_url")

        return {
            "id": work.get("id"),
            "doi": work.get("doi"),
            "title": work.get("display_name"),
            "authors": authors,
            "year": work.get("publication_year"),
            "journal": venue,
            "abstract": abstract,
            "url": primary_url or work.get("id"),
            "source": "openalex",
        }
