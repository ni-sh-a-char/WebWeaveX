from __future__ import annotations

from typing import Any, Dict, List


def apply_semantic_conservatism(bundle: Dict[str, Any], min_evidence: int = 2) -> Dict[str, Any]:
    """Prefer incomplete truth over hallucinated completeness when evidence is weak."""
    evidence = bundle.get("evidence", []) or []
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    contradicted = bundle.get("contradicted", {}) or {}

    if len(evidence) < min_evidence:
        ambiguities.append("weak_evidence")
    if contradicted.get("preserved") or contradicted.get("pairs"):
        ambiguities.append("unresolved_contradiction")

    confidence = dict(bundle.get("confidence_basis", {}) or {})
    score = float(confidence.get("score", 0.5))
    if len(evidence) < min_evidence:
        score = round(min(score, 0.35), 3)
    if contradicted.get("preserved"):
        score = round(min(score, 0.45), 3)

    confidence["score"] = score
    confidence["conservative"] = True
    confidence["deterministic_inputs"] = sorted(
        set(confidence.get("deterministic_inputs", []) or []) | {f"evidence_count={len(evidence)}"}
    )

    bundle["ambiguities"] = sorted(set(str(a) for a in ambiguities if a))
    bundle["confidence_basis"] = confidence
    if bundle.get("semantic_basis"):
        bundle["semantic_basis"] = {**bundle["semantic_basis"], "conservative_score": score}
    return bundle
