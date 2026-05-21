from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evidence.explainability_engine import build_explainability
from core.evidence.lineage_engine import build_lineage
from core.evidence.provenance_engine import build_provenance
from core.evidence.semantic_confidence_engine import score_semantic_confidence
from core.evidence.epistemic_evidence_engine import attach_epistemic_state
from core.evidence.formal_semantic_foundation_engine import apply_formal_semantic_foundation
from core.evidence.traceability_engine import build_traceability


def _ground_parser(parsed: Dict[str, Any]) -> Dict[str, Any]:
    flags = parsed.get("parser_evidence", parsed.get("evidence", {}))
    if not isinstance(flags, dict):
        flags = {}
    symbols = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    grounding = {
        "language": parsed.get("language", "text"),
        "symbol_count": len(symbols.get("classes", []) or []) + len(symbols.get("functions", []) or []),
        "flags": flags,
    }
    evidence = [f"parser:{k}" for k, v in sorted(flags.items()) if v]
    return build_provenance(evidence, grounding=grounding)


def build_semantic_integrity_object(
    observed: Optional[Dict[str, Any]] = None,
    parsed_facts: Optional[Dict[str, Any]] = None,
    inferred: Optional[Dict[str, Any]] = None,
    reconciled: Optional[Dict[str, Any]] = None,
    contradicted: Optional[Dict[str, Any]] = None,
    derived: Optional[Dict[str, Any]] = None,
    ambiguities: Optional[List[Any]] = None,
    parser_payload: Optional[Dict[str, Any]] = None,
    lineage_stages: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    observed = observed if isinstance(observed, dict) else {}
    parsed_facts = parsed_facts if isinstance(parsed_facts, dict) else {}
    inferred = inferred if isinstance(inferred, dict) else {}
    reconciled = reconciled if isinstance(reconciled, dict) else {}
    contradicted = contradicted if isinstance(contradicted, dict) else {}
    derived = derived if isinstance(derived, dict) else {}
    ambiguities = sorted(set(str(a) for a in (ambiguities or []) if a))

    prov = _ground_parser(parser_payload) if parser_payload else build_provenance(["no_parser"])
    confidence = score_semantic_confidence(parsed=parser_payload)
    lineage = build_lineage(lineage_stages or [{"stage": "semantic_integrity", "inputs": prov.get("sources", []), "outputs": []}])
    explain = build_explainability(parser_payload, confidence, prov)

    evidence_list = prov.get("evidence", [])
    traceability = build_traceability(evidence=evidence_list, lineage=lineage, stages=[s.get("stage", "") for s in (lineage_stages or []) if isinstance(s, dict)])
    out = {
        "observed": observed,
        "parsed": parsed_facts,
        "inferred": inferred,
        "reconciled": reconciled,
        "contradicted": contradicted,
        "derived": derived,
        "ambiguities": ambiguities,
        "evidence": evidence_list,
        "sources": prov.get("sources", []),
        "grounding": prov.get("grounding", {}),
        "lineage": lineage,
        "confidence_basis": confidence,
        "why": explain,
        "parser_basis": explain.get("parser_basis", {}),
        "graph_basis": explain.get("graph_basis", {}),
        "semantic_basis": explain.get("semantic_basis", {}),
        "traceability": traceability,
        "contradictions": contradicted,
    }
    return attach_epistemic_state(apply_formal_semantic_foundation(out))
