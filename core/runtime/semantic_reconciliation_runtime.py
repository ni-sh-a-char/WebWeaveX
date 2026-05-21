from __future__ import annotations

from typing import Any, Dict

from core.knowledge.ontology_reconciliation_engine import reconcile_ontology_edges


def reconcile_semantic_state(edges: list) -> Dict[str, Any]:
    return reconcile_ontology_edges(edges)
