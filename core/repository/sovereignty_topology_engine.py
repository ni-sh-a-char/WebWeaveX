from __future__ import annotations

from typing import Any, Dict


def apply_sovereignty_topology(edge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **edge,
        "epistemic_sovereignty": {"preserved": True},
        "self_determination": {"topology": True},
    }
