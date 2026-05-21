from __future__ import annotations

from typing import Any, Dict, List


MAX_CASCADE = 10000


def trace_execution_cascade(
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(
        transitions,
        key=lambda x: (
            str(x.get("from")),
            str(x.get("to")),
        ),
    )[:MAX_CASCADE]
    cascade = [
        {
            "from": t.get("from"),
            "to": t.get("to"),
        }
        for t in ordered
    ]
    return {
        "cascade": cascade,
        "cascade_length": len(cascade),
        "bounded": True,
    }
