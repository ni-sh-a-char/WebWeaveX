from __future__ import annotations

from typing import Any, Dict


def apply_anti_capture_ontology(edge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **edge,
        "anti_capture": {"active": True, "ontology_autonomy": True},
        "interpretive_autonomy": {"autonomous": True},
        "capture_resistance": {"resistant": True},
    }
