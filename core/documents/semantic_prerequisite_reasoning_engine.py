from __future__ import annotations

from typing import Any, Dict

from core.documents.semantic_prerequisite_engine import reconstruct_prerequisites
from core.documents.tutorial_dependency_engine import reconstruct_tutorial_dependencies
from core.evidence import structure_cognition


def reason_prerequisites(text: str) -> Dict[str, Any]:
    tutorial = reconstruct_tutorial_dependencies(text)
    prereqs = reconstruct_prerequisites(text)
    observed = {"tutorial_steps": tutorial.get("reconciled", {}).get("tutorial_flow", {})}
    inferred = {
        "tutorial_prerequisites": tutorial.get("inferred", {}),
        "concept_prerequisites": prereqs.get("reconciled", {}),
    }
    reconciled = {
        "what_conceptually_precedes_what": prereqs.get("reconciled", {}).get("concept_prerequisites", []),
        "tutorial_dependencies": tutorial.get("reconciled", {}),
    }
    return structure_cognition(observed, inferred, reconciled, parsed=None)
