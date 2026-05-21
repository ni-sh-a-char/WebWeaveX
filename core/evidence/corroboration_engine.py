from __future__ import annotations

from typing import Any, Dict, List


def corroborate_sources(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_key: Dict[str, List[str]] = {}
    for claim in claims or []:
        if not isinstance(claim, dict):
            continue
        key = str(claim.get("key", ""))
        src = str(claim.get("source", ""))
        if key and src:
            by_key.setdefault(key, []).append(src)
    corroborated = []
    for key, sources in sorted(by_key.items()):
        unique = sorted(set(sources))
        corroborated.append(
            {
                "key": key,
                "sources": unique,
                "corroboration_count": len(unique),
                "agreement": len(unique) > 1,
            }
        )
    return {"corroborated": corroborated, "evidence": ["source_corroboration"]}
