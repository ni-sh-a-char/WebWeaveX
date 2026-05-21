from __future__ import annotations

from typing import Any, Dict, List

from core.evidence import structure_cognition
from core.evidence.epistemic_confidence_engine import score_epistemic_confidence
from core.evidence.evidence_sufficiency_engine import assess_evidence_sufficiency
from core.evidence.semantic_support_engine import build_support
from core.evidence.semantic_weakness_engine import build_weaknesses
from core.knowledge.ontology_fragility_engine import assess_ontology_edge_fragility
from core.knowledge.ontology_restraint_engine import restrain_ontology_edge


def _normalize_edge(r: dict) -> Dict[str, Any]:
    ev = r.get("evidence", [])
    if isinstance(ev, str):
        ev = [ev]
    elif not isinstance(ev, list):
        ev = []
    support = build_support(ev)
    weaknesses = build_weaknesses(ev, r.get("ambiguities", []))
    sufficiency = assess_evidence_sufficiency(ev)
    epistemic_confidence = score_epistemic_confidence(evidence=ev, uncertainty_factors=r.get("ambiguities", []))
    observed = {"from": r.get("from"), "to": r.get("to"), "stated": bool(ev)}
    inferred = {} if ev else {"from": r.get("from"), "to": r.get("to"), "relation": "inferred_weak"}
    fragility = assess_ontology_edge_fragility({"evidence": ev, "ambiguities": r.get("ambiguities", [])})
    cap = fragility.get("confidence_limits", {}).get("max_score", 1.0)
    epistemic_confidence["score"] = round(min(epistemic_confidence["score"], cap), 3)
    edge = {
        "from": r.get("from"),
        "to": r.get("to"),
        "observed": observed,
        "inferred": inferred,
        "reconciled": {"from": r.get("from"), "to": r.get("to"), "evidence": sorted(set(str(e) for e in ev if e))},
        "evidence": sorted(set(str(e) for e in ev if e)),
        "lineage": r.get("lineage", {"stage": "ontology_edge"}),
        "confidence_basis": epistemic_confidence,
        "confidence_limits": fragility.get("confidence_limits", {}),
        "grounding": r.get("grounding", {"method": "stated_relation" if ev else "inferred_weak"}),
        "contradictions": r.get("contradictions", {}),
        "ambiguities": sorted(set(r.get("ambiguities", []) or ([] if ev else ["missing_edge_evidence"]))),
        "support": support,
        "weaknesses": weaknesses,
        "fragility": fragility,
        "uncertainties": {"insufficient": not sufficiency["sufficient"]},
        "unsupported_dimensions": fragility.get("missing_support", []),
        "evidence_sufficiency": sufficiency,
        "epistemic_state": {
            "sufficient": sufficiency["sufficient"],
            "unsupported": not ev,
            "confidence": epistemic_confidence["score"],
        },
    }
    return restrain_ontology_edge(edge)


def build_ontology(entities: List[str], relations: List[dict]) -> Dict[str, object]:
    ents = sorted(set(str(e) for e in (entities or []) if e))
    observed = {"entities": [{"id": e, "kind": "symbol"} for e in ents]}
    rels = [_normalize_edge(r) for r in (relations or []) if isinstance(r, dict) and r.get("from") and r.get("to")]
    rels = sorted(rels, key=lambda x: (x["from"], x["to"]))
    inferred = {"relations": rels}
    reconciled = {"entities": observed["entities"], "relations": rels}
    ambiguities = []
    if any(not edge["evidence"] for edge in rels):
        ambiguities.append("ontology_edges_without_evidence")
    return structure_cognition(observed, inferred, reconciled, parsed=None, ambiguities=ambiguities)
