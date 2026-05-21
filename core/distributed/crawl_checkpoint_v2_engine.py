from __future__ import annotations

from core.utils.deterministic_serializer import dumps_deterministic


def create_crawl_checkpoint_v2(state: dict):
    st = state or {}
    return {"checkpoint": dumps_deterministic(st)}
