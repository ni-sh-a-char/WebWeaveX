from __future__ import annotations

from typing import Any, Dict, List, Optional


def _suppression_record(
    reason: str,
    evidence_gap: Dict[str, Any],
    *,
    fragility_pressure: float = 0.0,
    contradiction_pressure: float = 0.0,
    ambiguity_pressure: float = 0.0,
    confidence_caps: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "reason": reason,
        "evidence_gap": evidence_gap,
        "fragility_pressure": {"level": fragility_pressure},
        "contradiction_pressure": {"level": contradiction_pressure},
        "ambiguity_pressure": {"level": ambiguity_pressure},
        "confidence_caps": confidence_caps or {},
    }


def suppress_speculative_inference(
    label: str,
    evidence: List[str],
    *,
    inferred: bool = False,
    min_evidence: int = 2,
    fragility_level: str = "medium",
) -> Dict[str, Any]:
    gap = {"required": min_evidence, "actual": len(evidence), "inferred": inferred}
    speculative = inferred and len(evidence) < min_evidence
    frag_map = {"high": 0.8, "medium": 0.5, "low": 0.2}
    if speculative:
        return {
            "suppressed": True,
            "label": label,
            "record": _suppression_record(
                f"speculative_{label}",
                gap,
                fragility_pressure=frag_map.get(fragility_level, 0.5),
            ),
        }
    return {"suppressed": False, "label": label, "record": None}


def collect_suppressed_speculation(
    evidence: List[str],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for key in inferred:
        r = suppress_speculative_inference(f"infer:{key}", evidence, inferred=True)
        if r["suppressed"] and r["record"]:
            out.append(r["record"])
    if reconciled and len(evidence) < 2:
        r = suppress_speculative_inference("reconcile", evidence)
        if r["suppressed"] and r["record"]:
            out.append(r["record"])
    return out
