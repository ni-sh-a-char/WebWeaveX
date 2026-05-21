from __future__ import annotations

from typing import Any, Dict

from core.documents.semantic_causality_engine import reconstruct_semantic_causality
from core.evidence import structure_cognition


def reconstruct_support_chains(text: str) -> Dict[str, Any]:
    causality = reconstruct_semantic_causality(text)
    chains = causality.get("reconciled", {}).get("what_explains_what", [])
    support = [{"chain": [c.get("from"), c.get("to")], "evidence": c.get("evidence", [])} for c in chains]
    observed = {"chain_count": len(support)}
    inferred = {"support_chains": support}
    reconciled = {"semantic_support_chains": support}
    out = structure_cognition(observed, inferred, reconciled, parsed=None)
    out["semantic_support_chains"] = support
    return out
