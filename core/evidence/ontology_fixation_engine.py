from __future__ import annotations

from typing import Any, Dict


def detect_ontology_fixation(entity_count: int, depth: int) -> Dict[str, Any]:
    fixation = entity_count <= 1 and depth >= 3
    return {"fixation": fixation, "suppress": fixation, "hardening_blocked": fixation}
