from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evidence.epistemic_confidence_engine import score_epistemic_confidence
from core.evidence.evidence_sufficiency_engine import assess_evidence_sufficiency
from core.evidence.incompleteness_engine import preserve_incompleteness
from core.evidence.insufficiency_engine import mark_insufficiency
from core.evidence.semantic_reliability_engine import score_reliability
from core.evidence.semantic_support_engine import build_support
from core.evidence.semantic_uncertainty_propagation_engine import propagate_uncertainty
from core.evidence.cognitive_integrity_engine import apply_cognitive_integrity
from core.evidence.semantic_restraint_engine import apply_epistemic_restraint
from core.evidence.cognitive_humility_engine import apply_cognitive_humility
from core.evidence.reality_alignment_engine import apply_reality_alignment
from core.evidence.truth_preservation_engine import apply_truth_preservation
from core.evidence.recursive_reality_integrity_engine import apply_recursive_reality_integrity
from core.evidence.epistemic_civilization_stability_engine import apply_epistemic_civilization_stability
from core.evidence.cognitive_anti_capture_engine import apply_cognitive_anti_capture
from core.evidence.recursive_epistemic_sovereignty_engine import apply_recursive_epistemic_sovereignty
from core.evidence.civilizational_epistemic_openness_engine import apply_civilizational_epistemic_openness
from core.semantic.contradiction_restraint_engine import apply_contradiction_restraint
from core.evidence.semantic_weakness_engine import build_weaknesses


def attach_epistemic_state(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    contradicted = bundle.get("contradicted", {}) or {}
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    contradicting = [f"contradiction:{p}" for p in pairs]
    parser_basis = bundle.get("parser_basis", {}) or {}
    parser_density = int(parser_basis.get("symbol_count", 0) or 0)

    support = build_support(evidence)
    weaknesses = build_weaknesses(evidence, ambiguities)
    sufficiency = assess_evidence_sufficiency(evidence)
    reliability = score_reliability(evidence, ambiguities, len(pairs))
    incompleteness = preserve_incompleteness(bundle)
    insufficiency = mark_insufficiency(bundle)
    epistemic_confidence = score_epistemic_confidence(
        evidence=evidence,
        contradicting=contradicting,
        uncertainty_factors=ambiguities,
        parser_density=parser_density,
    )
    lineage = bundle.get("lineage", {})
    how = {"stages": lineage.get("stages", []), "depth": lineage.get("depth", 0)}

    bundle["support"] = support
    bundle["weaknesses"] = weaknesses
    bundle["evidence_sufficiency"] = sufficiency
    bundle["reliability"] = reliability
    bundle["epistemic_state"] = {
        **incompleteness,
        "insufficient": insufficiency["insufficient"],
        "confidence": epistemic_confidence["score"],
    }
    bundle["confidence_basis"] = epistemic_confidence
    bundle["how"] = how
    bundle = propagate_uncertainty(bundle)
    if insufficiency["insufficient"]:
        ambiguities = sorted(set(ambiguities + ["insufficient_evidence"]))
        bundle["ambiguities"] = ambiguities
    bundle = apply_cognitive_integrity(bundle)
    bundle = apply_contradiction_restraint(bundle)
    chain = apply_reality_alignment(apply_cognitive_humility(apply_epistemic_restraint(bundle)))
    return apply_civilizational_epistemic_openness(
        apply_recursive_epistemic_sovereignty(
            apply_cognitive_anti_capture(
                apply_epistemic_civilization_stability(
                    apply_recursive_reality_integrity(apply_truth_preservation(chain))
                )
            )
        )
    )
