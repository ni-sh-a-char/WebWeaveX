from core.execution_physics import (
    compute_execution_physics,
)


def test_execution_physics():

    result = compute_execution_physics(
        {
            "transitions": [
                {"from": "a", "to": "b"}
            ],
            "events": [{"id": "e1"}],
        }
    )

    assert (
        result["physics_state"]
        == "stable"
    )
