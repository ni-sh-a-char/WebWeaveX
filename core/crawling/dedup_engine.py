from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit


def canonical_url(url: str) -> str:
    s = urlsplit((url or "").strip())
    return urlunsplit((s.scheme.lower(), s.netloc.lower(), s.path or "/", s.query, ""))

