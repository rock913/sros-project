from __future__ import annotations

import re
from typing import Any, Dict, Optional

import requests


class ExtHandler:
    """Phase-1 MVP external tool wrappers (CLI-Anything style).

    Keep behavior deterministic and offline-testable via monkeypatching requests.
    """

    @staticmethod
    def web_scrape(url: str, *, timeout_s: float = 15.0) -> Dict[str, Any]:
        u = (url or "").strip()
        if not u:
            return {"ok": False, "error": "Missing required arg: url"}

        try:
            resp = requests.get(
                u,
                timeout=float(timeout_s),
                headers={
                    "User-Agent": "SROS/4.0 Phase1 web-scrape (requests)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": f"Request failed: {e}", "url": u}

        if getattr(resp, "status_code", None) != 200:
            return {"ok": False, "error": f"HTTP {getattr(resp, 'status_code', 'unknown')}", "url": u}

        text = str(getattr(resp, "text", "") or "")
        headers = getattr(resp, "headers", {}) or {}
        if not hasattr(headers, "get"):
            headers = {}
        ctype = str(headers.get("content-type") or headers.get("Content-Type") or "")

        title: Optional[str] = None
        if "html" in ctype.lower() or "<html" in text.lower():
            m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
            if m:
                title = re.sub(r"\s+", " ", m.group(1)).strip() or None

            # super-lightweight tag stripping (MVP)
            cleaned = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
            cleaned = re.sub(r"<style[\s\S]*?</style>", " ", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"<[^>]+>", " ", cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            out_text = cleaned
        else:
            out_text = re.sub(r"\s+", " ", text).strip()

        return {"ok": True, "url": u, "title": title, "text": out_text}
