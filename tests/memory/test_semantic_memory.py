from core.memory.semantic_memory_engine import build_semantic_memory


def test_semantic_memory_concepts():
    semantic = {
        "semantic": {
            "entities": {"entities": [{"label": "api"}, {"label": "metric"}]},
            "domain": {"domain": "analytics"},
        },
    }

    first = build_semantic_memory(semantic, [])
    second = build_semantic_memory(semantic, [])

    assert first == second
    assert "api" in first["recurring_concepts"]
