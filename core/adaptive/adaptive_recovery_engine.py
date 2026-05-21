from __future__ import annotations

from typing import Any, Dict

from core.adaptive.infinite_scroll_recovery_engine import recover_infinite_scroll
from core.adaptive.modal_recovery_engine import recover_modal_runtime
from core.adaptive.pagination_recovery_engine import recover_pagination_flow


def recover_adaptive_runtime(
    page: Any,
    html: str,
    pagination_selector: str,
) -> Dict[str, Any]:
    return {
        "modal": recover_modal_runtime(page, html),
        "pagination": recover_pagination_flow(pagination_selector, html),
        "scroll": recover_infinite_scroll(page),
        "bounded": True,
    }
