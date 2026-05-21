from core.graph.semantic_symbol_graph_engine import build_semantic_symbol_graph


def test_symbol_graph_bounded():
    symbols = [{"name": f"s{i}", "references": []} for i in range(10)]
    symbols[0]["references"] = ["s1"]
    g = build_semantic_symbol_graph(symbols)
    assert len(g["nodes"]) == 10
    assert g["bounded"] is True
