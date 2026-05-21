from __future__ import annotations

from typing import Any, Dict


def apply_openness_ontology(edge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **edge,
        "civilizational_openness": {"open": True, "exploration": True},
        "ontology_exploration": {"active": True},
        "novelty_preservation": {"preserved": True},
    }
