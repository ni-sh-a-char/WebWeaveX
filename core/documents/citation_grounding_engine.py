from __future__ import annotations

from typing import Any, Dict

from core.evidence import structure_cognition
from core.internet.citation_lineage_engine import reconstruct_citation_lineage


def ground_citations(text: str) -> Dict[str, Any]:
    cites = reconstruct_citation_lineage(text)
    observed = {"citations": cites.get("citations", [])}
    inferred = {"targets": [c["target"] for c in cites.get("citations", [])]}
    reconciled = {"citation_lineage": cites, "grounded_targets": inferred["targets"]}
    return structure_cognition(observed, inferred, reconciled, parsed=None)
