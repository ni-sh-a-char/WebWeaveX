from __future__ import annotations

from typing import Any, Dict, List

from core.adaptive.extraction_fallback_engine import build_extraction_fallback_chain
from core.adaptive.interaction_recovery_engine import recover_interaction_flow
from core.adaptive.modal_recovery_engine import recover_modal_runtime
from core.adaptive.pagination_recovery_engine import recover_pagination_flow


def run_runtime_adaptation(
    url: str,
    dom_nodes: List[Dict[str, Any]],
    html: str,
    interactions: List[Dict[str, Any]],
    primary_selector: str,
    page: Any = None,
) -> Dict[str, Any]:
    fallback = build_extraction_fallback_chain(
        primary_selector,
        dom_nodes,
        html,
    )
    interaction_recovery = recover_interaction_flow(
        interactions,
        dom_nodes,
        html,
    )
    modal_recovery = recover_modal_runtime(page, html)
    pagination_recovery = recover_pagination_flow(
        primary_selector,
        html,
    )

    return {
        "url": url,
        "fallback": fallback,
        "interaction_recovery": interaction_recovery,
        "modal_recovery": modal_recovery,
        "pagination_recovery": pagination_recovery,
        "bounded": True,
    }
