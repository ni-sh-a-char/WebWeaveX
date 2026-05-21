from __future__ import annotations

from typing import Any, Dict, List

from core.internet.evidence_consensus_engine import build_evidence_consensus


def build_semantic_consensus_graph(sources: List[Dict[str, Any]], claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    consensus = build_evidence_consensus(sources, claims)
    return {
        "nodes": [s.get("url", s.get("id", "")) for s in sources or []],
        "consensus": consensus,
        "strength": consensus.get("strength", 0),
        "evidence": consensus.get("deterministic_inputs", []),
    }
