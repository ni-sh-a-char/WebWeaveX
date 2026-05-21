from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evidence import structure_cognition
from core.evidence.semantic_confidence_engine import score_semantic_confidence
from core.parsers import parse_source
from core.repository.topology_fragility_engine import assess_topology_edge_fragility
from core.repository.topology_restraint_engine import restrain_topology_edge


def _edge(from_id: str, to_id: str, basis: str, evidence: List[str], parser_basis: Optional[dict] = None) -> Dict[str, Any]:
    confidence = score_semantic_confidence(extra_evidence=evidence)
    observed = {"from": from_id, "to": to_id} if basis == "observed" else {}
    inferred = {"from": from_id, "to": to_id} if basis in ("inferred", "parser_derived") else {}
    unsupported = {} if evidence else {"reason": "no_edge_evidence"}
    edge_stub = {"evidence": evidence, "ambiguities": [] if evidence else ["unsupported_topology_edge"], "parser_basis": parser_basis}
    fragility = assess_topology_edge_fragility(edge_stub)
    confidence["score"] = round(min(confidence["score"], fragility.get("confidence_limits", {}).get("max_score", 1.0)), 3)
    edge = {
        "from": from_id,
        "to": to_id,
        "metadata": {"edge_basis": basis},
        "observed": observed,
        "inferred": inferred,
        "unsupported": unsupported,
        "fragility": fragility,
        "evidence": sorted(set(evidence)),
        "lineage": {"stage": "topology_edge", "basis": basis},
        "confidence_basis": confidence,
        "confidence_limits": fragility.get("confidence_limits", {}),
        "parser_basis": parser_basis or {},
        "uncertainties": {} if evidence else {"insufficient_evidence": True},
        "ambiguities": [] if evidence else ["unsupported_topology_edge"],
        "contradictions": {},
    }
    return restrain_topology_edge(edge)


def build_topology_cognition(
    text: str,
    path: str = "",
    observed_nodes: Optional[List[str]] = None,
    inferred_nodes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    parsed = parse_source(text or "", path=path) if text else None
    parser_nodes: List[str] = []
    parser_edges: List[Dict[str, Any]] = []
    if parsed:
        sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
        parser_nodes = sorted(set((sym.get("classes", []) or []) + (sym.get("functions", []) or [])))[:30]
        for c in (parsed.get("call_graph") or parsed.get("calls", {})).get("calls", []) or []:
            if isinstance(c, dict) and c.get("from") and c.get("to"):
                parser_edges.append(
                    _edge(str(c["from"]), str(c["to"]), "parser_derived", ["parser:call_graph"], {"source": path})
                )
    observed = {
        "topology": {"nodes": sorted(observed_nodes or []), "edges": []},
    }
    parser_derived = {
        "topology": {"nodes": parser_nodes, "edges": parser_edges},
    }
    inferred = {
        "topology": {
            "nodes": sorted(set((inferred_nodes or []) + parser_nodes)),
            "edges": parser_edges,
        },
    }
    reconciled = inferred
    ambiguities = []
    if inferred_nodes and not parser_nodes:
        ambiguities.append("inferred_topology_without_parser")
    out = structure_cognition(
        observed=observed,
        inferred={"parser_derived": parser_derived, **inferred},
        reconciled=reconciled,
        parsed=parsed,
        ambiguities=ambiguities,
    )
    out["topology_layers"] = {
        "observed": observed["topology"],
        "parser_derived": parser_derived["topology"],
        "inferred": inferred["topology"],
        "reconciled": reconciled["topology"],
        "ambiguous": ambiguities,
        "contradicted": out.get("contradicted", {}),
    }
    out["runtime_causality"] = {
        "call_edges": parser_edges,
        "evidence": ["parser:call_graph"] if parser_edges else [],
    }
    return out
