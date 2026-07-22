from __future__ import annotations
from core.serialize.deterministic_serializer import dumps_deterministic

def persist_crawl_state_v3(state: dict):
    return dumps_deterministic(state or {})
