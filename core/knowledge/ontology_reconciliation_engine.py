from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.semantic_merge_rigor_engine import merge_with_evidence
from core.knowledge.ontology_lineage_engine import stamp_ontology_lineage


def reconcile_ontology_edges(edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    reconciled = []
    rejected = []
    for e in edges or []:
        ev = e.get("evidence", []) or []
        if not ev:
            rejected.append({"edge": e, "reason": "missing_evidence"})
            continue
        stamped = stamp_ontology_lineage(e, stage="reconcile")
        reconciled.append(stamped)
    merge = merge_with_evidence([{"evidence": e.get("evidence", [])} for e in reconciled])
    return {
        "reconciled": reconciled,
        "rejected": rejected,
        "merge": merge,
        "lineage": {"stage": "ontology_reconciliation", "count": len(reconciled)},
    }
