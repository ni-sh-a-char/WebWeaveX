from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from .semantic_instruction_set import (
    SemanticInstruction,
)


MAX_BYTECODE = 10000


def compile_semantic_bytecode(
    semantic_ir: Dict[str, Any],
) -> Dict[str, Any]:

    instructions: List[
        SemanticInstruction
    ] = []

    inner = semantic_ir.get("optimized_ir", semantic_ir)
    edges = []
    if isinstance(inner, dict):
        edges = list(inner.get("edges", []) or [])
    if not edges:
        edges = list(semantic_ir.get("edges", []) or [])

    for edge in edges[:MAX_BYTECODE]:

        instructions.append(
            SemanticInstruction(
                opcode="LINK",
                operand={
                    "from": edge.get("from"),
                    "to": edge.get("to"),
                },
            )
        )

    return {
        "instructions": instructions,
        "count": len(instructions),
        "bounded": True,
    }
