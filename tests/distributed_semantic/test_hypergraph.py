from core.hypergraph import (
    build_semantic_hypergraph,
)


def test_hypergraph():

    r = build_semantic_hypergraph(
        nodes=[{"id": "a"}],
        relationships=[
            {
                "type": "group",
                "members": [
                    "a",
                    "b",
                ],
            }
        ],
    )

    assert len(
        r["hyperedges"]
    ) == 1
