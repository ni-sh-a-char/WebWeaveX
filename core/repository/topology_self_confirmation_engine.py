from __future__ import annotations

from typing import Any, Dict

from core.evidence.unsupported_stabilization_engine import _stabilization_record


def suppress_topology_self_confirmation(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    inferred = bool(edge.get("inferred"))
    self_confirm = inferred and len(ev) < 1
    record = _stabilization_record("topology_self_confirmation", {"required": 1, "actual": len(ev)}) if self_confirm else None
    return {
        **edge,
        "truth_preservation": {"preserved": not self_confirm, "self_confirmation_blocked": self_confirm},
        "instability": {"unstable": self_confirm or not ev, "preserved": True},
        "entropy": {"level": 0.5 if self_confirm else 0.1},
        "truth_boundaries": {"propagation_allowed": bool(ev)},
        "confidence_collapse": {"max": 0.35} if self_confirm else edge.get("confidence_caps", {}),
        "stabilization_suppressed": record,
    }
