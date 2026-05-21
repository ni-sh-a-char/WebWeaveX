from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.ontology_engine import build_ontology


def reconstruct_knowledge_causality(entities: List[str], relations: List[dict]) -> Dict[str, Any]:
    ont = build_ontology(entities, relations)
    causal = [
        {
            **r,
            "relation": "depends_on",
            "evidence": r.get("evidence", []),
            "lineage": r.get("lineage", {}),
        }
        for r in ont.get("reconciled", {}).get("relations", [])
    ]
    ont["causal_dependencies"] = causal
    return ont
