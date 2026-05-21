from __future__ import annotations

import hashlib
import re


def extract_metadata(text: str, source_url: str = "") -> dict:
    src = text or ""
    return {
        "source_url": source_url or "",
        "raw_length": len(src),
        "line_count": len(src.splitlines()),
        "url_count": len(set(re.findall(r"https?://[^\s\)]+", src))),
        "content_hash": hashlib.sha256(src.encode("utf-8", errors="ignore")).hexdigest(),
    }

