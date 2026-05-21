from __future__ import annotations

from typing import Any, Dict

from core.documents.tutorial_reasoning_engine import extract_tutorial_flow
from core.evidence import structure_cognition


def reconstruct_tutorial_dependencies(text: str) -> Dict[str, Any]:
    flow = extract_tutorial_flow(text)
    requires = flow.get("inferred", {}).get("requires_prior", [])
    steps = flow.get("reconciled", {}).get("steps", [])
    observed = {"steps": steps}
    inferred = {"tutorial_dependencies": requires, "prerequisite_edges": requires}
    reconciled = {"tutorial_flow": flow.get("reconciled", {}), "dependencies": requires}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
