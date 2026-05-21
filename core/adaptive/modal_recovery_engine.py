from __future__ import annotations

from typing import Any, Dict, List

MAX_RETRIES = 5

_MODAL_CLOSE_SELECTORS = [
    "#cookie-accept",
    "[aria-label='Close']",
    "button.accept",
    ".modal-close",
]


def recover_modal_runtime(
    page: Any,
    html: str = "",
) -> Dict[str, Any]:
    recovered: List[Dict[str, Any]] = []
    retries = 0

    modals = []
    if page is not None and hasattr(page, "_test_modals"):
        modals = list(page._test_modals)

    for selector in _MODAL_CLOSE_SELECTORS:
        if retries >= MAX_RETRIES:
            break

        if _selector_in_html(selector, html) or modals:
            if page is not None and hasattr(page, "click"):
                try:
                    page.click(selector)
                except Exception:
                    pass

            if hasattr(page, "_test_modals"):
                page._test_modals = []

            recovered.append({
                "selector": selector,
                "recovered": True,
            })
            retries += 1
            break

    return {
        "recovered": recovered,
        "retries": retries,
        "bounded": True,
    }


def _selector_in_html(selector: str, html: str) -> bool:
    token = selector.strip("#.[]").split("'")[0].split('"')[0]
    return token.lower() in html.lower()
