from __future__ import annotations

def dedup_frontier(urls: list[str]):
    return sorted(set(urls or []))
