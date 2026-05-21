from __future__ import annotations

from typing import Any, Dict, List


def mark_insufficiency(bundle: Dict[str, Any], min_evidence: int = 2) -> Dict[str, Any]:
    evidence = bundle.get("evidence", []) or []
    insufficient = len(evidence) < min_evidence
    flags = []
    if insufficient:
        flags.append("insufficient_evidence")
    if bundle.get("ambiguities"):
        flags.append("ambiguous_claim")
    return {
        "insufficient": insufficient,
        "flags": sorted(set(flags)),
        "evidence_count": len(evidence),
        "required": min_evidence,
        "message": "insufficient evidence" if insufficient else "evidence_ok",
    }
