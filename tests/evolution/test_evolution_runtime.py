from core.evolution import (
    evolve_semantic_runtime,
)


def test_evolution_runtime():

    result = (
        evolve_semantic_runtime(
            {
                "a": 1,
                "b": 2,
            }
        )
    )

    assert (
        result["evolution_size"]
        == 2
    )
