from __future__ import annotations

from typing import Any, Dict


def apply_openness_topology(edge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **edge,
        "civilizational_openness": {"open": True},
        "interpretive_exploration": {"active": True},
    }
