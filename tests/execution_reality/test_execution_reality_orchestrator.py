from core.execution_reality import (
    orchestrate_execution_reality,
)


def test_execution_reality():

    result = (
        orchestrate_execution_reality(
            {
                "distributed_topology": {
                    "nodes": [],
                    "edges": [],
                },
                "transitions": [],
                "event_stream": {
                    "events": [],
                },
                "semantic_crdt": {},
                "tasks": [],
                "distributed_workers": [],
            }
        )
    )

    assert (
        result[
            "state_convergence"
        ]["converged"]
        is True
    )
