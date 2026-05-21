from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evidence.semantic_confidence_engine import score_semantic_confidence


def build_semantic_edge(
    from_id: str,
    to_id: str,
    relation: str,
    evidence: Optional[List[str]] = None,
    parser_basis: Optional[Dict[str, Any]] = None,
    ambiguities: Optional[List[str]] = None,
    contradictions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    ev = sorted(set(str(e) for e in (evidence or []) if e))
    if not ev:
        ev = [f"relation:{relation}"]
    confidence = score_semantic_confidence(extra_evidence=ev)
    return {
        "from": from_id,
        "to": to_id,
        "relation": relation,
        "observed": {"from": from_id, "to": to_id, "relation": relation},
        "inferred": {"from": from_id, "to": to_id} if not parser_basis else {},
        "reconciled": {"from": from_id, "to": to_id, "relation": relation},
        "evidence": ev,
        "lineage": {"stage": "semantic_edge", "relation": relation},
        "parser_basis": parser_basis or {},
        "semantic_basis": {"relation": relation},
        "confidence_basis": confidence,
        "contradictions": contradictions or {},
        "ambiguities": sorted(set(ambiguities or ([] if ev else ["weak_edge_evidence"]))),
    }
