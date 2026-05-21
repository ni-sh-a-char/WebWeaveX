from core.world_model import (
    analyze_semantic_impact,
)


def test_impact_analysis():

    graph = {
        "edges": [
            {
                "from": "a.py",
                "to": "b.py",
            }
        ]
    }

    result = analyze_semantic_impact(
        "b.py",
        graph,
    )

    assert result["impact_size"] == 1
