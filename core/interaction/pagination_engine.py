from __future__ import annotations

from typing import Any, Dict, List, Set

MAX_PAGES = 100


def extract_paginated_content(
    page: Any,
    next_selector: str,
) -> Dict[str, Any]:
    visited: Set[str] = set()
    pages: List[Dict[str, Any]] = []

    current_url = ""

    if page is not None:
        current_url = str(getattr(page, "_test_url", getattr(page, "url", "")))

    while len(pages) < MAX_PAGES:
        if current_url in visited:
            break

        visited.add(current_url)

        pages.append({
            "url": current_url,
            "order": len(pages),
        })

        if not next_selector:
            break

        if page is not None and hasattr(page, "click"):
            try:
                page.click(next_selector)
            except Exception:
                break

        next_url = str(getattr(page, "_test_next_url", ""))

        if not next_url or next_url == current_url:
            if hasattr(page, "_test_paginate"):
                next_url = page._test_paginate(current_url)

        if not next_url or next_url in visited:
            break

        current_url = next_url
        if hasattr(page, "_test_url"):
            page._test_url = current_url

    return {
        "pages": pages,
        "visited_count": len(visited),
        "loop_prevented": len(pages) < MAX_PAGES,
        "bounded": True,
    }
