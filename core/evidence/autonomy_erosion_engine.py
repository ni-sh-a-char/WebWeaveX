from __future__ import annotations

from typing import Any, Dict


def resist_autonomy_erosion(autonomy_ok: bool, depth: int) -> Dict[str, Any]:
    erosion = depth >= 4 and not autonomy_ok
    return {"erosion_risk": erosion, "resist": True, "erosion_suppressed": erosion}
