from __future__ import annotations

def rank_frontier(urls: list[str]):
    return sorted(set(urls or []), key=lambda u: (u.count('/'), len(u), u))
