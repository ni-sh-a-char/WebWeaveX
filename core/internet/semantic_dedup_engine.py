from __future__ import annotations

import hashlib
from typing import List


def _fingerprint(text: str) -> str:
    normalized = " ".join((text or "").lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def semantic_dedup(texts: List[str]) -> List[str]:
    seen: dict[str, str] = {}
    for t in texts or []:
        fp = _fingerprint(t)
        if fp not in seen:
            seen[fp] = t
    return [seen[k] for k in sorted(seen)]
