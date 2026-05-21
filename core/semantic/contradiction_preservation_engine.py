from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.contradiction_evidence_engine import detect_contradiction_evidence
from core.evidence.lineage_engine import build_lineage
from core.evidence.reconciliation_evidence_engine import reconcile_evidence


def preserve_contradictions(snippets: List[str]) -> Dict[str, Any]:
    detection = detect_contradiction_evidence(snippets)
    pairs = detection.get("contradiction_pairs", []) or []
    conflicts = detection.get("conflicts", []) or []
    conflicting_claims = [
        {"polarity_a": c.get("polarity_a"), "polarity_b": c.get("polarity_b"), "evidence": c.get("evidence")}
        for c in conflicts
    ]
    reconciliation = reconcile_evidence(
        [{"key": str(p), "value": "conflict", "source": f"snippet:{i}"} for i, p in enumerate(pairs)]
    )
    lineage = build_lineage(
        [
            {
                "stage": "detect",
                "inputs": [f"snippet:{i}" for i in range(len(snippets or []))],
                "outputs": [str(p) for p in pairs],
            }
        ]
    )
    return {
        "observed": {"snippets": snippets},
        "parsed": {},
        "inferred": {},
        "reconciled": {},
        "contradicted": {"pairs": pairs, "preserved": bool(pairs), "collapsed": False},
        "derived": {"conflict_count": len(conflicts)},
        "ambiguities": ["competing_interpretations"] if pairs else [],
        "conflicting_claims": conflicting_claims,
        "evidence": list(detection.get("evidence", [])),
        "lineage": lineage,
        "reconciliation": reconciliation,
        "confidence_basis": {
            "basis": "contradiction_preservation",
            "pair_count": len(pairs),
            "score": round(max(0.0, 1.0 - len(pairs) * 0.2), 3),
            "deterministic_inputs": [f"pairs={len(pairs)}"],
        },
        "why": {"summary": "contradictions_preserved_not_collapsed"},
        "parser_basis": {},
        "graph_basis": {},
        "semantic_basis": {"conflict_count": len(conflicts)},
    }
