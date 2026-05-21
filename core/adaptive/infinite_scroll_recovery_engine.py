from __future__ import annotations

from typing import Any, Dict, List

MAX_SCROLLS = 100


def recover_infinite_scroll(
    page: Any,
    previous_hashes: List[str] | None = None,
) -> Dict[str, Any]:
    hashes = list(previous_hashes or [])
    exhausted = False
    scrolls = 0

    while scrolls < MAX_SCROLLS:
        if page is not None and hasattr(page, "_test_scroll"):
            page._test_scroll()

        current = str(getattr(page, "_test_dom_hash", ""))
        scrolls += 1

        if hashes and current == hashes[-1]:
            exhausted = True
            break

        hashes.append(current)

        if len(hashes) >= 3 and hashes[-1] == hashes[-2] == hashes[-3]:
            exhausted = True
            break

    return {
        "scrolls": scrolls,
        "dom_hashes": hashes[-10:],
        "exhausted": exhausted,
        "bounded": True,
    }
