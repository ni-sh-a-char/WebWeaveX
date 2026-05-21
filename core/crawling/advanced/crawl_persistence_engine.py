from __future__ import annotations
from core.serialize.deterministic_serializer import dumps_deterministic

def serialize_crawl_state(state: dict):
    return dumps_deterministic(state)
