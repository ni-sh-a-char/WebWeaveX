from core.evolution import (
    orchestrate_semantic_evolution,
)


def test_orchestrator():

    result = (
        orchestrate_semantic_evolution(
            {
                "runtime": True,
            }
        )
    )

    assert (
        result["stability"]["stable"]
        is True
    )
