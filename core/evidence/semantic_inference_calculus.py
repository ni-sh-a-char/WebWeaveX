from __future__ import annotations

from typing import Any, Dict, List


def infer_from_evidence(
    observed: Dict[str, Any],
    evidence: List[str],
    min_evidence: int = 1,
) -> Dict[str, Any]:
    """Formal inference: inferred keys only when evidence threshold met."""
    ev = sorted(set(str(e) for e in evidence if e))
    allowed = len(ev) >= min_evidence
    inferred = {k: v for k, v in (observed or {}).items()} if allowed else {}
    return {
        "inferred": inferred,
        "allowed": allowed,
        "evidence_count": len(ev),
        "rule": "inference_requires_evidence",
        "deterministic_inputs": [f"evidence_count={len(ev)}", f"min={min_evidence}"],
    }
