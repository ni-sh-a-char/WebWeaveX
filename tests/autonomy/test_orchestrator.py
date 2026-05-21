from core.autonomy import (
    orchestrate_semantic_runtime,
)


def test_orchestrator():

    result = (
        orchestrate_semantic_runtime(
            {
                "goal": "compile runtime",
            }
        )
    )

    assert (
        result["decomposition"]["count"]
        > 0
    )
