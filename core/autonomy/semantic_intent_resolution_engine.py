from __future__ import annotations

from typing import Any, Dict


MAX_INTENT_LEN = 4096


def resolve_semantic_intent(
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    intent = str(payload.get("intent", payload.get("goal", "")))[
        :MAX_INTENT_LEN
    ]
    tokens = sorted(
        t.strip().lower()
        for t in intent.split()
        if t.strip()
    )
    return {
        "intent": intent,
        "tokens": tokens,
        "resolved": bool(intent),
    }
