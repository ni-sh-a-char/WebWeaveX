from __future__ import annotations

from typing import Any, Dict

from core.evidence.semantic_conservatism_engine import apply_semantic_conservatism


def apply_epistemic_conservatism(bundle: Dict[str, Any]) -> Dict[str, Any]:
    return apply_semantic_conservatism(bundle)
