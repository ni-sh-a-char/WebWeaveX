from __future__ import annotations

from typing import Any, Dict

from core.ir.repository_ir import compile_repository_ir

ExecutionIR = Dict[str, Any]


def compile_execution_ir(source: str, path: str = "") -> ExecutionIR:
    repo = compile_repository_ir(source, path)
    return {
        "flows": repo.get("execution_flows", []),
        "topology": repo.get("topology", []),
        "services": repo.get("services", []),
        "evidence": repo.get("semantic_evidence", {}),
        "lineage": repo.get("lineage", {}),
        "confidence": repo.get("confidence", {}),
    }
