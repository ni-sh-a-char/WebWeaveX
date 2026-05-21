from core.memory.runtime_graph_memory_engine import build_runtime_memory_graph


def test_memory_graph_edges():
    graph = build_runtime_memory_graph(
        [{"id": "e1", "type": "entity"}],
        [{"from": "e1", "to": "e2", "relation": "depends_on"}],
    )

    assert graph["nodes"]
    assert graph["edges"][0]["relation"] == "depends_on"
