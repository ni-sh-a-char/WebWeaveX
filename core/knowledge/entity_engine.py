from __future__ import annotations

from typing import Dict, List


def build_entities(symbols: List[str]) -> Dict[str, object]:
    unique = sorted(set(str(s) for s in (symbols or []) if s))
    return {"entities": [{"id": u, "kind": "symbol"} for u in unique], "count": len(unique)}
