from __future__ import annotations

from typing import Any, Dict


def track_continuity(prior: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
    pk = set(str(k) for k in prior.keys())
    ck = set(str(k) for k in current.keys())
    return {
        "continuous_keys": sorted(pk & ck),
        "added_keys": sorted(ck - pk),
        "removed_keys": sorted(pk - ck),
        "continuous": len(pk & ck) > 0 or not prior,
        "deterministic_inputs": [f"prior={len(pk)}", f"current={len(ck)}"],
    }
