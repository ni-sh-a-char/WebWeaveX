from __future__ import annotations

from typing import Any, Dict


def preserve_ontology_freedom(competition: Dict[str, Any]) -> Dict[str, Any]:
    return {"free": competition.get("competitive", True), "caste_blocked": True}
