from __future__ import annotations

from typing import Any, Dict, List

from core.ast import compile_semantic_ast_ir

from .schema_types import (
    SemanticNode,
    SemanticEdge,
)


def compile_typed_repository_ir(
    source: str,
) -> Dict[str, Any]:

    ast_ir = compile_semantic_ast_ir(source)

    nodes: List[SemanticNode] = []
    edges: List[SemanticEdge] = []

    for fn in ast_ir["ast"]["functions"]:
        nodes.append(
            SemanticNode(
                id=fn["name"],
                type="function",
            )
        )

    funcs = ast_ir["ast"]["functions"]

    for i in range(len(funcs) - 1):
        edges.append(
            SemanticEdge(
                source=funcs[i]["name"],
                target=funcs[i + 1]["name"],
                relation="execution_flow",
                evidence=["ast_order"],
            )
        )

    return {
        "nodes": nodes,
        "edges": edges,
        "typed": True,
        "deterministic": True,
    }
