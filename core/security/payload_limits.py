from __future__ import annotations

MAX_HTML_SIZE = 2_000_000
MAX_MARKDOWN_SIZE = 2_000_000
MAX_JSON_SIZE = 2_000_000
MAX_GRAPH_SIZE = 500


def enforce_text_limit(text: str, limit: int) -> str:
    safe = text or ""
    if len(safe.encode("utf-8", errors="ignore")) > limit:
        return safe.encode("utf-8", errors="ignore")[:limit].decode("utf-8", errors="ignore")
    return safe
