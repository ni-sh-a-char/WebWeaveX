from core.engineering import (
    build_semantic_engineering_graph,
)


def test_engineering_graph():

    result = (
        build_semantic_engineering_graph(
            {
                "distributed_topology": {
                    "nodes": [
                        {"id": "api"},
                    ],
                    "edges": [],
                }
            }
        )
    )

    assert (
        result["graph_size"]
        == 1
    )
