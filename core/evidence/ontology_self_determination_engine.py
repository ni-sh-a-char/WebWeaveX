from __future__ import annotations

from typing import Any, Dict


def model_ontology_self_determination(entity_count: int) -> Dict[str, Any]:
    return {
        "self_determined": entity_count != 1,
        "submission_blocked": True,
        "reliance_blocked": True,
    }
