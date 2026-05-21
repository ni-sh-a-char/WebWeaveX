from __future__ import annotations

from typing import Any, Dict

from core.documents.discourse_structure_engine import reconstruct_discourse
from core.evidence import structure_cognition


def reconstruct_discourse_dependencies(text: str) -> Dict[str, Any]:
    discourse = reconstruct_discourse(text)
    extends = discourse.get("inferred", {}).get("discourse", {}).get("extends", [])
    introduces = discourse.get("inferred", {}).get("discourse", {}).get("introduces", [])
    observed = {"introduces": introduces}
    inferred = {"discourse_dependencies": extends, "introduces": introduces}
    reconciled = {"discourse_flow": extends, "introduces": introduces}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
