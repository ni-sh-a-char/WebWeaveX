from __future__ import annotations

from typing import Any, Dict


def apply_sovereignty_ontology(edge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **edge,
        "epistemic_sovereignty": {"preserved": True, "dependency_blocked": True},
        "self_determination": {"ontology": True},
        "sovereignty": {"active": True},
    }
