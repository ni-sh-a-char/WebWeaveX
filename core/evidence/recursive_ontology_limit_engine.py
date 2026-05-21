from __future__ import annotations

from typing import Any, Dict


def recursive_ontology_limits(depth: int) -> Dict[str, Any]:
    return {"lock_in_allowed": False, "max_recursive_depth": 3, "depth": depth}
