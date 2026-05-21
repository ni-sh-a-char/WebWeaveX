from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.confidence_cap_engine import apply_confidence_caps
from core.evidence.inference_refusal_engine import refuse_inference
from core.evidence.noninference_engine import model_noninference
from core.evidence.semantic_boundary_engine import model_semantic_boundaries
from core.evidence.unsupported_expansion_engine import detect_unsupported_expansion
from core.evidence.unsupported_scope_engine import model_unsupported_scope
from core.semantic.contradiction_pressure_engine import compute_contradiction_pressure


def apply_epistemic_restraint(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    contradicted = bundle.get("contradicted", {}) or bundle.get("contradictions", {}) or {}
    fragility = bundle.get("fragility", bundle.get("fragile", {})) or {}

    noninf = model_noninference(evidence, inferred, observed, reconciled)
    pressure = compute_contradiction_pressure(contradicted)
    pairs = pressure.get("pair_count", 0)
    topo_exp = detect_unsupported_expansion(evidence, "topology", len(inferred))
    onto_exp = detect_unsupported_expansion(evidence, "ontology", 0)
    unsupported_expansions = topo_exp.get("unsupported_expansions", []) + onto_exp.get("unsupported_expansions", [])

    cb = bundle.get("confidence_basis", {}) or {}
    capped = apply_confidence_caps(
        float(cb.get("score", 0.5)),
        fragility if isinstance(fragility, dict) else {},
        contradiction_count=pairs,
        ambiguity_count=len(ambiguities),
        unsupported_expansion_count=len(unsupported_expansions),
    )
    refusal = refuse_inference(noninf.get("noninferences", []), len(evidence))
    boundaries = model_semantic_boundaries(inferred, noninf["suppression_basis"].get("allowed", False))

    restraint = {
        "conservative_default": True,
        "suppress_propagation": pressure.get("suppress_propagation", False) or topo_exp.get("suppressed"),
        "suppress_reconciliation": pressure.get("suppress_reconciliation", False),
        "noninference_count": len(noninf.get("noninferences", [])),
    }

    bundle["restraint"] = restraint
    bundle["suppressed_inferences"] = noninf.get("refused_inferences", [])
    bundle["unsupported_expansions"] = unsupported_expansions
    bundle["confidence_caps"] = capped.get("caps", {})
    bundle["fragility_pressure"] = {
        "level": fragility.get("level", "unknown") if isinstance(fragility, dict) else "unknown",
        "contradiction": pressure.get("pressure", 0),
    }
    bundle["noninference_reasons"] = noninf.get("noninferences", [])
    bundle["semantic_boundaries"] = boundaries
    bundle["noninferences"] = noninf.get("noninferences", [])
    bundle["refused_inferences"] = noninf.get("refused_inferences", [])
    bundle["boundary_conditions"] = noninf.get("boundary_conditions", [])
    bundle["suppression_basis"] = noninf.get("suppression_basis", {})
    bundle["contradiction_pressure"] = pressure
    bundle["boundaries"] = {
        **bundle.get("boundaries", {}),
        "inference": boundaries,
        "unsupported_scope": model_unsupported_scope(noninf.get("noninferences", [])),
    }
    bundle["noninferable_dimensions"] = noninf.get("noninferences", [])
    bundle["inference_refusal"] = refusal
    cb = {**cb, **capped}
    bundle["confidence_basis"] = cb
    return bundle
