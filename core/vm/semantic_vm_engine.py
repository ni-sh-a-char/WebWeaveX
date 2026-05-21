from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from core.bytecode import (
    SemanticInstruction,
)


MAX_VM_STEPS = 10000


class SemanticVirtualMachine:

    def __init__(self) -> None:

        self.memory: Dict[str, Any] = {}

        self.execution_log: List[
            Dict[str, Any]
        ] = []

    def execute(
        self,
        instructions: List[
            SemanticInstruction
        ],
    ) -> Dict[str, Any]:

        executed = 0

        for ins in instructions:

            if executed >= MAX_VM_STEPS:
                break

            if ins.opcode == "LINK":

                key = (
                    f"{ins.operand['from']}"
                    "->"
                    f"{ins.operand['to']}"
                )

                self.memory[key] = True

            self.execution_log.append({
                "opcode": ins.opcode,
            })

            executed += 1

        return {
            "executed": executed,
            "memory": self.memory,
            "bounded": True,
        }
