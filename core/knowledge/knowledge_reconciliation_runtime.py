from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.ontology_reconciliation_engine import reconcile_ontology_edges
from core.knowledge.semantic_merge_validator import validate_semantic_merge


def reconcile_knowledge_runtime(sources: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    merge = validate_semantic_merge(sources, edges)
    recon = reconcile_ontology_edges(edges)
    return {"merge": merge, "reconciliation": recon, "deterministic": True}
