from __future__ import annotations

def prioritize_traversal_v3(urls: list[str]):
    return sorted(set(urls or []), key=lambda u: (u.count('/'), len(u), u))
