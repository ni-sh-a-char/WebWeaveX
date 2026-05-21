from __future__ import annotations

import json

from .protocol_intelligence_engine import detect_protocol_intelligence
from .structured_payload_engine import extract_structured_payload


def parse_universal_payload(text: str, source_url: str = ""):
    raw = text or ""
    payload = extract_structured_payload(raw)
    return {
        "source_url": source_url,
        "protocol": detect_protocol_intelligence(source_url),
        "structured": payload,
        "length": len(raw),
    }
