from __future__ import annotations

from typing import Any, Dict

from core.documents.document_semantic_ir_engine import build_document_semantic_ir
from core.ir._base import empty_confidence, empty_lineage, merge_evidence

DocumentIR = Dict[str, Any]


def empty_document_ir() -> DocumentIR:
    return {
        "concepts": [],
        "claims": [],
        "arguments": [],
        "tutorial_steps": [],
        "dependencies": [],
        "references": [],
        "contradictions": [],
        "rhetorical_units": [],
        "semantic_roles": [],
        "explanation_chains": [],
        "concept_progressions": [],
        "instructional_flows": [],
        "semantic_graph": {},
        "lineage": empty_lineage("document_ir"),
        "confidence": empty_confidence(),
    }


def compile_document_ir(text: str) -> DocumentIR:
    raw = build_document_semantic_ir(text)
    ir = empty_document_ir()
    rhet = raw.get("rhetorical", {})
    arg = raw.get("argument", {})
    ir["rhetorical_units"] = rhet.get("units", [])
    ir["semantic_roles"] = rhet.get("roles", [])
    ir["claims"] = arg.get("nodes", [])
    ir["arguments"] = arg.get("dependencies", [])
    ir["tutorial_steps"] = raw.get("prerequisites", {}).get("chain", [])
    ir["concept_progressions"] = raw.get("progression", {}).get("progression", [])
    ir["instructional_flows"] = raw.get("prerequisites", {}).get("prerequisites", [])
    ir["explanation_chains"] = raw.get("dependency_graph", {}).get("edges", [])
    ir["semantic_graph"] = raw.get("dependency_graph", {})
    ir["semantic_evidence"] = merge_evidence(raw.get("evidence", []))
    ir["lineage"] = empty_lineage("document_semantic_ir")
    ir["confidence"] = {"score": 0.7 if ir["rhetorical_units"] else 0.3, "basis": raw.get("evidence", []), "deterministic": True}
    ir["_raw"] = raw
    return ir
