from __future__ import annotations

from typing import Any, Dict, List

from core.ir._base import empty_confidence, empty_lineage, merge_evidence
from core.knowledge.ontology_reconciliation_engine import reconcile_ontology_edges

KnowledgeIR = Dict[str, Any]


def empty_knowledge_ir() -> KnowledgeIR:
    return {
        "entities": [],
        "relations": [],
        "ontology": [],
        "semantic_identity": [],
        "contradictions": [],
        "evidence": [],
        "lineage": [],
        "reconciliation": {},
        "confidence": empty_confidence(),
    }


def compile_knowledge_ir(entities: List[str], edges: List[Dict[str, Any]]) -> KnowledgeIR:
    from core.knowledge.semantic_identity_resolver import resolve_semantic_identities
    from core.knowledge.ontology_conflict_engine import detect_ontology_conflicts

    recon = reconcile_ontology_edges(edges)
    ids = resolve_semantic_identities(entities)
    conflicts = detect_ontology_conflicts(edges)
    ir = empty_knowledge_ir()
    ir["entities"] = entities
    ir["relations"] = recon.get("reconciled", [])
    ir["ontology"] = edges
    ir["semantic_identity"] = ids.get("entities", [])
    ir["contradictions"] = conflicts.get("conflicts", [])
    ir["evidence"] = [e.get("evidence", []) for e in edges if isinstance(e, dict)]
    ir["lineage"] = [recon.get("lineage", {})]
    ir["reconciliation"] = recon
    ir["confidence"] = {"score": 0.9 if not conflicts.get("conflicts") else 0.5, "basis": [], "deterministic": True}
    return ir
