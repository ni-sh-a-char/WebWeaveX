from __future__ import annotations

from typing import Any, Dict


def semantic_stop(reason: str, *, propagation: bool = True, expansion: bool = True) -> Dict[str, Any]:
    return {
        "stopped": True,
        "reason": reason,
        "propagation_halted": propagation,
        "expansion_halted": expansion,
    }
