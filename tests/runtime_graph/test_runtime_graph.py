from core.runtime_graph import (
    build_runtime_graph,
    query_runtime_graph,
)


def test_runtime_graph():
    graph = build_runtime_graph([
        {
            "ir": "document_runtime",
            "nodes": [
                {
                    "id": "doc1",
                    "type": "document",
                }
            ],
            "edges": [],
        }
    ])

    assert graph["ir"] == "unified_runtime_graph"

    result = query_runtime_graph(
        graph,
        {"type": "document"},
    )

    assert result["count"] == 1
