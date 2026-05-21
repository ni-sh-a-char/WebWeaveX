from core.application.action_graph_engine import build_action_graph


def test_action_graph_sequential():
    graph = build_action_graph([
        {"action": "click", "selector": "#login"},
        {"action": "fill", "selector": "#user"},
    ])

    assert len(graph["nodes"]) == 2
    assert graph["edges"][0]["relation"] == "sequential"
