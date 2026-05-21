from __future__ import annotations

def parse_semantic_payload(text: str):
    src = text or ''
    lines = [ln.strip() for ln in src.splitlines() if ln.strip()]
    return {
        "line_count": len(lines),
        "non_empty_ratio": 0.0 if not src else round(len('\n'.join(lines)) / max(1, len(src)), 6),
        "sample": lines[:20],
    }
