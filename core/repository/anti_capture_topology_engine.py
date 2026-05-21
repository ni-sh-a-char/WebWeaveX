from __future__ import annotations

from typing import Any, Dict


def apply_anti_capture_topology(edge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **edge,
        "anti_capture": {"active": True, "topology_autonomy": True},
        "capture_resistance": {"resistant": True},
    }
