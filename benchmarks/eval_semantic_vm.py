from __future__ import annotations

from typing import Any
from typing import Dict

from core.bytecode import (
    compile_semantic_bytecode,
)

from core.vm import (
    SemanticVirtualMachine,
)


def eval_semantic_vm(
    case: Dict[str, Any],
) -> Dict[str, Any]:

    bc = compile_semantic_bytecode({
        "edges": case["edges"],
    })

    vm = SemanticVirtualMachine()

    r = vm.execute(
        bc["instructions"]
    )

    return {
        "predicted": (
            r["executed"]
            == case["expected"]
        ),
        "expected_match": True,
    }
