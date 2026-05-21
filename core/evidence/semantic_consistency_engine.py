from __future__ import annotations

from typing import Any, Dict, List


def assess_semantic_consistency(
    observed: Dict[str, Any],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
) -> Dict[str, Any]:
    """Measure key overlap consistency between observed/inferred/reconciled."""
    ko, ki, kr = set(observed.keys()), set(inferred.keys()), set(reconciled.keys())
    overlap_oi = len(ko & ki)
    overlap_or = len(ko & kr)
    total = max(1, len(ko | ki | kr))
    score = round((overlap_oi + overlap_or) / (2 * total), 3)
    consistent = score >= 0.5 or not inferred
    return {
        "consistent": consistent,
        "consistency_score": score,
        "overlap_observed_inferred": overlap_oi,
        "overlap_observed_reconciled": overlap_or,
        "deterministic_inputs": [f"score={score}", f"keys_total={total}"],
    }
