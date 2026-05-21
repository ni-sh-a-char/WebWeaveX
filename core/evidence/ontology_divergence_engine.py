from __future__ import annotations

from typing import Any, Dict, List


def model_ontology_divergence(entities: List[str], depth: int) -> Dict[str, Any]:
    return {"divergence": len(set(entities)), "preserved": len(entities) > 1 or depth < 3, "hardening_blocked": True}
