from __future__ import annotations

from typing import Any, Dict


def ontology_truth_limits(boundaries: Dict[str, Any]) -> Dict[str, Any]:
    return {"self_confirmation_allowed": False, "equivalence": boundaries.get("equivalence_allowed", False)}
