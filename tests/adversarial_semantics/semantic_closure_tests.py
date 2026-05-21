from core.runtime.semantic_execution_graph import SemanticExecutionGraph


def test_graph_closure_bounded():
    g = SemanticExecutionGraph(max_nodes=3)
    for i in range(10):
        g.add_edge(f"a{i}", f"b{i}")
    assert len(g.edges) <= 3
