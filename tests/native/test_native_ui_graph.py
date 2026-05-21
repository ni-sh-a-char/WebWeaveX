from core.native.native_ui_graph_engine import build_native_ui_graph


def test_native_ui_graph_edges():
    graph = build_native_ui_graph(
        {"windows": [{"id": "w1", "title": "Main"}], "focused_window": "w1"},
        {"buttons": [{"id": "b1", "name": "OK"}]},
        [{"action": "click", "from": "w1", "to": "b1"}],
    )

    assert graph["nodes"]
    relations = {edge["relation"] for edge in graph["edges"]}
    assert "opens" in relations
