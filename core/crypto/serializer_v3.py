from __future__ import annotations
from core.crypto.cross_language_normalizer import normalize_value
from core.crypto.canonical_json_engine import canonical_json

def serialize_v3(payload):
    return canonical_json(normalize_value(payload))
