from __future__ import annotations

from typing import Any, Dict


def model_recursive_agency(autonomy_ok: bool, depth: int) -> Dict[str, Any]:
    return {
        "agency_preserved": autonomy_ok,
        "erosion_blocked": True,
        "depth": depth,
        "obedience_training_blocked": True,
    }
