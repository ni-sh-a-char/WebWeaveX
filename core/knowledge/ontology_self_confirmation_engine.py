from __future__ import annotations

from typing import Any, Dict

from core.evidence.unsupported_stabilization_engine import _stabilization_record


def suppress_ontology_self_confirmation(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    inferred = bool(edge.get("inferred"))
    self_confirm = inferred and len(ev) < 2
    record = _stabilization_record("ontology_self_confirmation", {"required": 2, "actual": len(ev)}) if self_confirm else None
    collapse = {"max": 0.35} if self_confirm else edge.get("confidence_caps", {})
    entropy = {"level": 0.6 if self_confirm else 0.1}
    return {
        **edge,
        "truth_preservation": {"preserved": not self_confirm, "self_confirmation_blocked": self_confirm},
        "instability": {"unstable": self_confirm, "preserved": True},
        "entropy": entropy,
        "truth_boundaries": {"equivalence_allowed": len(ev) >= 2},
        "confidence_collapse": collapse,
        "stabilization_suppressed": record,
    }
