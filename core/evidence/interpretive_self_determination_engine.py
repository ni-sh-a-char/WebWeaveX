from __future__ import annotations

from typing import Any, Dict, List


def model_interpretive_self_determination(interpretation_count: int) -> Dict[str, Any]:
    return {
        "self_determined": interpretation_count != 1,
        "agency_preserved": True,
        "passivity_blocked": True,
        "steering_blocked": True,
    }
