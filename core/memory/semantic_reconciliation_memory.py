from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.ontology_reconciliation_engine import reconcile_ontology_edges


def reconcile_memory_states(states: List[Dict[str, Any]]) -> Dict[str, Any]:
    edges = []
    for s in states:
        edges.extend(s.get("relations", s.get("edges", [])) or [])
    recon = reconcile_ontology_edges(edges if isinstance(edges, list) else [])
    return {"states": len(states), "reconciliation": recon, "deterministic": True}
