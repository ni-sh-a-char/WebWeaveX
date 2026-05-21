from __future__ import annotations

def score_structure_quality(graph: dict):
    n = len((graph or {}).get('nodes', [])); e = len((graph or {}).get('edges', []))
    if n == 0:
        return {"score": 0.0}
    return {"score": round(min(1.0, e / max(1, n * 2)), 6)}
