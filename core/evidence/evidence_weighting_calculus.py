from __future__ import annotations

from typing import Any, Dict, List


def weight_evidence_calculus(evidence: List[str], parser_backed: bool = False) -> Dict[str, Any]:
    """Deterministic weights: parser evidence > textual > inferred."""
    items = sorted(set(str(e) for e in evidence if e))
    weights: Dict[str, float] = {}
    for e in items:
        if e.startswith("parser:"):
            weights[e] = 1.0
        elif parser_backed:
            weights[e] = 0.85
        else:
            weights[e] = 0.6
    total = round(sum(weights.values()), 3)
    return {
        "weights": weights,
        "total": total,
        "parser_backed": parser_backed,
        "deterministic_inputs": [f"items={len(items)}", f"total={total}"],
    }
