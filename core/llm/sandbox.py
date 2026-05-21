from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict


def isolate_llm(core_result: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
    base = deepcopy(core_result)
    return {
        "structured_data": base,
        "llm": llm_output,
    }
