from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.continuity_refusal_engine import refuse_unsupported_continuity
from core.evidence.epistemic_boundary_engine import preserve_epistemic_boundaries
from core.evidence.evidence_boundary_engine import model_evidence_boundaries
from core.evidence.narrative_hallucination_engine import detect_narrative_hallucination
from core.evidence.ontology_boundary_engine import model_ontology_boundaries
from core.evidence.ontology_limit_engine import ontology_limits
from core.evidence.reality_bounded_confidence_engine import apply_reality_bounded_confidence
from core.evidence.reality_constraint_engine import apply_reality_constraints
from core.evidence.semantic_boundary_engine import model_semantic_boundaries
from core.evidence.semantic_drift_engine import detect_semantic_drift
from core.evidence.semantic_momentum_engine import measure_semantic_momentum
from core.evidence.semantic_stability_engine import model_semantic_stability
from core.evidence.semantic_stability_limit_engine import semantic_stability_limits
from core.evidence.semantic_termination_engine import terminate_semantic_chain
from core.evidence.speculative_coherence_engine import detect_speculative_coherence
from core.evidence.stability_boundary_engine import model_stability_boundary
from core.evidence.topology_boundary_engine import model_topology_boundaries
from core.evidence.topology_limit_engine import topology_limits
from core.evidence.unsupported_continuity_engine import collect_unsupported_continuity
from core.semantic.evidence_boundary_pressure_engine import compute_evidence_boundary_pressure
from core.semantic.semantic_boundary_pressure_engine import compute_semantic_boundary_pressure


def apply_reality_alignment(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    uncertainties: List[str] = list(bundle.get("uncertainties", bundle.get("uncertain", [])) or [])
    if isinstance(uncertainties, dict):
        uncertainties = list(uncertainties.keys())
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    noninferable = list(bundle.get("noninferable_regions", []) or [])
    fragility = bundle.get("fragility", bundle.get("semantic_fragility", {})) or {}
    if not isinstance(fragility, dict):
        fragility = {"level": "medium", "confidence_limits": {"max_score": 0.7}}

    parser_basis = bundle.get("parser_basis", {}) or {}
    parser_grounded = int(parser_basis.get("symbol_count", 0) or 0) > 0 or bool(bundle.get("grounding"))

    drift = detect_semantic_drift(observed, inferred, reconciled, evidence)
    unsupported_continuity = collect_unsupported_continuity(evidence, inferred, reconciled)
    momentum = measure_semantic_momentum(len(inferred), len(evidence))
    coherence = detect_speculative_coherence(evidence, inferred, reconciled)
    narrative = detect_narrative_hallucination(inferred, evidence, parser_grounded)

    ev_bound = model_evidence_boundaries(evidence)
    onto_bound = model_ontology_boundaries(evidence, inferred=bool(inferred) and not evidence)
    topo_bound = model_topology_boundaries(evidence, parser_grounded)
    sem_bound = model_semantic_boundaries(inferred, ev_bound["bounded"])

    stability = model_semantic_stability(
        evidence, drift["drift_pressure"], unsupported_continuity, parser_grounded
    )
    constraints = apply_reality_constraints(evidence, parser_grounded, drift["drift_pressure"])
    epistemic_bound = preserve_epistemic_boundaries(evidence, noninferable, stability["unstable_regions"])
    stab_bound = model_stability_boundary(stability["unstable_regions"])
    ev_pressure = compute_evidence_boundary_pressure(len(evidence))
    bound_pressure = compute_semantic_boundary_pressure(stab_bound.get("broken", False) and 1.0 or 0.0, drift["drift_pressure"])

    contradicted = bundle.get("contradicted", {}) or {}
    pairs = len(contradicted.get("pairs", [])) if isinstance(contradicted, dict) else 0
    cb = bundle.get("confidence_basis", {}) or {}
    bounded_conf = apply_reality_bounded_confidence(
        float(cb.get("score", 0.5)),
        fragility,
        drift_pressure=drift["drift_pressure"],
        continuity_count=len(unsupported_continuity),
        parser_gap=not parser_grounded,
        boundary_pressure=bound_pressure.get("pressure", 0),
        contradiction_count=pairs,
        ambiguity_count=len(ambiguities),
        uncertainty_count=len(uncertainties),
    )

    continuity_refusal = refuse_unsupported_continuity(unsupported_continuity)
    termination = terminate_semantic_chain(stability["unstable_regions"], continuity_refusal.get("continuity_refusals", []))
    stab_limits = semantic_stability_limits(stability)

    bundle["reality_alignment"] = {
        "aligned": stability["stable"] and ev_bound["bounded"],
        "parser_grounded": parser_grounded,
        "drift_suppressed": drift["suppress_continuation"],
        "continuity_suppressed": bool(unsupported_continuity),
        "narrative_suppressed": narrative.get("suppressed", False),
    }
    bundle["semantic_boundaries"] = sem_bound
    bundle["ontology_boundaries"] = onto_bound
    bundle["topology_boundaries"] = topo_bound
    bundle["evidence_boundaries"] = ev_bound
    bundle["semantic_stability"] = stability
    bundle["drift_pressure"] = drift
    bundle["unsupported_continuity"] = unsupported_continuity
    bundle["reality_constraints"] = constraints
    bundle["unstable_regions"] = stability["unstable_regions"]
    bundle["boundary_pressure"] = bound_pressure
    bundle["continuity_refusals"] = continuity_refusal.get("continuity_refusals", [])
    bundle["stability_failures"] = stability["unstable_regions"]
    bundle["boundary_failures"] = continuity_refusal.get("boundary_failures", [])
    bundle["semantic_limits"] = {**bundle.get("semantic_limits", {}), **stab_limits, "ontology": ontology_limits(onto_bound), "topology": topology_limits(topo_bound)}
    bundle["termination_reasons"] = sorted(set(bundle.get("termination_reasons", []) + continuity_refusal.get("termination_reasons", [])))
    bundle["epistemic_boundaries"] = epistemic_bound
    bundle["speculative_coherence"] = coherence
    bundle["narrative_hallucination"] = narrative
    bundle["semantic_momentum"] = momentum
    bundle["confidence_basis"] = {**cb, **bounded_conf}
    return bundle
