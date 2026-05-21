from __future__ import annotations

from typing import Any, Dict

from core.evidence.semantic_uncertainty_propagation_engine import propagate_uncertainty


def propagate_semantic_uncertainty(bundle: Dict[str, Any]) -> Dict[str, Any]:
    return propagate_uncertainty(bundle)
