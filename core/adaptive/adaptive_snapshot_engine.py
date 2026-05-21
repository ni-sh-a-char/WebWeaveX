from __future__ import annotations

from typing import Any, Dict


def build_adaptive_snapshot(
    dom: Dict[str, Any],
    selectors: Dict[str, Any],
    interaction_state: Dict[str, Any],
    streaming_state: Dict[str, Any],
    identity_state: Dict[str, Any],
    pagination_state: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "dom": dom,
        "selectors": selectors,
        "interaction_state": interaction_state,
        "streaming_state": streaming_state,
        "identity_state": identity_state,
        "pagination_state": pagination_state,
        "bounded": True,
    }
