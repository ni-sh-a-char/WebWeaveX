from __future__ import annotations

def score_semantic_confidence(result: dict):
    has_repo = bool(result.get('content', {}).get('repository'))
    has_docs = bool(result.get('content', {}).get('documents'))
    has_graph = bool(result.get('relationships', {}).get('execution_graph', {}).get('edges', []))
    score = (1 if has_repo else 0) + (1 if has_docs else 0) + (1 if has_graph else 0)
    return {"confidence": round(score / 3.0, 6)}
