from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.confidence_collapse_engine import apply_confidence_collapse
from core.evidence.confidence_echo_engine import detect_confidence_echo
from core.evidence.evidence_decay_engine import model_evidence_decay
from core.evidence.instability_preservation_engine import preserve_instability
from core.evidence.semantic_decay_engine import model_semantic_decay
from core.evidence.semantic_entropy_engine import model_semantic_entropy
from core.evidence.semantic_instability_engine import model_semantic_instability
from core.evidence.semantic_self_reinforcement_engine import detect_semantic_self_reinforcement
from core.evidence.semantic_truth_limit_engine import semantic_truth_limits
from core.evidence.stabilization_termination_engine import terminate_stabilization
from core.evidence.truth_boundary_engine import model_truth_boundaries
from core.evidence.truth_refusal_engine import refuse_unsupported_stabilization
from core.evidence.unsupported_stabilization_engine import detect_unsupported_stabilization
from core.semantic.evidence_decay_pressure_engine import compute_evidence_decay_pressure
from core.semantic.truth_boundary_pressure_engine import compute_truth_boundary_pressure


def apply_truth_preservation(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    uncertainties: List[str] = list(bundle.get("uncertainties", bundle.get("uncertain", [])) or [])
    if isinstance(uncertainties, dict):
        uncertainties = list(uncertainties.keys())
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    contradicted = bundle.get("contradicted", bundle.get("contradictions", {})) or {}
    unstable_regions = list(bundle.get("unstable_regions", []) or [])
    fragility = bundle.get("fragility", bundle.get("semantic_fragility", {})) or {}
    if not isinstance(fragility, dict):
        fragility = {"level": "medium", "confidence_limits": {"max_score": 0.7}}

    stabilization = detect_unsupported_stabilization(evidence, inferred, reconciled)
    suppressed_stab = stabilization.get("suppressed_stabilizations", [])
    reinforcement = detect_semantic_self_reinforcement(inferred, reconciled, evidence)
    entropy = model_semantic_entropy(ambiguities, uncertainties, contradicted)
    ev_decay = model_evidence_decay(evidence)
    sem_decay = model_semantic_decay(evidence, inferred, stabilization.get("count", 0))
    truth_bound = model_truth_boundaries(evidence)
    instability = preserve_instability(unstable_regions, evidence, suppressed_stab)
    sem_instability = model_semantic_instability(instability["regions"], entropy, evidence)

    ev_pressure = compute_evidence_decay_pressure(len(evidence))
    truth_pressure = compute_truth_boundary_pressure(truth_bound["truth_bounded"], entropy["entropy"])

    pairs = len(contradicted.get("pairs", [])) if isinstance(contradicted, dict) else 0
    cb = bundle.get("confidence_basis", {}) or {}
    raw_score = float(cb.get("score", 0.5))
    echo = detect_confidence_echo(raw_score, [])
    if echo.get("suppress"):
        raw_score = echo["collapse_to"]

    collapsed = apply_confidence_collapse(
        raw_score,
        fragility,
        reinforcement_count=1 if reinforcement.get("reinforcement_detected") else 0,
        stabilization_count=stabilization.get("count", 0),
        decay_pressure=sem_decay["decay_rate"],
        truth_boundary_pressure=truth_pressure.get("pressure", 0),
        contradiction_count=pairs,
        ambiguity_count=len(ambiguities),
        uncertainty_count=len(uncertainties),
        incompleteness=ev_decay.get("incomplete", False),
    )

    refusal = refuse_unsupported_stabilization(suppressed_stab)
    termination = terminate_stabilization(suppressed_stab, sem_instability["regions"])
    truth_limits = semantic_truth_limits(entropy, instability)

    bundle["truth_preservation"] = {
        "preserved": True,
        "prefer_truthfully_incomplete": True,
        "stabilization_suppressed": stabilization.get("count", 0),
        "echo_suppressed": echo.get("suppress", False),
    }
    bundle["semantic_decay"] = sem_decay
    bundle["confidence_collapse"] = collapsed.get("collapse_pressure", {})
    bundle["instability"] = {**instability, **sem_instability}
    bundle["truth_boundaries"] = truth_bound
    bundle["unsupported_stabilization"] = suppressed_stab
    bundle["semantic_entropy"] = entropy
    bundle["evidence_decay"] = ev_decay
    bundle["semantic_instability"] = sem_instability
    bundle["truth_pressure"] = truth_pressure
    bundle["entropy"] = entropy
    bundle["truth_refusals"] = refusal.get("truth_refusals", [])
    bundle["stabilization_failures"] = refusal.get("stabilization_failures", [])
    bundle["truth_boundary_failures"] = refusal.get("truth_boundary_failures", [])
    bundle["termination_reasons"] = sorted(set(bundle.get("termination_reasons", []) + refusal.get("termination_reasons", [])))
    bundle["semantic_limits"] = {**bundle.get("semantic_limits", {}), **truth_limits}
    bundle["confidence_basis"] = {**cb, **collapsed}
    return bundle
