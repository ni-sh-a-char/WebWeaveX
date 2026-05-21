from core.causality.causal_graph_engine import build_causal_graph
from core.causality.runtime_causality_engine import build_runtime_causality


def test_causal_graph_nodes():
    events = [
        {"id": "a", "runtime": "browser", "type": "click", "step": 0},
        {"id": "b", "runtime": "terminal", "type": "log", "step": 1},
    ]
    causality = build_runtime_causality(events, {"browser": 1})

    graph = build_causal_graph(events, causality)

    assert graph["nodes"]
    assert graph["edges"]
