from __future__ import annotations

from typing import Dict

from core.fetch.base import FetchResponse


def fetch_raw(text: str, source_url: str = "") -> Dict[str, object]:
    return FetchResponse(
        source="raw",
        url=source_url or "",
        status_code=200,
        content_type="text/plain",
        text=text or "",
        ok=True,
        error="",
        metadata={"length": str(len(text or ""))},
    ).to_dict()

