from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.epistemic_limit_engine import model_epistemic_limits
from core.evidence.inference_integrity_engine import model_inference_integrity
from core.evidence.inference_limit_engine import model_inference_limits
from core.evidence.semantic_fragility_engine import model_fragility
from core.evidence.semantic_honesty_engine import assess_semantic_honesty
from core.evidence.semantic_overreach_engine import detect_semantic_overreach
from core.evidence.unsupported_inference_engine import suppress_unsupported_inference
from core.evidence.unsupported_scope_engine import model_unsupported_scope


def apply_cognitive_integrity(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence: List[str] = list(bundle.get("evidence", []) or [])
    ambiguities: List[str] = list(bundle.get("ambiguities", []) or [])
    observed = bundle.get("observed", {}) or {}
    inferred = bundle.get("inferred", {}) or {}
    reconciled = bundle.get("reconciled", {}) or {}
    contradicted = bundle.get("contradicted", {}) or bundle.get("contradictions", {}) or {}
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    parser_basis = bundle.get("parser_basis", {}) or {}
    parser_density = int(parser_basis.get("symbol_count", 0) or 0)

    fragility = model_fragility(evidence, ambiguities, len(pairs), parser_density)
    suppression = suppress_unsupported_inference(evidence, inferred, observed)
    overreach = detect_semantic_overreach(evidence, inferred, reconciled)
    supported = {"keys": sorted(observed.keys()), "evidence": evidence}
    unsupported = {
        "claims": suppression.get("unsupported_dimensions", []),
        "dimensions": model_unsupported_scope(suppression.get("unsupported_dimensions", [])),
    }
    cb = bundle.get("confidence_basis", {}) or {}
    supporting = list(cb.get("supporting_evidence", evidence))
    contradicting = list(cb.get("contradicting_evidence", []))
    inference = model_inference_integrity(evidence, supporting, contradicting, fragility)
    limits = model_epistemic_limits(evidence, parser_density, fragility)
    boundaries = model_inference_limits(inferred if suppression.get("allowed_inference") else {}, len(evidence))
    honesty = assess_semantic_honesty(evidence, supported, unsupported, fragility)

    cap = float(fragility.get("confidence_limits", {}).get("max_score", 1.0))
    score = round(min(float(cb.get("score", 0.5)), cap), 3)
    cb = {
        **cb,
        "score": score,
        "support_basis": inference.get("basis", {}),
        "fragility_basis": fragility.get("basis", {}),
        "uncertainty_basis": bundle.get("uncertainties", {}),
        "contradiction_basis": {"count": len(pairs)},
        "confidence_limits": fragility.get("confidence_limits", {}),
    }

    bundle["supported"] = supported
    bundle["unsupported"] = unsupported
    bundle["fragile"] = fragility
    bundle["uncertain"] = bundle.get("uncertainties", {})
    bundle["contradicted"] = contradicted
    bundle["incomplete"] = bundle.get("epistemic_state", {}).get("incomplete", False)
    bundle["confidence_limits"] = fragility.get("confidence_limits", {})
    bundle["semantic_honesty"] = honesty
    bundle["fragility"] = fragility
    bundle["inference_integrity"] = inference
    bundle["epistemic_limits"] = limits
    bundle["unsupported_scope"] = unsupported.get("dimensions", {})
    bundle["inference_boundaries"] = boundaries
    bundle["confidence_basis"] = cb
    if overreach.get("overreach_detected"):
        ambiguities = sorted(set(ambiguities + overreach.get("overreach_flags", [])))
        bundle["ambiguities"] = ambiguities
    if not suppression.get("allowed_inference") and inferred:
        unsupported["inferred_keys"] = sorted(inferred.keys())
        ambiguities = sorted(set(ambiguities + ["unsupported_inference"]))
        bundle["ambiguities"] = ambiguities
    return bundle
