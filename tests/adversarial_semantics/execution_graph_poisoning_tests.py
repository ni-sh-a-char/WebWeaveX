from core.runtime import SemanticExecutionGraph


def test_poisoned_edges_bounded():
    g = SemanticExecutionGraph(max_nodes=5)
    for i in range(100):
        g.add_edge(f"n{i}", f"n{i+1}", evidence=["bad"])
    assert len(g.edges) <= 5
