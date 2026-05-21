from __future__ import annotations

from typing import Any, Dict, List

MAX_TABS = 50


def capture_tabs(context: Any) -> Dict[str, Any]:
    tabs: List[Dict[str, Any]] = []

    if context is None:
        return {
            "tabs": [],
            "bounded": True,
        }

    if hasattr(context, "_test_tabs"):
        return {
            "tabs": list(context._test_tabs)[:MAX_TABS],
            "bounded": True,
        }

    if hasattr(context, "pages"):
        for index, page in enumerate(context.pages()[:MAX_TABS]):
            url = ""
            if hasattr(page, "url"):
                try:
                    url = str(page.url)
                except Exception:
                    url = ""
            tabs.append({
                "index": index,
                "url": url[:2000],
            })

    return {
        "tabs": tabs,
        "bounded": True,
    }


def switch_tab(
    context: Any,
    index: int,
) -> Dict[str, Any]:
    bounded_index = min(max(int(index), 0), MAX_TABS - 1)

    if context is not None and hasattr(context, "_test_active_tab"):
        context._test_active_tab = bounded_index

    pages = []

    if context is not None and hasattr(context, "pages"):
        try:
            pages = list(context.pages())
        except Exception:
            pages = []

    if pages and bounded_index < len(pages):
        page = pages[bounded_index]
        if hasattr(page, "bring_to_front"):
            page.bring_to_front()

    return {
        "active_tab": bounded_index,
        "bounded": True,
    }
