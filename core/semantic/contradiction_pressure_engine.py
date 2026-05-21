from __future__ import annotations

from typing import Any, Dict


def compute_contradiction_pressure(contradicted: Dict[str, Any]) -> Dict[str, Any]:
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    preserved = contradicted.get("preserved", False) if isinstance(contradicted, dict) else False
    count = len(pairs)
    pressure = round(min(1.0, count * 0.25), 3)
    return {
        "pressure": pressure,
        "pair_count": count,
        "preserved": preserved,
        "suppress_propagation": count > 0,
        "suppress_reconciliation": count > 0,
        "suppress_ontology_expansion": count > 0,
        "suppress_topology_expansion": count > 0,
        "confidence_reduction": round(min(0.4, count * 0.15), 3),
    }
