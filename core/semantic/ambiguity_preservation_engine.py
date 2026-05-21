from __future__ import annotations

from typing import Any, Dict, List


def preserve_ambiguities(candidates: List[str], evidence: List[str]) -> Dict[str, Any]:
    unique = sorted(set(str(c) for c in (candidates or []) if c))
    unresolved = unique if len(unique) > 1 else []
    return {
        "ambiguities": unresolved,
        "preserved": bool(unresolved),
        "evidence": sorted(set(evidence or [])),
        "lineage": {"stage": "ambiguity_preservation", "count": len(unresolved)},
    }
