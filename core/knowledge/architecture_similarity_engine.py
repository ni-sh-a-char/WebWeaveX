from __future__ import annotations


def architecture_similarity(a: dict, b: dict):
    sa = set((a or {}).get("styles", []))
    sb = set((b or {}).get("styles", []))
    union = len(sa | sb)
    if union == 0:
        return {"score": 1.0, "shared": []}
    inter = sorted(sa & sb)
    return {"score": len(inter) / union, "shared": inter}
