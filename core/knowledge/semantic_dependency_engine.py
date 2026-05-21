from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.ontology_engine import build_ontology


def reconstruct_knowledge_dependencies(entities: List[str], relations: List[dict]) -> Dict[str, Any]:
    ont = build_ontology(entities, relations)
    deps = [
        {"from": r["from"], "to": r["to"], "evidence": r.get("evidence", [])}
        for r in ont.get("reconciled", {}).get("relations", [])
    ]
    ont["semantic_dependencies"] = deps
    return ont
