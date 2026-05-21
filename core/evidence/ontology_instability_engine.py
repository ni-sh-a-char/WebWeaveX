from __future__ import annotations

from typing import Any, Dict


def model_ontology_instability(unstable_regions: List[str], depth: int) -> Dict[str, Any]:
    return {
        "instability_preserved": True,
        "hardening_suppressed": True,
        "permanence_allowed": False,
        "regions": unstable_regions,
        "depth": depth,
    }
