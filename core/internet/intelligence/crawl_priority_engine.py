from __future__ import annotations

def rank_crawl_priority(urls: list[str]):
    return sorted(set(urls or []), key=lambda u: (u.count('/'), len(u), u))
