from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.recursive_coherence_inflation_engine import detect_recursive_coherence_inflation
from core.evidence.recursive_confidence_decay_engine import apply_recursive_confidence_decay
from core.evidence.recursive_confidence_echo_engine import detect_recursive_confidence_echo
from core.evidence.recursive_drift_engine import detect_recursive_drift
from core.evidence.recursive_entropy_engine import model_recursive_entropy
from core.evidence.recursive_evidence_ancestry_engine import track_recursive_evidence_ancestry
from core.evidence.recursive_instability_engine import model_recursive_instability
from core.evidence.recursive_lineage_engine import preserve_recursive_lineage
from core.evidence.recursive_provenance_engine import preserve_recursive_provenance
from core.evidence.recursive_reality_limit_engine import recursive_reality_limits
from core.evidence.recursive_self_confirmation_engine import detect_recursive_self_confirmation
from core.evidence.recursive_semantic_closure_engine import detect_recursive_semantic_closure
from core.evidence.recursive_stabilization_termination_engine import terminate_recursive_stabilization
from core.evidence.recursive_truth_boundary_engine import model_recursive_truth_boundaries
from core.evidence.recursive_truth_refusal_engine import refuse_recursive_stabilization
from core.evidence.recursive_uncertainty_preservation_engine import preserve_recursive_uncertainty
from core.evidence.recursive_ontology_limit_engine import recursive_ontology_limits
from core.evidence.recursive_topology_limit_engine import recursive_topology_limits
from core.semantic.recursive_boundary_pressure_engine import compute_recursive_boundary_pressure


def _lineage_depth(bundle: Dict[str, Any]) -> int:
    lineage = bundle.get("lineage", {}) or {}
    stages = lineage.get("stages", [])
    if isinstance(stages, list) and stages:
        return len(stages)
    return int(lineage.get("depth", 0) or 0)


def apply_recursive_reality_integrity(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    uncertainties: List[str] = list(bundle.get("uncertainties", bundle.get("uncertain", [])) or [])
    if isinstance(uncertainties, dict):
        uncertainties = list(uncertainties.keys())
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    contradicted = bundle.get("contradicted", bundle.get("contradictions", {})) or {}
    instability_obj = bundle.get("instability", {})
    unstable_regions = list(bundle.get("unstable_regions", instability_obj.get("regions", []) if isinstance(instability_obj, dict) else []))
    fragility = bundle.get("fragility", bundle.get("semantic_fragility", {})) or {}
    if not isinstance(fragility, dict):
        fragility = {"level": "medium", "confidence_limits": {"max_score": 0.7}}

    depth = _lineage_depth(bundle)
    closure = detect_recursive_semantic_closure(depth, inferred, reconciled, evidence)
    suppressed = closure.get("suppressed_closures", [])
    drift = detect_recursive_drift(depth, len(evidence), len(inferred))
    rentropy = model_recursive_entropy(ambiguities, uncertainties, contradicted, depth)
    rinstability = model_recursive_instability(unstable_regions, depth, len(evidence))
    rboundaries = model_recursive_truth_boundaries(depth, len(evidence))
    runcertainty = preserve_recursive_uncertainty(uncertainties, depth)
    lineage_p = preserve_recursive_lineage(bundle.get("lineage", {}), evidence, ambiguities, uncertainties, contradicted)
    provenance_p = preserve_recursive_provenance(bundle.get("sources", []), lineage_p)
    ancestry = track_recursive_evidence_ancestry(evidence, depth)
    self_confirm = detect_recursive_self_confirmation(depth, reconciled == inferred, len(evidence))
    coherence_inf = detect_recursive_coherence_inflation(depth, closure.get("closure_pressure", 0))
    bound_pressure = compute_recursive_boundary_pressure(rboundaries.get("erosion", 0), depth)

    pairs = len(contradicted.get("pairs", [])) if isinstance(contradicted, dict) else 0
    cb = bundle.get("confidence_basis", {}) or {}
    raw_score = float(cb.get("score", 0.5))
    echo = detect_recursive_confidence_echo(raw_score, depth, [])
    if echo.get("suppress"):
        raw_score = echo["decay_to"]

    decayed = apply_recursive_confidence_decay(
        raw_score,
        fragility,
        depth=depth,
        closure_count=closure.get("closure_detected") and len(suppressed) or 0,
        drift_pressure=drift["drift_pressure"],
        entropy=rentropy["entropy"],
        contradiction_count=pairs,
        ambiguity_count=len(ambiguities),
        uncertainty_count=len(uncertainties),
    )

    refusal = refuse_recursive_stabilization(suppressed)
    termination = terminate_recursive_stabilization(suppressed, depth)
    limits = recursive_reality_limits(depth, rentropy)

    bundle["recursive_reality_integrity"] = {
        "preserved": True,
        "depth": depth,
        "closure_suppressed": closure.get("closure_detected", False),
        "echo_suppressed": echo.get("suppress", False),
        "self_confirmation_suppressed": self_confirm.get("suppress", False),
    }
    bundle["recursive_entropy"] = rentropy
    bundle["recursive_instability"] = rinstability
    bundle["recursive_truth_boundaries"] = rboundaries
    bundle["recursive_drift"] = drift
    bundle["recursive_semantic_closure"] = closure
    bundle["recursive_confidence_decay"] = decayed.get("recursive_decay", {})
    bundle["recursive_uncertainty"] = runcertainty
    bundle["recursive_lineage"] = lineage_p
    bundle["recursive_provenance"] = provenance_p
    bundle["recursive_evidence_ancestry"] = ancestry
    bundle["recursive_truth_refusals"] = refusal.get("recursive_truth_refusals", [])
    bundle["recursive_stabilization_failures"] = refusal.get("recursive_stabilization_failures", [])
    bundle["recursive_limits"] = {**limits, "ontology": recursive_ontology_limits(depth), "topology": recursive_topology_limits(depth)}
    bundle["recursive_termination_reasons"] = sorted(
        set(bundle.get("recursive_termination_reasons", []) + refusal.get("recursive_termination_reasons", []))
    )
    bundle["recursive_boundary_failures"] = refusal.get("recursive_boundary_failures", [])
    bundle["confidence_basis"] = {**cb, **decayed}
    return bundle
