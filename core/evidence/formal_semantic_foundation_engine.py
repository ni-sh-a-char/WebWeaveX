from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.contradiction_lattice_engine import build_contradiction_lattice
from core.evidence.deterministic_reasoning_engine import reason_deterministically
from core.evidence.evidence_weighting_calculus import weight_evidence_calculus
from core.evidence.semantic_consistency_engine import assess_semantic_consistency
from core.evidence.semantic_entropy_engine import model_semantic_entropy
from core.evidence.semantic_justification_engine import build_justification
from core.evidence.uncertainty_propagation_math import propagate_uncertainty_math
from core.evidence.inference_validation_engine import validate_inference
from core.evidence.semantic_proof_engine import prove_semantic_claim


def apply_formal_semantic_foundation(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Attach mathematically explainable formal fields before epistemic layering."""
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    contradicted = bundle.get("contradicted", bundle.get("contradictions", {})) or {}
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    lineage = bundle.get("lineage", {}) or {}
    parser_basis = bundle.get("parser_basis", {}) or {}
    parser_backed = bool(parser_basis.get("symbol_count", 0) or parser_basis.get("flags"))

    lattice = build_contradiction_lattice(pairs)
    uncertainty = propagate_uncertainty_math(len(evidence), len(ambiguities), lattice["count"])
    entropy = model_semantic_entropy(ambiguities, list(uncertainty.get("factors", ambiguities)), contradicted)
    consistency = assess_semantic_consistency(observed, inferred, reconciled)
    weights = weight_evidence_calculus(evidence, parser_backed=parser_backed)
    reasoning = reason_deterministically(observed, evidence, ambiguities)
    justification = build_justification(evidence, lineage, uncertainty, entropy)

    bundle["uncertainty"] = uncertainty
    bundle["entropy"] = entropy
    bundle["contradictions"] = {**contradicted, **lattice}
    bundle["justification"] = justification
    bundle["formal_reasoning"] = reasoning
    bundle["evidence_weights"] = weights
    bundle["semantic_consistency"] = consistency
    validation = validate_inference(observed, evidence)
    proof = prove_semantic_claim("semantic_integrity", evidence, min_evidence=1)
    bundle["inference_validation"] = validation
    bundle["semantic_proof"] = proof
    bundle["deterministic_inputs"] = sorted(
        set(
            list(bundle.get("deterministic_inputs", []) or [])
            + uncertainty.get("deterministic_inputs", [])
            + justification.get("deterministic_inputs", [])
            + reasoning.get("deterministic_inputs", [])
            + validation.get("deterministic_inputs", [])
            + proof.get("deterministic_inputs", [])
        )
    )
    return bundle
