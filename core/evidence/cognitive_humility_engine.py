from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.ambiguity_visibility_engine import expose_ambiguity_visibility
from core.evidence.confidence_degradation_engine import apply_confidence_degradation
from core.evidence.inference_termination_engine import terminate_inference_chain
from core.evidence.noninferable_scope_engine import model_noninferable_regions
from core.evidence.semantic_limit_engine import semantic_limits
from core.evidence.semantic_refusal_engine import refuse_unsupported_conclusions
from core.evidence.semantic_self_limitation_engine import apply_semantic_self_limitation
from core.evidence.semantic_speculation_engine import detect_semantic_speculation
from core.evidence.uncertainty_visibility_engine import expose_uncertainty_visibility
from core.evidence.unsupported_confidence_engine import block_unsupported_confidence_escalation
from core.evidence.semantic_fragility_engine import model_fragility
from core.semantic.ambiguity_pressure_engine import compute_ambiguity_pressure
from core.semantic.uncertainty_pressure_engine import compute_uncertainty_pressure


def apply_cognitive_humility(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    uncertainties: List[str] = list(bundle.get("uncertainties", bundle.get("uncertain", [])) or [])
    if isinstance(uncertainties, dict):
        uncertainties = list(uncertainties.keys())
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    noninferences = list(bundle.get("noninferences", bundle.get("noninference_reasons", [])) or [])
    fragility = bundle.get("fragility", bundle.get("fragile", {})) or {}
    if not isinstance(fragility, dict):
        fragility = model_fragility(evidence, ambiguities, len(uncertainties))

    speculation = detect_semantic_speculation(evidence, inferred, reconciled)
    suppressed_speculation = speculation.get("suppressed_speculation", [])
    scope = model_noninferable_regions(inferred, evidence, noninferences)
    noninferable_regions = scope.get("noninferable_regions", [])

    unc_vis = expose_uncertainty_visibility(uncertainties, ambiguities, 0.5)
    amb_vis = expose_ambiguity_visibility(ambiguities, 0.5)
    unc_pressure = compute_uncertainty_pressure(uncertainties, ambiguities)
    amb_pressure = compute_ambiguity_pressure(ambiguities)

    contradicted = bundle.get("contradicted", {}) or {}
    pairs = len(contradicted.get("pairs", [])) if isinstance(contradicted, dict) else 0
    parser_basis = bundle.get("parser_basis", {}) or {}
    parser_weak = int(parser_basis.get("symbol_count", 0) or 0) < 1

    cb = bundle.get("confidence_basis", {}) or {}
    raw_score = float(cb.get("score", 0.5))
    escalation = block_unsupported_confidence_escalation(raw_score, len(evidence))
    degraded = apply_confidence_degradation(
        escalation["capped_score"],
        fragility,
        contradiction_count=pairs,
        ambiguity_count=len(ambiguities),
        uncertainty_count=len(uncertainties),
        unsupported_expansion_count=len(bundle.get("unsupported_expansions", []) or []),
        speculation_count=len(suppressed_speculation),
        parser_weakness=parser_weak,
    )

    self_limitation = apply_semantic_self_limitation(evidence, suppressed_speculation, noninferable_regions)
    refusal = refuse_unsupported_conclusions(noninferable_regions, suppressed_speculation)
    termination = terminate_inference_chain(
        list(bundle.get("refused_inferences", []) or []),
        suppressed_speculation,
    )
    limits = semantic_limits(len(evidence), noninferable_regions, self_limitation)

    bundle["humility"] = {
        "self_limiting": True,
        "prefer_cannot_determine": True,
        "speculation_suppressed": len(suppressed_speculation),
        "uncertainty_pressure": unc_pressure.get("pressure", 0),
        "ambiguity_pressure": amb_pressure.get("pressure", 0),
    }
    bundle["noninferable_regions"] = noninferable_regions
    bundle["suppressed_speculation"] = suppressed_speculation
    bundle["confidence_degradation"] = degraded.get("degradation", {})
    bundle["uncertainty_visibility"] = unc_vis
    bundle["ambiguity_visibility"] = amb_vis
    bundle["semantic_fragility"] = fragility
    bundle["self_limitation"] = self_limitation
    bundle["refusals"] = refusal.get("refusals", [])
    bundle["terminated_inferences"] = termination.get("terminated_inferences", [])
    bundle["semantic_limits"] = limits
    bundle["termination_reasons"] = refusal.get("termination_reasons", [])
    bundle["unsupported_regions"] = refusal.get("unsupported_regions", [])
    bundle["inference_voids"] = scope.get("inference_voids", [])
    bundle["epistemic_limits"] = scope.get("epistemic_limits", {})
    bundle["boundaries"] = {**bundle.get("boundaries", {}), **scope.get("semantic_boundaries", {})}
    bundle["confidence_basis"] = {**cb, **degraded}
    return bundle
