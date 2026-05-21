from core.execution_reality import (
    compute_execution_pressure,
)


def test_execution_pressure():

    result = (
        compute_execution_pressure(
            {
                "transitions": [
                    {"from": "a", "to": "b"}
                ],
                "event_stream": {
                    "events": [
                        {"id": "e1"}
                    ]
                },
            }
        )
    )

    assert (
        result["pressure_score"]
        == 2
    )
