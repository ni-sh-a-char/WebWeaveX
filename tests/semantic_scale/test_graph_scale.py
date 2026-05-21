from core.query.graph_scale_traversal_engine import (
    traverse_large_graph,
)


def test_graph_scale():

    graph = {
        "edges": [
            {
                "from": "a",
                "to": "b",
            },
            {
                "from": "b",
                "to": "c",
            },
        ]
    }

    r = traverse_large_graph(
        graph,
        "a",
    )

    assert r["count"] == 3
