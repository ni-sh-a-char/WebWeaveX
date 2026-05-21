from __future__ import annotations

from typing import Any, Dict


MAX_CONTEXT_KEYS = 256


def compress_semantic_context(
    state: Dict[str, Any],
) -> Dict[str, Any]:

    keys = sorted(
        state.keys()
    )[:MAX_CONTEXT_KEYS]

    return {
        "compressed": {
            key: state[key]
            for key in keys
        },
        "compression_ratio": round(
            len(keys)
            / max(len(state), 1),
            3,
        ),
    }
