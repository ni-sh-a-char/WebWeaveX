from __future__ import annotations

from typing import Any, Dict


def ontology_limits(boundaries: Dict[str, Any]) -> Dict[str, Any]:
    return {"inheritance": boundaries.get("inheritance_allowed", False), "equivalence": boundaries.get("equivalence_allowed", False)}
