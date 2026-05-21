from __future__ import annotations

def rank_sources(urls: list[str]):
    def score(u: str):
        return (0 if u.startswith('https://') else 1, len(u), u)
    return sorted(set(urls or []), key=score)
