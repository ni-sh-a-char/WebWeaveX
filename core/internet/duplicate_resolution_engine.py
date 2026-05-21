from __future__ import annotations

def resolve_duplicates(items: list[dict]):
    seen = set(); out = []
    for item in sorted(items or [], key=lambda x: str(x)):
        key = str(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out
