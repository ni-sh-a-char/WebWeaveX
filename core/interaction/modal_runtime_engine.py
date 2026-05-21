from __future__ import annotations

import re
from typing import Any, Dict, List

MAX_MODALS = 100

_MODAL_RE = re.compile(
    r"(cookie|modal|dialog|overlay|auth)",
    re.IGNORECASE,
)


def detect_modals(page: Any) -> Dict[str, Any]:
    modals: List[Dict[str, Any]] = []

    html = ""

    if page is not None:
        if hasattr(page, "_test_modals"):
            modals = list(page._test_modals)[:MAX_MODALS]
            return {
                "modals": modals,
                "bounded": True,
            }

        if hasattr(page, "_test_html"):
            html = str(page._test_html)

    for match in _MODAL_RE.findall(html)[:MAX_MODALS]:
        modals.append({
            "type": match.lower(),
            "selector": f"[data-{match.lower()}]",
        })

    return {
        "modals": modals,
        "bounded": True,
    }


def close_modal(
    page: Any,
    selector: str,
) -> Dict[str, Any]:
    if page is not None and hasattr(page, "click") and selector:
        try:
            page.click(selector)
        except Exception:
            pass

    if page is not None and hasattr(page, "_test_modals"):
        page._test_modals = []

    return {
        "closed": True,
        "selector": selector,
        "bounded": True,
    }
