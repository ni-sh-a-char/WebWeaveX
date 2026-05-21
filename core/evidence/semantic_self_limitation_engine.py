from __future__ import annotations

from typing import Any, Dict, List


def apply_semantic_self_limitation(
    evidence: List[str],
    suppressed_speculation: List[Dict[str, Any]],
    noninferable_regions: List[str],
) -> Dict[str, Any]:
    limited = len(evidence) < 2 or bool(suppressed_speculation) or bool(noninferable_regions)
    return {
        "active": limited,
        "prefer_cannot_determine": True,
        "propagation_allowed": not limited,
        "reconciliation_allowed": len(evidence) >= 2,
        "expansion_allowed": len(evidence) >= 2 and not noninferable_regions,
        "limit_reasons": sorted(
            set(
                (["insufficient_evidence"] if len(evidence) < 2 else [])
                + (["speculative_suppression"] if suppressed_speculation else [])
                + (["noninferable_regions"] if noninferable_regions else [])
            )
        ),
    }
