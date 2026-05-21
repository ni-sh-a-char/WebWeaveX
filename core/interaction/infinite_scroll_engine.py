from __future__ import annotations

from typing import Any, Dict, List

from core.crypto.kaalka_hash_engine import compute_kaalka_hash

MAX_SCROLLS = 100


def _dom_hash(page: Any) -> str:
    if hasattr(page, "_test_dom_hash") and page._test_dom_hash:
        return str(page._test_dom_hash)

    html = ""
    if hasattr(page, "_test_html"):
        html = str(page._test_html)
    elif hasattr(page, "content") and callable(page.content):
        try:
            html = str(page.content())
        except Exception:
            html = ""

    return compute_kaalka_hash(html[:1_000_000])


def extract_infinite_scroll(page: Any) -> Dict[str, Any]:
    scrolls = 0
    chunks: List[Dict[str, Any]] = []
    previous_hash = _dom_hash(page)
    stable_rounds = 0

    while scrolls < MAX_SCROLLS:
        if page is not None and hasattr(page, "evaluate"):
            try:
                page.evaluate(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
            except Exception:
                pass

        if hasattr(page, "_test_scroll"):
            page._test_scroll()

        scrolls += 1
        current_hash = _dom_hash(page)

        chunks.append({
            "scroll": scrolls,
            "dom_hash": current_hash,
        })

        if current_hash == previous_hash:
            stable_rounds += 1
        else:
            stable_rounds = 0

        if stable_rounds >= 2:
            break

        previous_hash = current_hash

    return {
        "scrolls": scrolls,
        "chunks": chunks,
        "stopped_on_stable_dom": stable_rounds >= 2,
        "bounded": True,
    }
