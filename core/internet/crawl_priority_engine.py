from __future__ import annotations

def prioritize_sources(urls: list[str]):
    return sorted(set(urls or []), key=lambda u: (u.count('/'), len(u), u))
