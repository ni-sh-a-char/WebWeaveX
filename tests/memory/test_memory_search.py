from core.memory.runtime_index_engine import build_runtime_index
from core.memory.runtime_search_engine import search_runtime_memory


def test_search_stability():
    index = build_runtime_index(
        entities=[{"id": "entity:api", "label": "api"}],
        workflows=[{"id": "wf:monitor", "objective": "monitor"}],
        graphs=[{"nodes": []}],
        streams=[],
        connectors=[],
    )

    first = search_runtime_memory(index, "api", "semantic")
    second = search_runtime_memory(index, "api", "semantic")

    assert first == second
    assert first["count"] >= 1
