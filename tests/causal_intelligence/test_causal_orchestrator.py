from core.causal_intelligence import (
    orchestrate_semantic_causal_intelligence,
)


def test_causal_orchestrator():

    result = (
        orchestrate_semantic_causal_intelligence(
            {
                "distributed_topology": {
                    "nodes": [],
                    "edges": [],
                },
                "transitions": [],
                "event_stream": {
                    "events": [],
                },
                "runtime_entropy": {
                    "entropy_score": 1,
                },
                "execution_pressure": {
                    "pressure_score": 1,
                },
                "runtime_conflicts": {
                    "conflicts": [],
                },
                "journal": {},
            }
        )
    )

    assert (
        result[
            "runtime_equilibrium"
        ]["equilibrium"]
        == "stable"
    )
