from __future__ import annotations

from typing import Any, Dict

from core.evidence.speculative_inference_engine import suppress_speculative_inference
from core.knowledge.ontology_self_confirmation_engine import suppress_ontology_self_confirmation
from core.knowledge.recursive_ontology_lock_engine import suppress_recursive_ontology_lock
from core.knowledge.civilization_ontology_engine import apply_civilization_ontology
from core.knowledge.anti_capture_ontology_engine import apply_anti_capture_ontology
from core.knowledge.sovereignty_ontology_engine import apply_sovereignty_ontology
from core.knowledge.openness_ontology_engine import apply_openness_ontology


def suppress_speculative_ontology_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    spec = suppress_speculative_inference("ontology_edge", ev, inferred=bool(edge.get("inferred")))
    fragility = edge.get("fragility", {})
    uncertainty = edge.get("uncertainty", {"visible": not ev})
    ambiguity = edge.get("ambiguity", {"visible": False})
    caps = edge.get("confidence_caps", edge.get("confidence_limits", {}))
    suppressed = spec.get("suppressed", False) or not ev
    reality = {"aligned": bool(ev) and not spec.get("suppressed"), "parser_bounded": bool(ev)}
    base = {
        **edge,
        "reality_alignment": reality,
        "boundary_pressure": {"edge": spec.get("suppressed", False)},
        "stability": {"stable": bool(ev), "level": "high" if ev else "low"},
        "supported": {"stated": bool(ev), "evidence_count": len(ev)},
        "unsupported": {"edge": suppressed, "speculative": spec.get("suppressed", False)},
        "suppressed": {"inheritance": suppressed, "equivalence": suppressed, "merge": suppressed},
        "fragility": fragility if fragility else {"level": "medium"},
        "uncertainty": uncertainty,
        "ambiguity": ambiguity,
        "confidence_caps": caps,
        "speculative_suppression": spec.get("record"),
    }
    return apply_openness_ontology(
        apply_sovereignty_ontology(
            apply_anti_capture_ontology(
                apply_civilization_ontology(
                    suppress_recursive_ontology_lock(suppress_ontology_self_confirmation(base))
                )
            )
        )
    )
