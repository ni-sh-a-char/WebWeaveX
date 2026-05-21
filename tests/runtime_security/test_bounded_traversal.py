from core.query.semantic_traversal_engine import traverse_graph, MAX_TRAVERSAL_DEPTH


def test_traversal_stops_at_max_depth():
    adj = {str(i): [str(i + 1)] for i in range(MAX_TRAVERSAL_DEPTH + 5)}
    order = traverse_graph(adj, "0")
    assert len(order) <= MAX_TRAVERSAL_DEPTH + 1
