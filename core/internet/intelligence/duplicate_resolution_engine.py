from __future__ import annotations

def resolve_duplicate_sources(items: list[dict]):
    seen=set(); out=[]
    for i in sorted(items or [], key=lambda x: str(x)):
        k=str(i)
        if k in seen: continue
        seen.add(k); out.append(i)
    return out
