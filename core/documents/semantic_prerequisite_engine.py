from __future__ import annotations

from typing import Any, Dict, List

from core.documents.tutorial_dependency_engine import reconstruct_tutorial_dependencies
from core.evidence import structure_cognition


def reconstruct_prerequisites(text: str) -> Dict[str, Any]:
    tutorial = reconstruct_tutorial_dependencies(text)
    prereqs: List[Dict[str, str]] = tutorial.get("inferred", {}).get("tutorial_dependencies", [])
    observed = {"source": "tutorial_flow"}
    inferred = {"prerequisites": prereqs}
    reconciled = {"concept_prerequisites": prereqs}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
