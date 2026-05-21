from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.uncertainty_engine import model_uncertainty


def propagate_uncertainty(bundle: Dict[str, Any]) -> Dict[str, Any]:
    evidence = bundle.get("evidence", []) or []
    ambiguities = bundle.get("ambiguities", []) or []
    contradicted = bundle.get("contradicted", {}) or {}
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    model = model_uncertainty(len(evidence), len(ambiguities), len(pairs))
    uncertainties = {
        **model,
        "factors": sorted(set(ambiguities + ([f"contradiction:{len(pairs)}"] if pairs else []))),
    }
    bundle["uncertainties"] = uncertainties
    return bundle
