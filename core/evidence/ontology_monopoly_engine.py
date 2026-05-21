from __future__ import annotations

from typing import Any, Dict, List


def detect_ontology_monopoly(entity_count: int, depth: int) -> Dict[str, Any]:
    monopoly = entity_count <= 1 and depth >= 3
    return {"monopoly": monopoly, "suppress": monopoly}
