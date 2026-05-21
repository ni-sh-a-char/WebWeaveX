from __future__ import annotations

from typing import Any, Dict


def resist_agency_decay(agency_ok: bool, depth: int) -> Dict[str, Any]:
    return {"decay_risk": depth >= 4 and not agency_ok, "resist": True, "erosion_suppressed": True}
