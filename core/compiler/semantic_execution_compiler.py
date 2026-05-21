from __future__ import annotations

from typing import Any
from typing import Dict

from core.bytecode import (
    compile_semantic_bytecode,
)


def compile_execution_plan(
    semantic_ir: Dict[str, Any],
) -> Dict[str, Any]:

    bytecode = (
        compile_semantic_bytecode(
            semantic_ir
        )
    )

    return {
        "plan": bytecode,
        "compiled": True,
    }
