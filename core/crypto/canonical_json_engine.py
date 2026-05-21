from __future__ import annotations
from core.serialize.deterministic_serializer import dumps_deterministic

def canonical_json(payload):
    return dumps_deterministic(payload)
