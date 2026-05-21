from __future__ import annotations

from typing import Any, Dict, List


def _continuation_record(reason: str, evidence_gap: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "reason": reason,
        "boundary_violation": {"type": "unsupported_continuity"},
        "evidence_gap": evidence_gap,
        "semantic_instability": {"unstable": True},
        "fragility": {"level": 0.7},
        "confidence_caps": {"max": 0.4},
    }


def suppress_unsupported_continuity(
    label: str,
    evidence: List[str],
    *,
    min_evidence: int = 2,
) -> Dict[str, Any]:
    gap = {"required": min_evidence, "actual": len(evidence)}
    if len(evidence) < min_evidence:
        return {"suppressed": True, "record": _continuation_record(f"continuity:{label}", gap)}
    return {"suppressed": False, "record": None}


def collect_unsupported_continuity(
    evidence: List[str],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for k in inferred:
        r = suppress_unsupported_continuity(f"infer:{k}", evidence)
        if r["suppressed"] and r["record"]:
            out.append(r["record"])
    if reconciled and len(evidence) < 2:
        r = suppress_unsupported_continuity("reconcile", evidence)
        if r["suppressed"] and r["record"]:
            out.append(r["record"])
    return out
