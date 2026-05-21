from __future__ import annotations

from typing import Any, Dict, List


MAX_TRACE_ENTRIES = 1000


def build_runtime_trace(
    steps: List[Dict[str, Any]],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    bounded = sorted(steps, key=lambda s: int(s.get("order", 0)))[:MAX_TRACE_ENTRIES]
    return {
        "trace": [
            {
                "id": s.get("id"),
                "label": s.get("label"),
                "order": s.get("order"),
            }
            for s in bounded
        ],
        "count": len(bounded),
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
        "bounded": len(bounded) <= MAX_TRACE_ENTRIES,
    }
