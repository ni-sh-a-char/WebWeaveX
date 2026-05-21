from __future__ import annotations

from dataclasses import dataclass

from typing import Dict
from typing import Any


@dataclass(frozen=True)
class SemanticInstruction:

    opcode: str

    operand: Dict[str, Any]
