from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.semantic_merge_rigor_engine import merge_with_evidence
from core.knowledge.ontology_conflict_engine import detect_ontology_conflicts


def validate_semantic_merge(sources: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    merge = merge_with_evidence(sources)
    conflicts = detect_ontology_conflicts(edges)
    allowed = merge.get("merged", False) and conflicts.get("pressure", 0) < 0.75
    return {
        "allowed": allowed,
        "merge": merge,
        "conflicts": conflicts,
        "rejected_reason": None if allowed else "merge_or_conflict_blocked",
    }
