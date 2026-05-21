from __future__ import annotations


def semantic_similarity(a: str, b: str) -> dict:
    sa = set((a or "").lower().split())
    sb = set((b or "").lower().split())
    if not sa and not sb:
        return {"score": 1.0}
    return {"score": round(len(sa & sb) / max(1, len(sa | sb)), 6)}
