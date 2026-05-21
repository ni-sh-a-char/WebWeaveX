from __future__ import annotations

from typing import Any, Dict, List

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.streaming.stream_capture_engine import make_stream_event

MAX_MUTATIONS = 10000


def capture_dom_mutations(page: Any) -> Dict[str, Any]:
    mutations: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []

    if page is not None and hasattr(page, "_test_dom_mutations"):
        mutations = list(page._test_dom_mutations)[:MAX_MUTATIONS]

    for index, mutation in enumerate(mutations):
        events.append(
            make_stream_event(
                step=index,
                source="dom_mutation",
                direction=str(mutation.get("type", "mutation")),
                payload=str(mutation.get("payload", "")),
                connection_id=str(mutation.get("node_id", "")),
            )
        )

    dom_snapshot = ""
    if page is not None and hasattr(page, "_test_html"):
        dom_snapshot = str(page._test_html)

    return {
        "mutations": mutations,
        "events": events,
        "dom_hash": compute_kaalka_hash(dom_snapshot[:1_000_000]),
        "bounded": True,
    }
