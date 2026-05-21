from __future__ import annotations

def score_extraction(result: dict):
    txt = result.get('raw_text', '') or ''
    edges = result.get('relationships', {}).get('execution_graph', {}).get('edges', [])
    return {"score": round(min(1.0, (len(txt) / 5000.0) + (len(edges) / 1000.0)), 6)}
