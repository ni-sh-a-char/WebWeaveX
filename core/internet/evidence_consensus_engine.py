from __future__ import annotations

from typing import Any, Dict, List

from core.internet.source_corroboration_engine import corroborate_sources
from core.internet.semantic_consensus_engine import measure_semantic_consensus


def build_evidence_consensus(sources: List[Dict[str, Any]], claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    corr = corroborate_sources(sources)
    consensus = measure_semantic_consensus(claims)
    strength = round(min(1.0, corr.get("corroboration_count", 0) * 0.2 + consensus.get("consensus", 0) * 0.8), 3)
    return {
        "corroboration": corr,
        "consensus": consensus,
        "strength": strength,
        "deterministic_inputs": [f"strength={strength}"],
    }
