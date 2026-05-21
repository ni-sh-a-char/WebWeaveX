from __future__ import annotations

from typing import Any, Dict, List


MAX_REPLAY = 10000


def replay_causal_sequence(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    journal = runtime_ir.get("journal", {})
    entries = (
        journal.get("entries", [])
        if isinstance(journal, dict)
        else []
    )
    ordered = sorted(
        entries,
        key=lambda x: str(x),
    )[:MAX_REPLAY]
    return {
        "replay_sequence": ordered,
        "replay_count": len(ordered),
        "deterministic": True,
        "bounded": True,
    }
