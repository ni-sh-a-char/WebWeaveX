from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.ontology_reconciliation_engine import reconcile_ontology_edges


def reconcile_query(entities: List[str], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    recon = reconcile_ontology_edges(edges)
    return {"entities": entities, "reconciliation": recon, "explainable": True}
