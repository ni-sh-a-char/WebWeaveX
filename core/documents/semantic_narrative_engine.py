from __future__ import annotations

from typing import Any, Dict

from core.documents.discourse_structure_engine import reconstruct_discourse
from core.evidence import structure_cognition


def reconstruct_narrative(text: str) -> Dict[str, Any]:
    discourse = reconstruct_discourse(text)
    flow = discourse.get("reconciled", {}).get("structure", {}).get("extends", [])
    observed = {"discourse": discourse.get("observed", {})}
    inferred = {"narrative_flow": flow}
    reconciled = {"explains": flow, "depends_on": []}
    out = structure_cognition(observed, inferred, reconciled, parsed=None)
    out["narrative_flow"] = flow
    return out
