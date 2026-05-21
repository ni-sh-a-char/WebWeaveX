from __future__ import annotations

from typing import Any, Dict


def model_recursive_phase_space(key_count: int, ambiguity_count: int, depth: int) -> Dict[str, Any]:
    volume = round(min(1.0, key_count * 0.1 + ambiguity_count * 0.08), 3)
    reduction = depth >= 4 and key_count <= 1
    return {"volume": volume, "reduction_blocked": reduction, "preserved": volume > 0}
