from __future__ import annotations

from typing import Any, Dict, List


def reconcile_runtime_states(
    left: Dict[str, Any],
    right: Dict[str, Any],
) -> Dict[str, Any]:
    left_keys = set(left.keys())
    right_keys = set(right.keys())
    only_left = sorted(left_keys - right_keys)
    only_right = sorted(right_keys - left_keys)
    shared = sorted(left_keys & right_keys)
    conflicts = sorted(k for k in shared if left.get(k) != right.get(k))
    return {
        "only_left": only_left,
        "only_right": only_right,
        "conflicts": conflicts,
        "aligned": sorted(k for k in shared if k not in conflicts),
        "deterministic": True,
    }
