from __future__ import annotations

def score_freshness(versioned: dict):
    pairs = sorted((versioned or {}).items())
    return {"score": 1.0 if pairs else 0.5, "signals": pairs}
