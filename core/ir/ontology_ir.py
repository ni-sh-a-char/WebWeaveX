from __future__ import annotations

from typing import Any, Dict, List

from core.ir.knowledge_ir import compile_knowledge_ir

OntologyIR = Dict[str, Any]


def compile_ontology_ir(entities: List[str], edges: List[Dict[str, Any]]) -> OntologyIR:
    k = compile_knowledge_ir(entities, edges)
    return {"ontology": k.get("ontology", []), "entities": k.get("entities", []), "reconciliation": k.get("reconciliation", {}), "confidence": k.get("confidence", {})}
