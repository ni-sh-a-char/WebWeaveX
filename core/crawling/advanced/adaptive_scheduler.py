from __future__ import annotations

def score_url(url: str):
    u=(url or '').lower()
    return (3 if 'docs' in u else 0) + (2 if 'api' in u else 0) + (2 if 'github.com' in u else 0)

def schedule(urls: list):
    return sorted(set(urls or []), key=lambda u: (-score_url(u), u))
