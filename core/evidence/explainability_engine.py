from __future__ import annotations

from typing import Any, Dict, Optional


def build_explainability(
    parser_payload: Optional[Dict[str, Any]],
    confidence: Dict[str, Any],
    provenance: Dict[str, Any],
) -> Dict[str, Any]:
    flags = {}
    if isinstance(parser_payload, dict):
        flags = parser_payload.get("parser_evidence", parser_payload.get("evidence", {}))
        if not isinstance(flags, dict):
            flags = {}
    parser_basis = {
        "language": parser_payload.get("language", "text") if parser_payload else "unknown",
        "flags": flags,
        "symbol_count": provenance.get("grounding", {}).get("symbol_count", 0),
    }
    graph_basis = {}
    if parser_payload and isinstance(parser_payload.get("semantic_graph"), dict):
        g = parser_payload["semantic_graph"]
        graph_basis = {
            "nodes": len(g.get("nodes", []) or []),
            "edges": len(g.get("edges", []) or []),
        }
    semantic_basis = {
        "confidence_score": confidence.get("score", 0.0),
        "deterministic_inputs": confidence.get("deterministic_inputs", []),
    }
    return {
        "parser_basis": parser_basis,
        "graph_basis": graph_basis,
        "semantic_basis": semantic_basis,
        "summary": sorted(provenance.get("evidence", []) or []),
    }
