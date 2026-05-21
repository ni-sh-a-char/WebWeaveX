from __future__ import annotations

def merge_semantic_sources(records: list[dict]):
    merged = {}
    for r in records or []:
        for k,v in sorted((r or {}).items()):
            merged.setdefault(k, set()).add(str(v))
    return {k: sorted(v) for k,v in sorted(merged.items())}
