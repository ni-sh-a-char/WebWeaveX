from __future__ import annotations

from typing import Any, Dict, List


MAX_CAUSALITY_EDGES = 500


def reconstruct_execution_causality(
    events: List[Dict[str, Any]],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    """Parser-grounded causal ordering from explicit event sequence."""
    ordered = sorted(events, key=lambda e: (int(e.get("order", 0)), str(e.get("id", ""))))[:MAX_CAUSALITY_EDGES]
    edges: List[Dict[str, Any]] = []
    for idx in range(1, len(ordered)):
        prev_e, cur_e = ordered[idx - 1], ordered[idx]
        edges.append(
            {
                "from": prev_e.get("id"),
                "to": cur_e.get("id"),
                "metadata": {"kind": "execution_cause", "basis": "event_order"},
            }
        )
    return {
        "edges": edges,
        "count": len(edges),
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
        "bounded": len(edges) <= MAX_CAUSALITY_EDGES,
    }
