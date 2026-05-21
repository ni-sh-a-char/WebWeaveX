from __future__ import annotations

from typing import Any, Callable, Dict, List


def filter_semantic_records(
    records: List[Dict[str, Any]],
    predicate: Callable[[Dict[str, Any]], bool],
) -> List[Dict[str, Any]]:
    return sorted(
        [r for r in records if predicate(r)],
        key=lambda r: str(r.get("id", "")),
    )
