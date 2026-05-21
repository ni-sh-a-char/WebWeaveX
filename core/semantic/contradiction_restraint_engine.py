from __future__ import annotations

from typing import Any, Dict

from core.semantic.contradiction_pressure_engine import compute_contradiction_pressure


def apply_contradiction_restraint(bundle: Dict[str, Any]) -> Dict[str, Any]:
    contradicted = bundle.get("contradicted", {}) or bundle.get("contradictions", {}) or {}
    pressure = compute_contradiction_pressure(contradicted)
    bundle["contradiction_pressure"] = pressure
    bundle["fragility_pressure"] = {
        **bundle.get("fragility_pressure", {}),
        "contradiction": pressure["pressure"],
    }
    return bundle
