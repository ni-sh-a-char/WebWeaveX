from core.graph.semantic_partition_engine import partition_graph


def test_large_partition_bounded():
    nodes = [{"id": f"n{i}", "kind": "x"} for i in range(200)]
    edges = [{"from": f"n{i}", "to": f"n{i+1}"} for i in range(199)]
    r = partition_graph({"nodes": nodes, "edges": edges})
    assert r["count"] >= 1
    assert r["count"] <= 200
