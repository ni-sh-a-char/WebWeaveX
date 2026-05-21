from __future__ import annotations

from typing import Any, Dict

from core.evidence.semantic_consistency_engine import assess_semantic_consistency


def prove_consistency(observed: Dict[str, Any], inferred: Dict[str, Any], reconciled: Dict[str, Any]) -> Dict[str, Any]:
    r = assess_semantic_consistency(observed, inferred, reconciled)
    return {**r, "proved": r["consistent"], "proof": "key_overlap_consistency"}
