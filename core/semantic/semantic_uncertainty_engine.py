from __future__ import annotations

from typing import Any, Dict

from core.evidence.uncertainty_engine import model_uncertainty
from core.evidence.semantic_conservatism_engine import apply_semantic_conservatism


def apply_semantic_uncertainty(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence = bundle.get("evidence", []) or []
    ambiguities = bundle.get("ambiguities", []) or []
    contradicted = bundle.get("contradicted", {}) or {}
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    uncertainty = model_uncertainty(len(evidence), len(ambiguities), len(pairs))
    bundle["uncertainty"] = uncertainty
    bundle = apply_semantic_conservatism(bundle)
    cb = bundle.get("confidence_basis", {})
    cb["score"] = round(min(float(cb.get("score", 0.5)), uncertainty["confidence_score"]), 3)
    bundle["confidence_basis"] = cb
    return bundle
