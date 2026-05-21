from core.execution_physics import (
    orchestrate_execution_physics,
)


def test_execution_physics_orchestrator():

    result = (
        orchestrate_execution_physics(
            {
                "distributed_topology": {
                    "edges": [],
                },
                "transitions": [],
                "events": [],
                "distributed_workers": [],
                "runtime_entropy": {
                    "entropy_score": 1,
                },
                "journal": {},
            }
        )
    )

    assert (
        result["runtime_turbulence"][
            "runtime_turbulence"
        ]
        == "low"
    )
