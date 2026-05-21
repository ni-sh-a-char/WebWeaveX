from __future__ import annotations

from typing import Any, Dict

from core.documents.explanation_chain_engine import build_explanation_chains
from core.evidence import structure_cognition


def reconstruct_explanation_dependencies(text: str) -> Dict[str, Any]:
    chains = build_explanation_chains(text)
    explains = chains.get("reconciled", {}).get("what_explains_what", [])
    observed = {"chains_observed": len(explains)}
    inferred = {"explanation_dependencies": explains}
    reconciled = {"what_explains_what": explains}
    out = structure_cognition(observed, inferred, reconciled, parsed=None)
    out["explanation_dependencies"] = explains
    return out
