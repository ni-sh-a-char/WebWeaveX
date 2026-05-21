from __future__ import annotations

from typing import Any, Dict

from core.evidence.recursive_semantic_closure_engine import _closure_record


def suppress_recursive_topology_lock(edge: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    lock = depth >= 2 and not ev
    record = _closure_record("recursive_topology_lock", depth) if lock else None
    return {
        **edge,
        "recursive_reality_integrity": {"preserved": not lock, "lock_suppressed": lock},
        "recursive_entropy": edge.get("entropy", {"level": 0.4 if lock else 0.1}),
        "recursive_instability": {"unstable": lock or not ev, "preserved": True},
        "recursive_truth_boundaries": {"normalization_allowed": False},
        "recursive_decay": {"active": lock},
        "recursive_uncertainty": edge.get("uncertainty", {"visible": not ev}),
        "recursive_ambiguity": edge.get("ambiguity", {"visible": False}),
        "recursive_contradictions": {"preserved": True},
        "recursive_closure_suppressed": record,
    }
