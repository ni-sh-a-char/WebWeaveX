from __future__ import annotations

from typing import Any, Dict


def model_cognitive_sovereignty(sovereign: bool) -> Dict[str, Any]:
    return {
        "sovereign": sovereign,
        "anti_dependent": True,
        "non_domesticating": True,
        "downstream_agency_required": True,
    }
