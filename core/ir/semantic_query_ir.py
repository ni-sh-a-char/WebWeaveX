from __future__ import annotations

from typing import Any, Dict

SemanticQueryIR = Dict[str, Any]


def compile_semantic_query_ir(query_type: str, target: str, result: Dict[str, Any]) -> SemanticQueryIR:
    return {
        "query_type": query_type,
        "target": target,
        "result": result,
        "evidence": result.get("evidence", result.get("semantic_evidence", {})),
        "explainable": True,
        "deterministic": True,
    }
