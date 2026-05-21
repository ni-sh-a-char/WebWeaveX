from __future__ import annotations

from typing import Any, Dict, List

from core.internet.semantic_consensus_engine import measure_semantic_consensus


def analyze_source_consistency(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    claims = [{"text": s.get("url", s.get("id", ""))} for s in sources or []]
    consensus = measure_semantic_consensus(claims)
    consistent = consensus.get("consensus", 0) >= 0.5 or len(sources or []) <= 1
    return {**consensus, "consistent": consistent, "source_count": len(sources or [])}
