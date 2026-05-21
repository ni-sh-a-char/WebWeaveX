from __future__ import annotations


def classify_link(url: str) -> str:
    u = (url or "").lower()
    if "github.com" in u:
        return "repository"
    if "docs" in u or "readthedocs" in u:
        return "documentation"
    if u.startswith("http://") or u.startswith("https://"):
        return "web"
    return "unknown"

