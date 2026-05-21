from __future__ import annotations

from typing import Any, Dict

from core.evidence.recursive_semantic_closure_engine import _closure_record


def suppress_recursive_ontology_lock(edge: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    lock = depth >= 2 and len(ev) < 2
    record = _closure_record("recursive_ontology_lock", depth) if lock else None
    return {
        **edge,
        "recursive_reality_integrity": {"preserved": not lock, "lock_suppressed": lock},
        "recursive_entropy": edge.get("entropy", {"level": 0.3 if lock else 0.1}),
        "recursive_instability": {"unstable": lock, "preserved": True},
        "recursive_truth_boundaries": {"lock_in_allowed": False},
        "recursive_decay": {"active": lock},
        "recursive_contradictions": edge.get("contradictions", {"preserved": True}),
        "recursive_closure_suppressed": record,
    }
