from core.runtime import SemanticExecutionGraph, SemanticMemory, run_semantic_pipeline


def test_execution_graph_bounded():
    g = SemanticExecutionGraph(max_nodes=5)
    for i in range(10):
        g.add_node(f"n{i}", "test")
    assert len(g.nodes) <= 5


def test_pipeline_deterministic():
    r = run_semantic_pipeline(["document"], {"text": "# Hi"})
    assert "document" in r["results"]


def test_memory_bounded():
    m = SemanticMemory(max_entries=2)
    m.put("a", 1)
    m.put("b", 2)
    m.put("c", 3)
    assert m.snapshot()["count"] <= 2
