"""Deterministic normalized extraction schema helpers."""

from __future__ import annotations

from typing import Any, Dict

NORMALIZED_KEYS = [
    "code",
    "content",
    "dependencies",
    "fingerprint",
    "metadata",
    "raw_text",
    "relationships",
    "source_url",
]


def empty_normalized(source_url: str = "") -> Dict[str, Any]:
    return {
        "content": {},
        "code": {},
        "dependencies": {},
        "metadata": {},
        "relationships": {},
        "raw_text": "",
        "source_url": source_url or "",
        "fingerprint": "",
    }

