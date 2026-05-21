from core.causal_intelligence import (
    build_semantic_causality_graph,
)


def test_causality_graph():

    result = (
        build_semantic_causality_graph(
            {
                "transitions": [
                    {
                        "from": "a",
                        "to": "b",
                    }
                ]
            }
        )
    )

    assert (
        result["edges"][0]["relation"]
        == "causes"
    )
