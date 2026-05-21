from core.runtime.semantic_cache_engine import (
    SemanticCache,
)


def test_semantic_cache():

    cache = SemanticCache()

    payload = {
        "x": 1,
    }

    cache.put(
        payload,
        {"ok": True},
    )

    r = cache.get(payload)

    assert r["ok"] is True
