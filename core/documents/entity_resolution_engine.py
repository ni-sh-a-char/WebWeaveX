from __future__ import annotations

import re
from typing import Any, Dict

from core.documents.reference_engine import extract_references


def resolve_references(text: str) -> Dict[str, Any]:
    refs = extract_references(text or "")
    external = refs.get("external_links", refs.get("external", []))
    internal = refs.get("internal_links", refs.get("internal", []))
    anchors = sorted(set(re.findall(r"\[[^\]]+\]\((#[^)]+)\)", text or "")))
    return {
        "external": external,
        "internal": internal,
        "anchors": anchors,
        "evidence": "reference_engine",
    }
